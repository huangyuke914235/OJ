"""图论基础 · 批量 G1（16 道）。"""
from __future__ import annotations

import heapq
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from genkit import CPP_HEADER, finalize, problem  # noqa: E402

OUT = ROOT / "oj" / "data" / "problems" / "06-graph"
P: list = []


def add(**kw):
    P.append(problem(**kw))


def L(t):
    return t.strip("\n").split("\n")


def read_graph(t, directed=False):
    ls = L(t)
    n, m = map(int, ls[0].split())
    g = [[] for _ in range(n + 1)]
    edges = []
    for i in range(1, m + 1):
        u, v = map(int, ls[i].split())
        g[u].append(v)
        if not directed:
            g[v].append(u)
        edges.append((u, v))
    return n, m, g, edges, ls


# ---------------------------------------------------------------- 1
def s_degree(t):
    n, m, g, edges, ls = read_graph(t)
    deg = [len(g[i]) for i in range(1, n + 1)]
    return " ".join(map(str, deg)) + "\n"


add(
    pid="graph-degree-count", title="统计各顶点的度数", difficulty="入门",
    tags=["图", "邻接表"], source="图论基础", url="https://leetcode.cn/problems/find-center-of-star-graph/",
    statement="给定一个**无向图**，输出每个顶点的**度数**（与该顶点相连的边数）。\n\n顶点编号 $1 \\sim n$，输出顺序按编号升序。\n\n**注意**：自环（$u = v$）对度数的贡献为 2。",
    input_format="第一行两个整数 $n, m$（$1 \\le n \\le 10^5$，$0 \\le m \\le 2\\times10^5$）。\n\n接下来 $m$ 行，每行两个整数 $u, v$（$1 \\le u, v \\le n$），表示一条无向边。",
    output_format="一行 $n$ 个整数，依次为各顶点的度数。",
    constraints=["1 ≤ n ≤ 10^5", "0 ≤ m ≤ 2×10^5", "可能有自环", "无重边"],
    solver=s_degree,
    specs=[("样例 1", "4 3\n1 2\n2 3\n3 4", 10), ("无边", "3 0", 10),
           ("自环", "2 1\n1 1", 15), ("完全图", "3 3\n1 2\n2 3\n1 3", 15),
           ("星形", "4 3\n1 2\n1 3\n1 4", 20), ("单点自环", "1 1\n1 1", 20),
           ("重边已排除", "5 4\n1 2\n1 3\n1 4\n1 5", 20)],
    cpp=CPP_HEADER + """int main(){int n,m;scanf("%d %d",&n,&m);vector<int>d(n+1,0);
for(int i=0;i<m;++i){int u,v;scanf("%d %d",&u,&v);
if(u==v)d[u]+=2;else{++d[u];++d[v];}}
for(int i=1;i<=n;++i){if(i>1)printf(" ");printf("%d",d[i]);}
printf("\\n");return 0;}
""",
    hint="**无向图度数**：每条边 $(u,v)$ 给 $u$ 和 $v$ 各贡献 1 度。\n\n> **易错点**：自环 $(u,u)$ 在无向图中对度数的贡献是 **2**（既算作出发也算作到达），不能只加 1。",
)

# ---------------------------------------------------------------- 2
def s_dfs_order(t):
    n, m, g, edges, ls = read_graph(t)
    start = int(ls[m + 1])
    for i in range(1, n + 1):
        g[i].sort()
    seen = [False] * (n + 1)
    order = []
    st = [start]
    while st:
        u = st.pop()
        if seen[u]:
            continue
        seen[u] = True
        order.append(u)
        for v in reversed(g[u]):
            if not seen[v]:
                st.append(v)
    return " ".join(map(str, order)) + "\n"


add(
    pid="graph-dfs-order", title="图的深度优先遍历", difficulty="入门",
    tags=["图", "DFS", "邻接表"], source="图论基础", url="https://leetcode.cn/problems/find-if-path-exists-in-graph/",
    statement="从起点 $s$ 出发，对无向图做**深度优先遍历**，输出访问顺序。\n\n**约定**：每个顶点有多个未访问邻居时，**按编号从小到大**优先访问（用栈实现时要注意入栈顺序）。\n\n只输出从 $s$ 能到达的顶点。",
    input_format="第一行两个整数 $n, m$（$1 \\le n \\le 10^5$，$0 \\le m \\le 2\\times10^5$）。\n\n接下来 $m$ 行，每行两个整数 $u, v$。\n\n最后一行一个整数 $s$，为起点。",
    output_format="一行，DFS 访问顺序，以空格分隔。",
    constraints=["1 ≤ n ≤ 10^5", "0 ≤ m ≤ 2×10^5", "邻居按编号升序优先"],
    solver=s_dfs_order,
    specs=[("样例 1", "4 3\n1 2\n2 3\n3 4\n1", 10), ("单点", "1 0\n1", 10),
           ("孤立点", "3 1\n1 2\n3", 15), ("星形", "4 3\n1 2\n1 3\n1 4\n1", 15),
           ("完全图", "4 6\n1 2\n1 3\n1 4\n2 3\n2 4\n3 4\n1", 20),
           ("链状", "5 4\n1 2\n2 3\n3 4\n4 5\n1", 20),
           ("多分支", "6 5\n1 2\n1 3\n2 4\n2 5\n3 6\n1", 20)],
    cpp=CPP_HEADER + """int main(){int n,m;scanf("%d %d",&n,&m);
vector<vector<int>>g(n+1);
for(int i=0;i<m;++i){int u,v;scanf("%d %d",&u,&v);
g[u].push_back(v);g[v].push_back(u);}
int s;scanf("%d",&s);
for(int i=1;i<=n;++i)sort(g[i].begin(),g[i].end());
vector<bool>vis(n+1,false);vector<int>order;vector<int>st;st.push_back(s);
while(!st.empty()){int u=st.back();st.pop_back();
if(vis[u])continue;vis[u]=true;order.push_back(u);
for(int i=(int)g[u].size()-1;i>=0;--i)if(!vis[g[u][i]])st.push_back(g[u][i]);}
for(size_t i=0;i<order.size();++i){if(i)printf(" ");printf("%d",order[i]);}
printf("\\n");return 0;}
""",
    hint="**用栈实现 DFS**：弹出栈顶就访问它，然后把它**所有未访问的邻居按倒序压栈**——这样最小的邻居会最先出栈。\n\n> **易错点**：入栈前先排序邻居，并且要**倒序入栈**，才能保证出栈时是从小到大。",
)

