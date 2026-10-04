"""生成「图论基础」与「排序与查找」分类的题目。"""
from __future__ import annotations

import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from genkit import build_tests, finalize, numbers  # noqa: E402

OUT_GRAPH = ROOT / "oj" / "data" / "problems" / "06-graph"
OUT_SORT = ROOT / "oj" / "data" / "problems" / "07-sort-search"


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


# ==================================================== 图：通用读图工具

def read_graph(text: str):
    """读入 n m 及 m 条边，返回 (n, adj)。节点编号 1..n。"""
    nums = numbers(text)
    n, m = nums[0], nums[1]
    adj = [[] for _ in range(n + 1)]
    idx = 2
    for _ in range(m):
        u, v = nums[idx], nums[idx + 1]
        idx += 2
        adj[u].append(v)
        adj[v].append(u)
    return n, adj


# ============================================================ 图 1. 连通块数量
def solve_components(text: str) -> str:
    n, adj = read_graph(text)
    seen = [False] * (n + 1)
    cnt = 0
    for s in range(1, n + 1):
        if seen[s]:
            continue
        cnt += 1
        dq = deque([s])
        seen[s] = True
        while dq:
            u = dq.popleft()
            for v in adj[u]:
                if not seen[v]:
                    seen[v] = True
                    dq.append(v)
    return f"{cnt}\n"


COMPONENTS_SPECS = [
    ("样例 1", "5 3\n1 2\n2 3\n4 5", 10),
    ("样例 2（无向孤立点）", "3 0", 10),
    ("单点单边", "2 1\n1 2", 10),
    ("完全连通链", "5 4\n1 2\n2 3\n3 4\n4 5", 15),
    ("全部孤立", "4 0", 15),
    ("环 + 孤立点", "6 3\n1 2\n2 3\n3 1", 20),
    ("两个连通块", "6 4\n1 2\n2 3\n4 5\n5 6", 20),
]

# ============================================================ 图 2. 单源最短路（BFS 无权图）
def solve_bfs_shortest(text: str) -> str:
    nums = numbers(text)
    n, m, s = nums[0], nums[1], nums[2]
    adj = [[] for _ in range(n + 1)]
    idx = 3
    for _ in range(m):
        u, v = nums[idx], nums[idx + 1]
        idx += 2
        adj[u].append(v)
        adj[v].append(u)
    dist = [-1] * (n + 1)
    dist[s] = 0
    dq = deque([s])
    while dq:
        u = dq.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                dq.append(v)
    return " ".join(str(dist[i]) for i in range(1, n + 1)) + "\n"


BFS_SPECS = [
    ("样例 1", "5 4 1\n1 2\n1 3\n2 4\n3 5", 10),
    ("样例 2（不可达）", "4 1 1\n1 2", 10),
    ("单点", "1 0 1", 10),
    ("链状", "5 4 1\n1 2\n2 3\n3 4\n4 5", 15),
    ("星形", "5 4 1\n1 2\n1 3\n1 4\n1 5", 15),
    ("从中间出发", "4 3 2\n1 2\n2 3\n3 4", 20),
    ("含环", "5 5 1\n1 2\n2 3\n3 1\n3 4\n4 5", 20),
]

# ============================================================ 图 3. 拓扑排序
def solve_topological(text: str) -> str:
    """有向图拓扑排序，字典序最小的合法序列（用最小堆）。"""
    import heapq
    nums = numbers(text)
    n, m = nums[0], nums[1]
    adj = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    idx = 2
    for _ in range(m):
        u, v = nums[idx], nums[idx + 1]
        idx += 2
        adj[u].append(v)
        indeg[v] += 1
    h = [i for i in range(1, n + 1) if indeg[i] == 0]
    heapq.heapify(h)
    res = []
    while h:
        u = heapq.heappop(h)
        res.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                heapq.heappush(h, v)
    if len(res) != n:
        return "NO\n"
    return " ".join(map(str, res)) + "\n"


TOPO_SPECS = [
    ("样例 1", "4 3\n1 2\n1 3\n3 4", 10),
    ("样例 2（无依赖）", "3 0", 10),
    ("单链", "4 3\n1 2\n2 3\n3 4", 15),
    ("有环", "3 3\n1 2\n2 3\n3 1", 15),
    ("多起点", "5 4\n1 3\n2 3\n3 4\n3 5", 20),
    ("单点", "1 0", 10),
    ("复杂 DAG", "6 6\n1 2\n2 4\n3 4\n4 5\n4 6\n1 3", 20),
]

# ============================================================ 排序 1. 快速排序
def solve_quicksort(text: str) -> str:
    nums = numbers(text)
    n, a = nums[0], nums[1:1 + nums[0]]
    return " ".join(map(str, sorted(a))) + "\n"


