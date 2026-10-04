"""题库生成框架。

动机
----
手写测试数据极易出错（本项目开工第一天就被校验脚本抓出 3 处错误）。
因此对于「有明确参考解」的题目，统一采用：

    写参考解 → 用参考解生成/校验每组数据 → 生成 JSON

这样测试数据的输出**必定**与参考解一致，从根本上消除数据错误。

用法：在 ``scripts/generators/`` 下定义题目，或直接调用本模块的工具函数。
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Callable, List, Optional, Sequence, Tuple

# 测试点规格：(名称, 输入字符串, 分值)
CaseSpec = Tuple[str, str, int]


def make_test(name: str, input_text: str, output_text: str, score: int, sample: bool = False) -> dict:
    return {
        "input": _ensure_trailing_nl(input_text),
        "output": _ensure_trailing_nl(output_text),
        "name": name,
        "score": score,
        "sample": sample,
    }


def _ensure_trailing_nl(text: str) -> str:
    if not text.endswith("\n"):
        return text + "\n"
    return text


def build_tests(
    specs: Sequence[CaseSpec],
    solver: Callable[[str], str],
) -> List[dict]:
    """用 ``solver`` 生成每组数据的标准输出。

    :param specs: [(名称, 输入, 分值), ...]
    :param solver: 接受输入字符串，返回标准输出字符串
    """
    tests = []
    for name, inp, score in specs:
        out = solver(inp)
        tests.append(make_test(name, inp, out, score))
    return tests


def finalize(problem: dict, out_path: Path, samples_from: int = 0) -> Path:
    """补全 samples、写盘、做基本自检。

    关键行为：``samples`` 直接**从 tests 中标记 sample 的测试点复制**，
    确保样例展示与判题数据永远一致（手工维护两份数据极易错位）。
    若题目已显式提供 ``samples``，则用其中的 ``explain`` 覆盖说明文字。
    """
    tests = problem.get("tests", [])
    if not tests:
        raise ValueError("题目没有任何测试点")

    sample_idx = [i for i, t in enumerate(tests) if t.get("sample")]
    if not sample_idx:
        for i in range(min(2, len(tests))):
            tests[i]["sample"] = True
        sample_idx = list(range(min(2, len(tests))))

    # 保留作者手写的 explain
    explains = [s.get("explain", "") for s in problem.get("samples", [])]

    samples = []
    for pos, i in enumerate(sample_idx):
        t = tests[i]
        samples.append(
            {
                "input": t["input"],
                "output": t["output"],
                "explain": explains[pos] if pos < len(explains) else "",
            }
        )
    problem["samples"] = samples

    problem["tests"] = tests
    problem.setdefault("time_limit", 2.0)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(problem, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return out_path


def numbers(text: str) -> List[int]:
    return [int(x) for x in text.split()]


def lines(text: str) -> List[str]:
    return text.strip("\n").split("\n")
