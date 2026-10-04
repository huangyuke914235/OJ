"""判题结果渲染组件。"""
from __future__ import annotations

from typing import Any, Dict, List

import streamlit as st

from oj.judge.engine import VERDICT_ICON, VERDICT_TEXT, JudgeResult
from ui.theme import escape


def _fmt_time(seconds: float) -> str:
    if seconds <= 0:
        return "—"
    if seconds < 1:
        return f"{seconds * 1000:.0f} ms"
    return f"{seconds:.2f} s"


def _fmt_mem(kb: int) -> str:
    if kb <= 0:
        return "—"
    if kb < 1024:
        return f"{kb} KB"
    return f"{kb / 1024:.1f} MB"


def _verdict_tint(v: str) -> tuple[str, str]:
    """返回 (背景色, 边框色)。"""
    return {
        "AC": ("#f0fdf4", "#86efac"),
        "WA": ("#fef2f2", "#fca5a5"),
        "TLE": ("#fffbeb", "#fcd34d"),
        "MLE": ("#faf5ff", "#d8b4fe"),
        "RE": ("#fef2f2", "#fca5a5"),
        "CE": ("#f0f9ff", "#7dd3fc"),
        "OLE": ("#fffbeb", "#fcd34d"),
    }.get(v, ("#f8fafc", "#e2e8f0"))


def render_verdict_header(res: JudgeResult, mode: str = "judge") -> None:
    """顶部大号判决条。"""
    bg, border = _verdict_tint(res.verdict)
    color = res.color
    icon = VERDICT_ICON.get(res.verdict, "❓")
    name = VERDICT_TEXT.get(res.verdict, res.verdict)

    if mode == "run":
        title = "运行完成"
        msg = res.message or "程序已执行完毕"
    else:
        title = f"{icon} {name}"
        msg = res.message

    stats = []
    if res.total:
        stats.append(f"通过 {res.passed}/{res.total}")
    if res.score:
        stats.append(f"得分 {res.score}/{res.max_score}")
    if res.time:
        stats.append(f"耗时 {_fmt_time(res.time)}")
    if res.memory_kb:
        stats.append(f"内存 {_fmt_mem(res.memory_kb)}")

    st.markdown(
        f"""
        <div class="verdict-big" style="background:{bg};border-color:{border};color:{color};">
          <div>
            <div class="verdict-name">{escape(title)}</div>
            <div class="verdict-msg">{escape(msg)}</div>
          </div>
          <div class="verdict-stats" style="color:{color};opacity:.75;">
            {' · '.join(escape(s) for s in stats)}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_compile_error(res: JudgeResult) -> None:
    if res.compile_output or res.compile_message:
        st.markdown('<div class="dsoj-h">编译输出</div>', unsafe_allow_html=True)
        st.code(res.compile_output or res.compile_message, language="text")


def render_cases(res: JudgeResult, show_all: bool = True) -> None:
    """逐测试点结果。"""
    if not res.cases:
        return

    rows = []
    for c in res.cases:
        color = {
            "AC": "#16a34a", "WA": "#dc2626", "TLE": "#d97706",
            "MLE": "#7c3aed", "RE": "#dc2626", "CE": "#0ea5e9", "OLE": "#d97706",
        }.get(c.verdict, "#64748b")

        tag = " 样例" if c.is_sample else ""
        rows.append(
            f'<div class="case-row">'
            f'<span style="font-size:15px;">{c.verdict_icon}</span>'
            f'<span class="case-name">{escape(c.name)}{tag}</span>'
            f'<span class="case-verdict" style="color:{color};">{escape(c.verdict)}'
            f' · {escape(VERDICT_TEXT.get(c.verdict, ""))}</span>'
            f'<span class="case-stat">{_fmt_time(c.time)}'
            f'{" · " + _fmt_mem(c.memory_kb) if c.memory_kb else ""}</span>'
            f'</div>'
        )

    st.markdown(
        f'<div class="dsoj-card" style="padding:6px 0;">{"".join(rows)}</div>',
        unsafe_allow_html=True,
    )


def render_case_details(res: JudgeResult, only_failed: bool = True) -> None:
    """展开每个失败测试点的详细差异。"""
    targets = [c for c in res.cases if (not only_failed or c.verdict != "AC")]
    if not targets:
        return

    st.markdown('<div class="dsoj-h">失败测试点详情</div>', unsafe_allow_html=True)
    for c in targets:
        color = "#dc2626" if c.verdict in ("WA", "RE") else "#d97706"
        with st.expander(f"{c.verdict_icon} {c.name} · {c.verdict}", expanded=len(targets) <= 3):
            if c.detail:
                st.markdown(
                    f'<div class="notice notice-err">{escape(c.detail).replace(chr(10), "<br>")}</div>',
                    unsafe_allow_html=True,
                )
            cols = st.columns(3)
            with cols[0]:
                st.caption("输入")
                st.code(c.input_preview or "(空)", language="text")
            with cols[1]:
                st.caption("期望输出")
                st.code(c.expected_preview or "(空)", language="text")
            with cols[2]:
                st.caption("实际输出")
                st.code(c.actual_preview or "(空)", language="text")


def render_run_output(out: Dict[str, Any]) -> None:
    """「自定义输入运行」的结果。"""
    if not out:
        return

    if not out.get("ok"):
        stage = out.get("stage", "")
        if stage == "compile":
            st.markdown(
                '<div class="notice notice-err">编译失败</div>', unsafe_allow_html=True
            )
            st.code(out.get("compile_output") or out.get("error", ""), language="text")
        else:
            st.markdown(
                f'<div class="notice notice-err">{escape(out.get("error", "运行失败"))}</div>',
                unsafe_allow_html=True,
            )
        return

    flags = []
    if out.get("timed_out"):
        flags.append("⏱️ 超时")
    if out.get("oom"):
        flags.append("🧠 超内存")
    if out.get("exit_code") not in (0, None):
        flags.append(f"💥 退出码 {out['exit_code']}")

    stat = f"耗时 {_fmt_time(out.get('time', 0))}"
    if out.get("memory_kb"):
        stat += f" · 内存 {_fmt_mem(out['memory_kb'])}"

    tint = "#fffbeb" if flags else "#f0fdf4"
    border = "#fcd34d" if flags else "#86efac"
    text = "#92400e" if flags else "#15803d"
    label = " · ".join(flags) if flags else "运行正常"

    st.markdown(
        f'<div class="verdict-big" style="background:{tint};border-color:{border};color:{text};">'
        f'<div><div class="verdict-name">{escape(label)}</div>'
        f'<div class="verdict-msg">程序执行完毕</div></div>'
        f'<div class="verdict-stats" style="color:{text};opacity:.75;">{escape(stat)}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(2)
    with cols[0]:
        st.caption("标准输出")
        st.code(out.get("stdout") or "(无输出)", language="text")
    with cols[1]:
        st.caption("标准错误")
        st.code(out.get("stderr") or "(无)", language="text")