QUICKSORT_SPECS = [
    ("样例 1", "5\n3 1 4 1 5", 10),
    ("样例 2（已排序）", "5\n1 2 3 4 5", 10),
    ("单元素", "1\n7", 10),
    ("逆序", "6\n6 5 4 3 2 1", 15),
    ("全相同", "5\n2 2 2 2 2", 15),
    ("含负数", "6\n-3 0 -1 5 -2 4", 20),
    ("大量数据", "15\n" + " ".join(str(x) for x in [7, 3, 9, 1, 5, 8, 2, 6, 4, 0, 12, 11, 10, 14, 13]), 20),
]

# ============================================================ 排序 2. 归并排序求逆序对
def solve_inversion_count(text: str) -> str:
    nums = numbers(text)
    n, a = nums[0], nums[1:1 + nums[0]]

    def merge_count(arr):
        if len(arr) <= 1:
            return arr, 0
        mid = len(arr) // 2
        left, cl = merge_count(arr[:mid])
        right, cr = merge_count(arr[mid:])
        merged = []
        i = j = 0
        cnt = cl + cr
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i]); i += 1
            else:
                merged.append(right[j]); j += 1
                cnt += len(left) - i
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged, cnt

    _, cnt = merge_count(a)
    return f"{cnt}\n"


INVERSION_SPECS = [
    ("样例 1", "5\n2 4 1 3 5", 10),
    ("样例 2（有序）", "4\n1 2 3 4", 10),
    ("逆序（最大值）", "4\n4 3 2 1", 15),
    ("单元素", "1\n5", 10),
    ("全相同", "4\n3 3 3 3", 15),
    ("含负数", "4\n-1 2 -3 4", 20),
    ("两元素有序", "2\n1 2", 10),
    ("较大规模", "6\n5 4 3 2 1 0", 20),
]

# ============================================================ 查找 1. 二分查找
def solve_binary_search(text: str) -> str:
    nums = numbers(text)
    n, q = nums[0], nums[1]
    a = nums[2:2 + n]
    queries = nums[2 + n:2 + n + q]
    out = []
    for x in queries:
        lo, hi, ans = 0, n - 1, -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if a[mid] == x:
                ans = mid
                break
            elif a[mid] < x:
                lo = mid + 1
            else:
                hi = mid - 1
        out.append(str(ans))
    return "\n".join(out) + "\n"


BINARY_SPECS = [
    ("样例 1", "5 3\n1 3 5 7 9\n3 5 10", 10),
    ("找不到", "3 2\n1 2 3\n0 4", 10),
    ("单元素命中", "1 1\n5\n5", 10),
    ("单元素未命中", "1 1\n5\n6", 10),
    ("首尾元素", "5 2\n10 20 30 40 50\n10 50", 15),
    ("含负数", "5 3\n-10 -5 0 5 10\n-5 0 10", 20),
    ("全部查询相同", "4 3\n1 2 3 4\n3 3 3", 15),
]

# ============================================================ 查找 2. 首个不小于 x 的位置（lower_bound）
def solve_lower_bound(text: str) -> str:
    nums = numbers(text)
    n, q = nums[0], nums[1]
    a = nums[2:2 + n]
    queries = nums[2 + n:2 + n + q]
    import bisect
    out = []
    for x in queries:
        pos = bisect.bisect_left(a, x)
        out.append(str(pos + 1) if pos < n else "0")
    return "\n".join(out) + "\n"


LOWER_BOUND_SPECS = [
    ("样例 1", "5 3\n1 3 5 7 9\n3 4 10", 10),
    ("都小于最小值", "3 1\n5 6 7\n1", 10),
    ("都大于最大值", "3 1\n1 2 3\n100", 10),
    ("命中边界", "4 2\n1 2 3 4\n1 4", 15),
    ("重复元素", "5 3\n1 2 2 2 3\n2 3 4", 20),
    ("含负数", "4 2\n-5 -3 0 1\n-4 0", 20),
    ("单元素", "1 2\n5\n5 6", 15),
]


