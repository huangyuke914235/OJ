"""题库校验脚本。

用途
----
1. 校验每道题的 JSON 结构是否合法；
2. 用题目自带的 C++ 参考解跑一遍**全部测试点**，确保测试数据与参考解一致；
3. 交叉验证样例输出与测试点输出是否吻合。

用法::

    python scripts/validate_problems.py           # 全量校验（含编译运行）
    python scripts/validate_problems.py --no-run  # 只校验 JSON 结构
    python scripts/validate_problems.py -k tree   # 只校验 id/标题含 tree 的题

退出码：0 全部通过；1 存在失败项。
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from oj.config import PROBLEMS_DIR  # noqa: E402
from oj.core.models import Problem, load_all  # noqa: E402
from oj.judge.engine import Judge  # noqa: E402
from oj.judge.toolchain import toolchain_info  # noqa: E402

GREEN, RED, YELLOW, DIM, RESET = (
    "\033[32m", "\033[31m", "\033[33m", "\033[2m", "\033[0m"
)


def structural_check(p: Problem) -> list[str]:
    """结构层面的告警（非致命）。"""
    warns: list[str] = []
    if not p.statement.strip():
        warns.append("statement 为空")
    if not p.samples:
        warns.append("没有样例（samples）")
    if "cpp" not in p.reference and "cpp17" not in p.reference:
        warns.append("缺少 C++ 参考解（reference.cpp）")
    for i, t in enumerate(p.tests, 1):
        if not t.input.strip() and not t.output.strip():
            warns.append(f"测试点 {i} 输入输出均为空")
    if not any(t.sample for t in p.tests):
        warns.append("没有任何测试点标记为 sample")
    # 样例与样例测试点一致性
    sample_ins = {(t.input.strip(), t.output.strip()) for t in p.tests if t.sample}
    for s in p.samples:
        if (s.input.strip(), s.output.strip()) not in sample_ins:
            warns.append(f"样例「{s.input[:20]!r}…」未在 tests 中找到对应的 sample 测试点")
    return warns


def main() -> int:
    ap = argparse.ArgumentParser(description="DS-OJ 题库校验")
    ap.add_argument("--no-run", action="store_true", help="跳过编译运行，只校验结构")
    ap.add_argument("-k", "--keyword", default="", help="只校验匹配关键字的题目")
    ap.add_argument("-v", "--verbose", action="store_true", help="打印每个测试点细节")
    args = ap.parse_args()

    print(f"{DIM}题库目录: {PROBLEMS_DIR}{RESET}")
    try:
        problems = load_all(PROBLEMS_DIR, strict=True)
    except Exception as exc:  # noqa: BLE001
        print(f"{RED}✗ 题库加载失败：{exc}{RESET}")
        return 1

    if args.keyword:
        kw = args.keyword.lower()
        problems = [
            p for p in problems if kw in p.id.lower() or kw in p.title.lower()
        ]

    print(f"共加载 {len(problems)} 道题目\n")

    if not args.no_run:
        info = toolchain_info()
        if not info["available"]:
            print(f"{YELLOW}! {info['name']}，跳过编译运行检查{RESET}")
            args.no_run = True
        else:
            print(f"{DIM}使用编译器: {info['name']}{RESET}\n")

    judge = Judge() if not args.no_run else None

    n_ok = n_fail = 0
    t0 = time.perf_counter()

    for p in problems:
        warns = structural_check(p)
        head = f"[{p.difficulty}] {p.id} · {p.title}  ({p.category}, {len(p.tests)} 测试点)"

        if args.no_run:
            if warns:
                n_fail += 1
                print(f"{YELLOW}△{RESET} {head}")
                for w in warns:
                    print(f"    {YELLOW}- {w}{RESET}")
            else:
                n_ok += 1
                print(f"{GREEN}✓{RESET} {head}")
            continue

        res = judge.verify_reference(p)
        if res.accepted:
            n_ok += 1
            extra = f"  {YELLOW}({len(warns)} 项告警){RESET}" if warns else ""
            print(
                f"{GREEN}✓{RESET} {head}  "
                f"{DIM}{res.time*1000:.0f}ms / {res.memory_kb//1024}MB{RESET}{extra}"
            )
            if args.verbose:
                for c in res.cases:
                    print(f"    {c.verdict_icon} {c.name}: {c.verdict_text} ({c.time*1000:.0f}ms)")
            for w in warns:
                print(f"    {YELLOW}- {w}{RESET}")
        else:
            n_fail += 1
            print(f"{RED}✗{RESET} {head} -> {res.verdict_text}")
            if res.compile_output:
                print(f"    {RED}编译输出：{res.compile_output[:600]}{RESET}")
            for c in res.cases:
                if c.verdict != "AC":
                    print(f"    {RED}{c.verdict_icon} {c.name}: {c.verdict_text}{RESET}")
                    if c.detail:
                        for line in c.detail.splitlines()[:4]:
                            print(f"      {DIM}{line}{RESET}")
            for w in warns:
                print(f"    {YELLOW}- {w}{RESET}")

    elapsed = time.perf_counter() - t0
    print()
    print("=" * 60)
    color = GREEN if n_fail == 0 else RED
    print(f"{color}通过 {n_ok} / {n_ok + n_fail} 道题目{RESET}  （耗时 {elapsed:.1f}s）")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