# ---------------------------------------------------------------- 3
def s_bfs_order(t):
    n, m, g, edges, ls = read_graph(t)
    start = int(ls[m + 1])
    for i in range(1, n + 1):
        g[i].sort()
    seen = [False] * (n + 1)
    order = []
    q = deque([start])
    seen[start] = True
    while q:
        u = q.popleft()
        order.append(u)
        for v in g[u]:
            if not seen[v]:
                seen[v] = True
                q.append(v)
    return " ".join(map(str, order)) + "\n"


add(
    pid="graph-bfs-order", title="图的广度优先遍历", difficulty="入门",
    tags=["图", "BFS", "邻接表"], source="图论基础", url="https://leetcode.cn/problems/find-if-path-exists-in-graph/",
    statement="从起点 $s$ 出发，对无向图做**广度优先遍历**，输出访问顺序。\n\n**约定**：同一层的邻居**按编号从小到大**依次入队。\n\n只输出从 $s$ 能到达的顶点。",
    input_format="第一行两个整数 $n, m$（$1 \\le n \\le 10^5$，$0 \\le m \\le 2\\times10^5$）。\n\n接下来 $m$ 行，每行两个整数 $u, v$。\n\n最后一行一个整数 $s$。",
    output_format="一行，BFS 访问顺序。",
    constraints=["1 ≤ n ≤ 10^5", "0 ≤ m ≤ 2×10^5", "邻居按编号升序入队"],
    solver=s_bfs_order,
    specs=[("样例 1", "4 3\n1 2\n2 3\n3 4\n1", 10), ("单点", "1 0\n1", 10),
           ("孤立点", "3 1\n1 2\n3", 15), ("星形", "4 3\n1 2\n1 3\n1 4\n1", 15),
           ("完全图", "4 6\n1 2\n1 3\n1 4\n2 3\n2 4\n3 4\n1", 20),
           ("链状", "5 4\n1 2\n2 3\n3 4\n4 5\n1", 20),
           ("多分支", "6 5\n1 2\n1 3\n2 4\n2 5\n3 6\n1", 20)],
    cpp=CPP_HEADER + """int main(){int n,m;scanf("%d %d",&n,&m);
vector<vector<int>>g(n+1);
for(int i=0;i<m;++i){int u,v;scanf("%d %d",&u,&v);
g[u].push_back(v);g[v].push_back(u);}
int s;scanf("%d",&s);
for(int i=1;i<=n;++i)sort(g[i].begin(),g[i].end());
vector<bool>vis(n+1,false);queue<int>q;q.push(s);vis[s]=true;
vector<int>order;
while(!q.empty()){int u=q.front();q.pop();order.push_back(u);
for(int v:g[u])if(!vis[v]){vis[v]=true;q.push(v);}}
for(size_t i=0;i<order.size();++i){if(i)printf(" ");printf("%d",order[i]);}
printf("\\n");return 0;}
""",
    hint="**BFS 的关键**：**入队时就标记已访问**（不是出队时），否则同一节点会被多次入队。\n\n邻居先排序，就能保证同层按编号升序访问。",
)

# ---------------------------------------------------------------- 4
def s_connected_two(t):
    n, m, g, edges, ls = read_graph(t)
    a, b = map(int, ls[m + 1].split())
    seen = [False] * (n + 1)
    q = deque([a])
    seen[a] = True
    while q:
        u = q.popleft()
        if u == b:
            return "YES\n"
        for v in g[u]:
            if not seen[v]:
                seen[v] = True
                q.append(v)
    return "YES\n" if seen[b] else "NO\n"


add(
    pid="graph-connected-two", title="判断两点是否连通", difficulty="入门",
    tags=["图", "BFS", "DFS", "连通性"], source="LeetCode 1971", url="https://leetcode.cn/problems/find-if-path-exists-in-graph/",
    statement="给定无向图和两个顶点 $a, b$，判断它们是否**连通**。\n\n连通输出 `YES`，否则 `NO`。",
    input_format="第一行两个整数 $n, m$（$1 \\le n \\le 10^5$，$0 \\le m \\le 2\\times10^5$）。\n\n接下来 $m$ 行，每行两个整数 $u, v$。\n\n最后一行两个整数 $a, b$。",
    output_format="一行，输出 `YES` 或 `NO`。",
    constraints=["1 ≤ n ≤ 10^5", "0 ≤ m ≤ 2×10^5"],
    solver=s_connected_two,
    specs=[("样例 1（连通）", "3 3\n0 1\n1 2\n2 0\n0 2", 10),
           ("样例 2（不连通）", "6 5\n0 1\n0 2\n3 5\n5 4\n4 3\n0 5", 10),
           ("同一点", "1 0\n1 1", 15), ("孤立点", "3 1\n1 2\n1 3", 15),
           ("链状", "5 4\n1 2\n2 3\n3 4\n4 5\n1 5", 20),
           ("大图连通", "6 6\n1 2\n2 3\n3 4\n4 5\n5 6\n6 1\n1 4", 20),
           ("两个分量", "4 2\n1 2\n3 4\n2 3", 20)],
    cpp=CPP_HEADER + """int main(){int n,m;scanf("%d %d",&n,&m);
vector<vector<int>>g(n+1);
for(int i=0;i<m;++i){int u,v;scanf("%d %d",&u,&v);
g[u].push_back(v);g[v].push_back(u);}
int a,b;scanf("%d %d",&a,&b);
vector<bool>vis(n+1,false);queue<int>q;q.push(a);vis[a]=true;
while(!q.empty()){int u=q.front();q.pop();
for(int v:g[u])if(!vis[v]){vis[v]=true;q.push(v);}}
printf("%s\\n",vis[b]?"YES":"NO");return 0;}
""",
    hint="**从 $a$ 出发做 BFS/DFS**，看能否到达 $b$。\n\n也可以先用**并查集**把连通分量维护好，之后每次查询 $O(\\alpha(n))$。",
)

# ---------------------------------------------------------------- 5
def s_undirected_cycle(t):
    n, m, g, edges, ls = read_graph(t)
    seen = [False] * (n + 1)
    for s in range(1, n + 1):
        if seen[s]:
            continue
        stack = [(s, 0)]
        seen[s] = True
        while stack:
            u, parent = stack.pop()
            for v in g[u]:
                if not seen[v]:
                    seen[v] = True
                    stack.append((v, u))
                elif v != parent:
                    return "YES\n"
    return "NO\n"