def build_components() -> dict:
    tests = build_tests(COMPONENTS_SPECS, solve_components)
    return _mk(
        "graph-connected-components", "无向图连通块数量", "入门",
        ["图", "DFS", "BFS", "并查集"],
        {"name": "LeetCode 547 变形 / 图论基础", "url": "https://leetcode.cn/problems/number-of-provinces/"},
        "给定一个包含 $n$ 个节点、$m$ 条边的**无向图**，请统计它有多少个**连通块**。\n\n"
        "若两个节点之间存在路径则它们属于同一连通块。单独一个没有任何边的节点也算一个连通块。\n\n"
        "节点编号为 $1 \\sim n$。",
        "第一行两个整数 $n, m$（$1 \\le n \\le 10^5$，$0 \\le m \\le 2 \\times 10^5$）。\n\n"
        "接下来 $m$ 行，每行两个整数 $u, v$，表示一条无向边。",
        "一行一个整数，表示连通块数量。",
        ["1 ≤ n ≤ 10^5", "0 ≤ m ≤ 2×10^5", "无重边、无自环"],
        [
            {"input": "5 3\n1 2\n2 3\n4 5\n", "output": "2\n",
             "explain": "{1,2,3} 构成一个连通块，{4,5} 构成另一个。"},
            {"input": "3 0\n", "output": "3\n", "explain": "没有边，3 个节点各自是独立连通块。"},
        ],
        "对每个未访问节点发起一次 DFS/BFS，把所有能到达的节点标记为已访问；"
        "发起搜索的次数即为连通块数量。\n\n时间 $O(n + m)$，空间 $O(n + m)$。\n\n"
        "也可以用**并查集**：把每条边的两个端点合并，最终不同集合的个数即为答案。",
        "#include <cstdio>\n#include <vector>\n#include <queue>\n\n"
        "int main() {\n"
        "    int n, m;\n    scanf(\"%d %d\", &n, &m);\n"
        "    std::vector<std::vector<int>> adj(n + 1);\n"
        "    for (int i = 0; i < m; ++i) {\n"
        "        int u, v;\n        scanf(\"%d %d\", &u, &v);\n"
        "        adj[u].push_back(v);\n        adj[v].push_back(u);\n"
        "    }\n\n"
        "    // TODO: 统计连通块数量\n\n"
        "    return 0;\n}\n",
        "#include <cstdio>\n#include <vector>\n#include <queue>\n\n"
        "int main() {\n"
        "    int n, m;\n    scanf(\"%d %d\", &n, &m);\n"
        "    std::vector<std::vector<int>> adj(n + 1);\n"
        "    for (int i = 0; i < m; ++i) {\n"
        "        int u, v;\n        scanf(\"%d %d\", &u, &v);\n"
        "        adj[u].push_back(v);\n        adj[v].push_back(u);\n"
        "    }\n\n"
        "    std::vector<char> seen(n + 1, 0);\n"
        "    int cnt = 0;\n"
        "    for (int s = 1; s <= n; ++s) {\n"
        "        if (seen[s]) continue;\n"
        "        ++cnt;\n"
        "        std::queue<int> q;\n        q.push(s);\n        seen[s] = 1;\n"
        "        while (!q.empty()) {\n"
        "            int u = q.front(); q.pop();\n"
        "            for (int v : adj[u]) if (!seen[v]) { seen[v] = 1; q.push(v); }\n"
        "        }\n"
        "    }\n"
        "    printf(\"%d\\n\", cnt);\n    return 0;\n}\n",
        tests,
    )


