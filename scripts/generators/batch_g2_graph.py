"""图论基础 · 批量 G2（14 道）。"""
from __future__ import annotations

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


def rg(t, directed=False):
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
def s_adj_to_list(t):
    ls = L(t)
    n = int(ls[0])
    out = []
    for i in range(1, n + 1):
        row = list(map(int, ls[i].split()))
        nb = [str(j + 1) for j in range(n) if row[j] == 1]
        out.append(str(len(nb)) + (" " + " ".join(nb) if nb else ""))
    return "\n".join(out) + "\n"


add(
    pid="graph-matrix-to-list", title="邻接矩阵转邻接表", difficulty="入门",
    tags=["图", "邻接矩阵", "邻接表"], source="图的存储", url="https://leetcode.cn/problems/find-center-of-star-graph/",
    statement="给定一个无向图的**邻接矩阵** $A$（$n \\times n$，$A_{ij}=1$ 表示 $i$ 与 $j$ 相邻），"
              "请转成**邻接表**输出。\n\n每行输出一个顶点的邻居：先输出**邻居个数**，再按**编号升序**输出所有邻居编号。\n\n"
              "**不含自环**（对角线均为 0）。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 200$）。\n\n接下来 $n$ 行，每行 $n$ 个整数（$0$ 或 $1$），为邻接矩阵。",
    output_format="共 $n$ 行，第 $i$ 行为顶点 $i$ 的邻居信息（个数 + 升序编号）。若没有邻居，只输出 `0`。",
    constraints=["1 ≤ n ≤ 200", "无自环", "无重边"],
    solver=s_adj_to_list,
    specs=[("样例 1", "3\n0 1 1\n1 0 0\n1 0 0", 10), ("无边", "2\n0 0\n0 0", 10),
           ("单点", "1\n0", 15), ("完全图", "3\n0 1 1\n1 0 1\n1 1 0", 15),
           ("链状", "4\n0 1 0 0\n1 0 1 0\n0 1 0 1\n0 0 1 0", 20),
           ("星形", "4\n0 1 1 1\n1 0 0 0\n1 0 0 0\n1 0 0 0", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);
vector<vector<int>>a(n,vector<int>(n));
for(int i=0;i<n;++i)for(int j=0;j<n;++j)scanf("%d",&a[i][j]);
for(int i=0;i<n;++i){vector<int>nb;
for(int j=0;j<n;++j)if(a[i][j])nb.push_back(j+1);
printf("%d",(int)nb.size());
for(int v:nb)printf(" %d",v);
printf("\\n");}
return 0;}
""",
    hint="**逐行扫描**：对每个顶点 $i$，扫描邻接矩阵第 $i$ 行，把所有 $A_{ij}=1$ 的 $j+1$ 收集起来（因为矩阵下标从 0 开始，顶点编号从 1 开始）。\n\n时间 $O(n^2)$。",
)

# ---------------------------------------------------------------- 2
def s_reverse_edges(t):
    n, m, g, edges, ls = rg(t, directed=True)
    rev = [[] for _ in range(n + 1)]
    for u, v in edges:
        rev[v].append(u)
    out = []
    for i in range(1, n + 1):
        out.append(f"{len(rev[i])}" + (" " + " ".join(map(str, sorted(rev[i]))) if rev[i] else ""))
    return "\n".join(out) + "\n"


add(
    pid="graph-reverse-edges", title="反转有向图的所有边", difficulty="入门",
    tags=["图", "有向图", "邻接表"], source="图的存储", url="https://leetcode.cn/problems/find-center-of-star-graph/",
    statement="给定一个有向图，把**所有边的方向反转**，输出反转后的邻接表。\n\n每行输出一个顶点的**出边**：先输出出度，再按**编号升序**输出所有出边指向的顶点。",
    input_format="第一行两个整数 $n, m$（$1 \\le n \\le 1000$，$0 \\le m \\le 5000$）。\n\n接下来 $m$ 行，每行两个整数 $u, v$，表示一条 $u \\to v$ 的边。",
    output_format="共 $n$ 行，第 $i$ 行为顶点 $i$ 的出度与出边（升序）。没有出边时只输出 `0`。",
    constraints=["1 ≤ n ≤ 1000", "0 ≤ m ≤ 5000", "可能有重边"],
    solver=s_reverse_edges,
    specs=[("样例 1", "3 2\n1 2\n2 3", 10), ("无边", "2 0", 10),
           ("单点自环", "1 1\n1 1", 15), ("双向边", "2 2\n1 2\n2 1", 15),
           ("星形", "4 3\n1 2\n1 3\n1 4", 20), ("链状", "4 3\n1 2\n2 3\n3 4", 20)],
    cpp=CPP_HEADER + """int main(){int n,m;scanf("%d %d",&n,&m);
vector<vector<int>>rev(n+1);
for(int i=0;i<m;++i){int u,v;scanf("%d %d",&u,&v);rev[v].push_back(u);}
for(int i=1;i<=n;++i){sort(rev[i].begin(),rev[i].end());
printf("%d",(int)rev[i].size());
for(int v:rev[i])printf(" %d",v);
printf("\\n");}
return 0;}
""",
    hint="**建反向图**：读边 $(u,v)$ 时，把它加进 `rev[v]` 而不是 `g[u]`。\n\n时间 $O(n + m)$。\n\n> **用途**：求「有多少点能到达 $t$」时，建反向图从 $t$ 出发做一次 BFS 即可。",
)

# ---------------------------------------------------------------- 3
def s_tree_check(t):
    n, m, g, edges, ls = rg(t)
    if m != n - 1:
        return "NO\n"
    seen = [False] * (n + 1)
    q = deque([1])
    seen[1] = True
    cnt = 1
    while q:
        u = q.popleft()
        for v in g[u]:
            if not seen[v]:
                seen[v] = True
                cnt += 1
                q.append(v)
    return "YES\n" if cnt == n else "NO\n"


add(
    pid="graph-tree-check", title="判断无向图是否为树", difficulty="简单",
    tags=["图", "连通性", "树"], source="树的性质", url="https://leetcode.cn/problems/redundant-connection/",
    statement="判断一个无向图是否是**树**。\n\n**树**的两个条件：\n\n1. **连通**（任意两点可达）；\n2. **无环**。\n\n等价地：边数恰好为 $n-1$ **且**图连通。\n\n是树输出 `YES`，否则 `NO`。",
    input_format="第一行两个整数 $n, m$（$1 \\le n \\le 10^5$，$0 \\le m \\le 2\\times10^5$）。\n\n接下来 $m$ 行，每行两个整数 $u, v$（$u \\ne v$）。",
    output_format="一行，输出 `YES` 或 `NO`。",
    constraints=["1 ≤ n ≤ 10^5", "0 ≤ m ≤ 2×10^5", "无自环"],
    solver=s_tree_check,
    specs=[("样例 1（是树）", "4 3\n1 2\n2 3\n3 4", 10),
           ("样例 2（有环）", "3 3\n1 2\n2 3\n3 1", 10),
           ("单点", "1 0", 15), ("不连通", "4 2\n1 2\n3 4", 15),
           ("边数不足", "4 2\n1 2\n2 3", 20), ("边数过多", "4 5\n1 2\n2 3\n3 4\n4 1\n1 3", 20),
           ("两点的树", "2 1\n1 2", 20)],
    cpp=CPP_HEADER + """int main(){int n,m;scanf("%d %d",&n,&m);
vector<vector<int>>g(n+1);
for(int i=0;i<m;++i){int u,v;scanf("%d %d",&u,&v);
g[u].push_back(v);g[v].push_back(u);}
if(m!=n-1){printf("NO\\n");return 0;}
vector<bool>vis(n+1,false);queue<int>q;q.push(1);vis[1]=true;int cnt=1;
while(!q.empty()){int u=q.front();q.pop();
for(int v:g[u])if(!vis[v]){vis[v]=true;++cnt;q.push(v);}}
printf("%s\\n",cnt==n?"YES":"NO");return 0;}
""",
    hint="**两步判断**：\n\n1. **边数必须恰好 $n-1$**（不满足直接 `NO`）；\n2. **从 1 号点 BFS，能访问到全部 $n$ 个点**（保证连通）。\n\n> **为什么这样就够了**：对于无向图，「连通 + 边数 $n-1$」等价于「无环 + 连通」，正是树的定义。\n\n> 也可以直接用**并查集**：加边时若两端已连通则成环，最终再看是否所有点同属一个集合。",
)

# ---------------------------------------------------------------- 4
def s_provinces(t):
    n, m, g, edges, ls = rg(t)
    seen = [False] * (n + 1)
    cnt = 0
    for s in range(1, n + 1):
        if seen[s]:
            continue
        cnt += 1
        q = deque([s])
        seen[s] = True
        while q:
            u = q.popleft()
            for v in g[u]:
                if not seen[v]:
                    seen[v] = True
                    q.append(v)
    return f"{cnt}\n"


add(
    pid="graph-provinces", title="省份数量", difficulty="中等",
    tags=["图", "并查集", "连通块", "DFS"], source="LeetCode 547", url="https://leetcode.cn/problems/number-of-provinces/",
    statement="有 $n$ 个城市，若两个城市**直接或间接相连**则属于同一个省。\n\n给定城市间的连接关系，求**省份总数**。",
    input_format="第一行两个整数 $n, m$（$1 \\le n \\le 200$，$0 \\le m \\le 10^4$）。\n\n接下来 $m$ 行，每行两个整数 $u, v$，表示城市 $u$ 与 $v$ 直接相连（无向）。",
    output_format="一行一个整数，表示省份数量。",
    constraints=["1 ≤ n ≤ 200", "0 ≤ m ≤ 10^4", "无向图"],
    solver=s_provinces,
    specs=[("样例 1", "3 1\n1 2", 10), ("样例 2", "3 0", 10),
           ("全连通", "4 3\n1 2\n2 3\n3 4", 15), ("单城市", "1 0", 15),
           ("两两连通", "3 3\n1 2\n2 3\n1 3", 20), ("两个分量", "4 2\n1 2\n3 4", 20),
           ("星形", "5 4\n1 2\n1 3\n1 4\n1 5", 20)],
    cpp=CPP_HEADER + """int main(){int n,m;scanf("%d %d",&n,&m);
vector<vector<int>>g(n+1);
for(int i=0;i<m;++i){int u,v;scanf("%d %d",&u,&v);
g[u].push_back(v);g[v].push_back(u);}
vector<bool>vis(n+1,false);int cnt=0;
for(int s=1;s<=n;++s){if(vis[s])continue;++cnt;
queue<int>q;q.push(s);vis[s]=true;
while(!q.empty()){int u=q.front();q.pop();
for(int v:g[u])if(!vis[v]){vis[v]=true;q.push(v);}}}
printf("%d\\n",cnt);return 0;}
""",
    hint="**数连通块**：对每个未访问的顶点发起一次 BFS/DFS，块数加一。\n\n> **并查集解法**：把所有相连的城市 `union` 起来，最后统计不同根的数量。两种做法复杂度都是 $O(n + m \\cdot \\alpha(n))$。",
)

# ---------------------------------------------------------------- 5
def s_keys_rooms(t):
    n, m, g, edges, ls = rg(t, directed=True)
    seen = [False] * (n + 1)
    q = deque([1])
    seen[1] = True
    cnt = 1
    while q:
        u = q.popleft()
        for v in g[u]:
            if not seen[v]:
                seen[v] = True
                cnt += 1
                q.append(v)
    return ("YES\n" if cnt == n else "NO\n")


add(
    pid="graph-keys-and-rooms", title="钥匙和房间", difficulty="中等",
    tags=["图", "BFS", "DFS", "有向图"], source="LeetCode 841", url="https://leetcode.cn/problems/keys-and-rooms/",
    statement="有 $n$ 个房间，编号 $1 \\sim n$，初始时你在 $1$ 号房间。\n\n每个房间里有一些**钥匙**，每把钥匙能打开对应的房间。你可以自由地在已打开的房间里移动。\n\n判断能否**进入所有房间**。能则输出 `YES`，否则 `NO`。",
    input_format="第一行两个整数 $n, m$（$1 \\le n \\le 1000$，$0 \\le m \\le 10^4$）。\n\n接下来 $m$ 行，每行两个整数 $a, b$，表示房间 $a$ 里有能打开房间 $b$ 的钥匙。",
    output_format="一行，输出 `YES` 或 `NO`。",
    constraints=["1 ≤ n ≤ 1000", "0 ≤ m ≤ 10^4", "有向图"],
    solver=s_keys_rooms,
    specs=[("样例 1（可以）", "4 3\n1 2\n2 3\n3 4", 10),
           ("样例 2（不可以）", "4 2\n1 2\n3 4", 10),
           ("单房间", "1 0", 15), ("自环钥匙", "2 2\n1 1\n1 2", 15),
           ("钥匙在死路", "3 2\n1 2\n2 1", 20), ("环形", "3 3\n1 2\n2 3\n3 1", 20)],
    cpp=CPP_HEADER + """int main(){int n,m;scanf("%d %d",&n,&m);
vector<vector<int>>g(n+1);
for(int i=0;i<m;++i){int a,b;scanf("%d %d",&a,&b);g[a].push_back(b);}
vector<bool>vis(n+1,false);queue<int>q;q.push(1);vis[1]=true;int cnt=1;
while(!q.empty()){int u=q.front();q.pop();
for(int v:g[u])if(!vis[v]){vis[v]=true;++cnt;q.push(v);}}
printf("%s\\n",cnt==n?"YES":"NO");return 0;}
""",
    hint="**从房间 1 出发做 BFS**：房间是顶点，钥匙是**有向边**。\n\n能到达的房间数等于 $n$ 就能进入所有房间。\n\n> **注意**：这是**有向图**（钥匙只能从 $a$ 打开 $b$），不能当成无向图。",
)

# ---------------------------------------------------------------- 6
def s_eventual_safe(t):
    ls = L(t)
    n, m = map(int, ls[0].split())
    g = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for i in range(1, m + 1):
        u, v = map(int, ls[i].split())
        g[v].append(u)          # 反向图
        indeg[u] += 1           # 反向图下的入度 = 原图的出度
    q = deque(i for i in range(1, n + 1) if indeg[i] == 0)
    safe = [False] * (n + 1)
    while q:
        u = q.popleft()
        safe[u] = True
        for v in g[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    res = [str(i) for i in range(1, n + 1) if safe[i]]
    return (" ".join(res) + "\n") if res else "\n"


add(
    pid="graph-eventual-safe", title="找到所有的安全节点", difficulty="中等",
    tags=["图", "拓扑排序", "反向图"], source="LeetCode 802", url="https://leetcode.cn/problems/find-eventual-safe-states/",
    statement="给定有向图。**安全节点**指「从它出发的**所有**路径最终都能走到一个**出度为 0** 的节点」（即不会陷入环）。\n\n请按**编号升序**输出所有安全节点的编号，以空格分隔。若无安全节点则输出空行。",
    input_format="第一行两个整数 $n, m$（$1 \\le n \\le 10^4$，$0 \\le m \\le 4\\times10^4$）。\n\n接下来 $m$ 行，每行两个整数 $u, v$，表示一条 $u \\to v$ 的边。",
    output_format="一行，升序输出安全节点编号，以空格分隔；无则输出空行。",
    constraints=["1 ≤ n ≤ 10^4", "0 ≤ m ≤ 4×10^4"],
    solver=s_eventual_safe,
    specs=[("样例 1", "4 3\n1 2\n2 3\n3 4", 10), ("样例 2", "5 5\n1 2\n2 3\n3 1\n4 2\n5 4", 10),
           ("无边", "3 0", 15), ("全环", "2 2\n1 2\n2 1", 15),
           ("单点", "1 0", 20), ("自环", "2 1\n1 1", 20)],
    cpp=CPP_HEADER + """int main(){int n,m;scanf("%d %d",&n,&m);
vector<vector<int>>g(n+1);vector<int>indeg(n+1,0);
for(int i=0;i<m;++i){int u,v;scanf("%d %d",&u,&v);
g[v].push_back(u);++indeg[u];}
queue<int>q;for(int i=1;i<=n;++i)if(indeg[i]==0)q.push(i);
vector<bool>safe(n+1,false);
while(!q.empty()){int u=q.front();q.pop();safe[u]=true;
for(int v:g[u])if(--indeg[v]==0)q.push(v);}
bool first=true;
for(int i=1;i<=n;++i)if(safe[i]){if(!first)printf(" ");printf("%d",i);first=false;}
printf("\\n");return 0;}
""",
    hint="**反向图 + 拓扑排序**：\n\n1. 建**反向图**（把每条边 $u \\to v$ 变成 $v \\to u$）；\n2. 在反向图上做拓扑排序，从「原图出度为 0」的点（即反向图入度为 0）出发；\n3. 能在这个拓扑过程中被访问到的点就是**安全节点**。\n\n> **直觉**：安全节点的定义是「不会走进环」，反向思考就是从「终点」逆着走能到达的点。\n\n> **易错点**：必须用**反向图**！在原图上做拓扑排序得到的是另一回事。",
)

# ---------------------------------------------------------------- 7
def s_all_paths(t):
    n, m, g, edges, ls = rg(t, directed=True)
    s, t = map(int, ls[m + 1].split())
    res = []
    path = [s]
    def dfs(u):
        if u == t:
            res.append("->".join(map(str, path)))
            return
        for v in sorted(g[u]):
            path.append(v)
            dfs(v)
            path.pop()
    dfs(s)
    return ("\n".join(res) + "\n") if res else "\n"


add(
    pid="graph-all-paths", title="所有可能的路径", difficulty="中等",
    tags=["图", "DFS", "回溯", "DAG"], source="LeetCode 797", url="https://leetcode.cn/problems/all-paths-from-source-to-target/",
    statement="给定一个有向无环图（DAG）和起点 $s$、终点 $t$，输出从 $s$ 到 $t$ 的**所有路径**。\n\n**输出要求**：每条路径占一行，节点编号用 `->` 连接；路径之间按**字典序**升序排列（即 DFS 时邻居按编号升序访问）。",
    input_format="第一行两个整数 $n, m$（$1 \\le n \\le 15$，$0 \\le m \\le 100$）。\n\n接下来 $m$ 行，每行两个整数 $u, v$，表示一条 $u \\to v$ 的边。\n\n最后一行两个整数 $s, t$。\n\n**保证**是 DAG。",
    output_format="每行一条路径；若无路径则输出空行。",
    constraints=["1 ≤ n ≤ 15", "0 ≤ m ≤ 100", "保证是 DAG", "按字典序输出"],
    solver=s_all_paths,
    specs=[("样例 1", "4 3\n1 2\n3 2\n3 4\n1 4", 10),
           ("样例 2", "5 5\n1 2\n1 3\n2 4\n3 4\n4 5\n1 5", 10),
           ("无路径", "3 1\n1 2\n1 3", 15), ("同一点", "1 0\n1 1", 15),
           ("唯一路径", "3 2\n1 2\n2 3\n1 3", 20), ("菱形", "4 4\n1 2\n1 3\n2 4\n3 4\n1 4", 20)],
    cpp=CPP_HEADER + """int n;vector<vector<int>>g;vector<int>path;vector<string>res;
void dfs(int u,int t){
if(u==t){string s;for(size_t i=0;i<path.size();++i){
if(i)s+="->";s+=to_string(path[i]);}res.push_back(s);return;}
for(int v:g[u]){path.push_back(v);dfs(v,t);path.pop_back();}}
int main(){int m;scanf("%d %d",&n,&m);g.assign(n+1,{});
for(int i=0;i<m;++i){int u,v;scanf("%d %d",&u,&v);g[u].push_back(v);}
for(int i=1;i<=n;++i)sort(g[i].begin(),g[i].end());
int s,t;scanf("%d %d",&s,&t);
path.push_back(s);dfs(s,t);
for(auto&x:res)printf("%s\\n",x.c_str());
if(res.empty())printf("\\n");
return 0;}
""",
    hint="**DFS + 回溯**：用 `path` 记录当前路径，访问到 $t$ 就把路径加入结果；否则递归所有邻居，**递归返回后要弹出最后一个节点**（回溯）。\n\n> **排序技巧**：先把每个顶点的邻居**排序**，这样 DFS 得到的路径天然是字典序。\n\n> **为什么不用 visited**：路径可以重复经过同一个点（只要不形成环，DAG 保证不会），所以不需要访问标记。",
)

# ---------------------------------------------------------------- 8
def s_word_search(t):
    ls = L(t)
    r, c = map(int, ls[0].split())
    g = [ls[i + 1].strip() for i in range(r)]
    word = ls[r + 1].strip()
    n, m = len(word), c

    def dfs(i, j, k):
        if k == n:
            return True
        if i < 0 or i >= r or j < 0 or j >= m or g[i][j] != word[k]:
            return False
        tmp = g[i][j]
        g[i] = g[i][:j] + "#" + g[i][j + 1:]
        ok = (dfs(i + 1, j, k + 1) or dfs(i - 1, j, k + 1)
              or dfs(i, j + 1, k + 1) or dfs(i, j - 1, k + 1))
        g[i] = g[i][:j] + tmp + g[i][j + 1:]
        return ok

    for i in range(r):
        for j in range(c):
            if dfs(i, j, 0):
                return "YES\n"
    return "NO\n"


add(
    pid="graph-word-search", title="单词搜索", difficulty="中等",
    tags=["图", "DFS", "回溯", "网格"], source="LeetCode 79", url="https://leetcode.cn/problems/word-search/",
    statement="给定一个字符网格和一个单词，判断单词是否存在于网格中。\n\n单词由**上下左右相邻**的格子依次连接而成，**同一个格子不能重复使用**。\n\n存在输出 `YES`，否则 `NO`。",
    input_format="第一行两个整数 $r, c$（$1 \\le r, c \\le 6$）。\n\n接下来 $r$ 行，每行一个长度为 $c$ 的字符串（仅含大写字母）。\n\n最后一行一个字符串 $word$（仅含大写字母）。",
    output_format="一行，输出 `YES` 或 `NO`。",
    constraints=["1 ≤ r, c ≤ 6", "仅含大写字母", "同一格不能重复使用"],
    solver=s_word_search,
    specs=[("样例 1（存在）", "3 4\nABCE\nSFCS\nADEE\nABCCED", 10),
           ("样例 2（存在）", "3 4\nABCE\nSFCS\nADEE\nSEE", 10),
           ("样例 3（不存在）", "3 4\nABCE\nSFCS\nADEE\nABCB", 15),
           ("单格命中", "1 1\nA\nA", 15), ("单格未命中", "1 1\nA\nB", 20),
           ("需回溯", "3 3\nAAA\nABA\nAAA\nAAAAA", 20),
           ("超出网格", "1 2\nAB\nABC", 20)],
    cpp=CPP_HEADER + """int r,c;vector<string>g;string w;
bool dfs(int i,int j,int k){
if(k==(int)w.size())return true;
if(i<0||i>=r||j<0||j>=c||g[i][j]!=w[k])return false;
char t=g[i][j];g[i][j]='#';
bool ok=dfs(i+1,j,k+1)||dfs(i-1,j,k+1)||dfs(i,j+1,k+1)||dfs(i,j-1,k+1);
g[i][j]=t;return ok;}
int main(){scanf("%d %d",&r,&c);g.resize(r);
for(int i=0;i<r;++i)cin>>g[i];
cin>>w;
for(int i=0;i<r;++i)for(int j=0;j<c;++j)
if(dfs(i,j,0)){printf("YES\\n");return 0;}
printf("NO\\n");return 0;}
""",
    hint="**DFS + 回溯**：从每个格子出发尝试匹配。\n\n匹配到第 $k$ 个字符时，若当前格子的字符不等于 `word[k]` 就失败；否则**临时把当前格子标记为已用**（例如改成 `#`），递归四个方向，**返回后恢复**。\n\n> **关键**：`k == len(word)` 时立即返回成功（在检查格子合法性**之前**判断）。\n\n> **易错点**：必须**回溯恢复**格子内容，否则后续的起点尝试会受污染。",
)

# ---------------------------------------------------------------- 9
def s_surrounded(t):
    ls = L(t)
    r, c = map(int, ls[0].split())
    g = [list(ls[i + 1].strip()) for i in range(r)]
    q = deque()
    for i in range(r):
        for j in (0, c - 1):
            if g[i][j] == "O":
                g[i][j] = "#"
                q.append((i, j))
    for j in range(c):
        for i in (0, r - 1):
            if g[i][j] == "O":
                g[i][j] = "#"
                q.append((i, j))
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < r and 0 <= ny < c and g[nx][ny] == "O":
                g[nx][ny] = "#"
                q.append((nx, ny))
    out = []
    for i in range(r):
        out.append("".join("O" if ch == "#" else "X" for ch in g[i]))
    return "\n".join(out) + "\n"


add(
    pid="graph-surrounded-regions", title="被围绕的区域", difficulty="中等",
    tags=["图", "DFS", "BFS", "网格"], source="LeetCode 130", url="https://leetcode.cn/problems/surrounded-regions/",
    statement="给定一个由 `'X'` 和 `'O'` 组成的矩阵，把**所有被 `'X'` 完全围绕的 `'O'`** 改成 `'X'`。\n\n**边界上的 `'O'` 及其连通的 `'O'` 不会被围绕**，应保持为 `'O'`。\n\n**连通**指上下左右相邻。",
    input_format="第一行两个整数 $r, c$（$1 \\le r, c \\le 200$）。\n\n接下来 $r$ 行，每行一个长度为 $c$ 的字符串（仅含 `X` 和 `O`）。",
    output_format="共 $r$ 行，为修改后的矩阵。",
    constraints=["1 ≤ r, c ≤ 200", "仅含 X 和 O", "上下左右连通"],
    solver=s_surrounded,
    specs=[("样例 1", "4 4\nXXXX\nXOOX\nXXOX\nXOXX", 10),
           ("全 X", "2 2\nXX\nXX", 10), ("全 O", "2 2\nOO\nOO", 15),
           ("单格 O", "1 1\nO", 15), ("单格 X", "1 1\nX", 20),
           ("中心被围", "3 3\nXXX\nXOX\nXXX", 20),
           ("边界连通", "3 3\nOXO\nXXX\nOXO", 20)],
    cpp=CPP_HEADER + """int main(){int r,c;scanf("%d %d",&r,&c);
vector<string>g(r);
for(int i=0;i<r;++i)cin>>g[i];
queue<pair<int,int>>q;
for(int i=0;i<r;++i)for(int j:{0,c-1})
if(g[i][j]=='O'){g[i][j]='#';q.push({i,j});}
for(int j=0;j<c;++j)for(int i:{0,r-1})
if(g[i][j]=='O'){g[i][j]='#';q.push({i,j});}
int dx[4]={1,-1,0,0},dy[4]={0,0,1,-1};
while(!q.empty()){auto pr=q.front();q.pop();
for(int d=0;d<4;++d){int nx=pr.first+dx[d],ny=pr.second+dy[d];
if(nx<0||nx>=r||ny<0||ny>=c)continue;
if(g[nx][ny]=='O'){g[nx][ny]='#';q.push({nx,ny});}}}
for(int i=0;i<r;++i){for(int j=0;j<c;++j)
printf("%c",g[i][j]=='#'?'O':'X');printf("\\n");}
return 0;}
""",
    hint="**反向思考（从边界出发）**：\n\n**正着想很难**（要判断一个 `O` 是否被完全包围）。**反着想很简单**：\n\n1. 把所有**边界上的 `O`** 及其**连通区域**标记为「安全」（临时改成 `#`）；\n2. 剩下还是 `O` 的，就是被完全围绕的 → 改成 `X`；\n3. 把临时的 `#` 改回 `O`。\n\n时间 $O(rc)$。",
)

# ---------------------------------------------------------------- 10
def s_grid_paths_obs(t):
    ls = L(t)
    r, c = map(int, ls[0].split())
    g = [list(map(int, ls[i + 1].split())) for i in range(r)]
    dp = [[0] * c for _ in range(r)]
    if g[0][0] == 0:
        dp[0][0] = 1
    for i in range(r):
        for j in range(c):
            if g[i][j] == 1 or (i == 0 and j == 0):
                continue
            if i > 0:
                dp[i][j] += dp[i - 1][j]
            if j > 0:
                dp[i][j] += dp[i][j - 1]
    return f"{dp[r - 1][c - 1]}\n"


add(
    pid="graph-unique-paths-obstacle", title="不同路径 II（含障碍）", difficulty="中等",
    tags=["动态规划", "网格", "计数"], source="LeetCode 63", url="https://leetcode.cn/problems/unique-paths-ii/",
    statement="给定一个 $r \\times c$ 的网格，$1$ 表示**障碍物**，$0$ 表示可通行。\n\n机器人从左上角出发，每次只能向右或向下，求到达右下角的**不同路径数**。\n\n**保证**起点和终点不是障碍物。",
    input_format="第一行两个整数 $r, c$（$1 \\le r, c \\le 100$）。\n\n接下来 $r$ 行，每行 $c$ 个整数（$0$ 或 $1$）。",
    output_format="一行一个整数，表示路径数。",
    constraints=["1 ≤ r, c ≤ 100", "起点终点非障碍", "元素为 0 或 1"],
    solver=s_grid_paths_obs,
    specs=[("样例 1", "3 3\n0 0 0\n0 1 0\n0 0 0", 10),
           ("无路可走", "2 2\n0 1\n1 0", 10), ("无阻碍", "2 2\n0 0\n0 0", 15),
           ("单格", "1 1\n0", 15), ("单行有障碍", "1 3\n0 1 0", 20),
           ("全障碍除起终", "3 3\n0 1 1\n1 1 1\n1 1 0", 20),
           ("单列", "3 1\n0\n0\n0", 20)],
    cpp=CPP_HEADER + """int main(){int r,c;scanf("%d %d",&r,&c);
vector<vector<int>>g(r,vector<int>(c));
for(int i=0;i<r;++i)for(int j=0;j<c;++j)scanf("%d",&g[i][j]);
vector<vector<long long>>dp(r,vector<long long>(c,0));
if(!g[0][0])dp[0][0]=1;
for(int i=0;i<r;++i)for(int j=0;j<c;++j){
if(g[i][j]||(i==0&&j==0))continue;
if(i)dp[i][j]+=dp[i-1][j];
if(j)dp[i][j]+=dp[i][j-1];}
printf("%lld\\n",dp[r-1][c-1]);return 0;}
""",
    hint="**与「不同路径」同框架，加一个障碍判断**：\n\n`dp[i][j] = dp[i-1][j] + dp[i][j-1]`，但**若 $(i,j)$ 是障碍则 `dp[i][j] = 0`**。\n\n> **易错点**：起点也要判断——若起点就是障碍，答案是 0（虽然题面保证不是）。",
)

# ---------------------------------------------------------------- 11
def s_binary_matrix(t):
    ls = L(t)
    r, c = map(int, ls[0].split())
    g = [list(map(int, ls[i + 1].split())) for i in range(r)]
    if g[0][0] == 1 or g[r - 1][c - 1] == 1:
        return "-1\n"
    dist = [[-1] * c for _ in range(r)]
    dist[0][0] = 1
    q = deque([(0, 0)])
    while q:
        x, y = q.popleft()
        if x == r - 1 and y == c - 1:
            return f"{dist[x][y]}\n"
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < r and 0 <= ny < c and g[nx][ny] == 0 and dist[nx][ny] == -1:
                dist[nx][ny] = dist[x][y] + 1
                q.append((nx, ny))
    return "-1\n"


add(
    pid="graph-binary-matrix-path", title="二进制矩阵中的最短路径", difficulty="中等",
    tags=["图", "BFS", "网格"], source="LeetCode 1091", url="https://leetcode.cn/problems/shortest-path-in-binary-matrix/",
    statement="给定 $0/1$ 矩阵，$0$ 表示可通行。\n\n从左上角走到右下角，每步可以走**八个方向**（上下左右 + 四个斜角）。\n\n求最短路径的**格子数**（含起点和终点）；若不可达输出 $-1$。",
    input_format="第一行两个整数 $r, c$（$1 \\le r, c \\le 100$）。\n\n接下来 $r$ 行，每行 $c$ 个整数（$0$ 或 $1$）。",
    output_format="一行一个整数，表示最短路径的格子数；不可达则输出 -1。",
    constraints=["1 ≤ r, c ≤ 100", "元素为 0 或 1", "八方向移动"],
    solver=s_binary_matrix,
    specs=[("样例 1", "2 2\n0 1\n1 0", 10), ("样例 2", "2 3\n0 0 0\n1 1 0", 10),
           ("单格 0", "1 1\n0", 15), ("单格 1", "1 1\n1", 15),
           ("全 0", "3 3\n0 0 0\n0 0 0\n0 0 0", 20),
           ("起点被堵", "2 2\n1 0\n0 0", 20), ("需绕路", "3 3\n0 0 1\n1 0 1\n1 0 0", 20)],
    cpp=CPP_HEADER + """int main(){int r,c;scanf("%d %d",&r,&c);
vector<vector<int>>g(r,vector<int>(c));
for(int i=0;i<r;++i)for(int j=0;j<c;++j)scanf("%d",&g[i][j]);
if(g[0][0]||g[r-1][c-1]){printf("-1\\n");return 0;}
vector<vector<int>>d(r,vector<int>(c,-1));d[0][0]=1;
queue<pair<int,int>>q;q.push({0,0});
int dx[8]={1,-1,0,0,1,1,-1,-1},dy[8]={0,0,1,-1,1,-1,1,-1};
while(!q.empty()){auto pr=q.front();q.pop();
if(pr.first==r-1&&pr.second==c-1){printf("%d\\n",d[pr.first][pr.second]);return 0;}
for(int k=0;k<8;++k){int nx=pr.first+dx[k],ny=pr.second+dy[k];
if(nx<0||nx>=r||ny<0||ny>=c)continue;
if(g[nx][ny]==0&&d[nx][ny]==-1){d[nx][ny]=d[pr.first][pr.second]+1;q.push({nx,ny});}}}
printf("-1\\n");return 0;}
""",
    hint="**BFS 求无权图最短路**：八方向的网格也是无权图，BFS 天然给出最短路径。\n\n`dist` 初值为 $-1$（未访问），起点为 $1$（含起点的格子数）。\n\n> **易错点**：**起点或终点是障碍**时要直接输出 $-1$，否则 BFS 会出错。",
)

# ---------------------------------------------------------------- 12
def s_min_cost_connect(t):
    ls = L(t)
    n = int(ls[0])
    pts = [tuple(map(int, ls[i + 1].split())) for i in range(n)]
    INF = float("inf")
    dist = [INF] * n
    used = [False] * n
    dist[0] = 0
    total = 0
    for _ in range(n):
        u = -1
        for i in range(n):
            if not used[i] and (u == -1 or dist[i] < dist[u]):
                u = i
        used[u] = True
        total += dist[u]
        for v in range(n):
            if not used[v]:
                d = abs(pts[u][0] - pts[v][0]) + abs(pts[u][1] - pts[v][1])
                if d < dist[v]:
                    dist[v] = d
    return f"{total}\n"


add(
    pid="graph-min-cost-connect", title="连接所有点的最小费用", difficulty="中等",
    tags=["图", "最小生成树", "Prim", "贪心"], source="LeetCode 1584", url="https://leetcode.cn/problems/min-cost-to-connect-all-points/",
    statement="给定平面上 $n$ 个点的坐标，连接两个点 $i$ 和 $j$ 的费用是它们的**曼哈顿距离** $|x_i-x_j| + |y_i-y_j|$。\n\n求让**所有点连通**所需的**最小总费用**。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 1000$）。\n\n接下来 $n$ 行，每行两个整数 $x_i, y_i$（$|x|, |y| \\le 10^6$）。",
    output_format="一行一个整数，表示最小总费用。",
    constraints=["1 ≤ n ≤ 1000", "|x|, |y| ≤ 10^6", "费用为曼哈顿距离"],
    solver=s_min_cost_connect,
    specs=[("样例 1", "3\n0 0\n2 2\n3 10", 10), ("样例 2", "3\n0 0\n0 0\n0 0", 10),
           ("单点", "1\n5 5", 15), ("两点", "2\n0 0\n3 4", 15),
           ("正方形", "4\n0 0\n0 1\n1 0\n1 1", 20), ("一条线", "4\n0 0\n1 0\n2 0\n3 0", 20),
           ("重复点", "4\n1 1\n1 1\n1 1\n1 1", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);
vector<long long>x(n),y(n);
for(int i=0;i<n;++i)scanf("%lld %lld",&x[i],&y[i]);
const long long INF=4e18;
vector<long long>dist(n,INF);vector<bool>used(n,false);
dist[0]=0;long long total=0;
for(int it=0;it<n;++it){
int u=-1;
for(int i=0;i<n;++i)if(!used[i]&&(u==-1||dist[i]<dist[u]))u=i;
used[u]=true;total+=dist[u];
for(int v=0;v<n;++v)if(!used[v]){
long long d=llabs(x[u]-x[v])+llabs(y[u]-y[v]);
if(d<dist[v])dist[v]=d;}}
printf("%lld\\n",total);return 0;}
""",
    hint="**Prim 算法（朴素版）**：\n\n1. `dist[i]` 表示「把点 $i$ 接入当前生成树」的最小费用，初始只有起点为 0；\n2. 每轮选一个**未使用且 `dist` 最小**的点加入生成树，累加费用；\n3. 用新加入的点**更新其他点的 `dist`**。\n\n时间 $O(n^2)$，适合稠密图。\n\n> **注意**：本题是完全图（任意两点间都有边），边数 $O(n^2)$，所以用朴素 Prim 比 Kruskal 更合适。",
)

