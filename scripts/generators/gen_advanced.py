"""生成「综合与进阶」分类的题目。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from genkit import build_tests, finalize, numbers  # noqa: E402

OUT = ROOT / "oj" / "data" / "problems" / "08-advanced"


def _mk(id_, title, difficulty, tags, source, statement, input_format, output_format,
        constraints, samples, hint, starter, reference, tests, tl=2.0):
    return {
        "id": id_, "title": title, "difficulty": difficulty, "tags": tags,
        "source": source, "statement": statement, "input_format": input_format,
        "output_format": output_format, "constraints": constraints,
        "samples": samples, "hint": hint,
        "starter_code": {"cpp": starter}, "tests": tests,
        "reference": {"cpp": reference}, "time_limit": tl,
    }


# ============================================================ 1. 滑动窗口最大值（单调队列）
def solve_sliding_max(text: str) -> str:
    from collections import deque
    nums = numbers(text)
    n, k = nums[0], nums[1]
    a = nums[2:2 + n]
    dq = deque()
    out = []
    for i, x in enumerate(a):
        while dq and a[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(str(a[dq[0]]))
    return " ".join(out) + "\n"


SLIDING_SPECS = [
    ("样例 1", "8 3\n1 3 -1 -3 5 3 6 7", 10),
    ("样例 2（k=1）", "4 1\n1 2 3 4", 10),
    ("k=n（整体最大）", "5 5\n1 9 3 2 8", 15),
    ("全相同", "5 2\n4 4 4 4 4", 15),
    ("递减", "5 3\n5 4 3 2 1", 20),
    ("递增", "5 3\n1 2 3 4 5", 20),
    ("含负数", "6 2\n-1 -3 -2 -5 -4 -6", 20),
]

# ============================================================ 2. 最长递增子序列
def solve_lis(text: str) -> str:
    import bisect
    nums = numbers(text)
    n, a = nums[0], nums[1:1 + nums[0]]
    tails = []
    for x in a:
        pos = bisect.bisect_left(tails, x)
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x
    return f"{len(tails)}\n"


LIS_SPECS = [
    ("样例 1", "8\n10 9 2 5 3 7 101 18", 10),
    ("样例 2（递减）", "5\n5 4 3 2 1", 10),
    ("单元素", "1\n7", 10),
    ("全相同", "4\n3 3 3 3", 15),
    ("严格递增", "5\n1 2 3 4 5", 15),
    ("含负数", "6\n-3 -1 -2 0 -5 4", 20),
    ("锯齿", "7\n1 3 2 4 3 5 4", 20),
]

# ============================================================ 3. 编辑距离
def solve_edit_distance(text: str) -> str:
    lines = text.strip("\n").split("\n")
    a = lines[0] if lines else ""
    b = lines[1] if len(lines) > 1 else ""
    n, m = len(a), len(b)
    prev = list(range(m + 1))
    for i in range(1, n + 1):
        cur = [i] + [0] * m
        for j in range(1, m + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost)
        prev = cur
    return f"{prev[m]}\n"


EDIT_SPECS = [
    ("样例 1", "horse\nros", 10),
    ("样例 2", "intention\nexecution", 10),
    ("都为空", "\n\n", 10),
    ("一个为空", "abc\n", 15),
    ("完全相同", "abc\nabc", 15),
    ("完全替换", "abc\nxyz", 20),
    ("长度差很大", "a\nabcdefg", 20),
]

# ============================================================ 4. 0-1 背包
def solve_knapsack(text: str) -> str:
    nums = numbers(text)
    n, cap = nums[0], nums[1]
    idx = 2
    items = []
    for _ in range(n):
        w, v = nums[idx], nums[idx + 1]
        idx += 2
        items.append((w, v))
    dp = [0] * (cap + 1)
    for w, v in items:
        for c in range(cap, w - 1, -1):
            if dp[c - w] + v > dp[c]:
                dp[c] = dp[c - w] + v
    return f"{dp[cap]}\n"


KNAPSACK_SPECS = [
    ("样例 1", "3 5\n2 3\n3 4\n4 6", 10),
    ("样例 2（装不下）", "2 1\n5 10\n6 20", 10),
    ("单件可装", "1 5\n3 7", 10),
    ("全装下", "3 10\n1 1\n2 2\n3 3", 15),
    ("恰好装满", "2 5\n2 10\n3 15", 15),
    ("重量等于容量", "1 4\n4 100", 20),
    ("需取舍", "4 6\n1 2\n2 4\n3 6\n4 9", 20),
]

# ============================================================ 5. 并查集
def solve_dsu(text: str) -> str:
    nums = numbers(text)
    n, q = nums[0], nums[1]
    parent = list(range(n + 1))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    idx = 2
    out = []
    for _ in range(q):
        op, a, b = nums[idx], nums[idx + 1], nums[idx + 2]
        idx += 3
        ra, rb = find(a), find(b)
        if op == 1:
            if ra != rb:
                parent[ra] = rb
        else:
            out.append("YES" if ra == rb else "NO")
    return ("\n".join(out) + "\n") if out else "\n"


DSU_SPECS = [
    ("样例 1", "5 5\n1 1 2\n2 1 2\n1 3 4\n2 3 4\n2 1 4", 10),
    ("无合并只查询", "3 2\n2 1 2\n2 2 3", 10),
    ("单点", "1 1\n2 1 1", 10),
    ("合并后再查询", "4 4\n1 1 2\n1 2 3\n2 1 3\n2 1 4", 15),
    ("重复合并", "3 5\n1 1 2\n1 1 2\n2 1 2\n1 2 3\n2 1 3", 20),
    ("形成大集合", "6 6\n1 1 2\n1 3 4\n1 5 6\n2 1 3\n2 1 5\n1 2 3", 20),
    ("链式合并", "5 5\n1 1 2\n1 2 3\n1 3 4\n2 1 4\n2 1 5", 20),
]


def build_sliding_max() -> dict:
    tests = build_tests(SLIDING_SPECS, solve_sliding_max)
    return _mk(
        "advanced-sliding-window-max", "滑动窗口最大值", "困难",
        ["队列", "单调队列", "滑动窗口"],
        {"name": "LeetCode 239", "url": "https://leetcode.cn/problems/sliding-window-maximum/"},
        "给定一个长度为 $n$ 的整数数组和一个窗口大小 $k$。"
        "窗口从左向右滑动，每次移动一格，请输出**每个窗口内元素的最大值**。\n\n"
        "共有 $n - k + 1$ 个窗口。\n\n"
        "**要求：时间复杂度 $O(n)$**。每次对窗口内 $k$ 个元素取最大值的朴素做法是 "
        "$O(nk)$，在 $n = 2 \\times 10^5$ 时会超时。",
        "第一行两个整数 $n, k$（$1 \\le k \\le n \\le 2 \\times 10^5$）。\n\n第二行 $n$ 个整数 $a_i$（$|a_i| \\le 10^9$）。",
        "一行 $n - k + 1$ 个整数，依次为每个窗口的最大值，以空格分隔。",
        ["1 ≤ k ≤ n ≤ 2×10^5", "|a_i| ≤ 10^9", "要求 O(n)"],
        [
            {"input": "8 3\n1 3 -1 -3 5 3 6 7\n", "output": "3 3 5 5 6 7\n",
             "explain": "窗口依次为 [1,3,-1]→3；[3,-1,-3]→3；[-1,-3,5]→5；[-3,5,3]→5；[5,3,6]→6；[3,6,7]→7。"},
            {"input": "4 1\n1 2 3 4\n", "output": "1 2 3 4\n",
             "explain": "窗口大小为 1 时，答案就是数组本身。"},
        ],
        "**单调队列**：维护一个双端队列 `dq` 存**下标**，"
        "保证队列中对应的元素值**从队首到队尾单调递减**。\n\n"
        "处理元素 $a_i$ 时：\n"
        "1. 从**队尾**弹出所有值 $\\le a_i$ 的下标（它们不可能再成为最大值）；\n"
        "2. 把 $i$ 压入队尾；\n"
        "3. 若队首下标 $\\le i - k$，说明它已滑出窗口，从**队首**弹出；\n"
        "4. 当 $i \\ge k - 1$ 时，队首对应的元素即为当前窗口最大值。\n\n"
        "每个元素最多入队、出队各一次，总时间 $O(n)$。",
        "#include <cstdio>\n#include <vector>\n#include <deque>\n\n"
        "int main() {\n"
        "    int n, k;\n    scanf(\"%d %d\", &n, &k);\n"
        "    std::vector<long long> a(n);\n"
        "    for (int i = 0; i < n; ++i) scanf(\"%lld\", &a[i]);\n\n"
        "    std::deque<int> dq;\n"
        "    // TODO: 单调队列求每个窗口最大值\n\n"
        "    return 0;\n}\n",
        "#include <cstdio>\n#include <vector>\n#include <deque>\n\n"
        "int main() {\n"
        "    int n, k;\n    scanf(\"%d %d\", &n, &k);\n"
        "    std::vector<long long> a(n);\n"
        "    for (int i = 0; i < n; ++i) scanf(\"%lld\", &a[i]);\n\n"
        "    std::deque<int> dq;\n"
        "    bool first = true;\n"
        "    for (int i = 0; i < n; ++i) {\n"
        "        while (!dq.empty() && a[dq.back()] <= a[i]) dq.pop_back();\n"
        "        dq.push_back(i);\n"
        "        if (dq.front() <= i - k) dq.pop_front();\n"
        "        if (i >= k - 1) {\n"
        "            if (!first) printf(\" \");\n"
        "            printf(\"%lld\", a[dq.front()]);\n"
        "            first = false;\n"
        "        }\n"
        "    }\n    printf(\"\\n\");\n    return 0;\n}\n",
        tests,
    )


def build_lis() -> dict:
    tests = build_tests(LIS_SPECS, solve_lis)
    return _mk(
        "advanced-lis", "最长递增子序列（严格）", "中等",
        ["动态规划", "二分查找", "贪心"],
        {"name": "LeetCode 300", "url": "https://leetcode.cn/problems/longest-increasing-subsequence/"},
        "给定一个长度为 $n$ 的整数数组，求它的**最长严格递增子序列**的长度。\n\n"
        "子序列不要求连续，但必须保持原有的相对顺序。\n\n"
        "例如 `[10,9,2,5,3,7,101,18]` 的最长严格递增子序列是 `[2,3,7,101]`（或 `[2,3,7,18]`），长度为 4。\n\n"
        "**进阶要求**：使用 $O(n \\log n)$ 的算法。",
        "第一行一个整数 $n$（$1 \\le n \\le 2 \\times 10^5$）。\n\n第二行 $n$ 个整数 $a_i$（$|a_i| \\le 10^9$）。",
        "一行一个整数，表示最长严格递增子序列的长度。",
        ["1 ≤ n ≤ 2×10^5", "|a_i| ≤ 10^9", "子序列严格递增"],
        [
            {"input": "8\n10 9 2 5 3 7 101 18\n", "output": "4\n",
             "explain": "`[2,3,7,101]` 或 `[2,3,7,18]`，长度 4。"},
            {"input": "5\n5 4 3 2 1\n", "output": "1\n",
             "explain": "严格递减，最长递增子序列只能是单个元素。"},
        ],
        "**方法一（DP，$O(n^2)$）**：设 $f_i$ 为以 $a_i$ 结尾的最长递增子序列长度，"
        "$f_i = 1 + \\max\\{f_j : j < i, a_j < a_i\\}$。\n\n"
        "**方法二（贪心 + 二分，$O(n \\log n)$）**：维护数组 `tails`，"
        "其中 `tails[l]` 表示「长度为 $l+1$ 的递增子序列」可能的最小结尾值。\n\n"
        "对每个 $x$，用 `lower_bound` 找到 `tails` 中第一个 $\\ge x$ 的位置："
        "找到就替换它，找不到就追加到末尾。最终 `tails` 的长度即为答案。\n\n"
        "注意 `tails` 本身**不是**某个具体的最长递增子序列，但它的长度是正确的。",
        "#include <cstdio>\n#include <vector>\n#include <algorithm>\n\n"
        "int main() {\n"
        "    int n;\n    scanf(\"%d\", &n);\n"
        "    std::vector<int> a(n);\n"
        "    for (int i = 0; i < n; ++i) scanf(\"%d\", &a[i]);\n\n"
        "    std::vector<int> tails;\n"
        "    // TODO: 贪心 + 二分维护 tails\n\n"
        "    printf(\"%d\\n\", (int)tails.size());\n"
        "    return 0;\n}\n",
        "#include <cstdio>\n#include <vector>\n#include <algorithm>\n\n"
        "int main() {\n"
        "    int n;\n    scanf(\"%d\", &n);\n"
        "    std::vector<int> a(n);\n"
        "    for (int i = 0; i < n; ++i) scanf(\"%d\", &a[i]);\n\n"
        "    std::vector<int> tails;\n"
        "    for (int x : a) {\n"
        "        auto it = std::lower_bound(tails.begin(), tails.end(), x);\n"
        "        if (it == tails.end()) tails.push_back(x);\n"
        "        else *it = x;\n"
        "    }\n"
        "    printf(\"%d\\n\", (int)tails.size());\n"
        "    return 0;\n}\n",
        tests,
    )


def build_edit_distance() -> dict:
    tests = build_tests(EDIT_SPECS, solve_edit_distance)
    return _mk(
        "advanced-edit-distance", "编辑距离", "中等",
        ["动态规划", "字符串", "二维 DP"],
        {"name": "LeetCode 72", "url": "https://leetcode.cn/problems/edit-distance/"},
        "给定两个字符串 $s$ 和 $t$，求把 $s$ 转换成 $t$ 所需的**最少操作次数**。\n\n"
        "允许的操作有三种：\n"
        "1. 插入一个字符；\n"
        "2. 删除一个字符；\n"
        "3. 替换一个字符。\n\n"
        "每次操作计为 1 步。",
        "第一行字符串 $s$。\n\n第二行字符串 $t$。\n\n（$0 \\le |s|, |t| \\le 2000$）",
        "一行一个整数，表示最小操作次数。",
        ["0 ≤ |s|, |t| ≤ 2000", "仅含可见 ASCII"],
        [
            {"input": "horse\nros\n", "output": "3\n",
             "explain": "horse → rorse（替换 h）→ rose（删除 r）→ ros（删除 e），共 3 步。"},
            {"input": "intention\nexecution\n", "output": "5\n",
             "explain": "经典例子，最少需要 5 次操作。"},
        ],
        "**二维 DP**：设 $dp[i][j]$ 表示把 $s$ 的前 $i$ 个字符变成 $t$ 的前 $j$ 个字符的最少操作数。\n\n"
        "边界：$dp[i][0] = i$（全删除），$dp[0][j] = j$（全插入）。\n\n"
        "转移：\n"
        "- 若 $s_i = t_j$：$dp[i][j] = dp[i-1][j-1]$；\n"
        "- 否则 $dp[i][j] = 1 + \\min(dp[i-1][j],\\ dp[i][j-1],\\ dp[i-1][j-1])$\n"
        "  （分别对应删除、插入、替换）。\n\n"
        "时间 $O(|s| \\cdot |t|)$。由于只依赖上一行，可用**滚动数组**把空间降到 $O(\\min(|s|,|t|))$。",
        "#include <cstdio>\n#include <string>\n#include <vector>\n#include <algorithm>\n#include <iostream>\n\n"
        "int main() {\n"
        "    std::string s, t;\n"
        "    std::getline(std::cin, s);\n"
        "    std::getline(std::cin, t);\n"
        "    int n = (int)s.size(), m = (int)t.size();\n\n"
        "    // TODO: 动态规划\n\n"
        "    return 0;\n}\n",
        "#include <cstdio>\n#include <string>\n#include <vector>\n#include <algorithm>\n#include <iostream>\n\n"
        "int main() {\n"
        "    std::string s, t;\n"
        "    std::getline(std::cin, s);\n"
        "    std::getline(std::cin, t);\n"
        "    int n = (int)s.size(), m = (int)t.size();\n\n"
        "    std::vector<int> prev(m + 1), cur(m + 1);\n"
        "    for (int j = 0; j <= m; ++j) prev[j] = j;\n\n"
        "    for (int i = 1; i <= n; ++i) {\n"
        "        cur[0] = i;\n"
        "        for (int j = 1; j <= m; ++j) {\n"
        "            if (s[i - 1] == t[j - 1]) cur[j] = prev[j - 1];\n"
        "            else cur[j] = 1 + std::min(std::min(prev[j], cur[j - 1]), prev[j - 1]);\n"
        "        }\n"
        "        std::swap(prev, cur);\n"
        "    }\n"
        "    printf(\"%d\\n\", prev[m]);\n"
        "    return 0;\n}\n",
        tests,
    )


def build_knapsack() -> dict:
    tests = build_tests(KNAPSACK_SPECS, solve_knapsack)
    return _mk(
        "advanced-01-knapsack", "0-1 背包问题", "中等",
        ["动态规划", "背包", "一维 DP"],
        {"name": "背包问题九讲 / 算法导论经典问题", "url": "https://oi-wiki.org/dp/knapsack/"},
        "有 $n$ 件物品和一个容量为 $C$ 的背包。第 $i$ 件物品重量为 $w_i$、价值为 $v_i$。"
        "每件物品**最多选一次**，求在总重量不超过 $C$ 的前提下能获得的最大总价值。",
        "第一行两个整数 $n, C$（$1 \\le n \\le 1000$，$1 \\le C \\le 1000$）。\n\n"
        "接下来 $n$ 行，每行两个整数 $w_i, v_i$（$1 \\le w_i, v_i \\le 1000$）。",
        "一行一个整数，表示最大总价值。",
        ["1 ≤ n, C ≤ 1000", "1 ≤ w_i, v_i ≤ 1000"],
        [
            {"input": "3 5\n2 3\n3 4\n4 6\n", "output": "7\n",
             "explain": "选第 1、2 件，总重 2+3=5 ≤ 5，价值 3+4=7。"},
            {"input": "2 1\n5 10\n6 20\n", "output": "0\n",
             "explain": "两件物品都超过容量，什么都装不下，价值为 0。"},
        ],
        "**一维 DP**：设 $dp[c]$ 表示容量为 $c$ 时能取得的最大价值。\n\n"
        "对每件物品 $(w, v)$，**从大到小**枚举容量：\n\n"
        "```cpp\n"
        "for (int c = C; c >= w; --c)\n"
        "    dp[c] = max(dp[c], dp[c - w] + v);\n"
        "```\n\n"
        "**为什么必须倒序？** 因为 `dp[c - w]` 必须是「未考虑当前物品」的旧值。"
        "正序枚举会让同一件物品被重复选取（那是**完全背包**的写法）。\n\n"
        "时间 $O(nC)$，空间 $O(C)$。",
        "#include <cstdio>\n#include <vector>\n#include <algorithm>\n\n"
        "int main() {\n"
        "    int n, C;\n    scanf(\"%d %d\", &n, &C);\n"
        "    std::vector<int> dp(C + 1, 0);\n"
        "    for (int i = 0; i < n; ++i) {\n"
        "        int w, v;\n        scanf(\"%d %d\", &w, &v);\n"
        "        // TODO: 倒序枚举容量\n"
        "    }\n"
        "    printf(\"%d\\n\", dp[C]);\n"
        "    return 0;\n}\n",
        "#include <cstdio>\n#include <vector>\n#include <algorithm>\n\n"
        "int main() {\n"
        "    int n, C;\n    scanf(\"%d %d\", &n, &C);\n"
        "    std::vector<int> dp(C + 1, 0);\n"
        "    for (int i = 0; i < n; ++i) {\n"
        "        int w, v;\n        scanf(\"%d %d\", &w, &v);\n"
        "        for (int c = C; c >= w; --c)\n"
        "            dp[c] = std::max(dp[c], dp[c - w] + v);\n"
        "    }\n"
        "    printf(\"%d\\n\", dp[C]);\n"
        "    return 0;\n}\n",
        tests,
    )


def build_dsu() -> dict:
    tests = build_tests(DSU_SPECS, solve_dsu)
    return _mk(
        "advanced-dsu", "并查集（Union-Find）", "中等",
        ["并查集", "图", "路径压缩"],
        {"name": "LeetCode 547 相关 / 算法导论 21.3", "url": "https://oi-wiki.org/ds/dsu/"},
        "请实现**并查集**，支持两种操作（共 $n$ 个元素，编号 $1 \\sim n$）：\n\n"
        "- `1 a b`：把元素 $a$ 与 $b$ 所在的集合**合并**；\n"
        "- `2 a b`：查询 $a$ 与 $b$ 是否在**同一个集合**中。\n\n"
        "对每次查询操作，输出 `YES` 或 `NO`。",
        "第一行两个整数 $n, q$（$1 \\le n, q \\le 2 \\times 10^5$）。\n\n"
        "接下来 $q$ 行，每行三个整数 $op, a, b$，其中 $op \\in \\{1, 2\\}$。",
        "对每个查询操作（$op = 2$），输出一行 `YES` 或 `NO`。",
        ["1 ≤ n, q ≤ 2×10^5", "op ∈ {1,2}", "1 ≤ a, b ≤ n"],
        [
            {"input": "5 5\n1 1 2\n2 1 2\n1 3 4\n2 3 4\n2 1 4\n",
             "output": "YES\nYES\nNO\n",
             "explain": "合并 {1,2}、{3,4}；前两次查询同集合输出 YES；1 与 4 不同集合，输出 NO。"},
            {"input": "3 2\n2 1 2\n2 2 3\n", "output": "NO\nNO\n",
             "explain": "没有任何合并操作，所有元素各自独立。"},
        ],
        "并查集用数组 `parent[i]` 表示 $i$ 的父节点，根节点满足 `parent[i] == i`。\n\n"
        "**两个关键优化**：\n"
        "1. **路径压缩**：`find` 时把沿途节点的父指针直接指向根，使后续查询接近 $O(1)$；\n"
        "2. **按秩合并**：合并时把较矮的树挂到较高的树上（本实现用朴素合并也能通过）。\n\n"
        "同时使用两者，单次操作的**均摊复杂度**为 $O(\\alpha(n))$，"
        "其中 $\\alpha$ 是增长极慢的反阿克曼函数（实际可视为常数）。",
        "#include <cstdio>\n#include <vector>\n\n"
        "std::vector<int> parent;\n\n"
        "int find(int x) {\n"
        "    // TODO: 带路径压缩的查找\n    return x;\n}\n\n"
        "int main() {\n"
        "    int n, q;\n    scanf(\"%d %d\", &n, &q);\n"
        "    parent.resize(n + 1);\n"
        "    for (int i = 1; i <= n; ++i) parent[i] = i;\n\n"
        "    for (int i = 0; i < q; ++i) {\n"
        "        int op, a, b;\n        scanf(\"%d %d %d\", &op, &a, &b);\n"
        "        // TODO: 合并或查询\n"
        "    }\n    return 0;\n}\n",
        "#include <cstdio>\n#include <vector>\n\n"
        "std::vector<int> parent;\n\n"
        "int find(int x) {\n"
        "    while (parent[x] != x) {\n"
        "        parent[x] = parent[parent[x]];   // 路径压缩（隔代压缩）\n"
        "        x = parent[x];\n"
        "    }\n"
        "    return x;\n}\n\n"
        "int main() {\n"
        "    int n, q;\n    scanf(\"%d %d\", &n, &q);\n"
        "    parent.resize(n + 1);\n"
        "    for (int i = 1; i <= n; ++i) parent[i] = i;\n\n"
        "    for (int i = 0; i < q; ++i) {\n"
        "        int op, a, b;\n        scanf(\"%d %d %d\", &op, &a, &b);\n"
        "        int ra = find(a), rb = find(b);\n"
        "        if (op == 1) {\n"
        "            if (ra != rb) parent[ra] = rb;\n"
        "        } else {\n"
        "            printf(\"%s\\n\", ra == rb ? \"YES\" : \"NO\");\n"
        "        }\n"
        "    }\n    return 0;\n}\n",
        tests,
    )


def main() -> None:
    builders = [build_sliding_max, build_lis, build_edit_distance, build_knapsack, build_dsu]
    for b in builders:
        prob = b()
        path = finalize(prob, OUT / f"{prob['id']}.json")
        total = sum(t["score"] for t in prob["tests"])
        print(f"生成 {prob['id']:32s} {len(prob['tests'])} 测试点, 总分 {total}  -> {path.name}")


if __name__ == "__main__":
    main()