def build_bfs_shortest() -> dict:
    tests = build_tests(BFS_SPECS, solve_bfs_shortest)
    return _mk(
        "graph-bfs-shortest", "无权图单源最短路", "简单",
        ["图", "BFS", "最短路"],
        {"name": "BFS 经典 / 算法导论 22.2", "url": "https://oi-wiki.org/graph/bfs/"},
        "给定一个 $n$ 个节点、$m$ 条边的**无向无权图**，以及起点 $s$，"
        "求 $s$ 到每个节点的**最短路径长度**（经过的边数）。\n\n"
        "若某节点从 $s$ 不可达，输出 $-1$。$s$ 到自身距离为 $0$。",
        "第一行三个整数 $n, m, s$（$1 \\le n \\le 10^5$，$0 \\le m \\le 2 \\times 10^5$）。\n\n"
        "接下来 $m$ 行，每行两个整数 $u, v$，表示一条无向边。",
        "一行 $n$ 个整数，依次为节点 $1 \\sim n$ 到 $s$ 的最短距离，以空格分隔（不可达为 $-1$）。",
        ["1 ≤ n ≤ 10^5", "0 ≤ m ≤ 2×10^5", "1 ≤ s ≤ n"],
        [
            {"input": "5 4 1\n1 2\n1 3\n2 4\n3 5\n", "output": "0 1 1 2 2\n",
             "explain": "1 到自身 0；2、3 距离 1；4、5 距离 2。"},
            {"input": "4 1 1\n1 2\n", "output": "0 1 -1 -1\n",
             "explain": "节点 3、4 从 1 无法到达，输出 -1。"},
        ],
        "**BFS** 天然按距离递增的顺序扩展：起点入队、`dist[s]=0`；"
        "每次出队节点 $u$，遍历其邻居 $v$——若 $v$ 尚未被访问，"
        "则 `dist[v] = dist[u] + 1` 并入队。\n\n"
        "无权图中 BFS 首次到达某节点时的距离即为最短路。时间 $O(n + m)$。",
        "#include <cstdio>\n#include <vector>\n#include <queue>\n\n"
        "int main() {\n"
        "    int n, m, s;\n    scanf(\"%d %d %d\", &n, &m, &s);\n"
        "    std::vector<std::vector<int>> adj(n + 1);\n"
        "    for (int i = 0; i < m; ++i) {\n"
        "        int u, v;\n        scanf(\"%d %d\", &u, &v);\n"
        "        adj[u].push_back(v);\n        adj[v].push_back(u);\n"
        "    }\n\n"
        "    std::vector<int> dist(n + 1, -1);\n"
        "    // TODO: BFS 计算最短路\n\n"
        "    for (int i = 1; i <= n; ++i) {\n"
        "        if (i > 1) printf(\" \");\n        printf(\"%d\", dist[i]);\n"
        "    }\n    printf(\"\\n\");\n    return 0;\n}\n",
        "#include <cstdio>\n#include <vector>\n#include <queue>\n\n"
        "int main() {\n"
        "    int n, m, s;\n    scanf(\"%d %d %d\", &n, &m, &s);\n"
        "    std::vector<std::vector<int>> adj(n + 1);\n"
        "    for (int i = 0; i < m; ++i) {\n"
        "        int u, v;\n        scanf(\"%d %d\", &u, &v);\n"
        "        adj[u].push_back(v);\n        adj[v].push_back(u);\n"
        "    }\n\n"
        "    std::vector<int> dist(n + 1, -1);\n"
        "    std::queue<int> q;\n"
        "    dist[s] = 0;\n    q.push(s);\n"
        "    while (!q.empty()) {\n"
        "        int u = q.front(); q.pop();\n"
        "        for (int v : adj[u]) if (dist[v] == -1) {\n"
        "            dist[v] = dist[u] + 1;\n            q.push(v);\n"
        "        }\n"
        "    }\n"
        "    for (int i = 1; i <= n; ++i) {\n"
        "        if (i > 1) printf(\" \");\n        printf(\"%d\", dist[i]);\n"
        "    }\n    printf(\"\\n\");\n    return 0;\n}\n",
        tests,
    )


def build_topological() -> dict:
    tests = build_tests(TOPO_SPECS, solve_topological)
    return _mk(
        "graph-topological-sort", "拓扑排序（字典序最小）", "中等",
        ["图", "拓扑排序", "DAG", "优先队列"],
        {"name": "LeetCode 210 变形 / 算法导论 22.4", "url": "https://oi-wiki.org/graph/topo/"},
        "给定一个 $n$ 个节点、$m$ 条边的**有向图**，求它的**拓扑排序**。\n\n"
        "拓扑排序要求：对每条有向边 $u \\to v$，在序列中 $u$ 必须排在 $v$ 之前。\n\n"
        "若存在**多个**合法的拓扑序，请输出**字典序最小**的那个"
        "（即每次选择编号最小的可用节点）。\n\n"
        "若图中存在**环**，则不存在拓扑序，输出 `NO`。",
        "第一行两个整数 $n, m$（$1 \\le n \\le 10^5$，$0 \\le m \\le 2 \\times 10^5$）。\n\n"
        "接下来 $m$ 行，每行两个整数 $u, v$，表示有向边 $u \\to v$。",
        "一行。若存在拓扑序，输出 $n$ 个节点编号（字典序最小）；否则输出 `NO`。",
        ["1 ≤ n ≤ 10^5", "0 ≤ m ≤ 2×10^5", "无自环"],
        [
            {"input": "4 3\n1 2\n1 3\n3 4\n", "output": "1 2 3 4\n",
             "explain": "1 必须先于 2、3；3 先于 4。可用节点中编号最小优先，得到 1 2 3 4。"},
            {"input": "3 3\n1 2\n2 3\n3 1\n", "output": "NO\n",
             "explain": "存在环 1→2→3→1，无法拓扑排序。"},
        ],
        "**Kahn 算法（BFS 版）**：\n"
        "1. 统计每个节点的入度；\n"
        "2. 把所有入度为 $0$ 的节点放入**最小堆**；\n"
        "3. 每次取出堆顶（当前编号最小的可用节点）加入答案，"
        "并把它的所有后继入度减一；减到 $0$ 的后继入堆；\n"
        "4. 若最终答案长度 $< n$，说明有环。\n\n"
        "用最小堆替代普通队列即可保证字典序最小，时间 $O((n+m)\\log n)$。",
        "#include <cstdio>\n#include <vector>\n#include <queue>\n\n"
        "int main() {\n"
        "    int n, m;\n    scanf(\"%d %d\", &n, &m);\n"
        "    std::vector<std::vector<int>> adj(n + 1);\n"
        "    std::vector<int> indeg(n + 1, 0);\n"
        "    for (int i = 0; i < m; ++i) {\n"
        "        int u, v;\n        scanf(\"%d %d\", &u, &v);\n"
        "        adj[u].push_back(v);\n        indeg[v]++;\n"
        "    }\n\n"
        "    // TODO: 用最小堆实现 Kahn 算法\n\n"
        "    return 0;\n}\n",
        "#include <cstdio>\n#include <vector>\n#include <queue>\n#include <functional>\n\n"
        "int main() {\n"
        "    int n, m;\n    scanf(\"%d %d\", &n, &m);\n"
        "    std::vector<std::vector<int>> adj(n + 1);\n"
        "    std::vector<int> indeg(n + 1, 0);\n"
        "    for (int i = 0; i < m; ++i) {\n"
        "        int u, v;\n        scanf(\"%d %d\", &u, &v);\n"
        "        adj[u].push_back(v);\n        indeg[v]++;\n"
        "    }\n\n"
        "    std::priority_queue<int, std::vector<int>, std::greater<int>> pq;\n"
        "    for (int i = 1; i <= n; ++i) if (indeg[i] == 0) pq.push(i);\n\n"
        "    std::vector<int> res;\n"
        "    while (!pq.empty()) {\n"
        "        int u = pq.top(); pq.pop();\n"
        "        res.push_back(u);\n"
        "        for (int v : adj[u]) {\n"
        "            if (--indeg[v] == 0) pq.push(v);\n"
        "        }\n"
        "    }\n"
        "    if ((int)res.size() != n) { printf(\"NO\\n\"); return 0; }\n"
        "    for (int i = 0; i < n; ++i) {\n"
        "        if (i) printf(\" \");\n        printf(\"%d\", res[i]);\n"
        "    }\n    printf(\"\\n\");\n    return 0;\n}\n",
        tests,
    )


