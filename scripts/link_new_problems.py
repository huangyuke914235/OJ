"""一次性维护脚本：把新增题目挂到知识点总结的题型清单里。

用法：python scripts/link_new_problems.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KDIR = ROOT / "oj" / "data" / "knowledge"

# {分类文件: {题型名: [要追加的题目 id]}}
ADD_TO_PATTERN = {
    "01-array-linkedlist": {
        "双指针（同向 / 快慢）": [
            "array-remove-duplicates",
            "array-move-zeroes",
            "list-middle-node",
        ],
    },
    "02-stack-queue": {
        "单调栈（下一个更大 / 更小元素）": ["stack-daily-temperatures"],
    },
    "03-string-hash": {
        "哈希表 / 计数数组做配对查找": [
            "string-first-unique-char",
            "string-group-anagrams",
        ],
        "子串查找（暴力 / KMP / 字符串哈希）": ["string-implement-strstr"],
    },
    "04-tree": {
        "递归求深度 / 高度 / 路径": ["tree-min-depth"],
        "BST 性质应用（验证 / 查找 / 第 k 小）": ["tree-bst-kth-smallest"],
    },
    "05-heap": {
        "Top-K 问题（第 K 大 / 第 K 小）": [
            "heap-top-k-frequent",
            "heap-k-closest-points",
        ],
        "贪心 + 堆（带截止时间的调度）": ["heap-last-stone-weight"],
    },
    "06-graph": {
        "网格图上的 BFS / DFS": ["graph-grid-islands"],
    },
    "07-sort-search": {
        "二分答案（答案单调性 + 判定函数）": ["search-sqrt"],
    },
    "08-advanced": {
        "区间 DP（编辑距离 / 序列对齐）": ["advanced-lcs"],
        "背包 DP（0-1 / 完全）": ["advanced-complete-knapsack"],
    },
}

# 需要新增的题型（追加到 patterns 末尾）
NEW_PATTERNS = {
    "01-array-linkedlist": [
        {
            "name": "多数元素 / 投票抵消",
            "signal": "求出现次数超过一半的元素；「两两抵消后剩下的那个」",
            "idea": "Boyer-Moore 投票算法：维护候选者 `cand` 与计数 `cnt`。遍历数组，"
                    "`cnt == 0` 时把当前元素设为候选者；与候选者相同则 `cnt++`，否则 `cnt--`。"
                    "直觉是「多数元素与其他元素一换一抵消后仍会剩下」。",
            "complexity": "时间 O(n) / 空间 O(1)",
            "pitfalls": [
                "答案必须「严格超过一半」，恰好等于一半不满足条件",
                "若题目不保证存在多数元素，投票后还需再扫一遍验证",
                "计数归零时换候选者，不要写成只在第一个元素时初始化",
            ],
            "problems": ["array-majority-element"],
        },
    ],
    "02-stack-queue": [
        {
            "name": "栈的设计（辅助栈 / O(1) 最值）",
            "signal": "要求 O(1) 查询栈内最值、栈的最小/最大值",
            "idea": "再开一个**辅助栈**与主栈同步，辅助栈顶存「当前栈内最值」。"
                    "入栈时把 `min(辅助栈顶, 新元素)` 压入辅助栈；出栈时两个栈同时弹出。"
                    "这样两栈高度始终一致，查询最值只需 O(1)。",
            "complexity": "所有操作 O(1) / 空间 O(n)",
            "pitfalls": [
                "辅助栈必须与主栈**同步**压入弹出，高度不一致会错位",
                "入辅助栈时是比较「辅助栈顶」而不是「主栈顶」",
                "空栈时查询最值要先判空",
            ],
            "problems": ["stack-min-stack"],
        },
        {
            "name": "表达式求值（后缀 / 逆波兰）",
            "signal": "逆波兰表达式求值、中缀转后缀、计算器",
            "idea": "**后缀表达式**用单栈：遇操作数入栈，遇运算符弹出两个操作数算完再入栈。"
                    "**中缀表达式**用双栈（操作数栈 + 运算符栈），遇右括号就弹出到左括号为止做一次运算。",
            "complexity": "时间 O(n) / 空间 O(n)",
            "pitfalls": [
                "**减法与除法不满足交换律**：先弹出的是右操作数，后弹出的是左操作数，顺序反了结果必错",
                "C++ 整数除法本身就是向零截断，与题面要求一致，无需额外处理",
                "多位数要连续读入，不能按单字符处理",
            ],
            "problems": ["stack-eval-rpn"],
        },
        {
            "name": "栈消除相邻重复",
            "signal": "反复删除相邻相同字符/元素；消消乐类问题",
            "idea": "从左到右扫描，若**栈顶与当前元素相同**则弹出栈顶（相当于删除这一对），"
                    "否则压入当前元素。栈顶始终代表「处理完前缀后剩下的最后一个元素」，"
                    "因此删除后产生的新相邻关系能被自动正确处理。",
            "complexity": "时间 O(n) / 空间 O(n)",
            "pitfalls": [
                "必须用 while/递归语义反复消除，不能只扫一遍就结束",
                "最后输出的是栈中剩余元素，顺序是从栈底到栈顶",
                "结果为空时要输出空行而不是什么都不输出",
            ],
            "problems": ["stack-remove-adjacent-duplicates"],
        },
    ],
    "03-string-hash": [
        {
            "name": "公共前缀 / 多串比较",
            "signal": "求一组字符串的最长公共前缀；多串同时逐位比较",
            "idea": "**纵向扫描**：以第一个串为基准，维护当前公共前缀长度 `k`，"
                    "依次与其他串逐字符比较，一旦不匹配或到达某串末尾就把 `k` 缩小。",
            "complexity": "时间 O(n·L) / 空间 O(1)",
            "pitfalls": [
                "必须同时判断「是否超出当前串长度」，否则越界",
                "基准串本身为空时公共前缀长度直接为 0",
                "输入可能含空行，读入时不能简单 strip 掉所有换行",
            ],
            "problems": ["string-longest-common-prefix"],
        },
    ],
    "04-tree": [
        {
            "name": "递归遍历的应用（翻转 / 路径）",
            "signal": "翻转二叉树、判断路径和、把树按某种规则改写",
            "idea": "这类题的共同点是「每个节点做的事只依赖自己与子树」，"
                    "因此递归结构非常直接：先处理子树，再处理当前节点（后序），"
                    "或先处理当前节点再递归（前序）。路径和类问题把「剩余需要的值」作为参数往下传。",
            "complexity": "时间 O(n) / 空间 O(h)",
            "pitfalls": [
                "**路径和必须在叶子处判定**，不能中途 `rest == 0` 就返回 true",
                "翻转时交换左右指针与递归的先后顺序无所谓，但别漏掉任何一侧",
                "输出层序序列时要删掉末尾多余的 null 占位",
            ],
            "problems": ["tree-invert", "tree-path-sum"],
        },
    ],
    "06-graph": [
        {
            "name": "带权最短路（Dijkstra）",
            "signal": "带权图求最短路且边权非负；「最少花费」「最短时间」",
            "idea": "堆优化的 Dijkstra：`dist[s]=0`，用小根堆存 `(距离, 顶点)`。"
                    "每次弹出堆顶，**若其距离已大于 `dist[u]` 说明是过期条目，跳过**；"
                    "否则遍历邻居做松弛，把改进后的距离压入堆。",
            "complexity": "时间 O((V+E) log V) / 空间 O(V+E)",
            "pitfalls": [
                "**边权必须非负**，有负权要用 Bellman-Ford 或 SPFA",
                "**必须跳过过期条目**，否则复杂度退化",
                "距离数组要用 long long，INF 取足够大（如 4e18）",
            ],
            "problems": ["graph-dijkstra"],
        },
        {
            "name": "二分图判定（染色）",
            "signal": "能否把点分成两组使每条边两端异组；判断奇环",
            "idea": "给顶点染 0/1 两色，从每个未染色的点出发 BFS：邻居未染色就染相反色，"
                    "若邻居已染色且与当前同色则判定失败。等价于「图中不存在奇环」。",
            "complexity": "时间 O(V+E) / 空间 O(V+E)",
            "pitfalls": [
                "**外层必须遍历所有顶点**，图不一定连通，只从 1 号点开始会漏判",
                "判断冲突是「邻居与当前点同色」，不是「邻居未染色」",
                "孤立点自成一组，不影响二分性",
            ],
            "problems": ["graph-bipartite"],
        },
    ],
    "07-sort-search": [
        {
            "name": "二分变体（旋转数组 / 非全局有序）",
            "signal": "数组被旋转过、局部有序但仍想二分",
            "idea": "关键观察：旋转数组从中间切开后，**至少有一半是完全有序的**。"
                    "每轮先判断哪一半有序，再看目标值是否落在该有序区间内，"
                    "据此决定收缩方向，从而仍然保持 O(log n)。",
            "complexity": "时间 O(log n) / 空间 O(1)",
            "pitfalls": [
                "判断区间是否包含目标时，开闭边界要与「mid 已单独判过相等」相配套",
                "用 `a[lo] <= a[mid]` 判断左半有序，`<=` 不能写成 `<`（两个元素时是关键）",
                "数组无重复元素时逻辑最简单；有重复需额外处理",
            ],
            "problems": ["search-rotated-array"],
        },
        {
            "name": "三路划分（荷兰国旗）",
            "signal": "只有 3 种取值需要原地分类；一趟遍历 + O(1) 空间",
            "idea": "用 `low`、`i`、`high` 三个指针把数组分成四段："
                    "`[0,low)` 放最小值、`[low,i)` 放中间值、`[i,high]` 待处理、`(high,n)` 放最大值。"
                    "看 `a[i]`：是最小值就与 `a[low]` 交换并双双前移；是中间值则 `i++`；"
                    "是最大值就与 `a[high]` 交换并 `high--`。",
            "complexity": "时间 O(n) / 空间 O(1)",
            "pitfalls": [
                "**处理最大值时 `i` 不能自增**——换过来的元素还没检查过",
                "循环条件是 `i <= high`（待处理区间为空时停止）",
                "是最小值交换后要同时 `low++` 和 `i++`，因为换过来的元素必然已在正确位置",
            ],
            "problems": ["sort-color-sort"],
        },
    ],
    "08-advanced": [
        {
            "name": "双状态 DP（正负翻转）",
            "signal": "乘积型最值问题；乘法中负数会翻转大小关系",
            "idea": "因为「负数 × 负数 = 正数」，当前最小的负数可能一跃成为最大值。"
                    "所以同时维护以 `i` 结尾的 `curMax` 与 `curMin`，"
                    "每步用 `{x, curMax*x, curMin*x}` 三者取极值更新。",
            "complexity": "时间 O(n) / 空间 O(1)",
            "pitfalls": [
                "必须**先算好两个新值再同时赋值**，否则 curMax 被覆盖后 curMin 就算错",
                "答案要取整个过程中的最大值，不能只返回最后的 curMax",
                "元素可能全为负，初值不能设成 0",
            ],
            "problems": ["advanced-max-product-subarray"],
        },
    ],
}


def main() -> int:
    changed = 0
    for stem, adds in ADD_TO_PATTERN.items():
        path = KDIR / f"{stem}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        for pat in data["patterns"]:
            extra = adds.get(pat["name"])
            if not extra:
                continue
            have = set(pat.get("problems", []))
            for pid in extra:
                if pid not in have:
                    pat.setdefault("problems", []).append(pid)
                    have.add(pid)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        changed += 1
        print(f"  更新引用 {stem}")

    for stem, pats in NEW_PATTERNS.items():
        path = KDIR / f"{stem}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        existing = {p["name"] for p in data["patterns"]}
        for p in pats:
            if p["name"] in existing:
                print(f"  跳过已存在题型 {stem} / {p['name']}")
                continue
            data["patterns"].append(p)
            print(f"  新增题型 {stem} / {p['name']}")
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"\n完成，处理 {changed} 个知识点文件的题目引用。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
