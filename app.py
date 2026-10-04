"""DS-OJ 在线判题系统 — Streamlit 前端入口。

本地运行::

    streamlit run app.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st  # noqa: E402

from oj.config import DEFAULT_LANG, SITE_NAME, SITE_SLOGAN  # noqa: E402
from oj.core import submissions  # noqa: E402
from oj.core.store import default_problem_set  # noqa: E402
from oj.judge.engine import VERDICT_COLOR, VERDICT_ICON, VERDICT_TEXT, Judge  # noqa: E402
from oj.judge.toolchain import toolchain_info  # noqa: E402

# 页面级 UI 组件
from ui import editor, results, sidebar, theme, views  # noqa: E402


def _init_state() -> None:
    defaults = {
        "page": "problems",           # problems | problem | submissions | about
        "current_pid": None,
        "code": {},                   # {problem_id: source}
        "last_result": None,          # JudgeResult
        "last_mode": None,            # "judge" | "run"
        "run_output": None,           # 自定义输入运行的结果
        "filter_keyword": "",
        "filter_difficulty": "全部",
        "filter_category": "全部",
        "filter_tag": "全部",
        "pending_verdict": None,
        "custom_input": "",
        "toolchain": None,
    }
    for k, v in defaults.items():
        st.session_state.setdefault(k, v)


def main() -> None:
    st.set_page_config(
        page_title=SITE_NAME,
        page_icon="🧩",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    theme.inject()
    _init_state()

    problemset = default_problem_set()
    if st.session_state.toolchain is None:
        st.session_state.toolchain = toolchain_info()

    sidebar.render(problemset)

    page = st.session_state.page
    if page == "problems":
        views.render_problem_list(problemset)
    elif page == "problem":
        views.render_problem_detail(problemset)
    elif page == "submissions":
        views.render_submissions(problemset)
    else:
        views.render_about(problemset)


if __name__ == "__main__":
    main()
