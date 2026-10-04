"""生成「堆与优先队列」分类的题目。"""
from __future__ import annotations

import heapq
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from genkit import build_tests, finalize, numbers  # noqa: E402

OUT = ROOT / "oj" / "data" / "problems" / "05-heap"


# ============================================================ 1. 数组中的第 K 大元素
def solve_kth_largest(text: str) -> str:
    nums = numbers(text)
    n, k = nums[0], nums[1]
    a = nums[2:2 + n]
    return f"{sorted(a, reverse=True)[k - 1]}\n"


KTH_SPECS = [
    ("样例 1", "6 2\n3 2 1 5 6 4", 10),
    ("样例 2（含重复）", "9 4\n3 2 3 1 2 4 5 5 6", 10),
    ("k=1（最大值）", "5 1\n-1 -5 -3 -2 -4", 15),
    ("k=n（最小值）", "5 5\n1 2 3 4 5", 15),
    ("全相同", "6 3\n7 7 7 7 7 7", 15),
    ("单元素", "1 1\n42", 10),
    ("跨越零", "5 3\n-2 -1 0 1 2", 15),
    ("大数值", "4 2\n1000000000 -1000000000 0 1", 10),
]

# ============================================================ 2. 合并 K 个有序数组
def solve_merge_k(text: str) -> str:
    lines = text.strip("\n").split("\n")
    k = int(lines[0])
    heap = []
    for i in range(1, k + 1):
        # 行数可能不足 k（尾部空数组），此时视为空数组
        if i >= len(lines):
            continue
        parts = lines[i].split()
        if parts:
            for v in map(int, parts):
                heapq.heappush(heap, v)
    res = []
    while heap:
        res.append(heapq.heappop(heap))
    return (" ".join(map(str, res)) + "\n") if res else "\n"


MERGE_K_SPECS = [
    ("样例 1", "3\n1 4 5\n1 3 4\n2 6", 10),
    ("样例 2（单数组）", "1\n1 2 3", 10),
    ("空数组混合", "3\n1 5\n\n2 3", 15),
    ("全部为空", "2\n\n", 10),
    ("有重复值", "3\n1 1 1\n1 1\n1", 15),
    ("负数值", "3\n-5 -1\n-3 0\n-4 2", 20),
    ("长度悬殊", "3\n1\n100 200 300 400\n50", 20),
]

# ============================================================ 3. 堆的基本操作模拟
def solve_heap_ops(text: str) -> str:
    """模拟小根堆：push x / pop / top / size。pop 需返回最小值。"""
    lines = text.strip("\n").split("\n")
    q = int(lines[0])
    heap = []
    out = []
    for i in range(1, q + 1):
        p = lines[i].split()
        if p[0] == "push":
            heapq.heappush(heap, int(p[1]))
        elif p[0] == "pop":
            out.append(str(heapq.heappop(heap)))
        elif p[0] == "top":
            out.append(str(heap[0]))
        elif p[0] == "size":
            out.append(str(len(heap)))
    return ("\n".join(out) + "\n") if out else "\n"


HEAP_OPS_SPECS = [
    ("样例 1", "5\npush 3\npush 1\npush 2\ntop\npop", 10),
    ("单元素", "3\npush 5\ntop\nsize", 10),
    ("逆序插入", "6\npush 5\npush 4\npush 3\npop\npop\npop", 15),
    ("插入弹出交替", "6\npush 2\npop\npush 1\npop\npush 9\npop", 15),
    ("含负数", "5\npush -1\npush -5\npush -3\ntop\npop", 20),
    ("多次 size", "6\npush 1\nsize\npush 2\nsize\npop\nsize", 15),
    ("大量操作", "9\npush 10\npush 20\npush 5\npop\ntop\npush 1\ntop\npop\ntop", 20),
]

# ============================================================ 4. 数据流中位数
def solve_median_stream(text: str) -> str:
    """用双堆求数据流中位数，每插入一个就输出当前中位数（下取整）。"""
    nums = numbers(text)
    n = nums[0]
    a = nums[1:1 + n]
    lo, hi = [], []  # lo: 大根堆(取负), hi: 小根堆
    out = []
    for x in a:
        heapq.heappush(lo, -x)
        heapq.heappush(hi, -heapq.heappop(lo))
        if len(hi) > len(lo):
            heapq.heappush(lo, -heapq.heappop(hi))
        out.append(str(-lo[0]))
    return "\n".join(out) + "\n"


