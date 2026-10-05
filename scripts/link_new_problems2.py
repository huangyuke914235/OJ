"""一次性维护脚本：把大批新增题目挂到知识点总结的题型清单里。

用法：python scripts/link_new_problems2.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KDIR = ROOT / "oj" / "data" / "knowledge"

# {分类: {题型名: [题目 id]}}
ADD = {
    "01-array-linkedlist": {
        "双指针（相向而行）": ["array-two-sum-hash", "sort-squares"],
        "双指针（同向 / 快慢）": [
            "array-remove-element", "array-move-negatives", "array-duplicate-zeros",
            "list-odd-even", "list-swap-pairs", "list-remove-duplicates", "list-palindrome",
        ],
        "原地反转 / 循环移位": ["array-rotate-left", "string-reverse-vowels"],
        "链表哑结点与指针重连": ["list-middle-node"],
        "前缀和 / 滑动窗口": [
            "array-max-average-subarray", "array-min-size-subarray",
            "array-pivot-index", "array-degree",
        ],
        "区间合并 / 排序后扫描": ["array-summary-ranges", "sort-non-overlapping"],
        "多数元素 / 投票抵消": ["array-single-number", "array-missing-number"],
    },
    "02-stack-queue": {
        "括号匹配 / 符号配对": ["stack-min-remove-brackets", "stack-bracket-depth"],
        "单调栈（下一个更大 / 更小元素）": [
            "stack-prev-smaller", "stack-next-smaller", "stack-prev-greater",
            "stack-132-pattern", "stack-histogram-area", "stack-largest-rectangle",
            "stack-trapping-rain",
        ],
        "栈的设计（辅助栈 / O(1) 最值）": [
            "stack-basic-ops", "queue-basic-ops", "deque-basic-ops",
        ],
        "表达式求值（后缀 / 逆波兰）": ["stack-eval-rpn"],
        "栈消除相邻重复": ["stack-remove-adjacent-nums"],
        "单调队列（滑动窗口最值）": ["queue-window-max-again", "queue-window-min"],
    },
    "03-string-hash": {
        "滑动窗口求最长/最短子串": ["string-longest-unique-substr"],
        "哈希表 / 计数数组做配对查找": [
            "string-first-char-twice", "string-check-pangram", "string-count-matches",
            "string-count-asterisks",
        ],
        "相向双指针判回文": ["string-reverse-vowels", "string-palindrome"],
        "按单词切分与反转": ["string-truncate-sentence", "string-capitalize-title"],
        "子串查找（暴力 / KMP / 字符串哈希）": ["string-implement-strstr"],
        "公共前缀 / 多串比较": ["string-longest-common-prefix"],
    },
    "04-tree": {
        "递归遍历（前 / 中 / 后序）": [
            "tree-preorder", "tree-postorder", "tree-inorder-iterative",
            "tree-postorder-iterative",
        ],
        "层序遍历（BFS）": [
            "tree-level-average", "tree-right-side-view", "tree-zigzag-level-order",
            "tree-level-max",
        ],
        "递归求深度 / 高度 / 路径": [
            "tree-height-edges", "tree-sum-depths", "tree-diameter",
            "tree-sum-left-leaves",
        ],
        "对称性 / 结构比较": ["tree-same", "tree-leaf-similar", "tree-merge"],
        "BST 性质应用（验证 / 查找 / 第 k 小）": [
            "tree-bst-search", "tree-bst-insert", "tree-bst-range-sum",
            "tree-bst-min", "tree-bst-max",
        ],
        "最近公共祖先（LCA）": ["tree-lca-bst"],
        "递归遍历的应用（翻转 / 路径）": [
            "tree-invert", "tree-path-sum", "tree-max-value", "tree-min-value",
            "tree-count-even", "tree-count-greater", "tree-search-value",
        ],
    },
    "05-heap": {
        "Top-K 问题（第 K 大 / 第 K 小）": [
            "heap-kth-smallest", "heap-k-largest-values", "heap-k-smallest-values",
            "heap-kth-largest-sort", "heap-kth-largest-quickselect",
            "heap-kth-largest-stream", "heap-kth-smallest-matrix",
        ],
        "合并 K 个有序序列": ["heap-merge-k-lists", "heap-k-pairs-smallest"],
        "对顶堆求中位数": ["heap-window-median-basic", "heap-window-median"],
        "堆的模拟与手写实现": [
            "heap-priority-queue-ops", "heap-max-heap-ops", "heap-sort-asc",
            "heap-sort-desc", "heap-min-heap-check", "heap-max-heap-check",
        ],
        "贪心 + 堆（带截止时间的调度）": [
            "heap-last-stone-weight", "heap-cookies", "heap-task-scheduler",
            "heap-furthest-building", "heap-halve-array-sum", "heap-meeting-rooms-min",
            "heap-meeting-rooms-ii", "heap-min-cost-remove", "heap-ugly-number",
        ],
    },
    "06-graph": {
        "BFS 求无权图最短路": ["graph-bfs-order", "graph-connected-two"],
        "DFS 求连通块 / 染色": ["graph-dfs-order", "graph-provinces"],
        "拓扑排序（Kahn 算法）": [
            "graph-topo-lex-min", "graph-course-schedule", "graph-eventual-safe",
            "graph-dag-shortest", "graph-count-paths",
        ],
        "并查集（动态连通性）": ["graph-tree-check", "graph-kruskal-mst"],
        "网格图上的 BFS / DFS": [
            "graph-grid-islands", "graph-max-island-area", "graph-flood-fill",
            "graph-rotting-oranges", "graph-zero-one-matrix", "graph-surrounded-regions",
            "graph-binary-matrix-path", "graph-word-search", "graph-unique-paths-obstacle",
        ],
        "带权最短路（Dijkstra）": ["graph-dijkstra", "graph-min-cost-connect"],
        "二分图判定（染色）": ["graph-bipartite", "graph-has-cycle"],
    },
    "07-sort-search": {
        "二分查找（精确查找）": [
            "search-exists", "search-insert-position", "search-lower-bound-practice",
            "search-upper-bound-practice", "search-count-occurrences",
        ],
        "二分查找边界（lower_bound / upper_bound）": [
            "search-lower-bound", "search-first-last", "search-kth-missing",
        ],
        "二分答案（答案单调性 + 判定函数）": ["search-sqrt", "search-sqrt-practice"],
        "归并排序求逆序对": ["sort-inversion-count", "sort-merge"],
        "快排 / 快速选择（第 K 小）": [
            "sort-quicksort", "sort-insertion", "sort-bubble", "sort-selection",
            "sort-counting", "sort-kth-largest", "sort-stable-demo",
        ],
        "二分变体（旋转数组 / 非全局有序）": ["search-rotated-array", "search-peak-element"],
        "三路划分（荷兰国旗）": ["sort-color-sort"],
    },
    "08-advanced": {
        "线性 DP（最长递增子序列 LIS）": [
            "dp-fibonacci", "dp-climb-stairs", "dp-tribonacci", "dp-house-robber",
            "dp-house-robber-ii", "dp-integer-break", "dp-max-subarray-circular",
            "dp-decode-ways", "dp-min-cost-climbing", "dp-min-cost-tickets",
            "dp-arithmetic-slices", "dp-delete-and-earn",
        ],
        "区间 DP（编辑距离 / 序列对齐）": [
            "dp-edit-distance", "dp-lcs", "dp-longest-common-substring",
            "dp-longest-palindromic-subseq", "dp-count-palindromic-substrings",
        ],
        "背包 DP（0-1 / 完全）": [
            "advanced-01-knapsack", "advanced-complete-knapsack",
            "dp-coin-change", "dp-coin-change-ii", "dp-partition-equal",
            "dp-target-sum", "dp-01-knapsack-basic", "dp-perfect-squares",
            "dp-rod-cutting",
        ],
        "并查集应用（连通性 / 环检测）": ["advanced-dsu", "graph-redundant-connection"],
        "单调队列（滑动窗口最值）": ["advanced-sliding-window-max", "queue-window-min"],
        "状态压缩 DP": [],
        "双状态 DP（正负翻转）": ["advanced-max-product-subarray"],
    },
}


def main() -> int:
    total_added = 0
    for stem, adds in ADD.items():
        path = KDIR / f"{stem}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        by_name = {p["name"]: p for p in data["patterns"]}
        for pat_name, ids in adds.items():
            pat = by_name.get(pat_name)
            if pat is None:
                print(f"  ! 未找到题型：{stem} / {pat_name}")
                continue
            have = set(pat.get("problems", []))
            for pid in ids:
                if pid not in have:
                    pat.setdefault("problems", []).append(pid)
                    have.add(pid)
                    total_added += 1
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"  ✓ {stem}")
    print(f"\n共新增 {total_added} 条题目引用。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
