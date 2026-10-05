"""导出静态题库站点（用于 GitHub Pages）。

把题库导出为
  static/
    index.html          题目列表
    problems/<id>.html  每道题的独立页面
    problems.json       原始题库数据（供前端检索/二次开发）
    style.css

题面为 Markdown，本脚本用轻量渲染器转换，**不依赖第三方 Markdown 库**，
保证可在 CI 中零依赖运行。

用法::

    python scripts/build_static.py
"""
from __future__ import annotations

import html
import json
import re
import shutil
import sys
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from oj.config import SITE_NAME, SITE_SLOGAN, STATIC_DIR  # noqa: E402
from oj.core.knowledge import load_all as load_knowledge  # noqa: E402
from oj.core.models import DIFFICULTIES, Problem, load_all  # noqa: E402
from oj.core.store import ProblemSet  # noqa: E402
from oj.config import PROBLEMS_DIR  # noqa: E402


# ============================================================ Markdown 渲染

def _inline(text: str) -> str:
    """处理行内 Markdown：代码、粗体、斜体、链接。"""
    # 先保护 code span，避免其中内容被后续规则破坏
    codes: List[str] = []

    def _stash(m: "re.Match[str]") -> str:
        codes.append(m.group(1))
        return f"\x00{len(codes) - 1}\x00"

    text = re.sub(r"`([^`]+)`", _stash, text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(
        r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
        r'<a href="\2" target="_blank" rel="noopener">\1</a>',
        text,
    )
    for i, c in enumerate(codes):
        text = text.replace(f"\x00{i}\x00", f"<code>{html.escape(c)}</code>")
    return text


def render_markdown(md: str) -> str:
    """把题面 Markdown 渲染为 HTML（支持标题、列表、表格、代码块、段落）。"""
    if not md or not md.strip():
        return ""

    lines = md.replace("\r\n", "\n").split("\n")
    out: List[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # ---------- 围栏代码块
        if line.strip().startswith("```"):
            lang = line.strip()[3:].strip()
            buf = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            cls = f' class="language-{html.escape(lang)}"' if lang else ""
            out.append(f"<pre><code{cls}>{html.escape(chr(10).join(buf))}</code></pre>")
            continue

        # ---------- 表格
        if "|" in line and i + 1 < len(lines) and re.match(r"^\s*\|?[\s:|-]+\|", lines[i + 1]):
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            th = "".join(f"<th>{_inline(c)}</th>" for c in header)
            trs = "".join(
                "<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in r) + "</tr>" for r in rows
            )
            out.append(f"<table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>")
            continue

        # ---------- 标题
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>{_inline(m.group(2))}</h{lvl}>")
            i += 1
            continue

        # ---------- 无序列表
        if re.match(r"^\s*[-*]\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append(re.sub(r"^\s*[-*]\s+", "", lines[i]))
                i += 1
            out.append("<ul>" + "".join(f"<li>{_inline(x)}</li>" for x in items) + "</ul>")
            continue

        # ---------- 有序列表
        if re.match(r"^\s*\d+\.\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
                items.append(re.sub(r"^\s*\d+\.\s+", "", lines[i]))
                i += 1
            out.append("<ol>" + "".join(f"<li>{_inline(x)}</li>" for x in items) + "</ol>")
            continue

        # ---------- 引用块
        if line.strip().startswith(">"):
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip()[1:].strip())
                i += 1
            out.append(f"<blockquote>{_inline(' '.join(buf))}</blockquote>")
            continue

        # ---------- 空行
        if not line.strip():
            i += 1
            continue

        # ---------- 段落（合并连续行）
        buf = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(
            r"^(#{1,6}\s|\s*[-*]\s|\s*\d+\.\s|>|```)", lines[i]
        ) and "|" not in lines[i]:
            buf.append(lines[i])
            i += 1
        out.append(f"<p>{_inline(' '.join(buf))}</p>")

    return "\n".join(out)


# ============================================================ 页面模板

def _esc(s: str) -> str:
    return html.escape(str(s), quote=True)


STYLE = """
:root{--ink:#0f172a;--muted:#64748b;--border:#e2e8f0;--soft:#f8fafc;
--accent:#4f46e5;--easy:#15803d;--medium:#b45309;--hard:#b91c1c;--intro:#1d4ed8}
*{box-sizing:border-box}
body{margin:0;background:#fff;color:var(--ink);
font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC",
"Hiragino Sans GB","Microsoft YaHei",sans-serif;line-height:1.7}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:1000px;margin:0 auto;padding:0 24px}
header.site{border-bottom:1px solid var(--border);background:#fff;
position:sticky;top:0;z-index:10}
header.site .wrap{display:flex;align-items:center;gap:14px;height:60px}
header.site b{font-size:17px;letter-spacing:-.3px}
header.site span{font-size:13px;color:var(--muted)}
h1{font-size:27px;letter-spacing:-.5px;margin:28px 0 6px}
h2{font-size:18px;margin:28px 0 10px;padding-left:10px;border-left:3.5px solid var(--accent)}
h3{font-size:15.5px;margin:20px 0 8px}
p{margin:9px 0}
code{background:var(--soft);padding:1.5px 5px;border-radius:4px;
font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.9em}
pre{background:#0f172a;color:#e2e8f0;padding:14px 16px;border-radius:10px;
overflow-x:auto;font-size:13px;line-height:1.6}
pre code{background:none;color:inherit;padding:0}
table{width:100%;border-collapse:collapse;margin:12px 0;font-size:14px}
th{text-align:left;padding:9px 11px;background:var(--soft);color:var(--muted);
font-size:12.5px;border-bottom:1.5px solid var(--border)}
td{padding:9px 11px;border-bottom:1px solid #f1f5f9}
blockquote{margin:12px 0;padding:10px 15px;background:var(--soft);
border-left:3px solid var(--border);color:var(--muted)}
ul,ol{margin:9px 0;padding-left:24px}
li{margin:3px 0}
.card{border:1px solid var(--border);border-radius:12px;padding:16px 18px;
margin-bottom:12px;transition:border-color .15s,box-shadow .15s}
.card:hover{border-color:#c7d2fe;box-shadow:0 2px 10px rgba(79,70,229,.07)}
.badge{display:inline-block;padding:2.5px 9px;border-radius:999px;font-size:12px;
font-weight:600;white-space:nowrap}
.b-intro{background:#dbeafe;color:var(--intro)}
.b-easy{background:#dcfce7;color:var(--easy)}
.b-medium{background:#fef3c7;color:var(--medium)}
.b-hard{background:#fee2e2;color:var(--hard)}
.b-tag{background:#eef2ff;color:#4338ca}
.b-cat{background:#f1f5f9;color:#475569}
.meta{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:12px 0 4px}
.sub{color:var(--muted);font-size:13.5px}
.sample{border:1px solid var(--border);border-radius:10px;overflow:hidden;margin:12px 0}
.sample .h{background:var(--soft);padding:8px 14px;font-size:13px;font-weight:600;
color:var(--muted);border-bottom:1px solid var(--border)}
.sample .b{display:flex}
.sample .col{flex:1;padding:12px 14px;min-width:0}
.sample .col+.col{border-left:1px solid var(--border)}
.lbl{font-size:11.5px;font-weight:600;color:var(--muted);letter-spacing:.04em;
margin-bottom:6px;text-transform:uppercase}
.sample pre{background:none;color:var(--ink);padding:0;margin:0;font-size:13px;
white-space:pre-wrap;word-break:break-word;line-height:1.55}
.sample .ex{padding:10px 14px;font-size:13px;color:var(--muted);
border-top:1px dashed var(--border);background:#fcfcfd}
table.list td{padding:11px 12px}
table.list .id{color:var(--muted);font-family:ui-monospace,monospace;font-size:12px}
footer{border-top:1px solid var(--border);margin-top:44px;padding:22px 0;
color:var(--muted);font-size:13px}
.stats{display:flex;gap:26px;flex-wrap:wrap;margin:18px 0 6px}
.stats div{font-size:13.5px;color:var(--muted)}
.stats b{display:block;font-size:22px;color:var(--ink);font-weight:700}
/* ---------- 页头导航 ---------- */
.sitenav{margin-left:auto;display:flex;gap:6px}
.navlink{font-size:13.5px;color:var(--muted);padding:5px 11px;border-radius:8px}
.navlink:hover{background:var(--soft);color:var(--accent);text-decoration:none}
/* ---------- 知识点 ---------- */
.lead{font-size:14.5px;color:var(--muted);margin:6px 0 20px;line-height:1.75}
.kb-meta{display:flex;gap:22px;flex-wrap:wrap;margin:14px 0 24px;
padding:14px 18px;background:var(--soft);border-radius:10px;font-size:13.5px;
color:var(--muted)}
.kb-item{display:block;padding:16px 20px;border:1px solid var(--border);
border-radius:12px;margin-bottom:12px;color:inherit}
.kb-item:hover{border-color:var(--accent);text-decoration:none;
box-shadow:0 1px 8px rgba(79,70,229,.08)}
.kb-item-h{font-size:16px;font-weight:700;color:var(--ink);margin-bottom:5px}
.kb-item-s{font-size:13.5px;color:var(--muted);line-height:1.7}
.kb-item-m{font-size:12.5px;color:#94a3b8;margin-top:8px}
.kb-overview{font-size:14px;color:#334155;line-height:1.8;background:var(--soft);
border-radius:10px;padding:16px 20px;margin-bottom:24px}
.kb-pat{border:1px solid var(--border);border-radius:12px;padding:16px 20px;
margin-bottom:12px}
.kb-pat-h{font-size:15.5px;font-weight:700;color:var(--ink);display:flex;
align-items:center;gap:9px;margin-bottom:9px}
.kb-num{display:inline-flex;align-items:center;justify-content:center;
width:22px;height:22px;border-radius:50%;background:#eef2ff;color:var(--accent);
font-size:12.5px;font-weight:700;flex:0 0 auto}
.kb-signal{font-size:13px;color:#475569;background:var(--soft);border-radius:8px;
padding:8px 12px;margin-bottom:9px}
.kb-idea{font-size:13.5px;color:#334155;line-height:1.8}
.kb-cx{font-size:12.5px;color:var(--muted);margin-top:8px}
.kb-pit{background:#fffbeb;border-left:3px solid #f59e0b;padding:10px 15px;
border-radius:0 8px 8px 0;font-size:13px;color:#92400e;margin:10px 0}
.kb-pit ul{margin:5px 0 0;padding-left:20px}
.kb-pit li{margin:3px 0;line-height:1.6}
.kb-probs{font-size:13px;margin-top:10px;color:var(--muted)}
.kb-plink{display:inline-block;margin:3px 6px 3px 0;padding:3px 10px;
background:#eef2ff;color:var(--accent);border-radius:6px;font-size:12.5px}
.kb-plink:hover{background:#e0e7ff;text-decoration:none}
.kb-check{font-size:13.5px;color:#334155;line-height:2;padding-left:22px}
.kb-check li{margin:5px 0}
table.data{width:100%;border-collapse:collapse;font-size:13.5px;margin:14px 0}
table.data th{background:var(--soft);text-align:left;padding:10px 14px;
font-weight:600;border-bottom:1px solid var(--border)}
table.data td{padding:9px 14px;border-bottom:1px solid #f1f5f9}
table.data .cx-t{color:var(--accent);font-weight:600;white-space:nowrap}
table.data .cx-n{color:var(--muted)}
"""


_HAS_KNOWLEDGE = False          # 由 main() 设置，决定页头是否显示「知识点」入口


def _page(title: str, body: str, depth: int = 0) -> str:
    up = "../" * depth
    kb_link = (
        f'<a class="navlink" href="{up}knowledge/index.html">知识点总结</a>'
        if _HAS_KNOWLEDGE else ""
    )
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{_esc(title)}</title>
<link rel="stylesheet" href="{up}style.css">
</head>
<body>
<header class="site"><div class="wrap">
  <b><a href="{up}index.html" style="color:inherit">🧩 DS-OJ</a></b>
  <span>{_esc(SITE_SLOGAN)}</span>
  <nav class="sitenav"><a class="navlink" href="{up}index.html">题库</a>{kb_link}</nav>
</div></header>
<div class="wrap">
{body}
</div>
<footer><div class="wrap">
  DS-OJ · 数据结构在线判题系统 · 静态题库站（在 <a href="{up}problems.json">problems.json</a> 获取原始数据）
</div></footer>
</body>
</html>"""


def _diff_badge(d: str) -> str:
    cls = {"入门": "b-intro", "简单": "b-easy", "中等": "b-medium", "困难": "b-hard"}
    return f'<span class="badge {cls.get(d, "b-tag")}">{_esc(d)}</span>'


def _tags(tags: List[str], limit: int = 6) -> str:
    h = "".join(f'<span class="badge b-tag">{_esc(t)}</span> ' for t in tags[:limit])
    if len(tags) > limit:
        h += f'<span class="badge b-cat">+{len(tags) - limit}</span>'
    return h


def build_index(ps: ProblemSet) -> str:
    stats = ps.stats()
    parts = [
        f"<h1>{_esc(SITE_NAME)}</h1>",
        '<div class="sub">按知识点组织的 C++ 数据结构题库，含完整题面、样例与多组测试数据。</div>',
        '<div class="stats">'
        f'<div><b>{stats["total"]}</b>道题目</div>'
        f'<div><b>{stats["category_count"]}</b>个知识点</div>'
        f'<div><b>{stats["test_count"]}</b>个测试点</div>'
        f'<div><b>{stats["tag_count"]}</b>个标签</div>'
        "</div>",
    ]

    grouped: dict = {}
    for p in ps:
        grouped.setdefault(p.category or "未分类", []).append(p)

    for cat, plist in grouped.items():
        parts.append(f"<h2>{_esc(cat)}</h2>")
        rows = []
        for p in plist:
            rows.append(
                f'<tr>'
                f'<td class="id">{_esc(p.id)}</td>'
                f'<td><a href="problems/{_esc(p.id)}.html">{_esc(p.title)}</a></td>'
                f'<td>{_diff_badge(p.difficulty)}</td>'
                f'<td>{_tags(p.tags, 4)}</td>'
                f'<td class="sub">{len(p.tests)} 点</td>'
                f'</tr>'
            )
        parts.append(
            '<table class="list"><thead><tr>'
            '<th style="width:160px">题号</th><th>标题</th>'
            '<th style="width:78px">难度</th><th>标签</th>'
            '<th style="width:70px">测试</th>'
            f'</tr></thead><tbody>{"".join(rows)}</tbody></table>'
        )
    return _page(SITE_NAME, "\n".join(parts))


def build_problem(p: Problem) -> str:
    src = ""
    if p.source_name:
        if p.source_url:
            src = f' · 来源：<a href="{_esc(p.source_url)}" target="_blank" rel="noopener">{_esc(p.source_name)} ↗</a>'
        else:
            src = f" · 来源：{_esc(p.source_name)}"

    parts = [
        f"<h1>{_esc(p.title)}</h1>",
        f'<div class="sub"><a href="../index.html">← 返回题库</a>'
        f' &nbsp;|&nbsp; 题号：{_esc(p.id)}{src}</div>',
        '<div class="meta">'
        + _diff_badge(p.difficulty)
        + f'<span class="badge b-cat">{_esc(p.category or "未分类")}</span> '
        + _tags(p.tags, 8)
        + f'<span class="badge b-cat">时间限制 {p.time_limit:g}s</span>'
        + f'<span class="badge b-cat">内存限制 {p.memory_limit}MB</span>'
        + "</div>",
        '<h2>题目描述</h2>',
        render_markdown(p.statement),
    ]

    if p.input_format:
        parts += ["<h2>输入格式</h2>", render_markdown(p.input_format)]
    if p.output_format:
        parts += ["<h2>输出格式</h2>", render_markdown(p.output_format)]

    if p.constraints:
        parts += ["<h2>数据范围与约定</h2>", "<ul>"]
        parts += [f"<li>{_inline(c)}</li>" for c in p.constraints]
        parts += ["</ul>"]

    if p.samples:
        parts.append("<h2>样例</h2>")
        for i, s in enumerate(p.samples, 1):
            ex = f'<div class="ex">{_inline(s.explain)}</div>' if s.explain else ""
            parts.append(
                f'<div class="sample"><div class="h">样例 {i}</div>'
                f'<div class="b">'
                f'<div class="col"><div class="lbl">输入</div>'
                f'<pre>{_esc(s.input.rstrip()) or "(空)"}</pre></div>'
                f'<div class="col"><div class="lbl">输出</div>'
                f'<pre>{_esc(s.output.rstrip()) or "(空)"}</pre></div>'
                f"</div>{ex}</div>"
            )

    if p.hint:
        parts += ["<h2>解题提示</h2>", render_markdown(p.hint)]

    # 测试点概览（不泄露期望输出）
    parts.append("<h2>测试点</h2>")
    parts.append(
        '<table><thead><tr><th>#</th><th>名称</th><th style="width:80px">分值</th>'
        '<th style="width:80px">类型</th></tr></thead><tbody>'
    )
    for i, t in enumerate(p.tests, 1):
        kind = "样例" if t.sample else "隐藏"
        parts.append(
            f"<tr><td>{i}</td><td>{_esc(t.name or f'测试点 {i}')}</td>"
            f"<td>{t.score}</td><td>{kind}</td></tr>"
        )
    parts.append("</tbody></table>")

    return _page(p.title, "\n".join(parts), depth=1)


def build_knowledge_index(knowledge: dict, ps: ProblemSet) -> str:
    """知识点总览页。"""
    total_pat = sum(k.pattern_count for k in knowledge.values())
    total_tech = sum(k.technique_count for k in knowledge.values())

    parts = [
        '<h1>知识点总结</h1>',
        '<p class="lead">按知识点整理的<b>题型清单</b>与<b>方法总结</b>，'
        '可作为复习提纲与按题型刷题的索引。</p>',
        '<div class="kb-meta">',
        f'<span><b>{len(knowledge)}</b> 个知识点</span>',
        f'<span><b>{total_pat}</b> 种题型</span>',
        f'<span><b>{total_tech}</b> 个方法模板</span>',
        f'<span><b>{len(ps)}</b> 道配套题目</span>',
        '</div>',
    ]

    for cat, k in sorted(knowledge.items()):
        n_prob = sum(len(p.problems) for p in k.patterns)
        # 本页位于 knowledge/ 目录内，链接只需文件名
        parts.append(
            f'<a class="kb-item" href="{cat}.html">'
            f'<div class="kb-item-h">{_esc(k.name)}</div>'
            f'<div class="kb-item-s">{_esc(k.summary)}</div>'
            f'<div class="kb-item-m">题型 {k.pattern_count} · 方法 {k.technique_count} · '
            f'题目 {n_prob}</div></a>'
        )

    return _page("知识点总结", "\n".join(parts), depth=1)


def build_knowledge_detail(k, ps: ProblemSet) -> str:
    """单个知识点的详细页面。"""
    by_id = {p.id: p for p in ps.items}
    parts = [
        f'<h1>{_esc(k.name)}</h1>',
        f'<p class="lead">{_esc(k.summary)}</p>',
    ]
    if k.overview:
        parts.append(f'<div class="kb-overview">{render_markdown(k.overview)}</div>')

    # ---------------- 题型清单
    parts.append('<h2>题型清单</h2>')
    for i, pat in enumerate(k.patterns, 1):
        probs = [by_id[pid] for pid in pat.problems if pid in by_id]
        links = " ".join(
            f'<a class="kb-plink" href="../problems/{p.id}.html">{_esc(p.title)}</a>'
            for p in probs
        )
        pit = ""
        if pat.pitfalls:
            lis = "".join(f"<li>{_esc(x)}</li>" for x in pat.pitfalls)
            pit = f'<div class="kb-pit"><b>易错点</b><ul>{lis}</ul></div>'

        parts.append(
            f'<div class="kb-pat">'
            f'<div class="kb-pat-h"><span class="kb-num">{i}</span>{_esc(pat.name)}</div>'
            f'<div class="kb-signal"><b>识别信号</b>：{_esc(pat.signal)}</div>'
            f'<div class="kb-idea">{render_markdown(pat.idea)}</div>'
            f'<div class="kb-cx"><b>复杂度</b>：{_esc(pat.complexity)}</div>'
            f'{pit}'
            + (f'<div class="kb-probs"><b>对应题目</b> {links}</div>' if links else "")
            + '</div>'
        )

    # ---------------- 方法总结
    if k.techniques:
        parts.append('<h2>方法总结</h2>')
        for t in k.techniques:
            parts.append(
                f'<h3>{_esc(t.name)}</h3>'
                f'<div class="kb-idea">{render_markdown(t.detail)}</div>'
            )
            if t.code:
                parts.append(f'<pre class="code"><code>{html.escape(t.code)}</code></pre>')

    # ---------------- 复杂度对照
    if k.complexity_table:
        parts.append('<h2>复杂度对照</h2>')
        rows = "".join(
            f'<tr><td>{_esc(r.op)}</td><td class="cx-t">{_esc(r.time)}</td>'
            f'<td class="cx-n">{_esc(r.note)}</td></tr>'
            for r in k.complexity_table
        )
        parts.append(
            '<table class="data"><thead><tr><th>操作 / 算法</th><th>时间复杂度</th>'
            f'<th>说明</th></tr></thead><tbody>{rows}</tbody></table>'
        )

    # ---------------- 复习要点
    if k.checklist:
        parts.append('<h2>复习要点</h2>')
        lis = "".join(f"<li>{_esc(x)}</li>" for x in k.checklist)
        parts.append(f'<ul class="kb-check">{lis}</ul>')

    return _page(k.name, "\n".join(parts), depth=1)


def main() -> None:
    global _HAS_KNOWLEDGE
    problems = load_all(PROBLEMS_DIR)
    ps = ProblemSet()
    knowledge = load_knowledge()
    _HAS_KNOWLEDGE = bool(knowledge)

    if STATIC_DIR.exists():
        shutil.rmtree(STATIC_DIR)
    (STATIC_DIR / "problems").mkdir(parents=True, exist_ok=True)
    if knowledge:
        (STATIC_DIR / "knowledge").mkdir(parents=True, exist_ok=True)

    (STATIC_DIR / "style.css").write_text(STYLE, encoding="utf-8")
    (STATIC_DIR / "index.html").write_text(build_index(ps), encoding="utf-8")

    for p in problems:
        (STATIC_DIR / "problems" / f"{p.id}.html").write_text(
            build_problem(p), encoding="utf-8"
        )

    # 知识点总结页面
    if knowledge:
        (STATIC_DIR / "knowledge" / "index.html").write_text(
            build_knowledge_index(knowledge, ps), encoding="utf-8"
        )
        for cat, k in knowledge.items():
            (STATIC_DIR / "knowledge" / f"{cat}.html").write_text(
                build_knowledge_detail(k, ps), encoding="utf-8"
            )

    # 原始数据（含参考答案与测试点输出，供二次开发 / 本地判题使用）
    data = {
        "site": SITE_NAME,
        "count": len(problems),
        "stats": ps.stats(),
        "problems": [p.to_dict(include_answers=True) for p in problems],
    }
    (STATIC_DIR / "problems.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # 知识点原始数据
    if knowledge:
        kdata = {
            "count": len(knowledge),
            "knowledge": {
                cat: {
                    "name": k.name,
                    "summary": k.summary,
                    "patterns": [
                        {
                            "name": p.name,
                            "signal": p.signal,
                            "idea": p.idea,
                            "complexity": p.complexity,
                            "pitfalls": p.pitfalls,
                            "problems": p.problems,
                        }
                        for p in k.patterns
                    ],
                    "techniques": [
                        {"name": t.name, "detail": t.detail, "code": t.code}
                        for t in k.techniques
                    ],
                    "complexity_table": [
                        {"op": r.op, "time": r.time, "note": r.note}
                        for r in k.complexity_table
                    ],
                    "checklist": k.checklist,
                }
                for cat, k in knowledge.items()
            },
        }
        (STATIC_DIR / "knowledge.json").write_text(
            json.dumps(kdata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    # 禁用 Jekyll（避免下划线开头的文件被忽略）
    (STATIC_DIR / ".nojekyll").write_text("", encoding="utf-8")

    print(f"✓ 已生成静态站点: {STATIC_DIR}")
    print(f"  - index.html")
    print(f"  - problems/*.html  （{len(problems)} 个页面）")
    print(f"  - problems.json    （{len(problems)} 道题目的完整数据）")
    if knowledge:
        print(f"  - knowledge/*.html （{len(knowledge)} 个知识点页面）")
        print(f"  - knowledge.json   （知识点总结数据）")
    print(f"  - style.css")


if __name__ == "__main__":
    main()
