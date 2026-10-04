"""判题引擎：编译 → 逐测试点运行 → 比对 → 汇总判决。

判决（Verdict）沿用主流 OJ 习惯：
  AC   Accepted            通过
  WA   Wrong Answer        答案错误
  TLE  Time Limit Exceeded 超时
  MLE  Memory Limit Exceeded 超内存
  RE   Runtime Error       运行时错误
  CE   Compile Error       编译错误
  OLE  Output Limit Exceeded 输出超限
  PE   Presentation Error  格式错误（输出内容对但格式差异较大时）
"""
from __future__ import annotations

import shutil
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from oj.config import COMPILE_GRACE, MAX_SOURCE_BYTES
from oj.core.models import Problem, TestCase
from oj.judge import comparator
from oj.judge.runner import run_program
from oj.judge.toolchain import CompileResult, compile_cpp, detect_toolchain

# 判决常量
AC = "AC"
WA = "WA"
TLE = "TLE"
MLE = "MLE"
RE = "RE"
CE = "CE"
OLE = "OLE"

VERDICT_TEXT = {
    AC: "通过",
    WA: "答案错误",
    TLE: "超出时间限制",
    MLE: "超出内存限制",
    RE: "运行时错误",
    CE: "编译错误",
    OLE: "输出超限",
}
VERDICT_ICON = {
    AC: "✅",
    WA: "❌",
    TLE: "⏱️",
    MLE: "🧠",
    RE: "💥",
    CE: "🔧",
    OLE: "📤",
}
# 红涨绿跌不适用；OJ 中习惯 AC 绿、错误红
VERDICT_COLOR = {
    AC: "#16a34a",
    WA: "#dc2626",
    TLE: "#d97706",
    MLE: "#7c3aed",
    RE: "#dc2626",
    CE: "#0ea5e9",
    OLE: "#d97706",
}


@dataclass
class CaseResult:
    index: int
    name: str
    verdict: str
    time: float = 0.0
    memory_kb: int = 0
    score: int = 0
    max_score: int = 0
    input_preview: str = ""
    expected_preview: str = ""
    actual_preview: str = ""
    detail: str = ""
    is_sample: bool = False

    @property
    def verdict_text(self) -> str:
        return VERDICT_TEXT.get(self.verdict, self.verdict)

    @property
    def verdict_icon(self) -> str:
        return VERDICT_ICON.get(self.verdict, "❓")


@dataclass
class JudgeResult:
    verdict: str
    passed: int = 0
    total: int = 0
    score: int = 0
    max_score: int = 0
    time: float = 0.0        # 最大单点耗时
    memory_kb: int = 0       # 最大单点内存
    compile_message: str = ""
    compile_output: str = ""
    compile_time: float = 0.0
    cases: List[CaseResult] = field(default_factory=list)
    message: str = ""
    toolchain: str = ""

    @property
    def verdict_text(self) -> str:
        return VERDICT_TEXT.get(self.verdict, self.verdict)

    @property
    def verdict_icon(self) -> str:
        return VERDICT_ICON.get(self.verdict, "❓")

    @property
    def color(self) -> str:
        return VERDICT_COLOR.get(self.verdict, "#64748b")

    @property
    def accepted(self) -> bool:
        return self.verdict == AC


def _truncate(text: str, limit: int = 2000) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + f"\n…（已截断，共 {len(text)} 字符）"


