"""题目数据模型。

题库存放在 ``oj/data/problems/*.json``，一个文件一道题。
使用纯 JSON 而非数据库，便于版本管理，也便于 GitHub Pages 静态站点直接消费。

题目 JSON 结构::

    {
      "id": "array-reverse",
      "title": "数组逆序",
      "difficulty": "入门",            // 入门 / 简单 / 中等 / 困难
      "tags": ["数组", "双指针"],
      "source": {"name": "LeetCode 344", "url": "https://..."},
      "statement": "题面（Markdown）",
      "input_format": "输入格式说明（Markdown）",
      "output_format": "输出格式说明（Markdown）",
      "constraints": ["1 <= n <= 10^5"],
      "samples": [{"input": "...", "output": "...", "explain": "..."}],
      "hint": "提示（Markdown，可空）",
      "starter_code": {"python3": "def solve():\\n    ..."},
      "tests": [
        {"input": "...", "output": "...", "name": "样例 1", "score": 10}
      ],
      "reference": {"python3": "完整参考解源码"},
      "time_limit": 2.0,               // 可选，覆盖默认
      "memory_limit": 256              // 可选，覆盖默认
    }
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from oj.config import DEFAULT_MEMORY_LIMIT, DEFAULT_TIME_LIMIT

DIFFICULTIES = ["入门", "简单", "中等", "困难"]
DIFFICULTY_ORDER = {d: i for i, d in enumerate(DIFFICULTIES)}

# 知识点分类目录 -> 展示名
CATEGORY_NAMES = {
    "01-array-linkedlist": "数组与链表",
    "02-stack-queue": "栈与队列",
    "03-string-hash": "字符串与哈希",
    "04-tree": "树与二叉树",
    "05-heap": "堆与优先队列",
    "06-graph": "图论基础",
    "07-sort-search": "排序与查找",
    "08-advanced": "综合与进阶",
}
CATEGORY_ORDER = {name: i for i, name in enumerate(CATEGORY_NAMES.values())}


class ProblemError(ValueError):
    """题目数据非法。"""


@dataclass
class Sample:
    input: str
    output: str
    explain: str = ""

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Sample":
        return cls(
            input=str(d.get("input", "")),
            output=str(d.get("output", "")),
            explain=str(d.get("explain", "")),
        )


@dataclass
class TestCase:
    input: str
    output: str
    name: str = ""
    score: int = 0
    # 是否样例（样例同时会出现在 samples 中，用于前端展示）
    sample: bool = False

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TestCase":
        return cls(
            input=str(d.get("input", "")),
            output=str(d.get("output", "")),
            name=str(d.get("name", "")),
            score=int(d.get("score", 0)),
            sample=bool(d.get("sample", False)),
        )


@dataclass
class Problem:
    id: str
    title: str
    statement: str = ""
    difficulty: str = "简单"
    tags: List[str] = field(default_factory=list)
    source: Dict[str, str] = field(default_factory=dict)
    input_format: str = ""
    output_format: str = ""
    constraints: List[str] = field(default_factory=list)
    samples: List[Sample] = field(default_factory=list)
    hint: str = ""
    starter_code: Dict[str, str] = field(default_factory=dict)
    tests: List[TestCase] = field(default_factory=list)
    reference: Dict[str, str] = field(default_factory=dict)
    time_limit: float = DEFAULT_TIME_LIMIT
    memory_limit: int = DEFAULT_MEMORY_LIMIT
    # 知识点分类（由所在文件夹决定，如 "数组与链表"）
    category: str = ""
    # 文件来源，便于排查
    _path: Optional[Path] = None

    # ---------------------------------------------------------- 序列化

    @classmethod
    def from_dict(cls, d: Dict[str, Any], path: Optional[Path] = None) -> "Problem":
        pid = str(d.get("id", "")).strip()
        if not pid:
            raise ProblemError("题目缺少 id 字段")
        title = str(d.get("title", "")).strip()
        if not title:
            raise ProblemError(f"题目 {pid} 缺少 title 字段")

        tests = [TestCase.from_dict(t) for t in d.get("tests", [])]
        if not tests:
            raise ProblemError(f"题目 {pid} 至少需要一个测试点")

        difficulty = str(d.get("difficulty", "简单"))
        if difficulty not in DIFFICULTY_ORDER:
            raise ProblemError(
                f"题目 {pid} 的 difficulty={difficulty!r} 非法，可选：{DIFFICULTIES}"
            )

        return cls(
            id=pid,
            title=title,
            statement=str(d.get("statement", "")),
            difficulty=difficulty,
            tags=[str(t) for t in d.get("tags", [])],
            source=dict(d.get("source", {}) or {}),
            input_format=str(d.get("input_format", "")),
            output_format=str(d.get("output_format", "")),
            constraints=[str(c) for c in d.get("constraints", [])],
            samples=[Sample.from_dict(s) for s in d.get("samples", [])],
            hint=str(d.get("hint", "")),
            starter_code=dict(d.get("starter_code", {}) or {}),
            tests=tests,
            reference=dict(d.get("reference", {}) or {}),
            time_limit=float(d.get("time_limit", DEFAULT_TIME_LIMIT)),
            memory_limit=int(d.get("memory_limit", DEFAULT_MEMORY_LIMIT)),
            _path=path,
        )

    def to_dict(self, include_answers: bool = False) -> Dict[str, Any]:
        """导出为 dict。

        ``include_answers=False`` 时剔除参考解与测试点输出，用于前端下发。
        """
        tests = []
        for t in self.tests:
            item = {"input": t.input, "name": t.name, "score": t.score, "sample": t.sample}
            if include_answers:
                item["output"] = t.output
            tests.append(item)

        data: Dict[str, Any] = {
            "id": self.id,
            "title": self.title,
            "difficulty": self.difficulty,
            "tags": self.tags,
            "source": self.source,
            "statement": self.statement,
            "input_format": self.input_format,
            "output_format": self.output_format,
            "constraints": self.constraints,
            "samples": [
                {"input": s.input, "output": s.output, "explain": s.explain}
                for s in self.samples
            ],
            "hint": self.hint,
            "starter_code": self.starter_code,
            "tests": tests,
            "time_limit": self.time_limit,
            "memory_limit": self.memory_limit,
            "test_count": len(self.tests),
            "category": self.category,
        }
        if include_answers:
            data["reference"] = self.reference
        return data

    # ---------------------------------------------------------- 便捷属性

    @property
    def total_score(self) -> int:
        return sum(t.score for t in self.tests) or len(self.tests)

    @property
    def source_name(self) -> str:
        return self.source.get("name", "")

    @property
    def source_url(self) -> str:
        return self.source.get("url", "")

    @property
    def order(self) -> int:
        return DIFFICULTY_ORDER.get(self.difficulty, 99)


def _category_from_path(path: Optional[Path], problems_dir: Optional[Path] = None) -> str:
    """从文件路径推导知识点分类展示名。"""
    if path is None:
        return ""
    folder = path.parent.name
    return CATEGORY_NAMES.get(folder, folder if folder != "problems" else "")


def load_problem_file(path: Path) -> Problem:
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:  # pragma: no cover
        raise ProblemError(f"无法读取题目文件 {path}: {exc}") from exc
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ProblemError(f"题目文件 {path.name} JSON 解析失败：{exc}") from exc
    problem = Problem.from_dict(data, path=path)
    if not problem.category:
        problem.category = _category_from_path(path)
    return problem


def load_all(problems_dir: Path, strict: bool = True) -> List[Problem]:
    """递归加载题库目录下所有题目（支持按知识点分文件夹），按难度、id 排序。

    ``strict=True`` 时任一题目非法即抛错；否则跳过非法题目。
    """
    problems: List[Problem] = []
    if not problems_dir.exists():
        return problems

    # 递归匹配所有 *.json，支持 oj/data/problems/<分类>/<题目>.json 结构
    for path in sorted(problems_dir.rglob("*.json")):
        if path.name.startswith("_"):
            continue
        try:
            problems.append(load_problem_file(path))
        except ProblemError:
            if strict:
                raise
    problems.sort(key=lambda p: (p.order, p.id))
    return problems