MEDIAN_SPECS = [
    ("样例 1", "4\n1 2 3 4", 10),
    ("样例 2", "5\n-1 5 3 2 0", 10),
    ("单元素", "1\n7", 10),
    ("递增", "5\n1 2 3 4 5", 15),
    ("递减", "5\n5 4 3 2 1", 15),
    ("全相同", "4\n3 3 3 3", 15),
    ("含负数", "6\n-5 -3 -1 0 2 4", 20),
]


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


def build_kth_largest() -> dict:
    tests = build_tests(KTH_SPECS, solve_kth_largest)
    return _mk(
        "heap-kth-largest", "数组中的第 K 大元素", "简单",
        ["堆", "优先队列", "快速选择", "排序"],
        {"name": "LeetCode 215", "url": "https://leetcode.cn/problems/kth-largest-element-in-an-array/"},
        "给定一个整数数组，返回其中**第 $k$ 大**的元素。\n\n"
        "注意是「第 $k$ 大」而非「第 $k$ 个不同的数」："
        "例如数组 `[3,2,3,1,2,4,5,5,6]` 的第 4 大元素是 **4**（排序后为 `6,5,5,4,...`）。",
        "第一行两个整数 $n, k$（$1 \\le k \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数 $a_i$（$|a_i| \\le 10^9$）。",
        "一行一个整数，表示第 $k$ 大的元素。",
        ["1 ≤ k ≤ n ≤ 10^5", "|a_i| ≤ 10^9"],
        [
            {"input": "6 2\n3 2 1 5 6 4\n", "output": "5\n",
             "explain": "降序排列为 6 5 4 3 2 1，第 2 大是 5。"},
            {"input": "9 4\n3 2 3 1 2 4 5 5 6\n", "output": "4\n",
             "explain": "降序为 6 5 5 4 3 3 2 2 1，第 4 大是 4。"},
        ],
        "**方法一（堆）**：维护一个大小为 $k$ 的**小根堆**，遍历数组，"
        "堆未满就入堆；满了则与堆顶比较——比堆顶大就替换堆顶。"
        "遍历结束时堆顶即答案。时间 $O(n \\log k)$。\n\n"
        "**方法二（快速选择）**：借用快速排序的 partition，期望 $O(n)$。\n\n"
        "直接排序是 $O(n \\log n)$，本题数据也能通过，但建议掌握堆的解法。",
        "#include <cstdio>\n#include <vector>\n#include <queue>\n#include <algorithm>\n\n"
        "int main() {\n"
        "    int n, k;\n    scanf(\"%d %d\", &n, &k);\n"
        "    std::vector<int> a(n);\n"
        "    for (int i = 0; i < n; ++i) scanf(\"%d\", &a[i]);\n\n"
        "    // TODO: 用大小为 k 的小根堆求解\n\n"
        "    return 0;\n}\n",
        "#include <cstdio>\n#include <vector>\n#include <queue>\n#include <functional>\n\n"
        "int main() {\n"
        "    int n, k;\n    scanf(\"%d %d\", &n, &k);\n"
        "    std::vector<int> a(n);\n"
        "    for (int i = 0; i < n; ++i) scanf(\"%d\", &a[i]);\n\n"
        "    std::priority_queue<int, std::vector<int>, std::greater<int>> pq;\n"
        "    for (int x : a) {\n"
        "        pq.push(x);\n"
        "        if ((int)pq.size() > k) pq.pop();\n"
        "    }\n"
        "    printf(\"%d\\n\", pq.top());\n"
        "    return 0;\n}\n",
        tests,
    )