class Judge:
    """判题器。持有工作目录与工具链，可复用于多次提交。"""

    def __init__(self, work_root: Optional[Path] = None, keep_artifacts: bool = False):
        self.work_root = Path(work_root) if work_root else None
        self.keep_artifacts = keep_artifacts
        self.toolchain = detect_toolchain()

    # ------------------------------------------------------------ 对外接口

    def judge(
        self,
        problem: Problem,
        source: str,
        lang: str = "cpp17",
        run_samples_only: bool = False,
    ) -> JudgeResult:
        """对一份源码判题。

        ``run_samples_only=True`` 时只跑样例点（用于「运行」按钮，快速反馈）。
        """
        if not self.toolchain:
            return JudgeResult(
                verdict=CE,
                message="未检测到 C++ 编译器，无法判题。",
                compile_message="未检测到 C++ 编译器",
            )

        if len(source.encode("utf-8")) > MAX_SOURCE_BYTES:
            return JudgeResult(
                verdict=CE,
                message=f"源代码过大（>{MAX_SOURCE_BYTES // 1024}KB）",
            )

        work_dir = Path(
            tempfile.mkdtemp(
                prefix="dsoj_", dir=str(self.work_root) if self.work_root else None
            )
        )
        try:
            return self._judge_in_dir(problem, source, work_dir, run_samples_only)
        finally:
            if not self.keep_artifacts:
                shutil.rmtree(work_dir, ignore_errors=True)

    # ------------------------------------------------------------ 内部实现

    def _judge_in_dir(
        self,
        problem: Problem,
        source: str,
        work_dir: Path,
        run_samples_only: bool,
    ) -> JudgeResult:
        src_path = work_dir / "main.cpp"
        src_path.write_text(source, encoding="utf-8")

        # ---------------- 编译
        comp: CompileResult = compile_cpp(
            src_path, work_dir, toolchain=self.toolchain,
            timeout=max(30.0, COMPILE_GRACE * 6),
        )
        if not comp.ok:
            return JudgeResult(
                verdict=CE,
                total=len(problem.tests),
                max_score=problem.total_score,
                compile_message=comp.message,
                compile_output=_truncate(comp.message, 6000),
                compile_time=comp.duration,
                toolchain=self.toolchain.name,
                message="编译失败",
            )

        # ---------------- 选取测试点
        cases = problem.tests
        if run_samples_only:
            cases = [t for t in problem.tests if t.sample] or problem.tests[: len(problem.samples) or 1]

        if not cases:
            return JudgeResult(
                verdict=CE, message="该题没有可运行的测试点", toolchain=self.toolchain.name
            )

        results: List[CaseResult] = []
        total_time = 0.0
        peak_mem = 0
        max_time = 0.0

        for i, tc in enumerate(cases, start=1):
            cr = self._run_case(problem, tc, comp.exe, work_dir, i)
            results.append(cr)
            total_time += cr.time
            max_time = max(max_time, cr.time)
            peak_mem = max(peak_mem, cr.memory_kb)

            # 非样例点出现非 AC，仍继续跑完便于用户看到全景
            # （若追求速度可在此 break，这里选择完整反馈）

        passed = sum(1 for r in results if r.verdict == AC)
        score = sum(r.score for r in results if r.verdict == AC)
        max_score = sum(r.max_score for r in results) or len(results)

        # ---------------- 汇总判决
        if passed == len(results):
            verdict = AC
            msg = f"全部通过（{passed}/{len(results)}）"
        else:
            first_bad = next((r for r in results if r.verdict != AC), None)
            verdict = first_bad.verdict if first_bad else WA
            # 优先级：CE > RE > TLE > MLE > OLE > WA
            priority = {AC: 0, WA: 1, OLE: 2, MLE: 3, TLE: 4, RE: 5, CE: 6}
            if not run_samples_only:
                verdict = max(
                    (r.verdict for r in results), key=lambda v: priority.get(v, 0)
                )
            msg = (
                f"{VERDICT_TEXT.get(verdict, verdict)}：通过 {passed}/{len(results)} 个测试点"
            )

        return JudgeResult(
            verdict=verdict,
            passed=passed,
            total=len(results),
            score=score,
            max_score=max_score,
            time=max_time,
            memory_kb=peak_mem,
            compile_message="",
            compile_output="",
            compile_time=comp.duration,
            cases=results,
            message=msg,
            toolchain=self.toolchain.name,
        )

    def _run_case(
        self,
        problem: Problem,
        tc: TestCase,
        exe: Path,
        work_dir: Path,
        index: int,
    ) -> CaseResult:
        # 样例点给一点额外宽限，避免边界抖动
        tl = problem.time_limit
        run = run_program(
            exe,
            tc.input,
            work_dir,
            time_limit=tl + 0.2,
            memory_limit_mb=problem.memory_limit,
        )

        cr = CaseResult(
            index=index,
            name=tc.name or f"测试点 {index}",
            verdict=WA,
            time=run.time,
            memory_kb=run.memory_kb,
            max_score=tc.score or 1,
            is_sample=tc.sample,
            input_preview=_truncate(tc.input, 800),
            expected_preview=_truncate(tc.output, 800),
            actual_preview=_truncate(run.stdout, 800),
        )

        if run.error:
            cr.verdict = RE
            cr.detail = run.error
            return cr

        if run.timed_out:
            cr.verdict = TLE
            cr.detail = f"运行时间超过限制 {tl:.2f}s"
            return cr

        if run.oom:
            cr.verdict = MLE
            cr.detail = f"运行内存超过限制 {problem.memory_limit}MB"
            return cr

        if run.output_truncated:
            cr.verdict = OLE
            cr.detail = "输出量过大"
            return cr

        # 非零退出码 → RE（注意：Windows 上某些程序正常返回非 0 也算 RE，符合 OJ 惯例）
        if run.exit_code not in (0, None):
            cr.verdict = RE
            cr.detail = f"程序返回非零退出码 {run.exit_code}"
            if run.stderr:
                cr.detail += f"\n{_truncate(run.stderr, 500)}"
            return cr

        if not comparator.compare(run.stdout, tc.output, mode="trim"):
            cr.verdict = WA
            cr.detail = comparator.first_diff(run.stdout, tc.output)
            return cr

        cr.verdict = AC
        cr.score = tc.score or 1
        cr.detail = "输出正确"
        return cr

    # ------------------------------------------------------------ 运行（不做比对）

    def run_with_input(
        self,
        source: str,
        stdin_data: str,
        time_limit: float = 2.0,
        memory_limit_mb: int = 256,
    ) -> Dict[str, Any]:
        """「自定义输入运行」：不比对答案，直接返回程序输出。"""
        if not self.toolchain:
            return {"ok": False, "error": "未检测到 C++ 编译器"}

        work_dir = Path(tempfile.mkdtemp(prefix="dsoj_run_"))
        try:
            src = work_dir / "main.cpp"
            src.write_text(source, encoding="utf-8")
            comp = compile_cpp(src, work_dir, toolchain=self.toolchain)
            if not comp.ok:
                return {
                    "ok": False,
                    "stage": "compile",
                    "error": comp.message,
                    "compile_output": _truncate(comp.message, 6000),
                }
            run = run_program(
                comp.exe, stdin_data, work_dir,
                time_limit=time_limit + 0.2, memory_limit_mb=memory_limit_mb,
            )
            return {
                "ok": True,
                "stdout": run.stdout,
                "stderr": run.stderr,
                "time": run.time,
                "memory_kb": run.memory_kb,
                "exit_code": run.exit_code,
                "timed_out": run.timed_out,
                "oom": run.oom,
                "compile_time": comp.duration,
            }
        finally:
            shutil.rmtree(work_dir, ignore_errors=True)

    def verify_reference(self, problem: Problem, lang: str = "cpp17") -> JudgeResult:
        """用题目自带参考解跑一遍全部测试点，用于题库自检。"""
        ref = problem.reference.get("cpp") or problem.reference.get(lang) or ""
        if not ref.strip():
            return JudgeResult(
                verdict=CE, message=f"题目 {problem.id} 缺少 C++ 参考解"
            )
        return self.judge(problem, ref, lang=lang)