add(
    pid="graph-has-cycle", title="无向图判环", difficulty="简单",
    tags=["图", "DFS", "判环"], source="图论基础", url="https://leetcode.cn/problems/redundant-connection/",
    statement="判断一个**无向图**中是否存在**环**。\n\n有环输出 `YES`，否则 `NO`。\n\n**注意**：图不一定连通。",
    input_format="第一行两个整数 $n, m$（$1 \\le n \\le 10^5$，$0 \\le m \\le 2\\times10^5$）。\n\n接下来 $m$ 行，每行两个整数 $u, v$（$u \\ne v$）。",
    output_format="一行，输出 `YES` 或 `NO`。",
    constraints=["1 ≤ n ≤ 10^5", "0 ≤ m ≤ 2×10^5", "无自环", "可能不连通"],
    solver=s_undirected_cycle,
    specs=[("样例 1（有环）", "3 3\n1 2\n2 3\n3 1", 10),
           ("样例 2（无环）", "4 3\n1 2\n2 3\n3 4", 10),
           ("单点", "1 0", 15), ("两个孤立点", "2 0", 15),
           ("含环且不连通", "6 4\n1 2\n2 3\n3 1\n4 5", 20),
           ("多个分量都无环", "6 3\n1 2\n3 4\n5 6", 20),
           ("偶环", "4 4\n1 2\n2 3\n3 4\n4 1", 20)],
    cpp=CPP_HEADER + """int main(){int n,m;scanf("%d %d",&n,&m);
vector<vector<int>>g(n+1);
for(int i=0;i<m;++i){int u,v;scanf("%d %d",&u,&v);
g[u].push_back(v);g[v].push_back(u);}
vector<bool>vis(n+1,false);bool cyc=false;
for(int s=1;s<=n&&!cyc;++s){
if(vis[s])continue;
vector<pair<int,int>>st;st.push_back({s,0});vis[s]=true;
while(!st.empty()&&!cyc){
auto pr=st.back();st.pop_back();
int u=pr.first,par=pr.second;
for(int v:g[u]){
if(!vis[v]){vis[v]=true;st.push_back({v,u});}
else if(v!=par){cyc=true;break;}}}}
printf("%s\\n",cyc?"YES":"NO");return 0;}
""",
    hint="**DFS 记录父节点**：遍历时若遇到**已访问且不是父节点**的邻居，说明存在环。\n\n> **易错点**：\n> 1. 必须跳过**父节点**，否则无向图的每条边都会被误判成环；\n> 2. 外层要遍历**所有**顶点，图不一定连通。\n\n> **另解**：用**并查集**——加边时若两端已属同一集合，说明成环。",
)

# ---------------------------------------------------------------- 6
def s_directed_cycle(t):
    n, m, g, edges, ls = read_graph(t, directed=True)
    color = [0] * (n + 1)     # 0=未访问 1=访问中 2=已完成
    found = [False]
    for s in range(1, n + 1):
        if color[s] or found[0]:
            continue
        st = [(s, 0)]
        color[s] = 1
        while st:
            u, idx = st.pop()
            if idx < len(g[u]):
                st.append((u, idx + 1))
                v = g[u][idx]
                if color[v] == 1:
                    found[0] = True
                    break
                if color[v] == 0:
                    color[v] = 1
                    st.append((v, 0))
            else:
                color[u] = 2
    return "YES\n" if found[0] else "NO\n"


add(
    pid="graph-directed-cycle", title="有向图判环", difficulty="中等",
    tags=["图", "DFS", "拓扑排序", "判环"], source="LeetCode 207", url="https://leetcode.cn/problems/course-schedule/",
    statement="判断一个**有向图**中是否存在**环**。\n\n有环输出 `YES`，否则 `NO`。\n\n图不一定连通。",
    input_format="第一行两个整数 $n, m$（$1 \\le n \\le 10^5$，$0 \\le m \\le 2\\times10^5$）。\n\n接下来 $m$ 行，每行两个整数 $u, v$，表示一条**从 $u$ 指向 $v$** 的有向边。",
    output_format="一行，输出 `YES` 或 `NO`。",
    constraints=["1 ≤ n ≤ 10^5", "0 ≤ m ≤ 2×10^5", "有向图", "可能不连通"],
    solver=s_directed_cycle,
    specs=[("样例 1（有环）", "3 3\n1 2\n2 3\n3 1", 10),
           ("样例 2（无环）", "4 3\n1 2\n2 3\n3 4", 10),
           ("单点", "1 0", 15), ("两条独立链", "4 2\n1 2\n3 4", 15),
           ("自环", "2 1\n1 1", 20), ("DAG", "5 4\n1 2\n1 3\n2 4\n3 5", 20),
           ("不连通含环", "6 4\n1 2\n2 3\n3 1\n4 5", 20)],
    cpp=CPP_HEADER + """int main(){int n,m;scanf("%d %d",&n,&m);
vector<vector<int>>g(n+1);
for(int i=0;i<m;++i){int u,v;scanf("%d %d",&u,&v);g[u].push_back(v);}
vector<int>color(n+1,0);bool cyc=false;
for(int s=1;s<=n&&!cyc;++s){
if(color[s])continue;
vector<pair<int,int>>st;st.push_back({s,0});color[s]=1;
while(!st.empty()&&!cyc){
auto&pr=st.back();
int u=pr.first;
if(pr.second<(int)g[u].size()){
int v=g[u][pr.second];++pr.second;
if(color[v]==1){cyc=true;break;}
if(color[v]==0){color[v]=1;st.push_back({v,0});}}
else{color[u]=2;st.pop_back();}}}
printf("%s\\n",cyc?"YES":"NO");return 0;}
""",
    hint="**三色标记 DFS**：\n\n- **白色（0）**：未访问；\n- **灰色（1）**：正在当前 DFS 栈中；\n- **黑色（2）**：已完成。\n\n若遇到一个**灰色**节点，说明它还在当前递归路径上 → 存在环。\n\n> **另解（Kahn 拓扑排序）**：不断删除入度为 0 的点，若最终删掉的点数少于 $n$，说明有环。",
)

# ---------------------------------------------------------------- 7
def s_star_center(t):
    n, m, g, edges, ls = read_graph(t)
    u1, v1 = edges[0]
    u2, v2 = edges[1]
    # 中心点必然同时出现在前两条边中
    return f"{u1 if u1 in (u2, v2) else v1}\n"