def build_quicksort() -> dict:
    tests = build_tests(QUICKSORT_SPECS, solve_quicksort)
    return _mk(
        "sort-quicksort", "排序（升序输出）", "入门",
        ["排序", "快速排序", "分治"],
        {"name": "排序算法基础 / 算法导论 7", "url": "https://oi-wiki.org/basic/quick-sort/"},
        "给定 $n$ 个整数，请把它们按**升序**排列后输出。\n\n"
        "请**自己实现排序算法**（如快速排序、归并排序、堆排序），"
        "不要直接调用库函数，以体会分治思想。\n\n"
        "（评测只看输出结果，但强烈建议手写实现。）",
        "第一行一个整数 $n$（$1 \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数 $a_i$（$|a_i| \\le 10^9$）。",
        "一行，输出升序排列后的序列，以空格分隔。",
        ["1 ≤ n ≤ 10^5", "|a_i| ≤ 10^9"],
        [
            {"input": "5\n3 1 4 1 5\n", "output": "1 1 3 4 5\n",
             "explain": "升序排列，重复元素保留。"},
            {"input": "5\n1 2 3 4 5\n", "output": "1 2 3 4 5\n",
             "explain": "已经有序时输出不变。"},
        ],
        "**快速排序**：选一个基准 `pivot`，把数组划分为「小于基准」与「不小于基准」两部分，"
        "再分别递归排序。平均时间 $O(n \\log n)$。\n\n"
        "**关键点**：若总取第一个元素作基准，**已排序数组**会退化成 $O(n^2)$ 并导致栈溢出。"
        "常见对策是随机选基准或三数取中。\n\n"
        "**归并排序**：稳定 $O(n \\log n)$，且能顺便统计逆序对（见下一题）。",
        "#include <cstdio>\n#include <vector>\n\n"
        "void quickSort(int* a, int l, int r) {\n"
        "    // TODO: 实现快速排序\n"
        "}\n\n"
        "int main() {\n"
        "    int n;\n    scanf(\"%d\", &n);\n"
        "    std::vector<int> a(n);\n"
        "    for (int i = 0; i < n; ++i) scanf(\"%d\", &a[i]);\n\n"
        "    quickSort(a.data(), 0, n - 1);\n\n"
        "    for (int i = 0; i < n; ++i) {\n"
        "        if (i) printf(\" \");\n        printf(\"%d\", a[i]);\n"
        "    }\n    printf(\"\\n\");\n    return 0;\n}\n",
        "#include <cstdio>\n#include <vector>\n#include <algorithm>\n#include <random>\n\n"
        "void quickSort(std::vector<long long>& a, int l, int r) {\n"
        "    if (l >= r) return;\n"
        "    // 三数取中，避免有序数据退化\n"
        "    int mid = l + (r - l) / 2;\n"
        "    long long p; \n"
        "    if ((a[l] <= a[mid] && a[mid] <= a[r]) || (a[r] <= a[mid] && a[mid] <= a[l])) p = a[mid];\n"
        "    else if ((a[mid] <= a[l] && a[l] <= a[r]) || (a[r] <= a[l] && a[l] <= a[mid])) p = a[l];\n"
        "    else p = a[r];\n\n"
        "    int i = l, j = r;\n"
        "    while (i <= j) {\n"
        "        while (a[i] < p) ++i;\n"
        "        while (a[j] > p) --j;\n"
        "        if (i <= j) { std::swap(a[i], a[j]); ++i; --j; }\n"
        "    }\n"
        "    quickSort(a, l, j);\n    quickSort(a, i, r);\n}\n\n"
        "int main() {\n"
        "    int n;\n    scanf(\"%d\", &n);\n"
        "    std::vector<long long> a(n);\n"
        "    for (int i = 0; i < n; ++i) scanf(\"%lld\", &a[i]);\n\n"
        "    quickSort(a, 0, n - 1);\n\n"
        "    for (int i = 0; i < n; ++i) {\n"
        "        if (i) printf(\" \");\n        printf(\"%lld\", a[i]);\n"
        "    }\n    printf(\"\\n\");\n    return 0;\n}\n",
        tests,
    )


