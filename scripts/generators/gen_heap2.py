"""生成「堆与优先队列」分类的第二批题目。"""
from __future__ import annotations

import heapq
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from genkit import build_tests, finalize, numbers  # noqa: E402

OUT = ROOT / "oj" / "data" / "problems" / "05-heap"


# ============================================================ 1. 最后一块石头的重量
def solve_last_stone(text: str) -> str:
    """大根堆（用负数模拟）：每次取两块最大的相减。"""
    nums = numbers(text)
    n, a = nums[0], nums[1:1 + nums[0]]
    h = [-x for x in a]
    heapq.heapify(h)
    while len(h) >= 2:
        x = -heapq.heappop(h)
        y = -heapq.heappop(h)
        if x != y:
            heapq.heappush(h, -(x - y))
    return f"{-h[0] if h else 0}\n"


LSW_SPECS = [
    ("样例 1", "6\n2 7 4 1 8 1", 10),
    ("样例 2（全消）", "2\n5 5", 10),
    ("单块", "1\n9", 10),
    ("两块不等", "2\n3 7", 15),
    ("全相同偶数个", "4\n6 6 6 6", 15),
    ("全相同奇数个", "3\n4 4 4", 15),
    ("递增序列", "5\n1 2 3 4 5", 20),
]


def build_last_stone() -> dict:
    tests = build_tests(LSW_SPECS, solve_last_stone)
    return {
        "id": "heap-last-stone-weight",
        "title": "最后一块石头的重量",
        "difficulty": "简单",
        "tags": ["堆", "优先队列", "模拟"],
        "source": {
            "name": "LeetCode 1046 / 大根堆模拟",
            "url": "https://leetcode.cn/problems/last-stone-weight/",
        },
        "statement": (
            "有一堆石头，每块石头的重量为正整数。\n\n"
            "每一回合，从中选出**两块最重**的石头，然后将它们一起粉碎：\n"
            "- 若两块重量**相等**，则两块都消失；\n"
            "- 若**不等**，则较轻的一块消失，较重的一块剩余重量变为两者之差。\n\n"
            "重复上述过程直到**最多只剩一块**石头，输出它的重量；若一块也不剩，输出 $0$。"
        ),
        "input_format": "第一行一个整数 $n$（$1 \\le n \\le 10^4$）。\n\n第二行 $n$ 个正整数 $a_i$（$1 \\le a_i \\le 10^4$）。",
        "output_format": "一行一个整数，表示最后剩下石头的重量；若全被粉碎则输出 $0$。",
        "constraints": ["1 ≤ n ≤ 10^4", "1 ≤ a_i ≤ 10^4"],
        "samples": [
            {"input": "6\n2 7 4 1 8 1\n", "output": "1\n",
             "explain": "取 8 与 7 粉碎得 1；再取 4 与 2 粉碎得 2；再取 2 与 1 粉碎得 1；"
                        "最后取 1 与 1 粉碎，全消失……最终剩 1。"},
            {"input": "2\n5 5\n", "output": "0\n",
             "explain": "两块等重，一起消失，一块不剩。"},
        ],
        "hint": (
            "**大根堆**：每次都要取「当前最重的两块」，这正是堆擅长的操作。\n\n"
            "1. 把所有石头放进大根堆；\n"
            "2. 每次弹出两个最大值 $x \\ge y$；若 $x \\ne y$，把 $x - y$ 放回堆；\n"
            "3. 堆中不足两块时停止，输出堆中剩余的（或 $0$）。\n\n"
            "**C++ 技巧**：`std::priority_queue` 默认就是大根堆，直接用即可。\n"
            "若用 Python 的 `heapq`（小根堆），需要**存负数**来模拟大根堆。\n\n"
            "每次操作 $O(\\log n)$，总共 $O(n \\log n)$。"
        ),
        "starter_code": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <vector>\n"
                "#include <queue>\n\n"
                "int main() {\n"
                "    int n;\n"
                "    scanf(\"%d\", &n);\n"
                "    std::priority_queue<long long> pq;   // 默认大根堆\n"
                "    for (int i = 0; i < n; ++i) {\n"
                "        long long x; scanf(\"%lld\", &x);\n"
                "        pq.push(x);\n"
                "    }\n\n"
                "    // TODO: 每次取两块最大的相减\n\n"
                "    printf(\"%lld\\n\", pq.empty() ? 0LL : pq.top());\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "tests": tests,
        "reference": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <vector>\n"
                "#include <queue>\n\n"
                "int main() {\n"
                "    int n;\n"
                "    scanf(\"%d\", &n);\n"
                "    std::priority_queue<long long> pq;\n"
                "    for (int i = 0; i < n; ++i) {\n"
                "        long long x; scanf(\"%lld\", &x);\n"
                "        pq.push(x);\n"
                "    }\n\n"
                "    while (pq.size() >= 2) {\n"
                "        long long x = pq.top(); pq.pop();\n"
                "        long long y = pq.top(); pq.pop();\n"
                "        if (x != y) pq.push(x - y);\n"
                "    }\n\n"
                "    printf(\"%lld\\n\", pq.empty() ? 0LL : pq.top());\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "time_limit": 2.0,
    }


