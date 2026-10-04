"""代码编辑器组件。

优先使用 streamlit-code-editor（Monaco，带语法高亮）；
未安装时回退到 st.text_area，保证在最小依赖下也能运行。
"""
from __future__ import annotations

from typing import Optional

import streamlit as st

try:
    from streamlit_ace import st_ace  # type: ignore
    _HAS_ACE = True
except ImportError:  # pragma: no cover
    st_ace = None  # type: ignore
    _HAS_ACE = False


def editor_available() -> bool:
    return _HAS_ACE


def code_editor(
    key: str,
    value: str,
    height: int = 460,
    language: str = "c_cpp",
    readonly: bool = False,
) -> str:
    """渲染代码编辑器并返回当前内容。"""
    if _HAS_ACE:
        content = st_ace(
            value=value,
            language=language,
            theme="chrome",
            key=key,
            height=height,
            font_size=14,
            tab_size=4,
            show_gutter=True,
            wrap=True,
            auto_update=False,
            readonly=readonly,
            keybinding="vscode",
        )
        # st_ace 在未交互时可能返回 None，此时沿用原值
        return value if content is None else content

    return st.text_area(
        "代码",
        value=value,
        height=height,
        key=key,
        label_visibility="collapsed",
        disabled=readonly,
    )


def render_code_block(code: str, language: str = "cpp") -> None:
    """只读展示代码（带语法高亮的只读编辑器）。"""
    if _HAS_ACE:
        st_ace(
            value=code,
            language=language,
            theme="chrome",
            height=min(620, 26 * code.count("\n") + 60),
            font_size=13.5,
            readonly=True,
            key=f"ro_{abs(hash(code)) % (10 ** 9)}",
        )
    else:
        st.markdown(f'<pre class="code">{_esc(code)}</pre>', unsafe_allow_html=True)


def _esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