def build_merge_k() -> dict:
    tests = build_tests(MERGE_K_SPECS, solve_merge_k)
    return _mk(
        "heap-merge-k-sorted", "合并 K 个有序数组", "中等",
        ["堆", "优先队列", "多路归并", "分治"],
        {"name": "LeetCode 23 变形", "url": "https://leetcode.cn/problems/merge-k-sorted-lists/"},
        "给定 $k$ 个**非递减**排列的整数数组，请把它们合并为一个非递减数组并输出。\n\n"
        "要求时间复杂度优于把所有元素直接合并后排序的 $O(N \\log N)$"
        "（$N$ 为元素总数），即 $O(N \\log k)$。\n\n"
        "允许存在空数组。",
        "第一行一个整数 $k$（$1 \\le k \\le 10^3$），表示数组个数。\n\n"
        "接下来 $k$ 行，第 $i$ 行给出第 $i$ 个数组的元素，以空格分隔；该行可能为空（表示空数组）。\n\n"
        "保证每个数组非递减。元素总数 $N \\le 2 \\times 10^5$，$|a| \\le 10^9$。",
        "一行，输出合并后的非递减序列，以空格分隔。若所有数组均为空，输出空行。",
        ["1 ≤ k ≤ 10^3", "元素总数 ≤ 2×10^5", "|a| ≤ 10^9", "每个数组非递减"],
        [
            {"input": "3\n1 4 5\n1 3 4\n2 6\n", "output": "1 1 2 3 4 4 5 6\n",
             "explain": "三个有序数组归并为一个有序数组。"},
            {"input": "1\n1 2 3\n", "output": "1 2 3\n",
             "explain": "只有一个数组时，合并结果就是它本身。"},
        ],
        "**多路归并 + 小根堆**：每个数组维护一个读取指针，初始把各数组的首元素"
        "（连同其所属数组编号）压入小根堆。\n\n"
        "每次弹出堆顶（当前全局最小值）加入答案，然后把该元素所在数组的**下一个元素**压入堆。\n\n"
        "堆的大小始终不超过 $k$，因此总时间 $O(N \\log k)$，空间 $O(k)$。",
        "#include <cstdio>\n#include <vector>\n#include <queue>\n#include <string>\n#include <sstream>\n#include <iostream>\n\n"
        "int main() {\n"
        "    int k;\n    scanf(\"%d\", &k);\n    getchar();\n"
        "    std::vector<std::vector<long long>> arrs(k);\n"
        "    for (int i = 0; i < k; ++i) {\n"
        "        std::string line;\n        std::getline(std::cin, line);\n"
        "        std::istringstream iss(line);\n        long long v;\n"
        "        while (iss >> v) arrs[i].push_back(v);\n"
        "    }\n\n"
        "    // TODO: 多路归并\n\n"
        "    return 0;\n}\n",
        "#include <cstdio>\n#include <vector>\n#include <queue>\n#include <string>\n#include <sstream>\n#include <iostream>\n\n"
        "struct Item {\n"
        "    long long val;\n    int arr, idx;\n"
        "    bool operator>(const Item& o) const { return val > o.val; }\n"
        "};\n\n"
        "int main() {\n"
        "    int k;\n    scanf(\"%d\", &k);\n    getchar();\n"
        "    std::vector<std::vector<long long>> arrs(k);\n"
        "    for (int i = 0; i < k; ++i) {\n"
        "        std::string line;\n        std::getline(std::cin, line);\n"
        "        std::istringstream iss(line);\n        long long v;\n"
        "        while (iss >> v) arrs[i].push_back(v);\n"
        "    }\n\n"
        "    std::priority_queue<Item, std::vector<Item>, std::greater<Item>> pq;\n"
        "    for (int i = 0; i < k; ++i)\n"
        "        if (!arrs[i].empty()) pq.push({arrs[i][0], i, 0});\n\n"
        "    std::vector<long long> out;\n"
        "    while (!pq.empty()) {\n"
        "        Item it = pq.top(); pq.pop();\n"
        "        out.push_back(it.val);\n"
        "        int ni = it.idx + 1;\n"
        "        if (ni < (int)arrs[it.arr].size())\n"
        "            pq.push({arrs[it.arr][ni], it.arr, ni});\n"
        "    }\n"
        "    for (size_t i = 0; i < out.size(); ++i) {\n"
        "        if (i) printf(\" \");\n        printf(\"%lld\", out[i]);\n"
        "    }\n    printf(\"\\n\");\n    return 0;\n}\n",
        tests,
    )