add(
    pid="graph-star-center", title="找到星形图的中心", difficulty="入门",
    tags=["图", "度数"], source="LeetCode 1791", url="https://leetcode.cn/problems/find-center-of-star-graph/",
    statement="给定一个**星形图**（存在一个中心点与其余所有点直接相连，没有其他边），找出这个**中心点**。\n\n中心点的**度数**为 $n-1$，其余点的度数都是 $1$。",
    input_format="第一行两个整数 $n, m$（$3 \\le n \\le 10^5$，$m = n-1$）。\n\n接下来 $m$ 行，每行两个整数 $u, v$。\n\n**保证**输入是星形图。",
    output_format="一行一个整数，表示中心点编号。",
    constraints=["3 ≤ n ≤ 10^5", "m = n-1", "保证是星形图"],
    solver=s_star_center,
    specs=[("样例 1", "4 3\n1 2\n2 3\n4 2", 10), ("样例 2", "3 2\n1 2\n2 3", 10),
           ("中心是 1", "5 4\n1 2\n1 3\n1 4\n1 5", 15),
           ("中心在末尾", "5 4\n1 5\n2 5\n3 5\n4 5", 15),
           ("n=3 中心 2", "3 2\n2 1\n3 2", 20),
           ("较大星形", "6 5\n6 1\n6 2\n6 3\n6 4\n6 5", 20)],
    cpp=CPP_HEADER + """int main(){int n,m;scanf("%d %d",&n,&m);
int u1,v1;scanf("%d %d",&u1,&v1);
int u2,v2;scanf("%d %d",&u2,&v2);
int c;
if(u1==u2||u1==v2)c=u1;else c=v1;
for(int i=2;i<m;++i){int a,b;scanf("%d %d",&a,&b);}
printf("%d\\n",c);return 0;}

""",
    hint="**只需看前两条边**：中心点必然同时出现在前两条边中（因为它与所有点相连）。\n\n所以取前两条边的**公共端点**即可，时间 $O(1)$（不算读入）。\n\n> 更一般地，统计度数找最大的那个也行，但没必要。",
)

# ---------------------------------------------------------------- 8
def s_flood_fill(t):
    ls = L(t)
    r, c = map(int, ls[0].split())
    g = [list(map(int, ls[i + 1].split())) for i in range(r)]
    sr, sc, color = map(int, ls[r + 1].split())
    old = g[sr][sc]
    if old != color:
        st = [(sr, sc)]
        g[sr][sc] = color
        while st:
            x, y = st.pop()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < r and 0 <= ny < c and g[nx][ny] == old:
                    g[nx][ny] = color
                    st.append((nx, ny))
    return "\n".join(" ".join(map(str, row)) for row in g) + "\n"


add(
    pid="graph-flood-fill", title="图像渲染", difficulty="简单",
    tags=["图", "DFS", "网格", "BFS"], source="LeetCode 733", url="https://leetcode.cn/problems/flood-fill/",
    statement="给定一个整数矩阵表示图像，从起点 $(sr, sc)$ 开始，把**与之连通（上下左右）且颜色相同**的所有格子都染成新颜色 $color$。\n\n输出渲染后的矩阵。",
    input_format="第一行两个整数 $r, c$（$1 \\le r, c \\le 50$）。\n\n接下来 $r$ 行，每行 $c$ 个整数（$0 \\le$ 颜色 $\\le 65535$）。\n\n最后一行三个整数 $sr, sc, color$。",
    output_format="共 $r$ 行，每行 $c$ 个整数，为渲染后的图像。",
    constraints=["1 ≤ r, c ≤ 50", "颜色值 ≤ 65535"],
    solver=s_flood_fill,
    specs=[("样例 1", "3 3\n1 1 1\n1 1 0\n1 0 1\n1 1 2", 10),
           ("新色与旧色相同", "3 3\n1 1 1\n1 1 0\n1 0 1\n1 1 1", 10),
           ("单格", "1 1\n0\n0 0 5", 15),
           ("全同色", "2 2\n5 5\n5 5\n0 0 1", 15),
           ("不连通区域", "3 3\n1 0 1\n0 0 0\n1 0 1\n0 0 9", 20),
           ("对角不连通", "2 2\n1 0\n0 1\n0 0 7", 20)],
    cpp=CPP_HEADER + """int main(){int r,c;scanf("%d %d",&r,&c);
vector<vector<int>>g(r,vector<int>(c));
for(int i=0;i<r;++i)for(int j=0;j<c;++j)scanf("%d",&g[i][j]);
int sr,sc,col;scanf("%d %d %d",&sr,&sc,&col);
int old=g[sr][sc];
if(old!=col){
vector<pair<int,int>>st;st.push_back({sr,sc});g[sr][sc]=col;
int dx[4]={1,-1,0,0},dy[4]={0,0,1,-1};
while(!st.empty()){auto pr=st.back();st.pop_back();
for(int d=0;d<4;++d){int nx=pr.first+dx[d],ny=pr.second+dy[d];
if(nx<0||nx>=r||ny<0||ny>=c)continue;
if(g[nx][ny]==old){g[nx][ny]=col;st.push_back({nx,ny});}}}}
for(int i=0;i<r;++i){for(int j=0;j<c;++j){if(j)printf(" ");printf("%d",g[i][j]);}printf("\\n");}
return 0;}
""",
    hint="**网格 DFS/BFS 染色**：从起点出发，把连通的同色格子逐个改成新颜色。\n\n> **易错点**：若**新颜色与旧颜色相同**，直接返回，否则会陷入死循环（改完颜色后仍满足「同色」条件，被反复访问）。",
)

# ---------------------------------------------------------------- 9
def s_max_island(t):
    ls = L(t)
    r, c = map(int, ls[0].split())
    g = [list(map(int, ls[i + 1].split())) for i in range(r)]
    best = 0
    for i in range(r):
        for j in range(c):
            if g[i][j] != 1:
                continue
            area = 0
            st = [(i, j)]
            g[i][j] = 0
            while st:
                x, y = st.pop()
                area += 1
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < r and 0 <= ny < c and g[nx][ny] == 1:
                        g[nx][ny] = 0
                        st.append((nx, ny))
            best = max(best, area)
    return f"{best}\n"


