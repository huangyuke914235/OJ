"""判题引擎端到端测试。

覆盖：
1. 参考解对每道题都应得 AC
2. 故意写错的代码应得 WA
3. 死循环应得 TLE
4. 语法错误应得 CE
5. 运行崩溃应得 RE
6. 自定义输入运行功能

用法::
    python tests/test_judge.py            # 全量
    python tests/test_judge.py -k tree    # 只测匹配关键字的题目
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from oj.config import PROBLEMS_DIR  # noqa: E402
from oj.core.models import load_all  # noqa: E402
from oj.judge.engine import AC, CE, RE, TLE, WA, Judge  # noqa: E402
from oj.judge.toolchain import toolchain_info  # noqa: E402

GREEN, RED, YELLOW, DIM, RESET = "\033[32m", "\033[31m", "\033[33m", "\033[2m", "\033[0m"

# ---------------- 用于负面测试的代码片段
CODE_WA = "#include <cstdio>\nint main(){printf(\"0\\n\");return 0;}\n"
CODE_CE = "#include <cstdio>\nint main(){ this is not valid c++ ; }\n"
CODE_RE = """#include <cstdio>
int main(){ int* p = nullptr; *p = 42; printf("%d", *p); return 0; }
"""
CODE_TLE = """#include <cstdio>
int main(){ volatile long long s=0; while(true){ s++; } return (int)s; }
"""


def check(label: str, got: str, want: str) -> bool:
    ok = got == want
    mark = f"{GREEN}✓{RESET}" if ok else f"{RED}✗{RESET}"
    print(f"  {mark} {label}: 期望 {want}, 实际 {got}")
    return ok


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("-k", "--keyword", default="")
    ap.add_argument("--skip-negative", action="store_true", help="跳过 WA/CE/RE/TLE 测试")
    args = ap.parse_args()

    info = toolchain_info()
    if not info["available"]:
        print(f"{RED}没有可用的 C++ 编译器，无法测试。{RESET}")
        return 1
    print(f"{DIM}编译器: {info['name']}{RESET}\n")

    problems = load_all(PROBLEMS_DIR, strict=True)
    if args.keyword:
        kw = args.keyword.lower()
        problems = [p for p in problems if kw in p.id.lower() or kw in p.title.lower()]

    judge = Judge()
    passed = failed = 0

    print("=" * 68)
    print(" 测试一：参考解应全部 AC")
    print("=" * 68)
    for p in problems:
        res = judge.verify_reference(p)
        if res.accepted:
            passed += 1
            print(f"{GREEN}✓{RESET} {p.id:36s} AC  {DIM}({res.time*1000:.0f}ms){RESET}")
        else:
            failed += 1
            print(f"{RED}✗{RESET} {p.id:36s} {res.verdict} — {res.message}")
            for c in res.cases:
                if c.verdict != AC:
                    print(f"    {RED}{c.name}: {c.verdict} — {c.detail[:140]}{RESET}")

    if args.skip_negative or not problems:
        _summary(passed, failed)
        return 0 if failed == 0 else 1

    # ---------------- 负面测试：挑一道题分别提交错误代码
    print()
    print("=" * 68)
    print(" 测试二：错误代码应得到对应判决")
    print("=" * 68)

    probe = next((p for p in problems if p.id == "array-reverse"), problems[0])
    print(f"{DIM}使用题目：{probe.id} · {probe.title}{RESET}")

    for label, code, want in [
        ("固定输出（WA）", CODE_WA, WA),
        ("语法错误（CE）", CODE_CE, CE),
        ("空指针写入（RE）", CODE_RE, RE),
        ("死循环（TLE）", CODE_TLE, TLE),
    ]:
        res = judge.judge(probe, code)
        if check(label, res.verdict, want):
            passed += 1
        else:
            failed += 1
            if res.cases:
                for c in res.cases[:2]:
                    print(f"      {DIM}{c.name}: {c.verdict} {c.detail[:120]}{RESET}")

    # ---------------- 自定义输入运行
    print()
    print("=" * 68)
    print(" 测试三：自定义输入运行")
    print("=" * 68)
    out = judge.run_with_input(
        "#include <cstdio>\nint main(){int a,b;scanf(\"%d %d\",&a,&b);printf(\"%d\\n\",a+b);return 0;}\n",
        "7 35\n",
    )
    ok = out.get("ok") and out.get("stdout", "").strip() == "42"
    print(
        f"  {GREEN + '✓' + RESET if ok else RED + '✗' + RESET} "
        f"7 + 35 = {out.get('stdout', '').strip()!r}（期望 '42'）"
    )
    passed += ok
    failed += not ok

    # ---------------- 样例运行模式
    print()
    print("=" * 68)
    print(" 测试四：仅测样例模式")
    print("=" * 68)
    res = judge.judge(probe, probe.reference["cpp"], run_samples_only=True)
    n_sample = sum(1 for t in probe.tests if t.sample)
    ok = res.accepted and res.total == n_sample
    print(
        f"  {GREEN + '✓' + RESET if ok else RED + '✗' + RESET} "
        f"样例数 {res.total}（题目标记 {n_sample} 个）· 判决 {res.verdict}"
    )
    passed += ok
    failed += not ok

    _summary(passed, failed)
    return 0 if failed == 0 else 1


def _summary(passed: int, failed: int) -> None:
    print()
    print("=" * 68)
    color = GREEN if failed == 0 else RED
    print(f"{color}通过 {passed} / {passed + failed} 项测试{RESET}")


if __name__ == "__main__":
    raise SystemExit(main())
