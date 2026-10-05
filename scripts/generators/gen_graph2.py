"""生成「图论基础」分类的第二批题目。"""
from __future__ import annotations

import heapq
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from genkit import build_tests, finalize  # noqa: E402

OUT = ROOT / "oj" / "data" / "problems" / "06-graph"


def _lines(text: str):
    return text.strip("\n").split("\n")


# ============================================================ 1. Dijkstra 最短路
def solve_dijkstra(text: str) -> str:
    """堆优化 Dijkstra，非负边权。"""
    ls = _lines(text)
    n, m = map(int, ls[0].split())
    g = [[] for _ in range(n + 1)]
    for i in range(1, m + 1):
        u, v, w = map(int, ls[i].split())
        g[u].append((v, w))
        g[v].append((u, w))          # 无向图
    s, t = map(int, ls[m + 1].split())

    INF = float("inf")
    dist = [INF] * (n + 1)
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in g[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return f"{dist[t]}\n" if dist[t] != INF else "-1\n"


DJ_SPECS = [
    ("样例 1", "5 6\n1 2 2\n1 3 4\n2 3 1\n2 4 7\n3 5 3\n4 5 1\n1 5", 10),
    ("样例 2（不连通）", "4 2\n1 2 5\n3 4 1\n1 4", 10),
    ("单点", "1 0\n1 1", 10),
    ("直达最短路", "2 1\n1 2 7\n1 2", 15),
    ("两点多路径", "3 3\n1 2 10\n2 3 10\n1 3 15\n1 3", 15),
    ("链状图", "4 3\n1 2 1\n2 3 1\n3 4 1\n1 4", 20),
    ("含 0 权边", "3 3\n1 2 0\n2 3 0\n1 3 5\n1 3", 20),
]


def build_dijkstra() -> dict:
    tests = build_tests(DJ_SPECS, solve_dijkstra)
    return {
        "id": "graph-dijkstra",
        "title": "单源最短路径（Dijkstra）",
        "difficulty": "中等",
        "tags": ["图", "最短路", "Dijkstra", "优先队列"],
        "source": {
            "name": "经典最短路算法 / 洛谷 P4779",
            "url": "https://www.luogu.com.cn/problem/P4779",
        },
        "statement": (
            "给定一个 $n$ 个点、$m$ 条边的**无向连通图**（边权非负），求从起点 $s$ 到终点 $t$ 的"
            "**最短路径长度**。\n\n"
            "若 $s$ 无法到达 $t$，输出 $-1$。\n\n"
            "**要求：时间复杂度 $O((n+m)\\log n)$**，即堆优化的 Dijkstra。"
        ),
        "input_format": (
            "第一行两个整数 $n, m$（$1 \\le n \\le 10^5$，$0 \\le m \\le 2 \\times 10^5$）。\n\n"
            "接下来 $m$ 行，每行三个整数 $u, v, w$，表示 $u$ 与 $v$ 之间有一条长度为 $w$ 的边"
            "（$0 \\le w \\le 10^4$）。\n\n"
            "最后一行两个整数 $s, t$（$1 \\le s, t \\le n$），为起点与终点。"
        ),
        "output_format": "一行一个整数，表示 $s$ 到 $t$ 的最短距离；若不可达则输出 $-1$。",
        "constraints": ["1 ≤ n ≤ 10^5", "0 ≤ m ≤ 2×10^5", "0 ≤ w ≤ 10^4", "无向图，边权非负"],
        "samples": [
            {"input": "5 6\n1 2 2\n1 3 4\n2 3 1\n2 4 7\n3 5 3\n4 5 1\n1 5\n", "output": "6\n",
             "explain": "路径 1→2→3→5 总长为 2+1+3=6，比 1→3→5（4+3=7）更短。"},
            {"input": "4 2\n1 2 5\n3 4 1\n1 4\n", "output": "-1\n",
             "explain": "1 所在的连通分量是 {1,2}，无法到达 4。"},
        ],
        "hint": (
            "**堆优化的 Dijkstra**：\n\n"
            "1. `dist[]` 全部初始化为 $\\infty$，`dist[s] = 0`；\n"
            "2. 用**小根堆**存 `(距离, 顶点)`，初始放入 `(0, s)`；\n"
            "3. 每次弹出堆顶 `(d, u)`：**若 `d > dist[u]` 说明是过期条目，直接跳过**"
            "（这叫「惰性删除」）；\n"
            "4. 否则遍历 `u` 的邻居 `v`，若 `dist[u] + w < dist[v]` 就松弛并压入新条目。\n\n"
            "每条边最多引起一次成功松弛，每次堆操作 $O(\\log n)$，"
            "因此总复杂度 $O((n+m)\\log n)$。\n\n"
            "> **两个关键点**：\n"
            "> 1. **边权必须非负**，否则 Dijkstra 的正确性不成立（有负权要用 Bellman-Ford / SPFA）；\n"
            "> 2. **必须跳过过期条目**（第 3 步），否则复杂度会退化。"
        ),
        "starter_code": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <vector>\n"
                "#include <queue>\n\n"
                "const long long INF = 4e18;\n\n"
                "int main() {\n"
                "    int n, m;\n"
                "    scanf(\"%d %d\", &n, &m);\n"
                "    std::vector<std::vector<std::pair<int,int>>> g(n + 1);\n"
                "    for (int i = 0; i < m; ++i) {\n"
                "        int u, v, w;\n"
                "        scanf(\"%d %d %d\", &u, &v, &w);\n"
                "        g[u].push_back({v, w});\n"
                "        g[v].push_back({u, w});\n"
                "    }\n"
                "    int s, t;\n"
                "    scanf(\"%d %d\", &s, &t);\n\n"
                "    // TODO: 堆优化 Dijkstra\n"
                "    long long ans = -1;\n\n"
                "    printf(\"%lld\\n\", ans);\n"
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
                "const long long INF = 4e18;\n\n"
                "int main() {\n"
                "    int n, m;\n"
                "    scanf(\"%d %d\", &n, &m);\n"
                "    std::vector<std::vector<std::pair<int,int>>> g(n + 1);\n"
                "    for (int i = 0; i < m; ++i) {\n"
                "        int u, v, w;\n"
                "        scanf(\"%d %d %d\", &u, &v, &w);\n"
                "        g[u].push_back({v, w});\n"
                "        g[v].push_back({u, w});\n"
                "    }\n"
                "    int s, t;\n"
                "    scanf(\"%d %d\", &s, &t);\n\n"
                "    std::vector<long long> dist(n + 1, INF);\n"
                "    dist[s] = 0;\n"
                "    using P = std::pair<long long,int>;\n"
                "    std::priority_queue<P, std::vector<P>, std::greater<P>> pq;\n"
                "    pq.push({0, s});\n\n"
                "    while (!pq.empty()) {\n"
                "        auto [d, u] = pq.top(); pq.pop();\n"
                "        if (d > dist[u]) continue;            // 过期条目，跳过\n"
                "        for (auto [v, w] : g[u]) {\n"
                "            long long nd = d + w;\n"
                "            if (nd < dist[v]) {\n"
                "                dist[v] = nd;\n"
                "                pq.push({nd, v});\n"
                "            }\n"
                "        }\n"
                "    }\n"
                "    printf(\"%lld\\n\", dist[t] == INF ? -1LL : dist[t]);\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "time_limit": 2.0,
    }


# ============================================================ 2. 二分图判定
def solve_bipartite(text: str) -> str:
    """BFS 染色，相邻点必须异色。"""
    ls = _lines(text)
    n, m = map(int, ls[0].split())
    g = [[] for _ in range(n + 1)]
    for i in range(1, m + 1):
        u, v = map(int, ls[i].split())
        g[u].append(v)
        g[v].append(u)
    color = [-1] * (n + 1)
    for st in range(1, n + 1):
        if color[st] != -1:
            continue
        color[st] = 0
        q = deque([st])
        while q:
            u = q.popleft()
            for v in g[u]:
                if color[v] == -1:
                    color[v] = color[u] ^ 1
                    q.append(v)
                elif color[v] == color[u]:
                    return "NO\n"
    return "YES\n"


BP_SPECS = [
    ("样例 1（是二分图）", "4 4\n1 2\n1 3\n4 2\n4 3", 10),
    ("样例 2（奇环）", "3 3\n1 2\n2 3\n3 1", 10),
    ("单点无边", "1 0", 10),
    ("两个孤立点", "2 0", 15),
    ("偶环", "4 4\n1 2\n2 3\n3 4\n4 1", 15),
    ("不连通且都二分", "6 2\n1 2\n4 5", 20),
    ("不连通有一块非二分", "6 4\n1 2\n3 4\n4 5\n5 3", 20),
]


def build_bipartite() -> dict:
    tests = build_tests(BP_SPECS, solve_bipartite)
    return {
        "id": "graph-bipartite",
        "title": "二分图判定",
        "difficulty": "中等",
        "tags": ["图", "BFS", "染色", "二分图"],
        "source": {
            "name": "LeetCode 785 / 染色法",
            "url": "https://leetcode.cn/problems/is-graph-bipartite/",
        },
        "statement": (
            "给定一个 $n$ 个点、$m$ 条边的**无向图**，判断它是否为**二分图**。\n\n"
            "**二分图**的定义：可以把顶点分成两个互不相交的集合，"
            "使得**每条边的两个端点都分属不同集合**。\n\n"
            "等价说法：图中**不存在长度为奇数的环**。\n\n"
            "是二分图输出 `YES`，否则输出 `NO`。"
        ),
        "input_format": (
            "第一行两个整数 $n, m$（$1 \\le n \\le 10^5$，$0 \\le m \\le 2 \\times 10^5$）。\n\n"
            "接下来 $m$ 行，每行两个整数 $u, v$，表示 $u$ 与 $v$ 之间有一条边。\n\n"
            "**图不一定连通**。"
        ),
        "output_format": "一行，输出 `YES` 或 `NO`。",
        "constraints": ["1 ≤ n ≤ 10^5", "0 ≤ m ≤ 2×10^5", "无向图，可能不连通", "无自环"],
        "samples": [
            {"input": "4 4\n1 2\n1 3\n4 2\n4 3\n", "output": "YES\n",
             "explain": "可以把 {1,4} 染成一色、{2,3} 染成另一色，每条边两端异色。"},
            {"input": "3 3\n1 2\n2 3\n3 1\n", "output": "NO\n",
             "explain": "存在长度为 3 的奇环，无法二分染色。"},
        ],
        "hint": (
            "**染色法（BFS 或 DFS）**：给每个顶点染上 0 或 1 两种颜色。\n\n"
            "从任意未染色的点出发染 0，然后 BFS：对每个邻居，"
            "若它**未染色**就染成相反色并入队；若**已染色且与当前点同色**，"
            "说明存在冲突，立即判定不是二分图。\n\n"
            "**关键**：外层要遍历**所有**顶点，对每个未染色的连通分量都发起一次 BFS，"
            "因为图不一定连通。\n\n"
            "时间 $O(n+m)$，空间 $O(n+m)$。\n\n"
            "> **易错点**：只从 1 号点开始 BFS 会漏掉其他连通分量中的奇环。"
        ),
        "starter_code": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <vector>\n"
                "#include <queue>\n\n"
                "int main() {\n"
                "    int n, m;\n"
                "    scanf(\"%d %d\", &n, &m);\n"
                "    std::vector<std::vector<int>> g(n + 1);\n"
                "    for (int i = 0; i < m; ++i) {\n"
                "        int u, v;\n"
                "        scanf(\"%d %d\", &u, &v);\n"
                "        g[u].push_back(v);\n"
                "        g[v].push_back(u);\n"
                "    }\n\n"
                "    std::vector<int> color(n + 1, -1);\n"
                "    // TODO: 遍历所有顶点，对每个未染色分量做 BFS 染色\n"
                "    bool ok = true;\n\n"
                "    printf(\"%s\\n\", ok ? \"YES\" : \"NO\");\n"
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
                "    int n, m;\n"
                "    scanf(\"%d %d\", &n, &m);\n"
                "    std::vector<std::vector<int>> g(n + 1);\n"
                "    for (int i = 0; i < m; ++i) {\n"
                "        int u, v;\n"
                "        scanf(\"%d %d\", &u, &v);\n"
                "        g[u].push_back(v);\n"
                "        g[v].push_back(u);\n"
                "    }\n\n"
                "    std::vector<int> color(n + 1, -1);\n"
                "    bool ok = true;\n"
                "    for (int st = 1; st <= n && ok; ++st) {\n"
                "        if (color[st] != -1) continue;        // 已属于某个分量\n"
                "        color[st] = 0;\n"
                "        std::queue<int> q;\n"
                "        q.push(st);\n"
                "        while (!q.empty() && ok) {\n"
                "            int u = q.front(); q.pop();\n"
                "            for (int v : g[u]) {\n"
                "                if (color[v] == -1) {\n"
                "                    color[v] = color[u] ^ 1;   // 异色\n"
                "                    q.push(v);\n"
                "                } else if (color[v] == color[u]) {\n"
                "                    ok = false; break;         // 同色冲突\n"
                "                }\n"
                "            }\n"
                "        }\n"
                "    }\n"
                "    printf(\"%s\\n\", ok ? \"YES\" : \"NO\");\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "time_limit": 2.0,
    }


# ============================================================ 3. 岛屿数量
def solve_islands(text: str) -> str:
    """网格 DFS，把访问过的陆地沉掉。"""
    ls = _lines(text)
    rows, cols = map(int, ls[0].split())
    grid = [list(ls[i + 1]) for i in range(rows)]

    def dfs(x, y):
        if x < 0 or x >= rows or y < 0 or y >= cols or grid[x][y] != "1":
            return
        grid[x][y] = "0"
        dfs(x + 1, y)
        dfs(x - 1, y)
        dfs(x, y + 1)
        dfs(x, y - 1)

    cnt = 0
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == "1":
                cnt += 1
                dfs(i, j)
    return f"{cnt}\n"


IS_SPECS = [
    ("样例 1", "4 5\n11110\n11010\n11000\n00000", 10),
    ("样例 2（三个岛）", "4 5\n11000\n11000\n00100\n00011", 10),
    ("全水", "2 3\n000\n000", 10),
    ("全陆", "2 2\n11\n11", 15),
    ("对角不算连通", "2 2\n10\n01", 15),
    ("单行", "1 5\n10101", 20),
    ("单列", "5 1\n1\n0\n1\n0\n1", 20),
]


def build_islands() -> dict:
    tests = build_tests(IS_SPECS, solve_islands)
    return {
        "id": "graph-grid-islands",
        "title": "岛屿数量",
        "difficulty": "中等",
        "tags": ["图", "DFS", "网格", "连通块"],
        "source": {
            "name": "LeetCode 200 / 网格 DFS",
            "url": "https://leetcode.cn/problems/number-of-islands/",
        },
        "statement": (
            "给定一个由 `'1'`（陆地）和 `'0'`（水）组成的二维网格，计算其中**岛屿的数量**。\n\n"
            "**岛屿**由水平或垂直方向上相邻的陆地连接而成，"
            "即上下左右四个方向连通（**对角线不算连通**）。\n\n"
            "可以认为网格的四条边之外都是水。"
        ),
        "input_format": (
            "第一行两个整数 $rows, cols$（$1 \\le rows, cols \\le 1000$）。\n\n"
            "接下来 $rows$ 行，每行一个长度为 $cols$ 的字符串，仅由 `0` 和 `1` 组成。"
        ),
        "output_format": "一行一个整数，表示岛屿数量。",
        "constraints": ["1 ≤ rows, cols ≤ 1000", "网格仅含 0 和 1", "上下左右连通，对角不算"],
        "samples": [
            {"input": "4 5\n11110\n11010\n11000\n00000\n", "output": "1\n",
             "explain": "所有陆地通过上下左右连通成一片，只有 1 个岛屿。"},
            {"input": "4 5\n11000\n11000\n00100\n00011\n", "output": "3\n",
             "explain": "左上 2×2 一块、中间单独一块、右下两块相邻成一块，共 3 个岛屿。"},
        ],
        "hint": (
            "**把网格看作图，用 DFS/BFS 数连通块**：\n\n"
            "遍历每个格子，遇到 `'1'` 就把岛屿数加一，然后从它出发做一次 DFS，"
            "把**与之相连的所有陆地都标记为已访问**（可以直接原地改成 `'0'`，省一个 visited 数组）。\n\n"
            "DFS 时用方向数组统一处理四个方向：\n"
            "```\n"
            "const int dx[4] = {1, -1, 0, 0};\n"
            "const int dy[4] = {0, 0, 1, -1};\n"
            "```\n\n"
            "时间 $O(rows \\times cols)$，每个格子最多被访问一次。\n\n"
            "> **两个易错点**：\n"
            "> 1. **边界检查必须写全**（`0 <= nx < rows && 0 <= ny < cols`），否则越界；\n"
            "> 2. 网格较大（$10^6$ 格）时**递归 DFS 可能爆栈**，"
            "建议改用显式栈或 BFS 队列。"
        ),
        "starter_code": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <vector>\n"
                "#include <string>\n"
                "#include <iostream>\n\n"
                "int rows, cols;\n"
                "std::vector<std::string> grid;\n\n"
                "// TODO: 写一个 DFS，把与 (x,y) 相连的陆地全部沉掉\n\n"
                "int main() {\n"
                "    scanf(\"%d %d\", &rows, &cols);\n"
                "    grid.resize(rows);\n"
                "    for (int i = 0; i < rows; ++i) std::cin >> grid[i];\n\n"
                "    int cnt = 0;\n"
                "    // TODO\n\n"
                "    printf(\"%d\\n\", cnt);\n"
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
                "#include <stack>\n"
                "#include <iostream>\n\n"
                "int main() {\n"
                "    int rows, cols;\n"
                "    scanf(\"%d %d\", &rows, &cols);\n"
                "    std::vector<std::string> grid(rows);\n"
                "    for (int i = 0; i < rows; ++i) std::cin >> grid[i];\n\n"
                "    const int dx[4] = {1, -1, 0, 0};\n"
                "    const int dy[4] = {0, 0, 1, -1};\n"
                "    int cnt = 0;\n\n"
                "    for (int i = 0; i < rows; ++i) {\n"
                "        for (int j = 0; j < cols; ++j) {\n"
                "            if (grid[i][j] != '1') continue;\n"
                "            ++cnt;\n"
                "            // 显式栈 DFS，避免大网格递归爆栈\n"
                "            std::stack<std::pair<int,int>> st;\n"
                "            grid[i][j] = '0';\n"
                "            st.push({i, j});\n"
                "            while (!st.empty()) {\n"
                "                auto [x, y] = st.top(); st.pop();\n"
                "                for (int d = 0; d < 4; ++d) {\n"
                "                    int nx = x + dx[d], ny = y + dy[d];\n"
                "                    if (nx < 0 || nx >= rows || ny < 0 || ny >= cols) continue;\n"
                "                    if (grid[nx][ny] != '1') continue;\n"
                "                    grid[nx][ny] = '0';\n"
                "                    st.push({nx, ny});\n"
                "                }\n"
                "            }\n"
                "        }\n"
                "    }\n"
                "    printf(\"%d\\n\", cnt);\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "time_limit": 2.0,
    }


def main() -> None:
    builders = [build_dijkstra, build_bipartite, build_islands]
    for b in builders:
        prob = b()
        path = finalize(prob, OUT / f"{prob['id']}.json")
        total = sum(t["score"] for t in prob["tests"])
        print(f"生成 {prob['id']:26s} {len(prob['tests'])} 测试点, 总分 {total:3d}  -> {path.name}")


if __name__ == "__main__":
    main()
