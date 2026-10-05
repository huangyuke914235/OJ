"""知识点总结视图：题型清单 + 方法总结 + 复杂度对照 + 复习要点。"""
from __future__ import annotations

from typing import Dict, List

import streamlit as st

from oj.core.knowledge import Knowledge, link_problems
from oj.core.store import ProblemSet
from ui import theme


def _goto(page: str, pid: str | None = None, cat: str | None = None) -> None:
    st.session_state.page = page
    if pid is not None:
        st.session_state.current_pid = pid
    if cat is not None:
        st.session_state.current_category = cat
    st.rerun()


def _card(html: str) -> None:
    st.markdown(f'<div class="kb-card">{html}</div>', unsafe_allow_html=True)


def render_knowledge_list(knowledge: Dict[str, Knowledge], ps: ProblemSet) -> None:
    """知识点总览：每个分类一张卡片，显示题型/方法数量与概要。"""
    st.markdown(
        '<div class="page-title">知识点总结</div>'
        '<div class="page-sub">按知识点整理的题型清单与方法总结，'
        '可作为复习提纲与按题型刷题的索引。</div>',
        unsafe_allow_html=True,
    )

    total_pat = sum(k.pattern_count for k in knowledge.values())
    total_tech = sum(k.technique_count for k in knowledge.values())
    total_prob = len(ps)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("知识点", len(knowledge))
    c2.metric("题型总数", total_pat)
    c3.metric("方法模板", total_tech)
    c4.metric("配套题目", total_prob)

    st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)

    for cat, k in sorted(knowledge.items()):
        n_prob = sum(len(p.problems) for p in k.patterns)
        pat_names = " · ".join(p.name for p in k.patterns[:4])
        if k.pattern_count > 4:
            pat_names += f" 等 {k.pattern_count} 类"

        cols = st.columns([7, 2, 2])
        with cols[0]:
            st.markdown(
                f'<div style="font-size:15.5px;font-weight:700;color:#0f172a;">{theme.escape(k.name)}</div>'
                f'<div style="font-size:12.5px;color:#64748b;margin-top:4px;line-height:1.6;">'
                f'{theme.escape(k.summary[:110])}{"…" if len(k.summary) > 110 else ""}</div>'
                f'<div style="font-size:12px;color:#94a3b8;margin-top:6px;">{theme.escape(pat_names)}</div>',
                unsafe_allow_html=True,
            )
        with cols[1]:
            st.markdown(
                f'<div style="font-size:12px;color:#64748b;text-align:right;padding-top:6px;">'
                f'题型 <b>{k.pattern_count}</b><br>方法 <b>{k.technique_count}</b></div>',
                unsafe_allow_html=True,
            )
        with cols[2]:
            if st.button("查看", key=f"kb_{cat}", use_container_width=True):
                _goto("knowledge_detail", cat=cat)

        st.markdown('<hr class="hr-soft">', unsafe_allow_html=True)