# ============================================================ 2. 最接近原点的 K 个点
def solve_k_closest(text: str) -> str:
    """按距离排序取前 k，输出按 (距离, x, y) 排序保证唯一。"""
    nums = numbers(text)
    n, k = nums[0], nums[1]
    pts = []
    idx = 2
    for _ in range(n):
        x, y = nums[idx], nums[idx + 1]
        idx += 2
        pts.append((x * x + y * y, x, y))
    pts.sort()
    sel = pts[:k]
    return "\n".join(f"{x} {y}" for _, x, y in sel) + "\n"


KC_SPECS = [
    ("样例 1", "3 2\n1 3\n-2 2\n2 -2", 10),
    ("样例 2（k=n）", "2 2\n0 1\n1 0", 10),
    ("k=1", "4 1\n3 4\n1 1\n0 5\n-2 -2", 10),
    ("含原点", "3 1\n0 0\n1 1\n-1 -1", 15),
    ("等距不同点", "4 2\n1 0\n-1 0\n0 1\n0 -1", 15),
    ("含负数", "3 3\n-3 -4\n-1 -1\n-2 -2", 20),
    ("大坐标", "3 2\n1000 1000\n1 1\n-500 500", 20),
]


def build_k_closest() -> dict:
    tests = build_tests(KC_SPECS, solve_k_closest)
    return {
        "id": "heap-k-closest-points",
        "title": "最接近原点的 K 个点",
        "difficulty": "中等",
        "tags": ["堆", "优先队列", "排序"],
        "source": {
            "name": "LeetCode 973 / Top-K",
            "url": "https://leetcode.cn/problems/k-closest-points-to-origin/",
        },
        "statement": (
            "给定平面上的 $n$ 个整数点和一个整数 $k$，找出距离原点 $(0,0)$ **最近的 $k$ 个点**。\n\n"
            "两点距离按**欧几里得距离**计算；为便于比较，可比较距离的平方 $x^2 + y^2$（无需开根号）。\n\n"
            "**输出要求**（为保证判题唯一性）：把这 $k$ 个点按"
            "「距离升序，距离相同则 $x$ 升序，再相同则 $y$ 升序」排列，每行输出一个点的 `x y`。"
        ),
        "input_format": (
            "第一行两个整数 $n, k$（$1 \\le k \\le n \\le 10^4$）。\n\n"
            "接下来 $n$ 行，每行两个整数 $x_i, y_i$（$|x_i|, |y_i| \\le 10^4$）。"
        ),
        "output_format": "共 $k$ 行，每行 `x y`，表示选中的点。",
        "constraints": ["1 ≤ k ≤ n ≤ 10^4", "|x|,|y| ≤ 10^4", "按 (距离, x, y) 升序输出"],
        "samples": [
            {"input": "3 2\n1 3\n-2 2\n2 -2\n", "output": "-2 2\n2 -2\n",
             "explain": "三点到原点距离平方分别为 10、8、8，最近的 2 个是 (-2,2) 与 (2,-2)，"
                        "两者等距，按 x 升序排列。"},
            {"input": "2 2\n0 1\n1 0\n", "output": "0 1\n1 0\n",
             "explain": "k=n，两点等距（都是 1），按 x 升序输出。"},
        ],
        "hint": (
            "**思路一：直接排序**（$O(n\\log n)$）。算出每个点的 $x^2+y^2$，"
            "按 (距离, x, y) 排序后取前 $k$ 个。本题数据规模下完全够用，实现也最简单。\n\n"
            "**思路二：大小为 $k$ 的大根堆**（$O(n\\log k)$）。"
            "维护「当前最近的 $k$ 个点」，堆顶是其中**最远**的。"
            "遇到新点时，若它比堆顶更近就替换堆顶。适合 $n$ 很大而 $k$ 很小的场景。\n\n"
            "> **易错点**：\n"
            "> 1. 比较距离用**平方**即可，避免浮点误差；\n"
            "> 2. 坐标可达 $10^4$，平方后约 $10^8$，两个相加约 $2\\times10^8$，"
            "虽在 int 范围内，但为稳妥建议用 `long long`；\n"
            "> 3. 等距点的输出顺序必须显式约定，否则判题不稳定。"
        ),
        "starter_code": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <vector>\n"
                "#include <algorithm>\n\n"
                "struct Point { long long x, y, d; };\n\n"
                "int main() {\n"
                "    int n, k;\n"
                "    scanf(\"%d %d\", &n, &k);\n"
                "    std::vector<Point> p(n);\n"
                "    for (int i = 0; i < n; ++i) {\n"
                "        scanf(\"%lld %lld\", &p[i].x, &p[i].y);\n"
                "        p[i].d = p[i].x * p[i].x + p[i].y * p[i].y;\n"
                "    }\n\n"
                "    // TODO: 选出最近的 k 个点并按 (d, x, y) 升序输出\n\n"
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
                "struct Point { long long x, y, d; };\n\n"
                "int main() {\n"
                "    int n, k;\n"
                "    scanf(\"%d %d\", &n, &k);\n"
                "    std::vector<Point> p(n);\n"
                "    for (int i = 0; i < n; ++i) {\n"
                "        scanf(\"%lld %lld\", &p[i].x, &p[i].y);\n"
                "        p[i].d = p[i].x * p[i].x + p[i].y * p[i].y;\n"
                "    }\n\n"
                "    std::sort(p.begin(), p.end(), [](const Point &a, const Point &b) {\n"
                "        if (a.d != b.d) return a.d < b.d;\n"
                "        if (a.x != b.x) return a.x < b.x;\n"
                "        return a.y < b.y;\n"
                "    });\n\n"
                "    for (int i = 0; i < k; ++i)\n"
                "        printf(\"%lld %lld\\n\", p[i].x, p[i].y);\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "time_limit": 2.0,
    }


