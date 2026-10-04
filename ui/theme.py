"""主题与全局样式。"""
from __future__ import annotations

import streamlit as st

# 配色（浅色主题）
INK = "#0f172a"
MUTED = "#64748b"
BORDER = "#e2e8f0"
BG_SOFT = "#f8fafc"
ACCENT = "#4f46e5"
ACCENT_SOFT = "#eef2ff"
GREEN = "#16a34a"
RED = "#dc2626"
AMBER = "#d97706"
BLUE = "#0ea5e9"
PURPLE = "#7c3aed"


CSS = f"""
<style>
/* ---------- 全局 ---------- */
html, body, [class*="css"] {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
                 "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
}}

.block-container {{
    padding-top: 1.6rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}}

/* ---------- 卡片 ---------- */
.dsoj-card {{
    background: #ffffff;
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 12px;
    transition: border-color .15s ease, box-shadow .15s ease;
}}
.dsoj-card:hover {{
    border-color: #c7d2fe;
    box-shadow: 0 2px 10px rgba(79,70,229,.07);
}}

/* ---------- 表格 ---------- */
.dsoj-table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
.dsoj-table th {{
    text-align: left; padding: 10px 12px; color: {MUTED};
    font-weight: 600; font-size: 12.5px; letter-spacing: .03em;
    border-bottom: 1.5px solid {BORDER}; background: {BG_SOFT};
    white-space: nowrap;
}}
.dsoj-table td {{
    padding: 11px 12px; border-bottom: 1px solid #f1f5f9;
    vertical-align: middle;
}}
.dsoj-table tr:hover td {{ background: {BG_SOFT}; }}
.dsoj-table td.id {{ color: {MUTED}; font-family: ui-monospace, monospace; font-size: 12px; }}

/* ---------- 徽章 ---------- */
.badge {{
    display: inline-block; padding: 2.5px 9px; border-radius: 999px;
    font-size: 12px; font-weight: 600; line-height: 1.5; white-space: nowrap;
}}
.badge-easy    {{ background: #dcfce7; color: #15803d; }}
.badge-medium  {{ background: #fef3c7; color: #b45309; }}
.badge-hard    {{ background: #fee2e2; color: #b91c1c; }}
.badge-intro   {{ background: #dbeafe; color: #1d4ed8; }}
.badge-tag     {{ background: {ACCENT_SOFT}; color: #4338ca; font-weight: 500; }}
.badge-cat     {{ background: #f1f5f9; color: #475569; font-weight: 500; }}

/* ---------- 题目详情头部 ---------- */
.dsoj-title {{ font-size: 26px; font-weight: 700; color: {INK}; margin: 0 0 6px 0; }}
.dsoj-sub   {{ color: {MUTED}; font-size: 13.5px; margin-bottom: 4px; }}
.dsoj-meta-row {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-top: 10px; }}

/* ---------- 小节标题 ---------- */
.dsoj-h {{
    font-size: 16px; font-weight: 700; color: {INK};
    margin: 22px 0 10px 0; padding-left: 10px;
    border-left: 3.5px solid {ACCENT}; line-height: 1.2;
}}

/* ---------- 样例块 ---------- */
.sample-box {{
    border: 1px solid {BORDER}; border-radius: 10px;
    overflow: hidden; margin-bottom: 12px; background: #fff;
}}
.sample-head {{
    background: {BG_SOFT}; padding: 8px 14px; font-size: 13px;
    font-weight: 600; color: {MUTED}; border-bottom: 1px solid {BORDER};
}}
.sample-body {{ display: flex; }}
.sample-col {{ flex: 1; padding: 12px 14px; }}
.sample-col + .sample-col {{ border-left: 1px solid {BORDER}; }}
.sample-lbl {{
    font-size: 11.5px; font-weight: 600; color: {MUTED};
    letter-spacing: .04em; margin-bottom: 7px; text-transform: uppercase;
}}
.sample-pre {{
    margin: 0; font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: 13px; color: {INK}; white-space: pre-wrap; word-break: break-word;
    line-height: 1.55;
}}
.sample-explain {{
    padding: 10px 14px; font-size: 13px; color: {MUTED};
    border-top: 1px dashed {BORDER}; background: #fcfcfd;
}}

/* ---------- 判决徽章 ---------- */
.verdict-big {{
    display: flex; align-items: center; gap: 14px;
    padding: 16px 20px; border-radius: 12px; margin-bottom: 14px;
    border: 1.5px solid; 
}}
.verdict-name {{ font-size: 20px; font-weight: 700; }}
.verdict-msg  {{ font-size: 13.5px; opacity: .8; margin-top: 2px; }}
.verdict-stats {{
    margin-left: auto; text-align: right; font-size: 13px;
    color: {MUTED}; white-space: nowrap;
}}

/* ---------- 测试点结果 ---------- */
.case-row {{
    display: flex; align-items: center; gap: 10px;
    padding: 8px 14px; border-bottom: 1px solid #f1f5f9; font-size: 13.5px;
}}
.case-row:last-child {{ border-bottom: none; }}
.case-name {{ font-weight: 600; color: {INK}; min-width: 108px; }}
.case-verdict {{ font-weight: 600; min-width: 104px; }}
.case-stat {{ color: {MUTED}; font-size: 12.5px; margin-left: auto; }}

/* ---------- 代码块 ---------- */
pre.code {{
    background: #0f172a; color: #e2e8f0; padding: 14px 16px;
    border-radius: 10px; overflow-x: auto; font-size: 13px;
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    line-height: 1.6;
}}
code {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: .92em; }}

/* 深色模式下保持可观 */
@media (prefers-color-scheme: dark) {{
    .dsoj-card, .sample-box {{ background: #1e293b; border-color: #334155; }}
    .dsoj-table td {{ border-color: #334155; }}
    .dsoj-table th {{ background: #1e293b; }}
    .dsoj-title, .dsoj-h {{ color: #f1f5f9; }}
}}

/* ---------- 其它 ---------- */
.hr-soft {{ height: 1px; background: {BORDER}; margin: 18px 0; border: 0; }}
.kv {{ display: flex; gap: 8px; font-size: 13.5px; margin: 4px 0; }}
.kv-k {{ color: {MUTED}; min-width: 88px; }}
.kv-v {{ color: {INK}; font-weight: 500; }}
.notice {{
    background: {ACCENT_SOFT}; border-left: 3px solid {ACCENT};
    padding: 11px 15px; border-radius: 0 8px 8px 0;
    font-size: 13.5px; color: #3730a3; margin-bottom: 14px;
}}
.notice-warn {{
    background: #fffbeb; border-left-color: {AMBER}; color: #92400e;
}}
.notice-err {{
    background: #fef2f2; border-left-color: {RED}; color: #991b1b;
}}
</style>
"""


def inject() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def difficulty_badge(diff: str) -> str:
    cls = {"入门": "badge-intro", "简单": "badge-easy", "中等": "badge-medium", "困难": "badge-hard"}
    return f'<span class="badge {cls.get(diff, "badge-tag")}">{diff}</span>'


def tag_badges(tags, limit: int = 5) -> str:
    shown = list(tags)[:limit]
    html = "".join(f'<span class="badge badge-tag">{t}</span>' for t in shown)
    if len(tags) > limit:
        html += f'<span class="badge badge-cat">+{len(tags) - limit}</span>'
    return html


def verdict_color(v: str) -> str:
    return VERDICT_COLOR.get(v, MUTED)


def escape(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
