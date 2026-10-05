"""侧边栏：导航、筛选、环境状态。"""
from __future__ import annotations

import streamlit as st

from oj.config import SITE_NAME, SITE_SLOGAN
from oj.core.models import DIFFICULTIES
from oj.core.store import ProblemSet


def _go(page: str, pid: str | None = None) -> None:
    st.session_state.page = page
    if pid is not None:
        st.session_state.current_pid = pid
    st.rerun()


def render(ps: ProblemSet) -> None:
    with st.sidebar:
        st.markdown(
            f"""
            <div style="padding:2px 0 14px 0;">
              <div style="font-size:21px;font-weight:800;letter-spacing:-.4px;
                          color:#0f172a;">🧩 DS-OJ</div>
              <div style="font-size:12.5px;color:#64748b;margin-top:3px;line-height:1.45;">
                数据结构在线判题系统
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ---------------- 导航
        page = st.session_state.page
        nav = [
            ("problems", "📚  题库"),
            ("knowledge", "📘  知识点"),
            ("submissions", "📝  提交记录"),
            ("about", "ℹ️  关于"),
        ]
        for key, label in nav:
            active = (
                (page == key)
                or (key == "problems" and page == "problem")
                or (key == "knowledge" and page == "knowledge_detail")
            )
            if st.button(
                label,
                key=f"nav_{key}",
                use_container_width=True,
                type="primary" if active else "secondary",
            ):
                _go(key)

        st.markdown('<hr class="hr-soft">', unsafe_allow_html=True)

        # ---------------- 筛选
        st.markdown(
            '<div style="font-size:12px;font-weight:700;color:#64748b;'
            'letter-spacing:.06em;margin-bottom:8px;">筛 选</div>',
            unsafe_allow_html=True,
        )

        st.session_state.filter_keyword = st.text_input(
            "搜索",
            value=st.session_state.filter_keyword,
            placeholder="题号 / 标题 / 标签…",
            label_visibility="collapsed",
        )

        cats = ["全部"] + ps.categories()
        cat = st.selectbox(
            "知识点", cats,
            index=cats.index(st.session_state.filter_category)
            if st.session_state.filter_category in cats else 0,
        )
        st.session_state.filter_category = cat

        diffs = ["全部"] + DIFFICULTIES
        diff = st.selectbox(
            "难度", diffs,
            index=diffs.index(st.session_state.filter_difficulty)
            if st.session_state.filter_difficulty in diffs else 0,
        )
        st.session_state.filter_difficulty = diff

        tags = ["全部"] + ps.all_tags()
        tag = st.selectbox(
            "标签", tags,
            index=tags.index(st.session_state.filter_tag)
            if st.session_state.filter_tag in tags else 0,
        )
        st.session_state.filter_tag = tag

        if st.button("重置筛选", use_container_width=True):
            st.session_state.filter_keyword = ""
            st.session_state.filter_difficulty = "全部"
            st.session_state.filter_category = "全部"
            st.session_state.filter_tag = "全部"
            st.rerun()

        st.markdown('<hr class="hr-soft">', unsafe_allow_html=True)

        # ---------------- 题库统计
        stats = ps.stats()
        st.markdown(
            f"""
            <div style="font-size:12px;font-weight:700;color:#64748b;
                        letter-spacing:.06em;margin-bottom:8px;">题 库 概 览</div>
            <div style="font-size:13px;line-height:1.9;color:#334155;">
              <div>共 <b>{stats['total']}</b> 道题目</div>
              <div>覆盖 <b>{stats['category_count']}</b> 个知识点</div>
              <div>共 <b>{stats['test_count']}</b> 个测试点</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<hr class="hr-soft">', unsafe_allow_html=True)

        # ---------------- 环境状态
        tc = st.session_state.toolchain or {}
        if tc.get("available"):
            st.markdown(
                f'<div style="font-size:12.5px;color:#15803d;line-height:1.6;">'
                f'● 编译器就绪<br><span style="color:#64748b;font-size:11.5px;">'
                f'{tc.get("name", "")}</span></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div style="font-size:12.5px;color:#b91c1c;line-height:1.6;">'
                '● 未检测到 C++ 编译器</div>',
                unsafe_allow_html=True,
            )
            if st.button("查看安装说明", use_container_width=True):
                _go("about")

        st.markdown(
            '<div style="margin-top:18px;font-size:11px;color:#94a3b8;line-height:1.6;">'
            '本地版 · Streamlit<br>判题语言：C++17</div>',
            unsafe_allow_html=True,
        )