def build_inversion_count() -> dict:
    tests = build_tests(INVERSION_SPECS, solve_inversion_count)
    return _mk(
        "sort-inversion-count", "逆序对数量（归并排序）", "中等",
        ["排序", "归并排序", "分治", "逆序对"],
        {"name": "LeetCode 剑指 Offer 51 / 算法导论思考题 2-4", "url": "https://leetcode.cn/problems/shu-zu-zhong-de-ni-xu-dui-lcof/"},
        "给定一个长度为 $n$ 的整数数组，统计其中**逆序对**的数量。\n\n"
        "逆序对指满足 $i < j$ 且 $a_i > a_j$ 的下标对 $(i, j)$。\n\n"
        "请使用**归并排序**的分治思想在 $O(n \\log n)$ 时间内求解"
        "（暴力双重循环是 $O(n^2)$，会超时）。",
        "第一行一个整数 $n$（$1 \\le n \\le 2 \\times 10^5$）。\n\n第二行 $n$ 个整数 $a_i$（$|a_i| \\le 10^9$）。",
        "一行一个整数，表示逆序对总数。\n\n**注意**：答案可能超过 32 位整数范围，请使用 `long long`。",
        ["1 ≤ n ≤ 2×10^5", "|a_i| ≤ 10^9", "答案可能超过 int 范围"],
        [
            {"input": "5\n2 4 1 3 5\n", "output": "3\n",
             "explain": "逆序对为 (2,1)、(4,1)、(4,3)，共 3 个。"},
            {"input": "4\n1 2 3 4\n", "output": "0\n", "explain": "已升序，不存在逆序对。"},
            {"input": "4\n4 3 2 1\n", "output": "6\n",
             "explain": "完全逆序时逆序对最多，为 n(n-1)/2 = 6。"},
        ],
        "**核心观察**：在归并排序「合并两个有序子数组」的过程中，"
        "当右半部分的元素 $a_j$ 被取出时，左半部分中**尚未取出的**所有元素都比 $a_j$ 大，"
        "它们都与 $a_j$ 构成逆序对。\n\n"
        "因此在合并时累加 `mid - i + 1`（左半剩余元素个数）即可。\n\n"
        "总复杂度与归并排序相同：$O(n \\log n)$。",
        "#include <cstdio>\n#include <vector>\n\n"
        "long long mergeCount(std::vector<long long>& a, std::vector<long long>& tmp, int l, int r) {\n"
        "    // TODO: 归并排序并统计逆序对\n    return 0;\n}\n\n"
        "int main() {\n"
        "    int n;\n    scanf(\"%d\", &n);\n"
        "    std::vector<long long> a(n);\n"
        "    for (int i = 0; i < n; ++i) scanf(\"%lld\", &a[i]);\n\n"
        "    std::vector<long long> tmp(n);\n"
        "    printf(\"%lld\\n\", mergeCount(a, tmp, 0, n - 1));\n"
        "    return 0;\n}\n",
        "#include <cstdio>\n#include <vector>\n\n"
        "long long mergeCount(std::vector<long long>& a, std::vector<long long>& tmp, int l, int r) {\n"
        "    if (l >= r) return 0;\n"
        "    int mid = l + (r - l) / 2;\n"
        "    long long cnt = mergeCount(a, tmp, l, mid) + mergeCount(a, tmp, mid + 1, r);\n\n"
        "    int i = l, j = mid + 1, k = l;\n"
        "    while (i <= mid && j <= r) {\n"
        "        if (a[i] <= a[j]) tmp[k++] = a[i++];\n"
        "        else {\n"
        "            tmp[k++] = a[j++];\n"
        "            cnt += mid - i + 1;   // 左半剩余元素都与 a[j] 构成逆序对\n"
        "        }\n"
        "    }\n"
        "    while (i <= mid) tmp[k++] = a[i++];\n"
        "    while (j <= r) tmp[k++] = a[j++];\n"
        "    for (int t = l; t <= r; ++t) a[t] = tmp[t];\n"
        "    return cnt;\n}\n\n"
        "int main() {\n"
        "    int n;\n    scanf(\"%d\", &n);\n"
        "    std::vector<long long> a(n);\n"
        "    for (int i = 0; i < n; ++i) scanf(\"%lld\", &a[i]);\n\n"
        "    std::vector<long long> tmp(n);\n"
        "    printf(\"%lld\\n\", mergeCount(a, tmp, 0, n - 1));\n"
        "    return 0;\n}\n",
        tests,
    )


