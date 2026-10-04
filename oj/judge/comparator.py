"""输出比对工具。

判题的核心敏感点之一：行尾空格与文末换行的差异不应判错。
这里统一采用「按行 strip 后比较 token 序列」的策略，兼容绝大多数 OJ 习惯。
"""
from __future__ import annotations

import re


def normalize(text: str) -> str:
    """规范化文本：统一换行、去掉每行首尾空白、去掉文末空行。"""
    if text is None:
        return ""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in text.split("\n")]
    # 去掉末尾连续空行
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def normalize_tokenwise(text: str) -> str:
    """按空白切分全部 token，用单空格连接（忽略所有换行差异）。"""
    return " ".join(normalize(text).split())


def compare(actual: str, expected: str, mode: str = "trim") -> bool:
    """比对输出。

    mode:
      - ``trim``     : 忽略行尾空白与文末换行（默认，推荐）
      - ``exact``    : 逐字节完全一致（规范化换行后）
      - ``token``    : 忽略一切空白差异（含换行）
      - ``float``    : 逐 token 按浮点数比较，容差 1e-6
    """
    if mode == "exact":
        return (
            actual.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n")
            == expected.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n")
        )
    if mode == "token":
        return normalize_tokenwise(actual) == normalize_tokenwise(expected)
    if mode == "float":
        return _compare_float(actual, expected)
    return normalize(actual) == normalize(expected)


def _compare_float(actual: str, expected: str, eps: float = 1e-6) -> bool:
    a_tokens = normalize_tokenwise(actual).split()
    e_tokens = normalize_tokenwise(expected).split()
    if len(a_tokens) != len(e_tokens):
        return False
    for a, e in zip(a_tokens, e_tokens):
        if a == e:
            continue
        try:
            fa, fe = float(a), float(e)
        except ValueError:
            return False
        if abs(fa - fe) > eps * max(1.0, abs(fe)):
            return False
    return True


def first_diff(actual: str, expected: str, max_lines: int = 8) -> str:
    """定位首个不同的行，用于给用户友好的 WA 反馈。"""
    a = normalize(actual).split("\n")
    e = normalize(expected).split("\n")
    for i in range(max(len(a), len(e))):
        av = a[i] if i < len(a) else "<缺失>"
        ev = e[i] if i < len(e) else "<缺失>"
        if av != ev:
            shown_av = _ellipsis(av)
            shown_ev = _ellipsis(ev)
            return f"第 {i + 1} 行不一致：\n  期望: {shown_ev}\n  实际: {shown_av}"
    return "输出与期望完全一致"


def _ellipsis(s: str, limit: int = 120) -> str:
    s = re.sub(r"\s+", " ", s)
    return s if len(s) <= limit else s[:limit] + "…"
