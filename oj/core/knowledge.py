"""知识点总结数据模型与加载器。

每个知识点分类对应 ``oj/data/knowledge/<分类目录>.json`` 一份总结，
内容包含「题型清单」与「方法总结」，用于复习与按题型刷题。

JSON 结构::

    {
      "category": "01-array-linkedlist",
      "name": "数组与链表",
      "summary": "一句话概述",
      "overview": "详细概述（Markdown）",
      "patterns": [                      // 题型清单
        {
          "name": "双指针（相向而行）",
          "signal": "看到「有序数组 + 找一对」就该想到",
          "idea": "思路（Markdown）",
          "complexity": "时间 O(n) / 空间 O(1)",
          "pitfalls": ["易错点"],
          "problems": ["array-two-sum-sorted"]
        }
      ],
      "techniques": [                    // 方法总结
        {
          "name": "快慢指针",
          "detail": "说明（Markdown）",
          "code": "C++ 模板代码",
          "lang": "cpp"
        }
      ],
      "complexity_table": [
        {"op": "按下标随机访问", "time": "O(1)", "note": "连续内存"}
      ],
      "checklist": ["复习要点"]
    }
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from oj.config import KNOWLEDGE_DIR


class KnowledgeError(ValueError):
    """知识点总结数据非法。"""


@dataclass
class Pattern:
    """一种题型。"""

    name: str
    signal: str = ""
    idea: str = ""
    complexity: str = ""
    pitfalls: List[str] = field(default_factory=list)
    problems: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> "Pattern":
        return cls(
            name=str(d.get("name", "")).strip(),
            signal=str(d.get("signal", "")).strip(),
            idea=str(d.get("idea", "")).strip(),
            complexity=str(d.get("complexity", "")).strip(),
            pitfalls=[str(x) for x in d.get("pitfalls", []) or []],
            problems=[str(x) for x in d.get("problems", []) or []],
        )


@dataclass
class Technique:
    """一种方法/模板。"""

    name: str
    detail: str = ""
    code: str = ""
    lang: str = "cpp"

    @classmethod
    def from_dict(cls, d: dict) -> "Technique":
        return cls(
            name=str(d.get("name", "")).strip(),
            detail=str(d.get("detail", "")).strip(),
            code=str(d.get("code", "")).rstrip(),
            lang=str(d.get("lang", "cpp")),
        )


@dataclass
class ComplexityRow:
    """复杂度表中的一行。"""

    op: str
    time: str = ""
    note: str = ""

    @classmethod
    def from_dict(cls, d: dict) -> "ComplexityRow":
        return cls(
            op=str(d.get("op", "")).strip(),
            time=str(d.get("time", "")).strip(),
            note=str(d.get("note", "")).strip(),
        )


@dataclass
class Knowledge:
    """一个知识点的完整总结。"""

    category: str                      # 分类目录名，如 01-array-linkedlist
    name: str                          # 展示名，如 数组与链表
    summary: str = ""
    overview: str = ""
    patterns: List[Pattern] = field(default_factory=list)
    techniques: List[Technique] = field(default_factory=list)
    complexity_table: List[ComplexityRow] = field(default_factory=list)
    checklist: List[str] = field(default_factory=list)

    @property
    def pattern_count(self) -> int:
        return len(self.patterns)

    @property
    def technique_count(self) -> int:
        return len(self.techniques)

    @classmethod
    def from_dict(cls, d: dict, category: str = "") -> "Knowledge":
        return cls(
            category=str(d.get("category", category)),
            name=str(d.get("name", "")).strip(),
            summary=str(d.get("summary", "")).strip(),
            overview=str(d.get("overview", "")).strip(),
            patterns=[Pattern.from_dict(x) for x in d.get("patterns", []) or []],
            techniques=[Technique.from_dict(x) for x in d.get("techniques", []) or []],
            complexity_table=[
                ComplexityRow.from_dict(x) for x in d.get("complexity_table", []) or []
            ],
            checklist=[str(x) for x in d.get("checklist", []) or []],
        )


# ---------------------------------------------------------------- 加载

def load_knowledge(path: Path) -> Knowledge:
    """从单个 JSON 文件加载一份知识点总结。"""
    if not path.exists():
        raise KnowledgeError(f"知识点文件不存在：{path}")
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise KnowledgeError(f"{path.name} JSON 解析失败：{exc}") from exc

    k = Knowledge.from_dict(raw, category=path.stem)
    if not k.name:
        raise KnowledgeError(f"{path.name} 缺少 name 字段")
    if not k.patterns:
        raise KnowledgeError(f"{path.name} 的 patterns（题型清单）不能为空")
    return k


def load_all(knowledge_dir: Path = KNOWLEDGE_DIR) -> Dict[str, Knowledge]:
    """加载全部知识点总结，返回 ``{分类目录名: Knowledge}``。

    目录不存在时返回空字典（知识点总结是可选的增强内容）。
    """
    result: Dict[str, Knowledge] = {}
    if not knowledge_dir.exists():
        return result
    for f in sorted(knowledge_dir.glob("*.json")):
        k = load_knowledge(f)
        result[k.category] = k
    return result


def link_problems(k: Knowledge, problems: List) -> Dict[str, List]:
    """把题型里引用的题目 id 解析成真实题目对象。

    :return: ``{题型名: [Problem, ...]}``，未找到的 id 会被忽略。
    """
    by_id = {p.id: p for p in problems}
    out: Dict[str, List] = {}
    for pat in k.patterns:
        out[pat.name] = [by_id[pid] for pid in pat.problems if pid in by_id]
    return out


def validate_links(knowledge: Dict[str, Knowledge], problems: List) -> List[str]:
    """校验知识点里引用的题目 id 是否都存在，返回问题描述列表。"""
    valid_ids = {p.id for p in problems}
    issues: List[str] = []
    for cat, k in knowledge.items():
        for pat in k.patterns:
            for pid in pat.problems:
                if pid not in valid_ids:
                    issues.append(f"[{cat}] 题型「{pat.name}」引用了不存在的题目：{pid}")
    return issues


def find_by_problem(knowledge: Dict[str, Knowledge], problem_id: str) -> Optional[Knowledge]:
    """反查某道题属于哪个知识点总结（按题型引用）。"""
    for k in knowledge.values():
        for pat in k.patterns:
            if problem_id in pat.problems:
                return k
    return None