def build_heap_ops() -> dict:
    tests = build_tests(HEAP_OPS_SPECS, solve_heap_ops)
    return _mk(
        "heap-basic-ops", "小根堆的操作模拟", "入门",
        ["堆", "优先队列", "数据结构设计"],
        {"name": "堆的经典操作 / 算法导论 6.5", "url": "https://oi-wiki.org/ds/heap/"},
        "请实现一个**小根堆**（优先队列），支持以下操作：\n\n"
        "- `push x`：把 $x$ 插入堆中；\n"
        "- `pop`：删除并输出堆中的**最小**元素；\n"
        "- `top`：输出堆中的**最小**元素（不删除）；\n"
        "- `size`：输出堆中元素个数。\n\n"
        "题目保证 `pop` 与 `top` 只在堆非空时调用。\n\n"
        "本题帮助理解堆「始终维护最小值在堆顶」这一核心性质。",
        "第一行一个整数 $q$（$1 \\le q \\le 2 \\times 10^5$），表示操作数。\n\n"
        "接下来 $q$ 行，每行一个操作，格式如上。$|x| \\le 10^9$。",
        "对每个 `pop`、`top`、`size` 操作，输出一行对应的结果。",
        ["1 ≤ q ≤ 2×10^5", "|x| ≤ 10^9", "pop/top 仅在堆非空时调用"],
        [
            {"input": "5\npush 3\npush 1\npush 2\ntop\npop\n", "output": "1\n1\n",
             "explain": "插入 3、1、2 后最小值是 1；`pop` 弹出并输出 1。"},
            {"input": "3\npush 5\ntop\nsize\n", "output": "5\n1\n",
             "explain": "堆中只有 5，`top` 输出 5，`size` 输出 1。"},
        ],
        "C++ 中可以直接使用 `std::priority_queue`：\n\n"
        "```cpp\n"
        "#include <queue>\n"
        "std::priority_queue<int, std::vector<int>, std::greater<int>> pq;  // 小根堆\n"
        "```\n\n"
        "若想手写，可用数组实现**完全二叉树**：下标 $i$ 的左右孩子为 $2i, 2i+1$，"
        "插入时「上浮」（与父节点比较交换），弹出时把末尾元素移到堆顶再「下沉」。",
        "#include <cstdio>\n#include <vector>\n#include <queue>\n#include <functional>\n#include <cstring>\n\n"
        "int main() {\n"
        "    int q;\n    scanf(\"%d\", &q);\n"
        "    std::priority_queue<int, std::vector<int>, std::greater<int>> pq;\n"
        "    for (int i = 0; i < q; ++i) {\n"
        "        char op[16];\n        scanf(\"%s\", op);\n"
        "        // TODO: 分派四种操作\n"
        "    }\n    return 0;\n}\n",
        "#include <cstdio>\n#include <vector>\n#include <queue>\n#include <functional>\n#include <cstring>\n\n"
        "int main() {\n"
        "    int q;\n    scanf(\"%d\", &q);\n"
        "    std::priority_queue<int, std::vector<int>, std::greater<int>> pq;\n"
        "    for (int i = 0; i < q; ++i) {\n"
        "        char op[16];\n        scanf(\"%s\", op);\n"
        "        if (strcmp(op, \"push\") == 0) {\n"
        "            int x;\n            scanf(\"%d\", &x);\n            pq.push(x);\n"
        "        } else if (strcmp(op, \"pop\") == 0) {\n"
        "            printf(\"%d\\n\", pq.top());\n            pq.pop();\n"
        "        } else if (strcmp(op, \"top\") == 0) {\n"
        "            printf(\"%d\\n\", pq.top());\n"
        "        } else if (strcmp(op, \"size\") == 0) {\n"
        "            printf(\"%d\\n\", (int)pq.size());\n"
        "        }\n    }\n    return 0;\n}\n",
        tests,
    )


