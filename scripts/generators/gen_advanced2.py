"""生成「综合与进阶」分类的第二批题目。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from genkit import build_tests, finalize, numbers  # noqa: E402

OUT = ROOT / "oj" / "data" / "problems" / "08-advanced"


def _lines(text: str):
    return text.strip("\n").split("\n")


# ============================================================ 1. 最长公共子序列
def solve_lcs(text: str) -> str:
    """二维 DP，滚动数组优化空间。"""
    ls = _lines(text)
    a = ls[0].strip()
    b = ls[1].strip() if len(ls) > 1 else ""
    m = len(b)
    prev = [0] * (m + 1)
    for i in range(1, len(a) + 1):
        cur = [0] * (m + 1)
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1] + 1
            else:
                cur[j] = max(prev[j], cur[j - 1])
        prev = cur
    return f"{prev[m]}\n"


LCS_SPECS = [
    ("样例 1", "abcde\nace", 10),
    ("样例 2（无公共）", "abc\ndef", 10),
    ("完全相同", "abc\nabc", 10),
    ("其中一个是空串", "abc\n", 15),
    ("全相同字符", "aaaa\naa", 15),
    ("单字符匹配", "a\nb", 20),
    ("交叉匹配", "abcbdab\nbdcaba", 20),
]


def build_lcs() -> dict:
    tests = build_tests(LCS_SPECS, solve_lcs)
    return {
        "id": "advanced-lcs",
        "title": "最长公共子序列",
        "difficulty": "中等",
        "tags": ["动态规划", "字符串", "LCS"],
        "source": {
            "name": "LeetCode 1143 / 经典二维 DP",
            "url": "https://leetcode.cn/problems/longest-common-subsequence/",
        },
        "statement": (
            "给定两个字符串 $a$ 和 $b$，求它们的**最长公共子序列**（LCS）的长度。\n\n"
            "**子序列**指从原串中删去若干字符（可以不删）后得到的序列，"
            "**不要求连续**，但**不能改变字符的相对顺序**。\n\n"
            "例如 `abcde` 与 `ace` 的最长公共子序列是 `ace`，长度为 $3$。"
        ),
        "input_format": "第一行一个字符串 $a$。\n\n第二行一个字符串 $b$（可能为空行）。\n\n两串长度均不超过 $5000$，仅含小写英文字母。",
        "output_format": "一行一个整数，表示最长公共子序列的长度。",
        "constraints": ["0 ≤ |a|, |b| ≤ 5000", "仅含小写字母", "子序列不要求连续"],
        "samples": [
            {"input": "abcde\nace\n", "output": "3\n",
             "explain": "`ace` 是两者的公共子序列，且长度已达上限。"},
            {"input": "abc\ndef\n", "output": "0\n",
             "explain": "没有任何公共字符，长度为 0。"},
        ],
        "hint": (
            "**状态定义**：`dp[i][j]` = 「$a$ 的前 $i$ 个字符」与「$b$ 的前 $j$ 个字符」的 LCS 长度。\n\n"
            "**转移方程**：\n"
            "```\n"
            "if (a[i-1] == b[j-1])\n"
            "    dp[i][j] = dp[i-1][j-1] + 1;     // 该字符可纳入公共子序列\n"
            "else\n"
            "    dp[i][j] = max(dp[i-1][j], dp[i][j-1]);   // 舍弃其中一边的末尾\n"
            "```\n\n"
            "**初值**：`dp[0][*] = dp[*][0] = 0`（与空串的 LCS 为 $0$）。\n\n"
            "答案即 `dp[n][m]`。时间 $O(nm)$。\n\n"
            "> **空间优化**：注意到 `dp[i][*]` 只依赖上一行，可以用**滚动数组**把空间从 "
            "$O(nm)$ 降到 $O(m)$。但更新 `cur[j]` 时用到的是 `prev[j-1]`（上一行的左一格），"
            "所以要**单独保留上一行**，不能直接原地覆盖。"
        ),
        "starter_code": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <vector>\n"
                "#include <string>\n"
                "#include <algorithm>\n"
                "#include <iostream>\n\n"
                "int main() {\n"
                "    std::string a, b;\n"
                "    std::getline(std::cin, a);\n"
                "    std::getline(std::cin, b);\n\n"
                "    int n = a.size(), m = b.size();\n"
                "    // TODO: 二维 DP（可用滚动数组优化空间）\n"
                "    int ans = 0;\n\n"
                "    printf(\"%d\\n\", ans);\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "tests": tests,
        "reference": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <vector>\n"
                "#include <string>\n"
                "#include <algorithm>\n"
                "#include <iostream>\n\n"
                "int main() {\n"
                "    std::string a, b;\n"
                "    std::getline(std::cin, a);\n"
                "    std::getline(std::cin, b);\n\n"
                "    int n = (int)a.size(), m = (int)b.size();\n"
                "    std::vector<int> prev(m + 1, 0), cur(m + 1, 0);\n\n"
                "    for (int i = 1; i <= n; ++i) {\n"
                "        cur.assign(m + 1, 0);\n"
                "        for (int j = 1; j <= m; ++j) {\n"
                "            if (a[i - 1] == b[j - 1])\n"
                "                cur[j] = prev[j - 1] + 1;\n"
                "            else\n"
                "                cur[j] = std::max(prev[j], cur[j - 1]);\n"
                "        }\n"
                "        prev = cur;\n"
                "    }\n"
                "    printf(\"%d\\n\", prev[m]);\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "time_limit": 2.0,
    }


# ============================================================ 2. 完全背包
def solve_complete_knapsack(text: str) -> str:
    """完全背包：内层容量正序遍历，允许重复选取。"""
    nums = numbers(text)
    n, W = nums[0], nums[1]
    dp = [0] * (W + 1)
    idx = 2
    for _ in range(n):
        w, v = nums[idx], nums[idx + 1]
        idx += 2
        for j in range(w, W + 1):        # 正序
            if dp[j - w] + v > dp[j]:
                dp[j] = dp[j - w] + v
    return f"{dp[W]}\n"


CK_SPECS = [
    ("样例 1", "3 10\n3 5\n4 6\n5 9", 10),
    ("样例 2（单物品）", "1 10\n3 4", 10),
    ("容量为 0", "2 0\n1 5\n2 3", 10),
    ("装不满", "1 10\n4 7", 15),
    ("大容量重复装", "2 20\n3 2\n7 5", 15),
    ("价值全为 1", "2 10\n3 1\n4 1", 20),
    ("多种物品组合", "4 15\n2 3\n3 4\n4 5\n5 8", 20),
]


def build_complete_knapsack() -> dict:
    tests = build_tests(CK_SPECS, solve_complete_knapsack)
    return {
        "id": "advanced-complete-knapsack",
        "title": "完全背包",
        "difficulty": "中等",
        "tags": ["动态规划", "背包问题"],
        "source": {
            "name": "经典背包问题 / 完全背包",
            "url": "https://www.luogu.com.cn/problem/P1616",
        },
        "statement": (
            "有 $n$ 种物品和一个容量为 $W$ 的背包。第 $i$ 种物品的重量为 $w_i$、价值为 $v_i$。\n\n"
            "**每种物品都可以选取任意多件**（数量不限），求在总重量不超过 $W$ 的前提下，"
            "能获得的最大总价值。"
        ),
        "input_format": (
            "第一行两个整数 $n, W$（$1 \\le n \\le 1000$，$0 \\le W \\le 10^4$）。\n\n"
            "接下来 $n$ 行，每行两个整数 $w_i, v_i$（$1 \\le w_i \\le 10^4$，$0 \\le v_i \\le 10^4$）。"
        ),
        "output_format": "一行一个整数，表示能获得的最大总价值。",
        "constraints": ["1 ≤ n ≤ 1000", "0 ≤ W ≤ 10^4", "每种物品可无限次选取"],
        "samples": [
            {"input": "3 10\n3 5\n4 6\n5 9\n", "output": "18\n",
             "explain": "选 2 件第 3 种物品，总重 10、总价值 18，是最优解。"},
            {"input": "1 10\n3 4\n", "output": "12\n",
             "explain": "第 1 种物品可以选 3 件，总重 9、价值 12。"},
        ],
        "hint": (
            "**一维滚动数组写法**：`dp[j]` 表示容量为 $j$ 时能获得的最大价值。\n\n"
            "```\n"
            "for (每种物品 i)\n"
            "    for (int j = w[i]; j <= W; ++j)        // 正序遍历！\n"
            "        dp[j] = max(dp[j], dp[j - w[i]] + v[i]);\n"
            "```\n\n"
            "**为什么完全背包要正序，而 0-1 背包要倒序？**\n\n"
            "- **0-1 背包**：每件物品只能用一次，所以计算 `dp[j]` 时用到的 `dp[j-w]` "
            "必须是「**还没考虑当前物品**」的旧值 → 容量**倒序**遍历，避免同一物品被重复使用。\n"
            "- **完全背包**：每件物品可以无限次使用，我们希望 `dp[j-w]` 已经**包含了当前物品**"
            "（这样再加一件就相当于多选一件）→ 容量**正序**遍历。\n\n"
            "> 这是背包问题**最容易记反**的一点。记法：「**0-1 倒着走，完全正着走**」。"
        ),
        "starter_code": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <vector>\n"
                "#include <algorithm>\n\n"
                "int main() {\n"
                "    int n, W;\n"
                "    scanf(\"%d %d\", &n, &W);\n"
                "    std::vector<long long> dp(W + 1, 0);\n\n"
                "    for (int i = 0; i < n; ++i) {\n"
                "        int w; long long v;\n"
                "        scanf(\"%d %lld\", &w, &v);\n"
                "        // TODO: 注意内层容量的遍历方向\n"
                "    }\n\n"
                "    printf(\"%lld\\n\", dp[W]);\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "tests": tests,
        "reference": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <vector>\n"
                "#include <algorithm>\n\n"
                "int main() {\n"
                "    int n, W;\n"
                "    scanf(\"%d %d\", &n, &W);\n"
                "    std::vector<long long> dp(W + 1, 0);\n\n"
                "    for (int i = 0; i < n; ++i) {\n"
                "        int w; long long v;\n"
                "        scanf(\"%d %lld\", &w, &v);\n"
                "        for (int j = w; j <= W; ++j)            // 正序：允许重复选取\n"
                "            dp[j] = std::max(dp[j], dp[j - w] + v);\n"
                "    }\n\n"
                "    printf(\"%lld\\n\", dp[W]);\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "time_limit": 2.0,
    }


# ============================================================ 3. 乘积最大子数组
def solve_max_product(text: str) -> str:
    """同时维护以 i 结尾的最大值与最小值（负数会翻转）。"""
    nums = numbers(text)
    n, a = nums[0], nums[1:1 + nums[0]]
    best = a[0]
    cur_max = cur_min = a[0]
    for i in range(1, n):
        x = a[i]
        cand = (x, cur_max * x, cur_min * x)
        cur_max = max(cand)
        cur_min = min(cand)
        best = max(best, cur_max)
    return f"{best}\n"


MP_SPECS = [
    ("样例 1", "4\n2 3 -2 4", 10),
    ("样例 2（含零）", "3\n-2 0 -1", 10),
    ("单元素正", "1\n5", 10),
    ("单元素负", "1\n-5", 15),
    ("全负数偶数个", "4\n-1 -2 -3 -4", 15),
    ("含零分隔", "5\n1 2 0 3 4", 20),
    ("负负得正", "3\n-2 -3 -1", 20),
]


def build_max_product() -> dict:
    tests = build_tests(MP_SPECS, solve_max_product)
    return {
        "id": "advanced-max-product-subarray",
        "title": "乘积最大子数组",
        "difficulty": "中等",
        "tags": ["动态规划", "数组"],
        "source": {
            "name": "LeetCode 152 / 双状态 DP",
            "url": "https://leetcode.cn/problems/maximum-product-subarray/",
        },
        "statement": (
            "给定一个整数数组 $a$，求其中**乘积最大的连续子数组**的乘积。\n\n"
            "子数组要求**连续**（不能跳着取），且至少包含一个元素。"
        ),
        "input_format": "第一行一个整数 $n$（$1 \\le n \\le 2 \\times 10^5$）。\n\n第二行 $n$ 个整数 $a_i$（$|a_i| \\le 10$）。",
        "output_format": "一行一个整数，表示最大乘积。",
        "constraints": ["1 ≤ n ≤ 2×10^5", "|a_i| ≤ 10", "子数组必须连续"],
        "samples": [
            {"input": "4\n2 3 -2 4\n", "output": "6\n",
             "explain": "子数组 `[2,3]` 的乘积为 6；`[2,3,-2,4]` 为 -48，更小。"},
            {"input": "3\n-2 0 -1\n", "output": "0\n",
             "explain": "最大乘积来自子数组 `[0]`，值为 0。"},
        ],
        "hint": (
            "**难点**：不能像「最大子段和」那样只维护一个最大值。"
            "因为**负数乘以负数会变成正数**——当前最小的那个负数，"
            "乘上下一个负数后可能一跃成为最大值。\n\n"
            "**所以要同时维护两个状态**（都以 $i$ 结尾）：\n"
            "- `curMax`：以 $i$ 结尾的最大乘积；\n"
            "- `curMin`：以 $i$ 结尾的最小乘积。\n\n"
            "转移时，三者取极值：\n"
            "```\n"
            "long long c1 = x, c2 = curMax * x, c3 = curMin * x;\n"
            "curMax = max({c1, c2, c3});\n"
            "curMin = min({c1, c2, c3});\n"
            "best   = max(best, curMax);\n"
            "```\n\n"
            "> **易错点**：\n"
            "> 1. 必须**先算好两个新值再同时赋值**，否则 `curMax` 被覆盖后 `curMin` 就算错了；\n"
            "> 2. 答案要取**整个过程中的最大值**，不能直接返回最后的 `curMax`；\n"
            "> 3. 元素可能是负数，所以初值不能设成 $0$。"
        ),
        "starter_code": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <vector>\n"
                "#include <algorithm>\n\n"
                "int main() {\n"
                "    int n;\n"
                "    scanf(\"%d\", &n);\n"
                "    std::vector<long long> a(n);\n"
                "    for (int i = 0; i < n; ++i) scanf(\"%lld\", &a[i]);\n\n"
                "    long long curMax = a[0], curMin = a[0], best = a[0];\n"
                "    // TODO: 同时维护最大值与最小值\n\n"
                "    printf(\"%lld\\n\", best);\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "tests": tests,
        "reference": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <vector>\n"
                "#include <algorithm>\n\n"
                "int main() {\n"
                "    int n;\n"
                "    scanf(\"%d\", &n);\n"
                "    std::vector<long long> a(n);\n"
                "    for (int i = 0; i < n; ++i) scanf(\"%lld\", &a[i]);\n\n"
                "    long long curMax = a[0], curMin = a[0], best = a[0];\n"
                "    for (int i = 1; i < n; ++i) {\n"
                "        long long x = a[i];\n"
                "        long long c1 = x, c2 = curMax * x, c3 = curMin * x;\n"
                "        curMax = std::max({c1, c2, c3});\n"
                "        curMin = std::min({c1, c2, c3});\n"
                "        best = std::max(best, curMax);\n"
                "    }\n"
                "    printf(\"%lld\\n\", best);\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "time_limit": 2.0,
    }


def main() -> None:
    builders = [build_lcs, build_complete_knapsack, build_max_product]
    for b in builders:
        prob = b()
        path = finalize(prob, OUT / f"{prob['id']}.json")
        total = sum(t["score"] for t in prob["tests"])
        print(f"生成 {prob['id']:34s} {len(prob['tests'])} 测试点, 总分 {total:3d}  -> {path.name}")


if __name__ == "__main__":
    main()