add(
    pid="graph-max-island-area", title="岛屿的最大面积", difficulty="中等",
    tags=["图", "DFS", "网格", "连通块"], source="LeetCode 695", url="https://leetcode.cn/problems/max-area-of-island/",
    statement="给定一个 $0/1$ 矩阵，$1$ 表示陆地。求**面积最大的岛屿**的面积。\n\n**岛屿**由上下左右相邻的陆地组成（**对角不算连通**）。若没有陆地则输出 $0$。",
    input_format="第一行两个整数 $r, c$（$1 \\le r, c \\le 50$）。\n\n接下来 $r$ 行，每行 $c$ 个整数（$0$ 或 $1$）。",
    output_format="一行一个整数，表示最大岛屿面积。",
    constraints=["1 ≤ r, c ≤ 50", "元素为 0 或 1", "上下左右连通"],
    solver=s_max_island,
    specs=[("样例 1", "8 13\n0 0 1 0 0 0 0 1 0 0 0 0 0\n0 0 0 0 0 0 0 1 1 1 0 0 0\n0 1 1 0 1 0 0 1 1 1 0 0 0\n0 1 0 0 1 1 0 0 1 0 1 0 0\n0 1 0 0 1 1 0 0 1 1 1 0 0\n0 0 0 0 0 0 0 0 0 0 1 0 0\n0 0 0 0 0 0 0 1 1 1 0 0 0\n0 0 0 0 0 0 0 1 1 0 0 0 0", 10),
           ("全水", "2 2\n0 0\n0 0", 10), ("全陆", "2 2\n1 1\n1 1", 15),
           ("单格", "1 1\n1", 15), ("对角不算连通", "2 2\n1 0\n0 1", 20),
           ("一条线", "1 5\n1 1 1 1 1", 20), ("两岛取大", "2 3\n1 1 0\n0 0 1", 20)],
    cpp=CPP_HEADER + """int main(){int r,c;scanf("%d %d",&r,&c);
vector<vector<int>>g(r,vector<int>(c));
for(int i=0;i<r;++i)for(int j=0;j<c;++j)scanf("%d",&g[i][j]);
int best=0;int dx[4]={1,-1,0,0},dy[4]={0,0,1,-1};
for(int i=0;i<r;++i)for(int j=0;j<c;++j){
if(g[i][j]!=1)continue;
int area=0;vector<pair<int,int>>st;st.push_back({i,j});g[i][j]=0;
while(!st.empty()){auto pr=st.back();st.pop_back();++area;
for(int d=0;d<4;++d){int nx=pr.first+dx[d],ny=pr.second+dy[d];
if(nx<0||nx>=r||ny<0||ny>=c)continue;
if(g[nx][ny]==1){g[nx][ny]=0;st.push_back({nx,ny});}}}
best=max(best,area);}
printf("%d\\n",best);return 0;}
""",
    hint="**遍历每个陆地格子，做一次 DFS 统计面积**，取最大值。\n\n访问过的陆地直接改成 0，省去 visited 数组。\n\n> **易错点**：面积在**出栈时**累加（每个格子只入栈一次），或在入栈时标记后累加——两种写法都行，但要一致。",
)

# ---------------------------------------------------------------- 10
def s_rotting(t):
    ls = L(t)
    r, c = map(int, ls[0].split())
    g = [list(map(int, ls[i + 1].split())) for i in range(r)]
    q = deque()
    fresh = 0
    for i in range(r):
        for j in range(c):
            if g[i][j] == 2:
                q.append((i, j, 0))
            elif g[i][j] == 1:
                fresh += 1
    if fresh == 0:
        return "0\n"
    minutes = 0
    while q:
        x, y, t = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < r and 0 <= ny < c and g[nx][ny] == 1:
                g[nx][ny] = 2
                fresh -= 1
                minutes = t + 1
                q.append((nx, ny, t + 1))
    return f"{minutes if fresh == 0 else -1}\n"


add(
    pid="graph-rotting-oranges", title="腐烂的橘子", difficulty="中等",
    tags=["图", "BFS", "多源BFS", "网格"], source="LeetCode 994", url="https://leetcode.cn/problems/rotting-oranges/",
    statement="给定网格，$0$ 表示空格、$1$ 表示新鲜橘子、$2$ 表示腐烂橘子。\n\n**每分钟**，每个腐烂橘子会让**上下左右相邻**的新鲜橘子腐烂。\n\n求让**所有**橘子都腐烂所需的**最少分钟数**；若不可能，输出 $-1$。若一开始就没有新鲜橘子，输出 $0$。",
    input_format="第一行两个整数 $r, c$（$1 \\le r, c \\le 100$）。\n\n接下来 $r$ 行，每行 $c$ 个整数（$0$、$1$ 或 $2$）。",
    output_format="一行一个整数，表示最少分钟数；不可能则输出 -1。",
    constraints=["1 ≤ r, c ≤ 100", "元素为 0/1/2"],
    solver=s_rotting,
    specs=[("样例 1", "3 3\n2 1 1\n1 1 0\n0 1 1", 10),
           ("样例 2（不可能）", "3 3\n2 1 1\n0 1 1\n1 0 1", 10),
           ("全为空", "1 2\n0 0", 15), ("无新鲜橘子", "1 2\n2 2", 15),
           ("单个新鲜橘子", "1 1\n1", 20), ("单个腐烂橘子", "1 1\n2", 20),
           ("一次扩散完成", "1 3\n2 1 1", 20)],
    cpp=CPP_HEADER + """int main(){int r,c;scanf("%d %d",&r,&c);
vector<vector<int>>g(r,vector<int>(c));
for(int i=0;i<r;++i)for(int j=0;j<c;++j)scanf("%d",&g[i][j]);
queue<tuple<int,int,int>>q;int fresh=0;
for(int i=0;i<r;++i)for(int j=0;j<c;++j){
if(g[i][j]==2)q.push({i,j,0});
else if(g[i][j]==1)++fresh;}
if(fresh==0){printf("0\\n");return 0;}
int minutes=0;int dx[4]={1,-1,0,0},dy[4]={0,0,1,-1};
while(!q.empty()){auto [x,y,t]=q.front();q.pop();
for(int d=0;d<4;++d){int nx=x+dx[d],ny=y+dy[d];
if(nx<0||nx>=r||ny<0||ny>=c)continue;
if(g[nx][ny]==1){g[nx][ny]=2;--fresh;minutes=t+1;q.push({nx,ny,t+1});}}}
printf("%d\\n",fresh==0?minutes:-1);return 0;}
""",
    hint="**多源 BFS**：把**所有**腐烂橘子**一次性**入队，各自带一个「时间」字段（初始为 0）。\n\n每扩展一层时间加 1。最后若还有新鲜橘子没被感染，输出 $-1$。\n\n> **易错点**：\n> 1. 不要写成「对每个腐烂橘子分别做 BFS」——必须**多源同时**入队，否则时间会算错；\n> 2. 「一开始就没有新鲜橘子」要输出 $0$，不能输出 $-1$。",
)

# ---------------------------------------------------------------- 11
def s_zero_one_matrix(t):
    ls = L(t)
    r, c = map(int, ls[0].split())
    g = [list(map(int, ls[i + 1].split())) for i in range(r)]
    dist = [[-1] * c for _ in range(r)]
    q = deque()
    for i in range(r):
        for j in range(c):
            if g[i][j] == 0:
                dist[i][j] = 0
                q.append((i, j))
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < r and 0 <= ny < c and dist[nx][ny] == -1:
                dist[nx][ny] = dist[x][y] + 1
                q.append((nx, ny))
    return "\n".join(" ".join(map(str, row)) for row in dist) + "\n"