def render_knowledge_detail(knowledge: Dict[str, Knowledge], ps: ProblemSet) -> None:
    """单个知识点的详细总结。"""
    cat = st.session_state.get("current_category")
    k = knowledge.get(cat) if cat else None
    if k is None:
        st.warning("未找到该知识点，请从列表重新进入。")
        if st.button("返回知识点列表"):
            _goto("knowledge")
        return

    if st.button("← 返回知识点列表", key="kb_back"):
        _goto("knowledge")

    st.markdown(
        f'<div class="page-title">{theme.escape(k.name)}</div>'
        f'<div class="page-sub">{theme.escape(k.summary)}</div>',
        unsafe_allow_html=True,
    )

    by_pattern = link_problems(k, ps.items)

    tab_pat, tab_tech, tab_cx, tab_todo = st.tabs(
        ["📋 题型清单", "🛠 方法总结", "📊 复杂度对照", "✅ 复习要点"]
    )

    # ------------------------------------------------ 题型清单
    with tab_pat:
        if k.overview:
            st.markdown(k.overview)
            st.markdown('<hr class="hr-soft">', unsafe_allow_html=True)

        for i, pat in enumerate(k.patterns, 1):
            probs: List = by_pattern.get(pat.name, [])
            st.markdown(
                f'<div class="kb-pat">'
                f'<div class="kb-pat-h"><span class="kb-pat-i">{i}</span>'
                f'{theme.escape(pat.name)}</div>'
                f'<div class="kb-pat-s"><b>识别信号</b>：{theme.escape(pat.signal)}</div>'
                f'<div class="kb-pat-body">{_md(pat.idea)}</div>'
                f'<div class="kb-pat-c"><b>复杂度</b>：{theme.escape(pat.complexity)}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            if pat.pitfalls:
                items = "".join(f"<li>{theme.escape(x)}</li>" for x in pat.pitfalls)
                st.markdown(
                    f'<div class="kb-pitfall"><b>易错点</b><ul>{items}</ul></div>',
                    unsafe_allow_html=True,
                )

            if probs:
                st.markdown(
                    '<div style="font-size:12.5px;color:#64748b;margin:6px 0 4px;">'
                    '<b>对应题目</b></div>',
                    unsafe_allow_html=True,
                )
                cols = st.columns(min(4, len(probs)))
                for idx, p in enumerate(probs):
                    with cols[idx % len(cols)]:
                        if st.button(
                            f"{p.id} · {p.title}",
                            key=f"kbp_{cat}_{i}_{p.id}",
                            use_container_width=True,
                        ):
                            _goto("problem", pid=p.id)
            st.markdown('<hr class="hr-soft">', unsafe_allow_html=True)

    # ------------------------------------------------ 方法总结
    with tab_tech:
        if not k.techniques:
            st.info("该知识点暂无方法模板。")
        for t in k.techniques:
            st.markdown(
                f'<div class="kb-tech-h">{theme.escape(t.name)}</div>'
                f'<div class="kb-tech-d">{_md(t.detail)}</div>',
                unsafe_allow_html=True,
            )
            if t.code:
                st.code(t.code, language=t.lang)
            st.markdown('<div style="height:6px"></div>', unsafe_allow_html=True)

    # ------------------------------------------------ 复杂度对照
    with tab_cx:
        if not k.complexity_table:
            st.info("该知识点暂无复杂度对照表。")
        else:
            rows = "".join(
                f'<tr><td class="kb-td-op">{theme.escape(r.op)}</td>'
                f'<td class="kb-td-t">{theme.escape(r.time)}</td>'
                f'<td class="kb-td-n">{theme.escape(r.note)}</td></tr>'
                for r in k.complexity_table
            )
            st.markdown(
                '<table class="kb-table"><thead><tr>'
                '<th>操作 / 算法</th><th>时间复杂度</th><th>说明</th>'
                f'</tr></thead><tbody>{rows}</tbody></table>',
                unsafe_allow_html=True,
            )

    # ------------------------------------------------ 复习要点
    with tab_todo:
        if not k.checklist:
            st.info("该知识点暂无复习要点。")
        else:
            items = "".join(f"<li>{theme.escape(x)}</li>" for x in k.checklist)
            st.markdown(f'<ul class="kb-check">{items}</ul>', unsafe_allow_html=True)

        st.markdown('<hr class="hr-soft">', unsafe_allow_html=True)
        n_prob = sum(len(p.problems) for p in k.patterns)
        if st.button(f"查看本知识点的全部题目（{n_prob} 题）", key=f"kb_all_{cat}"):
            st.session_state.filter_category = k.name
            st.session_state.filter_keyword = ""
            st.session_state.filter_difficulty = "全部"
            st.session_state.filter_tag = "全部"
            _goto("problems")


def _md(text: str) -> str:
    """极简 Markdown 处理：转义 HTML，保留 **粗体** 与 `代码`。"""
    import re

    s = theme.escape(text)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = s.replace("\n", "<br>")
    return s


def render_problem_knowledge_hint(knowledge: Dict[str, Knowledge], problem_id: str) -> None:
    """在题目详情页显示「本题所属题型」的小提示。"""
    for cat, k in knowledge.items():
        for pat in k.patterns:
            if problem_id in pat.problems:
                st.markdown(
                    f'<div class="kb-hint">📘 本题属于知识点'
                    f'<b>{theme.escape(k.name)}</b> 的题型「{theme.escape(pat.name)}」'
                    f'</div>',
                    unsafe_allow_html=True,
                )
                return