# ---------------------------------------------------------------- 13
def s_topo_lex(t):
    ls = L(t)
    n, m = map(int, ls[0].split())
    g = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for i in range(1, m + 1):
        u, v = map(int, ls[i].split())
        g[u].append(v)
        indeg[v] += 1
    import heapq
    h = [i for i in range(1, n + 1) if indeg[i] == 0]
    heapq.heapify(h)
    order = []
    while h:
        u = heapq.heappop(h)
        order.append(u)
        for v in g[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                heapq.heappush(h, v)
    if len(order) != n:
        return "-1\n"
    return " ".join(map(str, order)) + "\n"


add(
    pid="graph-topo-lex-min", title="字典序最小的拓扑序", difficulty="中等",
    tags=["图", "拓扑排序", "优先队列"], source="拓扑排序变体", url="https://www.luogu.com.cn/problem/P1113",
    statement="给定一个有向图，求它的**字典序最小的拓扑序**。\n\n若图中有环（无法拓扑排序），输出 $-1$。",
    input_format="第一行两个整数 $n, m$（$1 \\le n \\le 10^5$，$0 \\le m \\le 2\\times10^5$）。\n\n接下来 $m$ 行，每行两个整数 $u, v$，表示一条 $u \\to v$ 的边。",
    output_format="一行 $n$ 个整数，为字典序最小的拓扑序；有环则输出 -1。",
    constraints=["1 ≤ n ≤ 10^5", "0 ≤ m ≤ 2×10^5", "可能有环"],
    solver=s_topo_lex,
    specs=[("样例 1", "4 3\n1 2\n2 3\n3 4", 10), ("有环", "3 3\n1 2\n2 3\n3 1", 10),
           ("无边", "3 0", 15), ("单点", "1 0", 15),
           ("多入度 0", "4 2\n1 3\n2 4", 20), ("菱形", "4 4\n1 2\n1 3\n2 4\n3 4", 20),
           ("逆序边", "3 2\n1 3\n2 3", 20)],
    cpp=CPP_HEADER + """int main(){int n,m;scanf("%d %d",&n,&m);
vector<vector<int>>g(n+1);vector<int>indeg(n+1,0);
for(int i=0;i<m;++i){int u,v;scanf("%d %d",&u,&v);g[u].push_back(v);++indeg[v];}
priority_queue<int,vector<int>,greater<int>>pq;
for(int i=1;i<=n;++i)if(indeg[i]==0)pq.push(i);
vector<int>order;
while(!pq.empty()){int u=pq.top();pq.pop();order.push_back(u);
for(int v:g[u])if(--indeg[v]==0)pq.push(v);}
if((int)order.size()!=n){printf("-1\\n");return 0;}
for(int i=0;i<n;++i){if(i)printf(" ");printf("%d",order[i]);}
printf("\\n");return 0;}
""",
    hint="**把队列换成小根堆**：Kahn 算法的骨架完全不变，只需把存放「入度为 0 的点」的**队列换成小根堆**——每次取编号最小的，就得到字典序最小的拓扑序。\n\n时间 $O((n+m)\\log n)$。",
)

# ---------------------------------------------------------------- 14
def s_network_rank(t):
    ls = L(t)
    n, m = map(int, ls[0].split())
    deg = [0] * (n + 1)
    es = set()
    for i in range(1, m + 1):
        u, v = map(int, ls[i].split())
        deg[u] += 1
        deg[v] += 1
        es.add((min(u, v), max(u, v)))
    best = 0
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            r = deg[i] + deg[j] - (1 if (i, j) in es else 0)
            best = max(best, r)
    return f"{best}\n"


add(
    pid="graph-max-network-rank", title="最大网络秩", difficulty="简单",
    tags=["图", "度数", "枚举"], source="LeetCode 1615", url="https://leetcode.cn/problems/maximal-network-rank/",
    statement="给定 $n$ 个城市和若干**无向道路**。\n\n两个不同城市的**网络秩** = 「与城市 A 直接相连的城市数」+「与城市 B 直接相连的城市数」− 「A 与 B 之间是否有直接道路（有则减 1）」。\n\n求所有城市对中的**最大网络秩**。",
    input_format="第一行两个整数 $n, m$（$2 \\le n \\le 100$，$0 \\le m \\le n(n-1)/2$）。\n\n接下来 $m$ 行，每行两个整数 $u, v$，表示 $u$ 与 $v$ 之间有道路。",
    output_format="一行一个整数，表示最大网络秩。",
    constraints=["2 ≤ n ≤ 100", "0 ≤ m ≤ n(n−1)/2", "无自环、无重边"],
    solver=s_network_rank,
    specs=[("样例 1", "4 4\n1 2\n2 3\n3 4\n4 1", 10),
           ("无边", "3 0", 10), ("完全图", "3 3\n1 2\n2 3\n1 3", 15),
           ("两城一道路", "2 1\n1 2", 15), ("星形", "4 3\n1 2\n1 3\n1 4", 20),
           ("链状", "4 3\n1 2\n2 3\n3 4", 20)],
    cpp=CPP_HEADER + """int main(){int n,m;scanf("%d %d",&n,&m);
vector<int>deg(n+1,0);set<pair<int,int>>es;
for(int i=0;i<m;++i){int u,v;scanf("%d %d",&u,&v);
++deg[u];++deg[v];es.insert({min(u,v),max(u,v)});}
int best=0;
for(int i=1;i<=n;++i)for(int j=i+1;j<=n;++j){
int r=deg[i]+deg[j]-(es.count({i,j})?1:0);
best=max(best,r);}
printf("%d\\n",best);return 0;}
""",
    hint="**枚举所有城市对**：$n \\le 100$，直接 $O(n^2)$ 枚举即可。\n\n用度数数组快速得到「相连城市数」，再用集合判断两点之间是否有直接道路。\n\n时间 $O(n^2)$。\n\n> **优化思路**：只需考虑度数最大的那些城市对，但本题规模下没必要。",
)


def main() -> None:
    for p in P:
        finalize(p, OUT / f"{p['id']}.json")
        total = sum(t["score"] for t in p["tests"])
        print(f"生成 {p['id']:34s} {len(p['tests'])} 测试点, 总分 {total:3d}")


if __name__ == "__main__":
    main()