add(
    pid="graph-zero-one-matrix", title="01 矩阵（最近 0 的距离）", difficulty="中等",
    tags=["图", "BFS", "多源BFS", "网格"], source="LeetCode 542", url="https://leetcode.cn/problems/01-matrix/",
    statement="给定一个 $0/1$ 矩阵，输出一个同样大小的矩阵，其中每个格子填**它到最近的 $0$ 的距离**（曼哈顿距离，即只能上下左右移动的步数）。\n\n$0$ 所在格子的距离为 $0$。",
    input_format="第一行两个整数 $r, c$（$1 \\le r, c \\le 100$）。\n\n接下来 $r$ 行，每行 $c$ 个整数（$0$ 或 $1$）。",
    output_format="共 $r$ 行，每行 $c$ 个整数，为距离矩阵。",
    constraints=["1 ≤ r, c ≤ 100", "元素为 0 或 1", "保证至少有一个 0"],
    solver=s_zero_one_matrix,
    specs=[("样例 1", "3 3\n0 0 0\n0 1 0\n0 0 0", 10),
           ("样例 2", "3 3\n0 0 0\n0 1 0\n1 1 1", 10),
           ("全为 0", "2 2\n0 0\n0 0", 15), ("单格", "1 1\n0", 15),
           ("单行", "1 4\n1 1 0 1", 20), ("单列", "4 1\n1\n0\n1\n1", 20),
           ("角落的 0", "3 3\n0 1 1\n1 1 1\n1 1 1", 20)],
    cpp=CPP_HEADER + """int main(){int r,c;scanf("%d %d",&r,&c);
vector<vector<int>>g(r,vector<int>(c));
vector<vector<int>>dist(r,vector<int>(c,-1));
queue<pair<int,int>>q;
for(int i=0;i<r;++i)for(int j=0;j<c;++j){
scanf("%d",&g[i][j]);
if(g[i][j]==0){dist[i][j]=0;q.push({i,j});}}
int dx[4]={1,-1,0,0},dy[4]={0,0,1,-1};
while(!q.empty()){auto pr=q.front();q.pop();
for(int d=0;d<4;++d){int nx=pr.first+dx[d],ny=pr.second+dy[d];
if(nx<0||nx>=r||ny<0||ny>=c)continue;
if(dist[nx][ny]==-1){dist[nx][ny]=dist[pr.first][pr.second]+1;q.push({nx,ny});}}}
for(int i=0;i<r;++i){for(int j=0;j<c;++j){if(j)printf(" ");printf("%d",dist[i][j]);}printf("\\n");}
return 0;}
""",
    hint="**多源 BFS（从所有 0 出发）**：把所有 $0$ 一次性入队，距离设为 0；然后像普通 BFS 一样向外扩散，每个格子的距离是「上一层距离 + 1」。\n\n> **为什么不能从每个 1 出发做 BFS**：那样要对每个 $1$ 都做一次 BFS，复杂度爆炸。**反向思考**——从所有 $0$ 出发同时扩散，一次 BFS 就得到全部答案。\n\n> **易错点**：`dist` 初始化为 $-1$，既表示「未访问」又能存距离。",
)

# ---------------------------------------------------------------- 12
def s_kruskal(t):
    ls = L(t)
    n, m = map(int, ls[0].split())
    edges = []
    for i in range(1, m + 1):
        u, v, w = map(int, ls[i].split())
        edges.append((w, u, v))
    edges.sort()
    parent = list(range(n + 1))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    total = 0
    used = 0
    for w, u, v in edges:
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
            total += w
            used += 1
            if used == n - 1:
                break
    if used != n - 1:
        return "-1\n"
    return f"{total}\n"


add(
    pid="graph-kruskal-mst", title="最小生成树（Kruskal）", difficulty="中等",
    tags=["图", "并查集", "最小生成树", "贪心"], source="洛谷 P3366", url="https://www.luogu.com.cn/problem/P3366",
    statement="给定一个 $n$ 个点、$m$ 条边的**无向带权图**，求它的**最小生成树**的边权之和。\n\n若图**不连通**，输出 $-1$。",
    input_format="第一行两个整数 $n, m$（$1 \\le n \\le 5000$，$0 \\le m \\le 2\\times10^5$）。\n\n接下来 $m$ 行，每行三个整数 $u, v, w$（$1 \\le w \\le 10^4$）。",
    output_format="一行一个整数，表示最小生成树的边权之和；不连通则输出 -1。",
    constraints=["1 ≤ n ≤ 5000", "0 ≤ m ≤ 2×10^5", "1 ≤ w ≤ 10^4"],
    solver=s_kruskal,
    specs=[("样例 1", "4 5\n1 2 1\n1 3 4\n2 3 2\n2 4 5\n3 4 3", 10),
           ("单点", "1 0", 10), ("两点一边", "2 1\n1 2 7", 15),
           ("不连通", "4 2\n1 2 1\n3 4 2", 15),
           ("三角形", "3 3\n1 2 1\n2 3 2\n1 3 3", 20),
           ("等权边", "4 6\n1 2 1\n1 3 1\n1 4 1\n2 3 1\n2 4 1\n3 4 1", 20),
           ("链状", "5 4\n1 2 3\n2 3 1\n3 4 4\n4 5 2", 20)],
    cpp=CPP_HEADER + """int main(){int n,m;scanf("%d %d",&n,&m);
vector<tuple<int,int,int>>e(m);
for(int i=0;i<m;++i){int u,v,w;scanf("%d %d %d",&u,&v,&w);e[i]={w,u,v};}
sort(e.begin(),e.end());
vector<int>p(n+1);for(int i=0;i<=n;++i)p[i]=i;
function<int(int)> find=[&](int x){while(p[x]!=x){p[x]=p[p[x]];x=p[x];}return x;};
long long total=0;int used=0;
for(auto&[w,u,v]:e){int ru=find(u),rv=find(v);
if(ru!=rv){p[ru]=rv;total+=w;if(++used==n-1)break;}}
printf("%lld\\n",used==n-1?total:-1LL);return 0;}
""",
    hint="**Kruskal 算法**：\n\n1. 把所有边按**权值升序**排序；\n2. 依次考虑每条边，若它的两个端点**尚不连通**（用并查集判断），就选入生成树并合并；\n3. 选够 $n-1$ 条边即完成。\n\n时间 $O(m\\log m)$（排序主导）。\n\n> **正确性**：这是贪心——每次选当前能选的最小边，不会破坏最优性（可用**切割性质**证明）。\n\n> **不连通判定**：若最终选中的边数少于 $n-1$，说明图不连通。",
)

