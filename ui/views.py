"""主页面视图：题库列表、题目详情、提交记录、关于。"""
from __future__ import annotations

import html
import time
from typing import List, Optional

import streamlit as st

from oj.config import DEFAULT_LANG, SITE_NAME
from oj.core import submissions
from oj.core.models import DIFFICULTIES, Problem
from oj.core.store import ProblemSet
from oj.judge.engine import AC, Judge
from ui import editor as editor_ui
from ui import results as results_ui
from ui.knowledge import render_problem_knowledge_hint
from ui.theme import difficulty_badge, escape, tag_badges


def _goto(page: str, pid: Optional[str] = None) -> None:
    st.session_state.page = page
    if pid is not None:
        st.session_state.current_pid = pid
    st.rerun()


# ==================================================================== 题库列表

def render_problem_list(ps: ProblemSet, knowledge: Optional[dict] = None) -> None:
    kw = st.session_state.filter_keyword
    diff = st.session_state.filter_difficulty
    cat = st.session_state.filter_category
    tag = st.session_state.filter_tag

    items = ps.search(
        keyword=kw,
        difficulty=None if diff == "全部" else diff,
        category=None if cat == "全部" else cat,
        tags=None if tag == "全部" else [tag],
    )

    # ---------------- 头部
    st.markdown(
        f"""
        <div style="margin-bottom:18px;">
          <div style="font-size:27px;font-weight:800;letter-spacing:-.5px;color:#0f172a;">
            题库
          </div>
          <div style="font-size:13.5px;color:#64748b;margin-top:4px;">
            共 {len(items)} 道题目
            {'（已筛选）' if (kw or diff != '全部' or cat != '全部' or tag != '全部') else ''}
            · 点击任意题目进入作答
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not items:
        st.markdown(
            '<div class="notice notice-warn">没有匹配的题目，试试调整筛选条件。</div>',
            unsafe_allow_html=True,
        )
        return

    # ---------------- 按知识点分组
    grouped: dict[str, List[Problem]] = {}
    for p in items:
        grouped.setdefault(p.category or "未分类", []).append(p)

    # 记录已提交状态，便于显示
    submitted = _submitted_map()

    for cat_name, plist in grouped.items():
        st.markdown(f'<div class="dsoj-h">{escape(cat_name)}</div>', unsafe_allow_html=True)
        rows = []
        for p in plist:
            badge = submitted.get(p.id)
            status = ""
            if badge == "AC":
                status = '<span class="badge badge-easy">已通过</span>'
            elif badge:
                status = f'<span class="badge badge-medium">已尝试</span>'
            rows.append(
                f'<tr>'
                f'<td class="id">{escape(p.id)}</td>'
                f'<td><b>{escape(p.title)}</b></td>'
                f'<td>{difficulty_badge(p.difficulty)}</td>'
                f'<td>{tag_badges(p.tags)}</td>'
                f'<td style="color:#64748b;font-size:12.5px;">{len(p.tests)} 点 · {p.total_score} 分</td>'
                f'<td>{status}</td>'
                f'</tr>'
            )

        st.markdown(
            f"""
            <table class="dsoj-table">
              <thead><tr>
                <th style="width:150px;">题号</th>
                <th>标题</th>
                <th style="width:78px;">难度</th>
                <th>标签</th>
                <th style="width:118px;">测试数据</th>
                <th style="width:86px;">状态</th>
              </tr></thead>
              <tbody>{''.join(rows)}</tbody>
            </table>
            """,
            unsafe_allow_html=True,
        )

        # 用按钮进入（Streamlit 表格无法直接点击行）
        cols = st.columns(min(len(plist), 4))
        for i, p in enumerate(plist):
            with cols[i % min(len(plist), 4)]:
                if st.button(
                    f"▶ {p.title[:14]}",
                    key=f"open_{p.id}",
                    use_container_width=True,
                ):
                    _goto("problem", p.id)
        st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)


def _submitted_map() -> dict:
    """{problem_id: 最高状态}，AC 优先于其它。"""
    out: dict = {}
    for r in submissions.list_submissions(limit=1000):
        pid = r.get("problem_id")
        if not pid:
            continue
        v = r.get("verdict")
        if out.get(pid) == "AC":
            continue
        out[pid] = "AC" if v == AC else "TRIED"
    return out


# ==================================================================== 题目详情

def render_problem_detail(ps: ProblemSet, knowledge: Optional[dict] = None) -> None:
    pid = st.session_state.current_pid
    problem = ps.get(pid) if pid else None
    if problem is None:
        st.markdown('<div class="notice notice-err">题目不存在。</div>', unsafe_allow_html=True)
        if st.button("← 返回题库"):
            _goto("problems")
        return

    if st.button("← 返回题库", key="back_to_list"):
        _goto("problems")

    # 若该题已被知识点总结引用，显示归属提示
    if knowledge:
        render_problem_knowledge_hint(knowledge, problem.id)

    _render_statement(problem)
    st.markdown('<hr class="hr-soft">', unsafe_allow_html=True)
    _render_workspace(problem)


def _render_statement(p: Problem) -> None:
    src = ""
    if p.source_name:
        if p.source_url:
            src = (
                f'<a href="{escape(p.source_url)}" target="_blank" '
                f'style="color:#4f46e5;text-decoration:none;">{escape(p.source_name)} ↗</a>'
            )
        else:
            src = escape(p.source_name)

    st.markdown(
        f"""
        <div style="margin-bottom:6px;">
          <div class="dsoj-title">{escape(p.title)}</div>
          <div class="dsoj-sub">题号：{escape(p.id)}{f' · 来源：{src}' if src else ''}</div>
          <div class="dsoj-meta-row">
            {difficulty_badge(p.difficulty)}
            <span class="badge badge-cat">{escape(p.category or '未分类')}</span>
            {tag_badges(p.tags, limit=8)}
            <span class="badge badge-cat">时间限制 {p.time_limit:g}s</span>
            <span class="badge badge-cat">内存限制 {p.memory_limit}MB</span>
            <span class="badge badge-cat">共 {len(p.tests)} 个测试点</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="dsoj-h">题目描述</div>', unsafe_allow_html=True)
    st.markdown(p.statement)

    if p.input_format:
        st.markdown('<div class="dsoj-h">输入格式</div>', unsafe_allow_html=True)
        st.markdown(p.input_format)

    if p.output_format:
        st.markdown('<div class="dsoj-h">输出格式</div>', unsafe_allow_html=True)
        st.markdown(p.output_format)

    if p.constraints:
        st.markdown('<div class="dsoj-h">数据范围与约定</div>', unsafe_allow_html=True)
        st.markdown("\n".join(f"- {c}" for c in p.constraints))

    if p.samples:
        st.markdown('<div class="dsoj-h">样例</div>', unsafe_allow_html=True)
        for i, s in enumerate(p.samples, 1):
            explain = (
                f'<div class="sample-explain">{escape(s.explain)}</div>'
                if s.explain else ""
            )
            st.markdown(
                f"""
                <div class="sample-box">
                  <div class="sample-head">样例 {i}</div>
                  <div class="sample-body">
                    <div class="sample-col">
                      <div class="sample-lbl">输入</div>
                      <pre class="sample-pre">{escape(s.input.rstrip()) or '(空)'}</pre>
                    </div>
                    <div class="sample-col">
                      <div class="sample-lbl">输出</div>
                      <pre class="sample-pre">{escape(s.output.rstrip()) or '(空)'}</pre>
                    </div>
                  </div>
                  {explain}
                </div>
                """,
                unsafe_allow_html=True,
            )

    if p.hint:
        st.markdown('<div class="dsoj-h">解题提示</div>', unsafe_allow_html=True)
        with st.expander("点击展开提示", expanded=False):
            st.markdown(p.hint)


def _render_workspace(p: Problem) -> None:
    """代码编辑 + 运行 + 提交。"""
    st.markdown('<div class="dsoj-h">作答区</div>', unsafe_allow_html=True)

    tc = st.session_state.toolchain or {}
    if not tc.get("available"):
        st.markdown(
            f'<div class="notice notice-err"><b>无法判题：</b>'
            f'{escape(tc.get("name", "未检测到 C++ 编译器"))}。'
            f'请切换到「关于」页面查看安装说明。</div>',
            unsafe_allow_html=True,
        )

    # ---------------- 代码
    starters = p.starter_code or {}
    default_code = starters.get("cpp") or starters.get(DEFAULT_LANG) or _DEFAULT_TEMPLATE
    code_key = f"code_{p.id}"
    if code_key not in st.session_state.code:
        st.session_state.code[code_key] = default_code

    left, right = st.columns([3, 2], gap="large")

    with left:
        st.caption(
            f"C++17 · 编辑器："
            f"{'Monaco（语法高亮）' if editor_ui.editor_available() else '纯文本框'}"
        )
        code = editor_ui.code_editor(
            key=f"ace_{p.id}",
            value=st.session_state.code[code_key],
            language="c_cpp",
            height=480,
        )
        st.session_state.code[code_key] = code

        c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
        with c1:
            run_clicked = st.button("▶ 运行", use_container_width=True, disabled=not tc.get("available"))
        with c2:
            submit_clicked = st.button(
                "🚀 提交判题", type="primary", use_container_width=True,
                disabled=not tc.get("available"),
            )
        with c3:
            if st.button("↺ 重置代码", use_container_width=True):
                st.session_state.code[code_key] = default_code
                st.session_state[f"ace_{p.id}"] = default_code
                st.rerun()
        with c4:
            sample_only = st.checkbox("仅测样例", value=False, help="加快反馈速度")

        if p.reference.get("cpp"):
            with st.expander("查看参考解（AC 代码）"):
                editor_ui.render_code_block(p.reference["cpp"])

    with right:
        st.caption("自定义输入（用于「运行」）")
        st.session_state.custom_input = st.text_area(
            "stdin",
            value=st.session_state.custom_input
            or (p.samples[0].input if p.samples else ""),
            height=150,
            label_visibility="collapsed",
            key=f"stdin_{p.id}",
        )
        st.caption("判题结果")

        holder = st.container()

        if run_clicked:
            with st.spinner("编译并运行中…"):
                judge = Judge()
                out = judge.run_with_input(
                    code,
                    st.session_state.custom_input,
                    time_limit=p.time_limit,
                    memory_limit_mb=p.memory_limit,
                )
            st.session_state.run_output = out
            st.session_state.last_result = None

        if submit_clicked:
            with st.spinner("编译并判题中…"):
                judge = Judge()
                res = judge.judge(p, code, run_samples_only=sample_only)
            st.session_state.last_result = res
            st.session_state.run_output = None
            submissions.save_submission(
                {
                    "problem_id": p.id,
                    "problem_title": p.title,
                    "difficulty": p.difficulty,
                    "category": p.category,
                    "lang": "cpp17",
                    "verdict": res.verdict,
                    "passed": res.passed,
                    "total": res.total,
                    "score": res.score,
                    "max_score": res.max_score,
                    "time": res.time,
                    "memory_kb": res.memory_kb,
                    "source": code,
                    "message": res.message,
                }
            )

        with holder:
            if st.session_state.last_result is not None:
                res = st.session_state.last_result
                results_ui.render_verdict_header(res)
                if res.verdict == "CE":
                    results_ui.render_compile_error(res)
                else:
                    results_ui.render_cases(res)
                    results_ui.render_case_details(res)
            elif st.session_state.run_output is not None:
                results_ui.render_run_output(st.session_state.run_output)
            else:
                st.markdown(
                    '<div style="color:#94a3b8;font-size:13px;padding:14px 0;">'
                    '点击「运行」用自定义输入测试，或点击「提交判题」跑完整测试点。</div>',
                    unsafe_allow_html=True,
                )


_DEFAULT_TEMPLATE = """#include <cstdio>

int main() {
    // 从标准输入读取数据，向标准输出打印结果
    return 0;
}
"""


# ==================================================================== 提交记录

def render_submissions(ps: ProblemSet) -> None:
    st.markdown(
        '<div style="font-size:27px;font-weight:800;letter-spacing:-.5px;'
        'color:#0f172a;margin-bottom:4px;">提交记录</div>',
        unsafe_allow_html=True,
    )

    records = submissions.list_submissions(limit=200)
    if not records:
        st.markdown(
            '<div class="notice">还没有提交记录，去题库挑一道题开始吧。</div>',
            unsafe_allow_html=True,
        )
        return

    n_ac = sum(1 for r in records if r.get("verdict") == AC)
    st.markdown(
        f'<div style="font-size:13.5px;color:#64748b;margin-bottom:16px;">'
        f'最近 {len(records)} 次提交 · 通过 {n_ac} 次 · '
        f'通过率 {n_ac / len(records) * 100:.1f}%</div>',
        unsafe_allow_html=True,
    )

    rows = []
    for r in records:
        v = r.get("verdict", "?")
        color = {
            "AC": "#16a34a", "WA": "#dc2626", "TLE": "#d97706",
            "MLE": "#7c3aed", "RE": "#dc2626", "CE": "#0ea5e9",
        }.get(v, "#64748b")
        ts = time.strftime("%m-%d %H:%M", time.localtime(r.get("time", 0)))
        rows.append(
            f'<tr>'
            f'<td style="color:#64748b;font-size:12.5px;white-space:nowrap;">{ts}</td>'
            f'<td><b>{escape(r.get("problem_title", ""))}</b>'
            f'<div class="id" style="color:#94a3b8;font-size:11.5px;">'
            f'{escape(r.get("problem_id", ""))}</div></td>'
            f'<td>{difficulty_badge(r.get("difficulty", ""))}</td>'
            f'<td style="color:{color};font-weight:700;">{escape(v)}</td>'
            f'<td style="font-size:12.5px;color:#475569;">'
            f'{r.get("passed", 0)}/{r.get("total", 0)}</td>'
            f'<td style="font-size:12.5px;color:#64748b;">'
            f'{(r.get("time") or 0) * 1000:.0f} ms</td>'
            f'</tr>'
        )

    st.markdown(
        f"""
        <table class="dsoj-table">
          <thead><tr>
            <th style="width:104px;">时间</th>
            <th>题目</th>
            <th style="width:78px;">难度</th>
            <th style="width:64px;">结果</th>
            <th style="width:82px;">通过</th>
            <th style="width:88px;">耗时</th>
          </tr></thead>
          <tbody>{''.join(rows)}</tbody>
        </table>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div style="height:14px;"></div>', unsafe_allow_html=True)
    with st.expander("查看某次提交的代码"):
        labels = {
            f'{time.strftime("%m-%d %H:%M", time.localtime(r.get("time", 0)))} · '
            f'{r.get("problem_title", "")} · {r.get("verdict", "")}': r
            for r in records[:60]
        }
        pick = st.selectbox("选择提交", list(labels.keys()), key="pick_sub")
        if pick:
            rec = labels[pick]
            st.caption(
                f'{rec.get("verdict")} · 通过 {rec.get("passed")}/{rec.get("total")} · '
                f'{rec.get("message", "")}'
            )
            editor_ui.render_code_block(rec.get("source", ""))

    if st.button("清空所有提交记录"):
        submissions.clear_submissions()
        st.rerun()


# ==================================================================== 关于

def render_about(ps: ProblemSet) -> None:
    tc = st.session_state.toolchain or {}
    stats = ps.stats()

    st.markdown(
        '<div style="font-size:27px;font-weight:800;letter-spacing:-.5px;'
        'color:#0f172a;margin-bottom:16px;">关于本系统</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="dsoj-card">
          <div style="font-size:15px;font-weight:700;color:#0f172a;margin-bottom:10px;">
            🧩 {escape(SITE_NAME)}
          </div>
          <div style="font-size:13.5px;color:#475569;line-height:1.85;">
            一个面向**数据结构**课程的在线判题系统。题库按知识点组织，
            每道题包含完整题面、样例、多个测试点与 C++ 参考解。<br>
            当前共收录 <b>{stats['total']}</b> 道题目、<b>{stats['test_count']}</b> 个测试点，
            覆盖 <b>{stats['category_count']}</b> 个知识点分类。
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="dsoj-h">题目分布</div>', unsafe_allow_html=True)
        rows = []
        for cat, n in stats["by_category"].items():
            rows.append(
                f'<tr><td>{escape(cat)}</td>'
                f'<td style="text-align:right;font-weight:700;">{n}</td></tr>'
            )
        total = stats["total"] or 1
        for d in DIFFICULTIES:
            n = stats["by_difficulty"].get(d, 0)
            if n:
                rows.append(
                    f'<tr><td>{difficulty_badge(d)}</td>'
                    f'<td style="text-align:right;font-weight:700;">{n}</td></tr>'
                )
        st.markdown(
            f'<table class="dsoj-table"><tbody>{"".join(rows)}</tbody></table>',
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown('<div class="dsoj-h">判题环境</div>', unsafe_allow_html=True)
        if tc.get("available"):
            st.markdown(
                f"""
                <div class="dsoj-card" style="border-color:#86efac;background:#f0fdf4;">
                  <div style="font-size:13.5px;color:#15803d;font-weight:600;">
                    ● 编译器已就绪
                  </div>
                  <div style="font-size:12.5px;color:#166534;margin-top:6px;
                              font-family:ui-monospace,monospace;">
                    {escape(tc.get("name", ""))}
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="dsoj-card" style="border-color:#fca5a5;background:#fef2f2;">
                  <div style="font-size:13.5px;color:#b91c1c;font-weight:600;">
                    ● 未检测到 C++ 编译器
                  </div>
                  <div style="font-size:13px;color:#7f1d1d;margin-top:8px;
                              line-height:1.75;white-space:pre-wrap;">{escape(tc.get("hint", ""))}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            """
            <div style="font-size:13px;color:#475569;line-height:1.9;margin-top:6px;">
              <b>判题流程</b><br>
              编译 → 逐测试点运行（限时/限内存）→ 输出比对 → 汇总判决
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="dsoj-h">判决说明</div>', unsafe_allow_html=True)
    st.markdown(
        """
| 判决 | 含义 | 常见原因 |
|---|---|---|
| **AC** | Accepted 通过 | 全部测试点输出正确 |
| **WA** | Wrong Answer 答案错误 | 逻辑有误，或输出格式不符 |
| **TLE** | Time Limit Exceeded 超时 | 算法复杂度过高，或死循环 |
| **MLE** | Memory Limit Exceeded 超内存 | 数组开得过大 |
| **RE** | Runtime Error 运行时错误 | 数组越界、除零、空指针、栈溢出 |
| **CE** | Compile Error 编译错误 | 语法错误，请看编译输出 |
| **OLE** | Output Limit Exceeded 输出超限 | 输出量过大，可能有死循环 |
        """
    )

    st.markdown('<div class="dsoj-h">输出比对规则</div>', unsafe_allow_html=True)
    st.markdown(
        """
为了避免无关紧要的格式差异造成误判，判题采用**宽松比对**：

- 忽略**行尾空白**（` ` 和 `\\t`）
- 忽略**文末多余换行**
- 不忽略行内 token 之间的空格数量与顺序

因此你**不必**纠结末尾少了或多了个换行，但输出的数字顺序与个数必须完全正确。
        """
    )

    st.markdown('<div class="dsoj-h">本地运行与部署</div>', unsafe_allow_html=True)
    st.markdown(
        """
```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 校验题库（会用参考解编译运行全部测试点）
python scripts/validate_problems.py

# 3. 启动 Web 界面
streamlit run app.py
```

浏览器打开 `http://localhost:8501` 即可开始答题。
        """
    )
