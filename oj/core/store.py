"""题库访问层：带缓存地提供题目列表与详情。"""
from __future__ import annotations

from functools import lru_cache
from typing import Dict, List, Optional

from oj.config import PROBLEMS_DIR
from oj.core.models import Problem, load_all


class ProblemSet:
    """题库。

    题目为静态文件，进程内缓存一次即可；提供显式 ``reload`` 供开发热更新。
    """

    def __init__(self, problems_dir=PROBLEMS_DIR, strict: bool = True):
        self.problems_dir = problems_dir
        self.strict = strict
        self._items: List[Problem] = []
        self._by_id: Dict[str, Problem] = {}
        self.reload()

    # -------------------------------------------------------------- 加载

    def reload(self) -> "ProblemSet":
        self._items = load_all(self.problems_dir, strict=self.strict)
        self._by_id = {p.id: p for p in self._items}
        return self

    # -------------------------------------------------------------- 查询

    @property
    def items(self) -> List[Problem]:
        return list(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def get(self, problem_id: str) -> Optional[Problem]:
        return self._by_id.get(problem_id)

    def search(
        self,
        keyword: str = "",
        difficulty: Optional[str] = None,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
    ) -> List[Problem]:
        """按关键字/难度/标签/知识点筛选。"""
        kw = (keyword or "").strip().lower()
        tag_set = {t.lower() for t in (tags or [])}
        out: List[Problem] = []
        for p in self._items:
            if difficulty and p.difficulty != difficulty:
                continue
            if category and p.category != category:
                continue
            if tag_set and not tag_set.issubset({t.lower() for t in p.tags}):
                continue
            if kw:
                haystack = " ".join(
                    [p.id, p.title, p.statement, " ".join(p.tags), p.source_name, p.category]
                ).lower()
                if kw not in haystack:
                    continue
            out.append(p)
        return out

    def categories(self) -> List[str]:
        """按预定义顺序返回出现过的知识点分类。"""
        from oj.core.models import CATEGORY_NAMES, CATEGORY_ORDER

        present = {p.category for p in self._items if p.category}
        return sorted(present, key=lambda c: CATEGORY_ORDER.get(c, 99))

    def all_tags(self) -> List[str]:
        tags: Dict[str, int] = {}
        for p in self._items:
            for t in p.tags:
                tags[t] = tags.get(t, 0) + 1
        return [t for t, _ in sorted(tags.items(), key=lambda kv: (-kv[1], kv[0]))]

    def stats(self) -> Dict[str, object]:
        by_diff: Dict[str, int] = {}
        by_cat: Dict[str, int] = {}
        for p in self._items:
            by_diff[p.difficulty] = by_diff.get(p.difficulty, 0) + 1
            if p.category:
                by_cat[p.category] = by_cat.get(p.category, 0) + 1
        return {
            "total": len(self._items),
            "by_difficulty": by_diff,
            "by_category": by_cat,
            "category_count": len(by_cat),
            "tag_count": len(self.all_tags()),
            "test_count": sum(len(p.tests) for p in self._items),
        }


@lru_cache(maxsize=1)
def default_problem_set() -> ProblemSet:
    return ProblemSet()