def build_binary_search() -> dict:
    tests = build_tests(BINARY_SPECS, solve_binary_search)
    return _mk(
        "search-binary", "二分查找（返回下标）", "入门",
        ["查找", "二分查找"],
        {"name": "LeetCode 704", "url": "https://leetcode.cn/problems/binary-search/"},
        "给定一个**升序**排列的长度为 $n$ 的数组 $a$ 和 $q$ 次查询，"
        "每次查询一个整数 $x$，请输出 $x$ 在数组中的**下标**（从 $0$ 开始计数）。\n\n"
        "若数组中不存在 $x$，输出 $-1$。\n\n"
        "要求每次查询使用**二分查找**，复杂度 $O(\\log n)$。",
        "第一行两个整数 $n, q$（$1 \\le n \\le 10^5$，$1 \\le q \\le 10^5$）。\n\n"
        "第二行 $n$ 个**升序**整数 $a_i$。\n\n"
        "第三行 $q$ 个整数，为查询的 $x$。",
        "共 $q$ 行，每行一个整数，表示对应查询的答案（不存在则 $-1$）。",
        ["1 ≤ n, q ≤ 10^5", "|a_i|, |x| ≤ 10^9", "数组升序"],
        [
            {"input": "5 3\n1 3 5 7 9\n3 5 10\n", "output": "1\n2\n-1\n",
             "explain": "3 在下标 1，5 在下标 2；10 不存在，输出 -1。"},
            {"input": "3 2\n1 2 3\n0 4\n", "output": "-1\n-1\n",
             "explain": "0 和 4 都不在数组中。"},
        ],
        "**标准二分**：维护闭区间 `[lo, hi]`，每次取 `mid = (lo + hi) / 2`：\n\n"
        "- `a[mid] == x` → 找到；\n"
        "- `a[mid] < x` → 答案在右半，`lo = mid + 1`；\n"
        "- `a[mid] > x` → 答案在左半，`hi = mid - 1`。\n\n"
        "注意 `mid` 用 `lo + (hi - lo) / 2` 可避免两数相加溢出。",
        "#include <cstdio>\n#include <vector>\n\n"
        "int main() {\n"
        "    int n, q;\n    scanf(\"%d %d\", &n, &q);\n"
        "    std::vector<long long> a(n);\n"
        "    for (int i = 0; i < n; ++i) scanf(\"%lld\", &a[i]);\n\n"
        "    for (int t = 0; t < q; ++t) {\n"
        "        long long x;\n        scanf(\"%lld\", &x);\n"
        "        // TODO: 二分查找并输出下标\n"
        "    }\n    return 0;\n}\n",
        "#include <cstdio>\n#include <vector>\n\n"
        "int main() {\n"
        "    int n, q;\n    scanf(\"%d %d\", &n, &q);\n"
        "    std::vector<long long> a(n);\n"
        "    for (int i = 0; i < n; ++i) scanf(\"%lld\", &a[i]);\n\n"
        "    for (int t = 0; t < q; ++t) {\n"
        "        long long x;\n        scanf(\"%lld\", &x);\n"
        "        int lo = 0, hi = n - 1, ans = -1;\n"
        "        while (lo <= hi) {\n"
        "            int mid = lo + (hi - lo) / 2;\n"
        "            if (a[mid] == x) { ans = mid; break; }\n"
        "            else if (a[mid] < x) lo = mid + 1;\n"
        "            else hi = mid - 1;\n"
        "        }\n"
        "        printf(\"%d\\n\", ans);\n"
        "    }\n    return 0;\n}\n",
        tests,
    )