def build_median_stream() -> dict:
    tests = build_tests(MEDIAN_SPECS, solve_median_stream)
    return _mk(
        "heap-median-stream", "数据流的中位数", "困难",
        ["堆", "优先队列", "对顶堆", "设计"],
        {"name": "LeetCode 295", "url": "https://leetcode.cn/problems/find-median-from-data-stream/"},
        "给定一个整数序列，请依次把每个数加入集合，"
        "并在**每次加入后**输出当前集合的**中位数**。\n\n"
        "若有偶数个元素，返回**较小**的那个中间值（即下标 $\\lceil n/2 \\rceil$，从 1 计数）。\n\n"
        "例如当前集合为 `{-1, 5, 3, 2, 0}`，排序后为 `-1, 0, 2, 3, 5`，中位数为 **2**。",
        "第一行一个整数 $n$（$1 \\le n \\le 2 \\times 10^5$）。\n\n第二行 $n$ 个整数 $a_i$（$|a_i| \\le 10^9$）。",
        "共 $n$ 行，第 $i$ 行输出前 $i$ 个数的中位数。",
        ["1 ≤ n ≤ 2×10^5", "|a_i| ≤ 10^9", "偶数个元素时取下中位数"],
        [
            {"input": "4\n1 2 3 4\n", "output": "1\n1\n2\n2\n",
             "explain": "依次为 {1}→1；{1,2}→1；{1,2,3}→2；{1,2,3,4}→2。"},
            {"input": "5\n-1 5 3 2 0\n", "output": "-1\n-1\n3\n2\n2\n",
             "explain": "依次为 {-1}→-1；{-1,5}→-1；排序 -1,3,5 取中得 3；"
                        "排序 -1,2,3,5 取下中 2；排序 -1,0,2,3,5 取中 2。"},
        ],
        "**对顶堆（双堆）**：维护两个堆：\n\n"
        "- **大根堆 `lo`** 存较小的一半，堆顶是这一半的最大值；\n"
        "- **小根堆 `hi`** 存较大的一半，堆顶是这一半的最小值。\n\n"
        "插入 $x$：先入 `lo`，再把 `lo` 堆顶移到 `hi`；"
        "若 `hi` 比 `lo` 多，则把 `hi` 堆顶移回 `lo`。"
        "这样恒有 $|lo| \\ge |hi|$ 且 $|lo| - |hi| \\le 1$，"
        "**中位数始终是 `lo` 的堆顶**。\n\n每个元素 $O(\\log n)$，总计 $O(n \\log n)$。",
        "#include <cstdio>\n#include <vector>\n#include <queue>\n#include <functional>\n\n"
        "int main() {\n"
        "    int n;\n    scanf(\"%d\", &n);\n\n"
        "    std::priority_queue<long long> lo;  // 大根堆\n"
        "    std::priority_queue<long long, std::vector<long long>, std::greater<long long>> hi;\n\n"
        "    for (int i = 0; i < n; ++i) {\n"
        "        long long x;\n        scanf(\"%lld\", &x);\n"
        "        // TODO: 维护对顶堆并输出中位数\n"
        "    }\n    return 0;\n}\n",
        "#include <cstdio>\n#include <vector>\n#include <queue>\n#include <functional>\n\n"
        "int main() {\n"
        "    int n;\n    scanf(\"%d\", &n);\n\n"
        "    std::priority_queue<long long> lo;\n"
        "    std::priority_queue<long long, std::vector<long long>, std::greater<long long>> hi;\n\n"
        "    for (int i = 0; i < n; ++i) {\n"
        "        long long x;\n        scanf(\"%lld\", &x);\n"
        "        lo.push(x);\n        hi.push(lo.top()); lo.pop();\n"
        "        if (hi.size() > lo.size()) { lo.push(hi.top()); hi.pop(); }\n"
        "        printf(\"%lld\\n\", lo.top());\n"
        "    }\n    return 0;\n}\n",
        tests,
    )


def main() -> None:
    builders = [build_kth_largest, build_merge_k, build_heap_ops, build_median_stream]
    for b in builders:
        prob = b()
        path = finalize(prob, OUT / f"{prob['id']}.json")
        total = sum(t["score"] for t in prob["tests"])
        print(f"生成 {prob['id']:28s} {len(prob['tests'])} 测试点, 总分 {total}  -> {path.name}")


if __name__ == "__main__":
    main()