# ---------------------------------------------------------------- 13
def s_course(t):
    ls = L(t)
    n, m = map(int, ls[0].split())
    g = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for i in range(1, m + 1):
        a, b = map(int, ls[i].split())    # a 是 b 的先修课：a -> b
        g[a].append(b)
        indeg[b] += 1
    q = deque(i for i in range(1, n + 1) if indeg[i] == 0)
    cnt = 0
    while q:
        u = q.popleft()
        cnt += 1
        for v in g[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return ("YES\n" if cnt == n else "NO\n")


add(
    pid="graph-course-schedule", title="课程表（能否完成所有课程）", difficulty="中等",
    tags=["图", "拓扑排序", "BFS", "判环"], source="LeetCode 207", url="https://leetcode.cn/problems/course-schedule/",
    statement="有 $n$ 门课程，编号 $1 \\sim n$。给定若干**先修关系** $(a, b)$，表示修 $b$ 之前必须先修 $a$。\n\n判断是否**能修完所有课程**（即依赖关系无环）。\n\n能则输出 `YES`，否则 `NO`。",
    input_format="第一行两个整数 $n, m$（$1 \\le n \\le 10^5$，$0 \\le m \\le 2\\times10^5$）。\n\n接下来 $m$ 行，每行两个整数 $a, b$，表示 $a$ 是 $b$ 的先修课。",
    output_format="一行，输出 `YES` 或 `NO`。",
    constraints=["1 ≤ n ≤ 10^5", "0 ≤ m ≤ 2×10^5", "无重复边"],
    solver=s_course,
    specs=[("样例 1（可以）", "2 1\n1 2", 10),
           ("样例 2（有环）", "2 2\n1 2\n2 1", 10),
           ("无先修关系", "3 0", 15), ("单课程", "1 0", 15),
           ("链式依赖", "4 3\n1 2\n2 3\n3 4", 20),
           ("长环", "3 3\n1 2\n2 3\n3 1", 20),
           ("不连通有环", "4 3\n1 2\n2 3\n3 2", 20)],
    cpp=CPP_HEADER + """int main(){int n,m;scanf("%d %d",&n,&m);
vector<vector<int>>g(n+1);vector<int>indeg(n+1,0);
for(int i=0;i<m;++i){int a,b;scanf("%d %d",&a,&b);g[a].push_back(b);++indeg[b];}
queue<int>q;for(int i=1;i<=n;++i)if(indeg[i]==0)q.push(i);
int cnt=0;
while(!q.empty()){int u=q.front();q.pop();++cnt;
for(int v:g[u])if(--indeg[v]==0)q.push(v);}
printf("%s\\n",cnt==n?"YES":"NO");return 0;}
""",
    hint="**Kahn 拓扑排序**：统计入度，把入度为 0 的课入队，逐个「修完」并把它指向的课入度减 1。\n\n若最终修完的课程数等于 $n$，说明无环，可以全部修完。\n\n> **直觉**：有环的依赖关系意味着「互相是对方的先修课」，永远无法开始。",
)

# ---------------------------------------------------------------- 14
def s_dag_shortest(t):
    ls = L(t)
    n, m = map(int, ls[0].split())
    g = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for i in range(1, m + 1):
        u, v, w = map(int, ls[i].split())
        g[u].append((v, w))
        indeg[v] += 1
    s, t = map(int, ls[m + 1].split())
    INF = float("inf")
    dist = [INF] * (n + 1)
    dist[s] = 0
    q = deque(i for i in range(1, n + 1) if indeg[i] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v, w in g[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    for u in order:
        if dist[u] == INF:
            continue
        for v, w in g[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return f"{dist[t]}\n" if dist[t] != INF else "-1\n"


add(
    pid="graph-dag-shortest", title="DAG 上的单源最短路", difficulty="中等",
    tags=["图", "拓扑排序", "动态规划", "最短路"], source="DAG 最短路", url="https://www.luogu.com.cn/problem/P1113",
    statement="给定一个**有向无环图（DAG）**，每条边有权值，求从 $s$ 到 $t$ 的**最短路径长度**。\n\n若不可达，输出 $-1$。\n\n**要求**：利用 DAG 的性质，用**拓扑排序 + DP** 做到 $O(n+m)$（比 Dijkstra 更快）。",
    input_format="第一行两个整数 $n, m$（$1 \\le n \\le 10^5$，$0 \\le m \\le 2\\times10^5$）。\n\n接下来 $m$ 行，每行三个整数 $u, v, w$，表示一条从 $u$ 到 $v$ 的边，权值为 $w$（$0 \\le w \\le 10^4$）。\n\n最后一行两个整数 $s, t$。\n\n**保证**图是 DAG。",
    output_format="一行一个整数，表示最短距离；不可达则输出 -1。",
    constraints=["1 ≤ n ≤ 10^5", "0 ≤ m ≤ 2×10^5", "保证是 DAG", "0 ≤ w ≤ 10^4"],
    solver=s_dag_shortest,
    specs=[("样例 1", "4 4\n1 2 1\n2 3 2\n1 3 5\n3 4 1\n1 4", 10),
           ("不可达", "3 1\n1 2 1\n1 3", 10), ("同一点", "1 0\n1 1", 15),
           ("直达最短", "2 1\n1 2 7\n1 2", 15),
           ("多路径", "4 4\n1 2 1\n2 4 1\n1 3 1\n3 4 1\n1 4", 20),
           ("链状", "4 3\n1 2 2\n2 3 3\n3 4 4\n1 4", 20),
           ("含零权边", "3 3\n1 2 0\n2 3 0\n1 3 5\n1 3", 20)],
    cpp=CPP_HEADER + """int main(){int n,m;scanf("%d %d",&n,&m);
vector<vector<pair<int,int>>>g(n+1);vector<int>indeg(n+1,0);
for(int i=0;i<m;++i){int u,v,w;scanf("%d %d %d",&u,&v,&w);
g[u].push_back({v,w});++indeg[v];}
int s,t;scanf("%d %d",&s,&t);
const long long INF=4e18;
vector<long long>dist(n+1,INF);dist[s]=0;
queue<int>q;for(int i=1;i<=n;++i)if(indeg[i]==0)q.push(i);
vector<int>order;
while(!q.empty()){int u=q.front();q.pop();order.push_back(u);
for(auto&pr:g[u])if(--indeg[pr.first]==0)q.push(pr.first);}
for(int u:order){if(dist[u]==INF)continue;
for(auto&pr:g[u])dist[pr.first]=min(dist[pr.first],dist[u]+pr.second);}
printf("%lld\\n",dist[t]==INF?-1LL:dist[t]);return 0;}
""",
    hint="**拓扑排序 + 松弛**：先求出一个拓扑序，然后**按拓扑序**依次处理每个点，用它去松弛所有出边。\n\n因为拓扑序保证「处理 $u$ 时，$u$ 的所有前驱都已处理完」，所以每个点的 `dist` 已经是最终值——这正是 DAG 上最短路能做到 $O(n+m)$ 的原因。\n\n> **对比 Dijkstra**：Dijkstra 需要堆，是 $O(m\\log n)$；DAG 上有更快的线性做法。",
)

# ---------------------------------------------------------------- 15
def s_count_paths(t):
    ls = L(t)
    n, m = map(int, ls[0].split())
    g = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for i in range(1, m + 1):
        u, v = map(int, ls[i].split())
        g[u].append(v)
        indeg[v] += 1
    s, t = map(int, ls[m + 1].split())
    dp = [0] * (n + 1)
    dp[s] = 1
    q = deque(i for i in range(1, n + 1) if indeg[i] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in g[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    for u in order:
        if dp[u] == 0:
            continue
        for v in g[u]:
            dp[v] += dp[u]
    return f"{dp[t]}\n"


add(
    pid="graph-count-paths", title="DAG 中两点间的路径数", difficulty="中等",
    tags=["图", "拓扑排序", "动态规划"], source="DAG 路径计数", url="https://www.luogu.com.cn/problem/P1113",
    statement="给定一个**有向无环图（DAG）**和两个顶点 $s, t$，求从 $s$ 到 $t$ 的**不同路径条数**。\n\n**要求**：用拓扑排序 + DP 做到 $O(n+m)$。",
    input_format="第一行两个整数 $n, m$（$1 \\le n \\le 10^5$，$0 \\le m \\le 2\\times10^5$）。\n\n接下来 $m$ 行，每行两个整数 $u, v$，表示一条从 $u$ 到 $v$ 的有向边。\n\n最后一行两个整数 $s, t$。\n\n**保证**图是 DAG。",
    output_format="一行一个整数，表示路径条数。",
    constraints=["1 ≤ n ≤ 10^5", "0 ≤ m ≤ 2×10^5", "保证是 DAG"],
    solver=s_count_paths,
    specs=[("样例 1", "4 4\n1 2\n2 4\n1 3\n3 4\n1 4", 10),
           ("无路径", "3 1\n1 2\n1 3", 10), ("同一点", "1 0\n1 1", 15),
           ("唯一路径", "3 2\n1 2\n2 3\n1 3", 15),
           ("多条路径", "4 5\n1 2\n1 3\n2 4\n3 4\n1 4\n1 4", 20),
           ("链状", "4 3\n1 2\n2 3\n3 4\n1 4", 20),
           ("菱形加直连", "4 5\n1 2\n2 3\n3 4\n1 3\n2 4\n1 4", 20)],
    cpp=CPP_HEADER + """int main(){int n,m;scanf("%d %d",&n,&m);
vector<vector<int>>g(n+1);vector<int>indeg(n+1,0);
for(int i=0;i<m;++i){int u,v;scanf("%d %d",&u,&v);g[u].push_back(v);++indeg[v];}
int s,t;scanf("%d %d",&s,&t);
vector<long long>dp(n+1,0);dp[s]=1;
queue<int>q;for(int i=1;i<=n;++i)if(indeg[i]==0)q.push(i);
vector<int>order;
while(!q.empty()){int u=q.front();q.pop();order.push_back(u);
for(int v:g[u])if(--indeg[v]==0)q.push(v);}
for(int u:order){if(dp[u]==0)continue;
for(int v:g[u])dp[v]+=dp[u];}
printf("%lld\\n",dp[t]);return 0;}
""",
    hint="**拓扑排序 + 路径计数 DP**：\n\n- 初值：`dp[s] = 1`（从 $s$ 到自己有 1 条路径）；\n- 按拓扑序处理每个点 $u$，对它的每条出边 $(u,v)$，执行 `dp[v] += dp[u]`。\n\n因为拓扑序保证 $u$ 的 `dp` 在处理它时已完整，所以一次遍历即可。\n\n> **为什么不用 BFS**：BFS 无法保证「先处理完所有前驱」，会导致重复计数。",
)

# ---------------------------------------------------------------- 16
def s_town_judge(t):
    n, m, g, edges, ls = read_graph(t, directed=True)
    indeg = [0] * (n + 1)
    outdeg = [0] * (n + 1)
    for u, v in edges:
        outdeg[u] += 1
        indeg[v] += 1
    for i in range(1, n + 1):
        if indeg[i] == n - 1 and outdeg[i] == 0:
            return f"{i}\n"
    return "-1\n"


add(
    pid="graph-town-judge", title="找到小镇的法官", difficulty="简单",
    tags=["图", "度数", "有向图"], source="LeetCode 997", url="https://leetcode.cn/problems/find-the-town-judge/",
    statement="小镇里有 $n$ 个人，编号 $1 \\sim n$。给定若干**信任关系** $(a, b)$，表示 $a$ 信任 $b$。\n\n**法官**的定义：\n\n1. 法官**不信任任何人**（出度为 0）；\n2. **除法官外**的所有人都信任法官（入度为 $n-1$）。\n\n找出法官编号；若不存在则输出 $-1$。\n\n**保证**不存在自己信任自己的情况。",
    input_format="第一行两个整数 $n, m$（$1 \\le n \\le 1000$，$0 \\le m \\le 10^4$）。\n\n接下来 $m$ 行，每行两个整数 $a, b$，表示 $a$ 信任 $b$（$a \\ne b$）。",
    output_format="一行一个整数，表示法官编号；不存在则输出 -1。",
    constraints=["1 ≤ n ≤ 1000", "0 ≤ m ≤ 10^4", "a ≠ b"],
    solver=s_town_judge,
    specs=[("样例 1（有法官）", "3 3\n1 3\n2 3\n3 1", 10),
           ("样例 2（无法官）", "3 2\n1 3\n2 3", 10),
           ("样例 3", "3 3\n1 2\n2 3\n3 1", 15),
           ("n=1 无信任", "1 0", 15),
           ("n=2 有法官", "2 1\n1 2", 20),
           ("n=2 互相信任", "2 2\n1 2\n2 1", 20),
           ("多个人都不信任", "4 3\n1 4\n2 4\n3 4", 20)],
    cpp=CPP_HEADER + """int main(){int n,m;scanf("%d %d",&n,&m);
vector<int>indeg(n+1,0),outdeg(n+1,0);
for(int i=0;i<m;++i){int a,b;scanf("%d %d",&a,&b);
++outdeg[a];++indeg[b];}
int judge=-1;
for(int i=1;i<=n;++i)if(indeg[i]==n-1&&outdeg[i]==0){judge=i;break;}
printf("%d\\n",judge);return 0;}
""",
    hint="**度数法**：法官的**入度 = $n-1$**（被所有人信任）且**出度 = 0**（不信任任何人）。\n\n统计所有人的入度和出度，找满足条件的那个。\n\n> **易错点**：$n = 1$ 时，唯一的人既是法官（入度 0 = $n-1$，出度 0）。",
)


def main() -> None:
    for p in P:
        finalize(p, OUT / f"{p['id']}.json")
        total = sum(t["score"] for t in p["tests"])
        print(f"生成 {p['id']:34s} {len(p['tests'])} 测试点, 总分 {total:3d}")


if __name__ == "__main__":
    main()