# ============================================================ 3. 前 K 个高频元素
def solve_top_k_frequent(text: str) -> str:
    """统计频次后按 (频次降序, 值升序) 排序取前 k。"""
    nums = numbers(text)
    n, k = nums[0], nums[1]
    a = nums[2:2 + n]
    cnt = Counter(a)
    items = sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))
    sel = [v for v, _ in items[:k]]
    return " ".join(map(str, sel)) + "\n"


TKF_SPECS = [
    ("样例 1", "6 2\n1 1 1 2 2 3", 10),
    ("样例 2（k=1）", "2 1\n1 2", 10),
    ("全相同", "4 1\n5 5 5 5", 10),
    ("频次相同按值排", "6 3\n3 3 2 2 1 1", 15),
    ("含负数", "6 2\n-1 -1 -1 2 2 3", 15),
    ("k 等于不同值个数", "5 3\n1 2 2 3 3", 20),
    ("多频次混杂", "10 3\n4 4 4 4 1 1 1 2 2 3", 20),
]


def build_top_k_frequent() -> dict:
    tests = build_tests(TKF_SPECS, solve_top_k_frequent)
    return {
        "id": "heap-top-k-frequent",
        "title": "前 K 个高频元素",
        "difficulty": "中等",
        "tags": ["堆", "优先队列", "哈希表", "Top-K"],
        "source": {
            "name": "LeetCode 347 / 哈希 + 堆",
            "url": "https://leetcode.cn/problems/top-k-frequent-elements/",
        },
        "statement": (
            "给定一个整数数组和一个整数 $k$，返回其中出现**频率最高的 $k$ 个元素**。\n\n"
            "**输出要求**（为保证判题唯一性）：按「频率降序；频率相同则元素值升序」排列，"
            "在同一行以空格分隔。"
        ),
        "input_format": "第一行两个整数 $n, k$（$1 \\le k \\le$ 不同值的个数 $\\le n \\le 10^5$）。\n\n第二行 $n$ 个整数 $a_i$（$|a_i| \\le 10^9$）。",
        "output_format": "一行 $k$ 个整数，按上述规则排列，以空格分隔。",
        "constraints": ["1 ≤ n ≤ 10^5", "|a_i| ≤ 10^9", "k 不超过不同值的个数", "按 (频次降序, 值升序) 输出"],
        "samples": [
            {"input": "6 2\n1 1 1 2 2 3\n", "output": "1 2\n",
             "explain": "1 出现 3 次、2 出现 2 次、3 出现 1 次，频率最高的两个是 1 和 2。"},
            {"input": "6 3\n3 3 2 2 1 1\n", "output": "1 2 3\n",
             "explain": "三个数频率都是 2，按值升序输出 `1 2 3`。"},
        ],
        "hint": (
            "**两步走**：\n\n"
            "**第一步：统计频率。** 用哈希表（`unordered_map` 或排序后扫描）统计每个值的出现次数。\n\n"
            "**第二步：取频率最高的 $k$ 个。** 两种做法：\n"
            "1. **排序**：把 (值, 频次) 全部排序，$O(m\\log m)$（$m$ 为不同值个数），实现简单；\n"
            "2. **大小为 $k$ 的小根堆**：维护「当前频率最高的 $k$ 个」，"
            "堆顶是其中频率最低的，新元素频率更高就替换，$O(m\\log k)$。\n\n"
            "> **易错点**：本题要求「频率相同时按值升序」，排序时要写成"
            "「先比频次降序，再比值升序」的双关键字比较，只比频次会导致输出顺序不稳定。"
        ),
        "starter_code": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <vector>\n"
                "#include <unordered_map>\n"
                "#include <algorithm>\n\n"
                "int main() {\n"
                "    int n, k;\n"
                "    scanf(\"%d %d\", &n, &k);\n"
                "    std::unordered_map<long long, int> cnt;\n"
                "    for (int i = 0; i < n; ++i) {\n"
                "        long long x; scanf(\"%lld\", &x);\n"
                "        ++cnt[x];\n"
                "    }\n\n"
                "    // TODO: 按 (频次降序, 值升序) 排序，取前 k 个输出\n\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "tests": tests,
        "reference": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <vector>\n"
                "#include <unordered_map>\n"
                "#include <algorithm>\n\n"
                "int main() {\n"
                "    int n, k;\n"
                "    scanf(\"%d %d\", &n, &k);\n"
                "    std::unordered_map<long long, int> cnt;\n"
                "    for (int i = 0; i < n; ++i) {\n"
                "        long long x; scanf(\"%lld\", &x);\n"
                "        ++cnt[x];\n"
                "    }\n\n"
                "    std::vector<std::pair<long long,int>> v(cnt.begin(), cnt.end());\n"
                "    std::sort(v.begin(), v.end(), [](const auto &a, const auto &b) {\n"
                "        if (a.second != b.second) return a.second > b.second;  // 频次降序\n"
                "        return a.first < b.first;                              // 值升序\n"
                "    });\n\n"
                "    for (int i = 0; i < k; ++i) {\n"
                "        if (i) printf(\" \");\n"
                "        printf(\"%lld\", v[i].first);\n"
                "    }\n"
                "    printf(\"\\n\");\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "time_limit": 2.0,
    }


def main() -> None:
    builders = [build_last_stone, build_k_closest, build_top_k_frequent]
    for b in builders:
        prob = b()
        path = finalize(prob, OUT / f"{prob['id']}.json")
        total = sum(t["score"] for t in prob["tests"])
        print(f"生成 {prob['id']:30s} {len(prob['tests'])} 测试点, 总分 {total:3d}  -> {path.name}")


if __name__ == "__main__":
    main()