def build_lower_bound() -> dict:
    tests = build_tests(LOWER_BOUND_SPECS, solve_lower_bound)
    return _mk(
        "search-lower-bound", "查找首个不小于 x 的位置", "中等",
        ["查找", "二分查找", "下界"],
        {"name": "LeetCode 35 / STL lower_bound", "url": "https://leetcode.cn/problems/search-insert-position/"},
        "给定一个**非递减**排列的数组 $a$ 和 $q$ 次查询，每次查询整数 $x$。\n\n"
        "请输出数组中**第一个大于或等于 $x$ 的元素的位置**（从 $1$ 开始计数）。\n\n"
        "若数组中所有元素都小于 $x$，输出 $0$ 表示不存在。\n\n"
        "该位置也等价于「把 $x$ 插入数组后仍保持非递减，它应占据的下标 $+1$」。",
        "第一行两个整数 $n, q$（$1 \\le n \\le 10^5$，$1 \\le q \\le 10^5$）。\n\n"
        "第二行 $n$ 个**非递减**整数 $a_i$。\n\n"
        "第三行 $q$ 个整数，为查询的 $x$。",
        "共 $q$ 行，每行一个整数，表示首个 $\\ge x$ 的元素位置（$1$ 开始）；不存在则输出 $0$。",
        ["1 ≤ n, q ≤ 10^5", "|a_i|, |x| ≤ 10^9", "数组非递减（可含重复）"],
        [
            {"input": "5 3\n1 3 5 7 9\n3 4 10\n", "output": "2\n4\n0\n",
             "explain": "$\\ge 3$ 的首个位置是 2（值为 3）；$\\ge 4$ 的是 4（值为 5）；$\\ge 10$ 的没有，输出 0。"},
            {"input": "3 1\n5 6 7\n1\n", "output": "1\n",
             "explain": "所有元素都 $\\ge 1$，首个位置是 1。"},
        ],
        "这是二分的经典变体。注意**不要**在 `a[mid] == x` 时直接返回——"
        "因为可能有更靠前的相等元素。\n\n"
        "正确区间：`ans = n+1`（哨兵）；当 `a[mid] >= x` 时记录 `ans = mid` 并 `hi = mid - 1`；"
        "否则 `lo = mid + 1`。循环结束后若 `ans == n+1` 则输出 0。\n\n"
        "C++ 中也可直接用 `std::lower_bound(a.begin(), a.end(), x)`。",
        "#include <cstdio>\n#include <vector>\n\n"
        "int main() {\n"
        "    int n, q;\n    scanf(\"%d %d\", &n, &q);\n"
        "    std::vector<long long> a(n);\n"
        "    for (int i = 0; i < n; ++i) scanf(\"%lld\", &a[i]);\n\n"
        "    for (int t = 0; t < q; ++t) {\n"
        "        long long x;\n        scanf(\"%lld\", &x);\n"
        "        // TODO: 求首个 >= x 的位置\n"
        "    }\n    return 0;\n}\n",
        "#include <cstdio>\n#include <vector>\n#include <algorithm>\n\n"
        "int main() {\n"
        "    int n, q;\n    scanf(\"%d %d\", &n, &q);\n"
        "    std::vector<long long> a(n);\n"
        "    for (int i = 0; i < n; ++i) scanf(\"%lld\", &a[i]);\n\n"
        "    for (int t = 0; t < q; ++t) {\n"
        "        long long x;\n        scanf(\"%lld\", &x);\n"
        "        int pos = (int)(std::lower_bound(a.begin(), a.end(), x) - a.begin());\n"
        "        printf(\"%d\\n\", pos < n ? pos + 1 : 0);\n"
        "    }\n    return 0;\n}\n",
        tests,
    )


def main() -> None:
    graph = [build_components, build_bfs_shortest, build_topological]
    sortq = [build_quicksort, build_inversion_count, build_binary_search, build_lower_bound]

    for b in graph:
        prob = b()
        path = finalize(prob, OUT_GRAPH / f"{prob['id']}.json")
        total = sum(t["score"] for t in prob["tests"])
        print(f"[图] {prob['id']:32s} {len(prob['tests'])} 点, 总分 {total}  -> {path.name}")

    for b in sortq:
        prob = b()
        path = finalize(prob, OUT_SORT / f"{prob['id']}.json")
        total = sum(t["score"] for t in prob["tests"])
        print(f"[排序] {prob['id']:30s} {len(prob['tests'])} 点, 总分 {total}  -> {path.name}")


if __name__ == "__main__":
    main()
