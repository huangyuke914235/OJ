"""堆与优先队列 · 批量 H1（16 道）。"""
from __future__ import annotations

import heapq
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from genkit import CPP_HEADER, finalize, numbers, problem  # noqa: E402

OUT = ROOT / "oj" / "data" / "problems" / "05-heap"
P: list = []


def add(**kw):
    P.append(problem(**kw))


def arr(t):
    v = numbers(t)
    return v[0], v[1:1 + v[0]]


# ---------------------------------------------------------------- 1
def s_kth_smallest(t):
    v = numbers(t)
    n, k = v[0], v[1]
    a = v[2:2 + n]
    h = [-x for x in a[:k]]
    heapq.heapify(h)
    for x in a[k:]:
        if x < -h[0]:
            heapq.heapreplace(h, -x)
    return f"{-h[0]}\n"


add(
    pid="heap-kth-smallest", title="数组中的第 K 小元素", difficulty="简单",
    tags=["堆", "优先队列", "Top-K"], source="LeetCode 215 变体", url="https://leetcode.cn/problems/kth-largest-element-in-an-array/",
    statement="给定数组和整数 $k$，求数组中**第 $k$ 小**的元素。\n\n**要求**：用大小为 $k$ 的**大根堆**，时间复杂度 $O(n\\log k)$。",
    input_format="第一行两个整数 $n, k$（$1 \\le k \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数（$|a_i| \\le 10^9$）。",
    output_format="一行一个整数，表示第 $k$ 小的元素。",
    constraints=["1 ≤ k ≤ n ≤ 10^5", "|a_i| ≤ 10^9", "要求 O(n log k)"],
    solver=s_kth_smallest,
    specs=[("样例 1", "6 2\n3 2 1 5 6 4", 10), ("样例 2", "3 1\n3 2 1", 10),
           ("k = n", "4 4\n1 2 3 4", 15), ("全相同", "4 2\n5 5 5 5", 15),
           ("含负数", "5 3\n-1 -2 -3 -4 -5", 20), ("单元素", "1 1\n7", 20),
           ("含重复", "6 3\n2 2 1 1 3 3", 20)],
    cpp=CPP_HEADER + """int main(){int n,k;scanf("%d %d",&n,&k);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
priority_queue<long long>pq;
for(int i=0;i<k;++i)pq.push(a[i]);
for(int i=k;i<n;++i)if(a[i]<pq.top()){pq.pop();pq.push(a[i]);}
printf("%lld\\n",pq.top());return 0;}
""",
    hint="**大小为 $k$ 的大根堆**：堆中保存「当前最小的 $k$ 个元素」，堆顶是其中**最大**的，也就是全局第 $k$ 小。\n\n遇到比堆顶小的元素就替换堆顶。\n\n> **对比**：求第 $k$ **大**要用**小根堆**，方向正好相反。",
)

# ---------------------------------------------------------------- 2
def s_heap_sort(t):
    n, a = arr(t)
    heapq.heapify(a)
    res = [heapq.heappop(a) for _ in range(n)]
    return " ".join(map(str, res)) + "\n"


add(
    pid="heap-sort-asc", title="堆排序（升序）", difficulty="简单",
    tags=["堆", "排序"], source="经典堆排序", url="https://leetcode.cn/problems/sort-an-array/",
    statement="使用**堆排序**把数组升序排列并输出。\n\n**要求**：时间复杂度 $O(n\\log n)$。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数（$|a_i| \\le 10^9$）。",
    output_format="一行 $n$ 个整数，升序排列，以空格分隔。",
    constraints=["1 ≤ n ≤ 10^5", "|a_i| ≤ 10^9", "要求 O(n log n)"],
    solver=s_heap_sort,
    specs=[("样例 1", "5\n3 1 4 1 5", 10), ("已有序", "4\n1 2 3 4", 10),
           ("逆序", "4\n4 3 2 1", 15), ("单元素", "1\n7", 15),
           ("全相同", "4\n2 2 2 2", 20), ("含负数", "5\n-1 0 -3 2 -2", 20),
           ("两元素", "2\n5 3", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
priority_queue<long long,vector<long long>,greater<long long>>pq(a.begin(),a.end());
bool first=true;
while(!pq.empty()){if(!first)printf(" ");printf("%lld",pq.top());pq.pop();first=false;}
printf("\\n");return 0;}
""",
    hint="**建堆 + 逐个弹出**：把所有元素放入小根堆（`O(n)` 建堆），然后反复弹出堆顶——弹出的顺序就是升序。\n\n总时间 $O(n\\log n)$。\n\n> **手写堆排序**则用大根堆 + 原地交换：每次把堆顶换到末尾，再对前 $n-1$ 个元素下沉。",
)

# ---------------------------------------------------------------- 3
def s_min_heap_check(t):
    n, a = arr(t)
    ok = all(a[(i - 1) // 2] <= a[i] for i in range(1, n))
    return ("YES\n" if ok else "NO\n")


add(
    pid="heap-min-heap-check", title="判断是否为小根堆", difficulty="入门",
    tags=["堆", "数组", "树"], source="堆性质检验", url="https://leetcode.cn/problems/minimum-absolute-difference-in-bst/",
    statement="给定一个按**层序**存储的完全二叉树（数组形式），判断它是否满足**小根堆性质**：\n\n**每个节点**的值都不大于它的两个孩子。\n\n是则输出 `YES`，否则 `NO`。\n\n下标规则：节点 $i$ 的孩子是 $2i+1$ 与 $2i+2$（下标从 $0$ 开始）。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数（$|a_i| \\le 10^9$），为完全二叉树的层序。",
    output_format="一行，输出 `YES` 或 `NO`。",
    constraints=["1 ≤ n ≤ 10^5", "|a_i| ≤ 10^9", "下标从 0 开始"],
    solver=s_min_heap_check,
    specs=[("样例 1（是）", "5\n1 3 5 7 9", 10), ("样例 2（不是）", "5\n1 5 3 7 9", 10),
           ("单元素", "1\n7", 15), ("全相同", "4\n5 5 5 5", 15),
           ("严格递增", "6\n1 2 3 4 5 6", 20), ("含负数", "5\n-5 -1 0 -2 3", 20),
           ("根不是最小", "3\n5 1 2", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
bool ok=true;
for(int i=1;i<n;++i)if(a[(i-1)/2]>a[i]){ok=false;break;}
printf("%s\\n",ok?"YES":"NO");return 0;}
""",
    hint="**只需检查每个节点与它的父节点**：对下标 $i \\ge 1$，判断 `a[(i-1)/2] <= a[i]`。\n\n只要有一个不满足，就不是小根堆。\n\n> **技巧**：检查「父 ≤ 子」比分别检查两个孩子更简洁，且等价。",
)

# ---------------------------------------------------------------- 4
def s_kth_stream(t):
    ls = t.strip("\n").split("\n")
    n, k = map(int, ls[0].split())
    a = list(map(int, ls[1].split()))
    h = []
    out = []
    for i, x in enumerate(a):
        heapq.heappush(h, x)
        if len(h) > k:
            heapq.heappop(h)
        if i >= k - 1:
            out.append(str(h[0]))
    return " ".join(out) + "\n"


add(
    pid="heap-kth-largest-stream", title="数据流中第 K 大的元素", difficulty="中等",
    tags=["堆", "优先队列", "Top-K", "数据流"], source="LeetCode 703", url="https://leetcode.cn/problems/kth-largest-element-in-a-stream/",
    statement="依次读入数据，**每读入一个数**就输出「当前已读入的所有数中**第 $k$ 大**的值」。\n\n从读入第 $k$ 个数开始输出（前 $k-1$ 个时还没有第 $k$ 大）。\n\n**要求**：每次操作 $O(\\log k)$。",
    input_format="第一行两个整数 $n, k$（$1 \\le k \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数（$|a_i| \\le 10^9$）。",
    output_format="一行 $n-k+1$ 个整数，依次为每次读入后的第 $k$ 大。",
    constraints=["1 ≤ k ≤ n ≤ 10^5", "|a_i| ≤ 10^9", "每次 O(log k)"],
    solver=s_kth_stream,
    specs=[("样例 1", "4 3\n4 5 8 2", 10), ("k = 1", "3 1\n3 1 2", 10),
           ("k = n", "3 3\n1 2 3", 15), ("递增", "5 2\n1 2 3 4 5", 15),
           ("递减", "5 2\n5 4 3 2 1", 20), ("全相同", "4 2\n7 7 7 7", 20),
           ("含负数", "5 3\n-1 -2 -3 -4 -5", 20)],
    cpp=CPP_HEADER + """int main(){int n,k;scanf("%d %d",&n,&k);
priority_queue<long long,vector<long long>,greater<long long>>pq;
bool first=true;
for(int i=0;i<n;++i){long long x;scanf("%lld",&x);
pq.push(x);
if((int)pq.size()>k)pq.pop();
if(i>=k-1){if(!first)printf(" ");printf("%lld",pq.top());first=false;}}
printf("\\n");return 0;}
""",
    hint="**维护大小为 $k$ 的小根堆**：每读入一个数就压入；若堆大小超过 $k$，弹出堆顶（最小值）。\n\n此时堆中就是「当前最大的 $k$ 个数」，堆顶即第 $k$ 大。\n\n时间 $O(n\\log k)$。",
)

# ---------------------------------------------------------------- 5
def s_k_pairs(t):
    ls = t.strip("\n").split("\n")
    n, m, k = map(int, ls[0].split())
    a = list(map(int, ls[1].split()))
    b = list(map(int, ls[2].split()))
    h = []
    for i in range(min(n, k)):
        for j in range(min(m, k)):
            # 小根堆存 (-和, -i, -j)：堆顶是「和最大、i 最大、j 最大」的那对
            heapq.heappush(h, (-(a[i] + b[j]), -i, -j))
            if len(h) > k:
                heapq.heappop(h)
    res = sorted([(-s, -i, -j) for s, i, j in h])
    return "\n".join(f"{i} {j}" for _, i, j in res) + "\n"


add(
    pid="heap-k-pairs-smallest", title="查找和最小的 K 对数字", difficulty="中等",
    tags=["堆", "优先队列", "Top-K"], source="LeetCode 373", url="https://leetcode.cn/problems/find-k-pairs-with-smallest-sums/",
    statement="给定两个**升序**数组 $A$、$B$ 和整数 $k$，找出**和最小的 $k$ 对** $(i, j)$（$i$ 是 $A$ 的下标，$j$ 是 $B$ 的下标）。\n\n**输出要求**：每行一对 `i j`，按「和升序；和相同则 $i$ 升序；再相同则 $j$ 升序」排列。",
    input_format="第一行三个整数 $n, m, k$（$1 \\le n, m \\le 10^4$，$1 \\le k \\le \\min(nm, 10^4)$）。\n\n第二行 $n$ 个整数（升序）。\n\n第三行 $m$ 个整数（升序）。",
    output_format="共 $k$ 行，每行 `i j`。",
    constraints=["1 ≤ n, m ≤ 10^4", "1 ≤ k ≤ min(nm, 10^4)", "两数组升序"],
    solver=s_k_pairs,
    specs=[("样例 1", "3 3 3\n1 7 11\n2 4 6", 10), ("样例 2", "2 2 2\n1 1\n1 1", 10),
           ("k = 1", "3 3 1\n1 2 3\n1 2 3", 15), ("k = nm", "2 3 6\n1 2\n3 4 5", 15),
           ("含负数", "2 2 3\n-3 -1\n-2 0", 20), ("单元素", "1 1 1\n5\n7", 20),
           ("长度不等", "3 2 4\n1 2 3\n10 20", 20)],
    cpp=CPP_HEADER + """int main(){int n,m,k;scanf("%d %d %d",&n,&m,&k);
vector<long long>a(n),b(m);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
for(int i=0;i<m;++i)scanf("%lld",&b[i]);
priority_queue<pair<long long,pair<int,int>>>pq;
for(int i=0;i<min(n,k);++i)for(int j=0;j<min(m,k);++j){
pq.push({a[i]+b[j],{i,j}});          // 大根堆：堆顶是当前和最大的
if((int)pq.size()>k)pq.pop();        // 弹掉和最大的，保留和最小的 k 个
}
vector<pair<long long,pair<int,int>>>res;
while(!pq.empty()){res.push_back(pq.top());pq.pop();}
reverse(res.begin(),res.end());
for(auto&pr:res)printf("%d %d\\n",pr.second.first,pr.second.second);
return 0;}
""",
    hint="**大小为 $k$ 的大根堆**：枚举前 $\\min(n,k) \\times \\min(m,k)$ 对，用大根堆保留「和最小的 $k$ 对」。\n\n> **剪枝**：只需枚举前 $k$ 行与前 $k$ 列——因为第 $k+1$ 行之后的和一定比前 $k$ 行的某些组合更大。\n\n> **输出顺序**：堆弹出的是「和最大的」，所以要**收集后反转**（或按规则排序）才能得到升序。",
)

# ---------------------------------------------------------------- 6
def s_halve(t):
    n, a = arr(t)
    total = sum(a)
    target = total / 2
    h = [-x for x in a]
    heapq.heapify(h)
    cur = total
    ops = 0
    while cur > target:
        x = -heapq.heappop(h)
        cur -= x - x // 2
        heapq.heappush(h, -(x // 2))
        ops += 1
    return f"{ops}\n"


add(
    pid="heap-halve-array-sum", title="将数组和减半的最少操作次数", difficulty="中等",
    tags=["堆", "优先队列", "贪心"], source="LeetCode 2208", url="https://leetcode.cn/problems/minimum-operations-to-halve-array-sum/",
    statement="每次操作可以选一个数把它**减半**（向下取整，即 `x → ⌊x/2⌋`）。\n\n求让数组总和**至少减半**所需的**最少操作次数**。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 10^5$）。\n\n第二行 $n$ 个正整数（$1 \\le a_i \\le 10^7$）。",
    output_format="一行一个整数，表示最少操作次数。",
    constraints=["1 ≤ n ≤ 10^5", "1 ≤ a_i ≤ 10^7"],
    solver=s_halve,
    specs=[("样例 1", "5\n5 19 8 1", 10), ("样例 2", "3\n3 8 20", 10),
           ("单元素", "1\n10", 15), ("全为 1", "3\n1 1 1", 15),
           ("已经很小", "2\n1 1", 20), ("大值", "2\n10000000 1", 20),
           ("两个大值", "2\n7 7", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);
priority_queue<long long>pq;long long total=0;
for(int i=0;i<n;++i){long long x;scanf("%lld",&x);total+=x;pq.push(x);}
double target=total/2.0;long long cur=total;int ops=0;
while(cur>target){long long x=pq.top();pq.pop();
cur-=x-x/2;pq.push(x/2);++ops;}
printf("%d\\n",ops);return 0;}
""",
    hint="**贪心 + 大根堆**：每次**减半当前最大的数**收益最大。\n\n循环：弹出堆顶 $x$，总和减少 `x - x/2`，把 `x/2` 放回堆，操作数加一；直到总和不超过原来的一半。\n\n> **易错点**：目标是比较「总和 ≤ 原总和 / 2」，用 `double` 或两边乘 2 比较可避免整除误差。",
)

# ---------------------------------------------------------------- 7
def s_furthest(t):
    ls = t.strip("\n").split("\n")
    n = int(ls[0])
    heights = list(map(int, ls[1].split()))
    bricks, ladders = map(int, ls[2].split())
    h = []
    for i in range(n - 1):
        d = heights[i + 1] - heights[i]
        if d <= 0:
            continue
        heapq.heappush(h, d)
        if len(h) > ladders:
            bricks -= heapq.heappop(h)
            if bricks < 0:
                return f"{i}\n"
    return f"{n - 1}\n"


add(
    pid="heap-furthest-building", title="到达最远的建筑", difficulty="中等",
    tags=["堆", "优先队列", "贪心"], source="LeetCode 1642", url="https://leetcode.cn/problems/furthest-building-you-can-reach/",
    statement="从左到右依次经过建筑，每栋高度为 $h_i$。从 $i$ 到 $i+1$：\n\n- 若下一栋**不更高**，可以直接通过；\n- 若更高，需要付出高度差——可以用**砖块**（消耗等量砖）或**梯子**（不限高度，但数量有限）。\n\n求最多能到达的**建筑下标**（从 $0$ 开始）。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数 $h_i$（$1 \\le h_i \\le 10^9$）。\n\n第三行两个整数 $bricks, ladders$（$0 \\le bricks \\le 10^9$，$0 \\le ladders \\le n$）。",
    output_format="一行一个整数，表示能到达的最远建筑下标。",
    constraints=["1 ≤ n ≤ 10^5", "1 ≤ h_i ≤ 10^9", "0 ≤ bricks ≤ 10^9"],
    solver=s_furthest,
    specs=[("样例 1", "5\n4 2 7 6 9 14 12\n5 1", 10), ("样例 2", "5\n4 12 2 7 3 18 20 3 19\n10 2", 10),
           ("单建筑", "1\n5\n0 0", 15), ("全程下坡", "4\n5 4 3 2\n0 0", 15),
           ("梯子足够", "4\n1 5 9 13\n0 3", 20), ("砖不够", "3\n1 10 20\n5 0", 20),
           ("砖梯都够", "3\n1 2 3\n10 10", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>h(n);
for(int i=0;i<n;++i)scanf("%lld",&h[i]);
long long bricks,ladders;scanf("%lld %lld",&bricks,&ladders);
priority_queue<long long,vector<long long>,greater<long long>>pq;
for(int i=0;i+1<n;++i){
long long d=h[i+1]-h[i];
if(d<=0)continue;
pq.push(d);
if((long long)pq.size()>ladders){bricks-=pq.top();pq.pop();
if(bricks<0){printf("%d\\n",i);return 0;}}}
printf("%d\\n",n-1);return 0;}
""",
    hint="**小根堆 + 贪心**：把遇到的高度差都放进小根堆，**梯子优先留给最高的落差**。\n\n当落差数量超过梯子数时，把**最小的落差**改用砖块支付；若砖块不够，说明卡在这里。\n\n> **核心思路**：先假设所有上坡都用梯子，超出的部分再用砖块补——用堆来选出「最不值得用梯子的那些」。",
)

# ---------------------------------------------------------------- 8
def s_cookies(t):
    ls = t.strip("\n").split("\n")
    n, need = map(int, ls[0].split())
    a = list(map(int, ls[1].split()))
    heapq.heapify(a)
    ops = 0
    while len(a) >= 2 and a[0] < need:
        x = heapq.heappop(a)
        y = heapq.heappop(a)
        heapq.heappush(a, x + 2 * y)
        ops += 1
    return f"{ops if a and a[0] >= need else -1}\n"


add(
    pid="heap-cookies", title="分饼干（贪心 + 堆）", difficulty="简单",
    tags=["堆", "优先队列", "贪心"], source="LeetCode 1140 变体", url="https://leetcode.cn/problems/minimum-operations-to-exceed-threshold-value-ii/",
    statement="有一堆饼干，每个有甜度。每次操作：取**甜度最小的两块** $x \\le y$，把它们合并成一块新饼干，甜度为 `x + 2y`。\n\n求让**所有**饼干甜度都 $\\ge need$ 所需的**最少操作次数**；若无法做到，输出 $-1$。",
    input_format="第一行两个整数 $n, need$（$1 \\le n \\le 10^5$，$1 \\le need \\le 10^9$）。\n\n第二行 $n$ 个正整数（$1 \\le a_i \\le 10^6$）。",
    output_format="一行一个整数，表示最少操作次数；无法达成输出 -1。",
    constraints=["1 ≤ n ≤ 10^5", "1 ≤ need ≤ 10^9", "1 ≤ a_i ≤ 10^6"],
    solver=s_cookies,
    specs=[("样例 1", "6 7\n1 2 3 9 10 12", 10), ("样例 2（无法达成）", "3 100\n1 1 1", 10),
           ("已全部满足", "3 5\n5 6 7", 15), ("单元素已满足", "1 10\n1", 15),
           ("单元素不满足", "1 5\n1", 20), ("两个元素", "2 10\n1 2", 20),
           ("需多步", "3 20\n1 1 1", 20)],
    cpp=CPP_HEADER + """int main(){int n;long long need;scanf("%d %lld",&n,&need);
priority_queue<long long,vector<long long>,greater<long long>>pq;
for(int i=0;i<n;++i){long long x;scanf("%lld",&x);pq.push(x);}
int ops=0;
while(pq.size()>=2&&pq.top()<need){
long long x=pq.top();pq.pop();
long long y=pq.top();pq.pop();
pq.push(x+2*y);++ops;}
printf("%d\\n",(pq.top()>=need)?ops:-1);return 0;}
""",
    hint="**小根堆 + 贪心**：每次都取最小的两块合并——因为合并结果 `x + 2y` 中 $y$ 的权重更大，所以让 $y$ 尽量大（即把第二小和最小配对）。\n\n循环直到堆顶 $\\ge need$，或堆中只剩 1 个元素。\n\n> **易错点**：若最后堆顶仍小于 `need`，说明无解，输出 $-1$。",
)

# ---------------------------------------------------------------- 9
def s_reorganize(t):
    s = t.strip("\n").split("\n")[0]
    cnt = Counter(s)
    # 小根堆存 (-次数, 字符编码)：堆顶 = 次数最多；次数相同时字符最小
    h = [(-c, ord(ch), ch) for ch, c in cnt.items()]
    heapq.heapify(h)
    res = []
    prev = None
    while h:
        c, code, ch = heapq.heappop(h)
        res.append(ch)
        if prev:
            heapq.heappush(h, prev)
            prev = None
        c = -c - 1
        if c > 0:
            prev = (-c, code, ch)
    out = "".join(res)
    if len(out) != len(s):
        return "\n"
    return out + "\n"


add(
    pid="heap-reorganize-string", title="重构字符串", difficulty="中等",
    tags=["堆", "优先队列", "贪心", "字符串"], source="LeetCode 767", url="https://leetcode.cn/problems/reorganize-string/",
    statement="给定一个字符串，重新排列它的字符，使得**任意两个相邻字符都不相同**。\n\n若无法做到，输出**空行**。\n\n**输出要求**：若有多种方案，输出任意一种即可——本题约定输出**按算法贪心得到的确定结果**（见提示）。",
    input_format="一行一个字符串 $s$（$1 \\le |s| \\le 500$），仅含小写英文字母。",
    output_format="一行，重排后的字符串；无解则输出空行。",
    constraints=["1 ≤ |s| ≤ 500", "仅小写字母"],
    solver=s_reorganize,
    specs=[("样例 1", "aab", 10), ("样例 2（无解）", "aaab", 10),
           ("单字符", "a", 15), ("全相同两个", "aa", 15),
           ("可解", "vvvlo", 20), ("三字符", "aabbcc", 20),
           ("奇数长度", "aaabb", 20)],
    cpp=CPP_HEADER + """int main(){string s;cin>>s;
int cnt[26]={0};for(char c:s)++cnt[c-'a'];
priority_queue<tuple<int,int,char>>pq;
for(int i=0;i<26;++i)if(cnt[i])pq.push({cnt[i],-('a'+i),(char)('a'+i)});
string res;tuple<int,int,char> prev{0,0,0};
while(!pq.empty()){
auto cur=pq.top();pq.pop();
res+=get<2>(cur);
if(get<0>(prev)>0)pq.push(prev);
prev={get<0>(cur)-1,get<1>(cur),get<2>(cur)};}
if((int)res.size()!=(int)s.size())printf("\\n");
else printf("%s\\n",res.c_str());
return 0;}
""",
    hint="**大根堆 + 暂存上一个**：每次从堆中取**出现次数最多**的字符拼到结果末尾；取出后**先不立刻放回堆**，而是暂存，等下一轮再放回。\n\n这样能保证同一个字符不会连续出现两次。\n\n> **无解判定**：若最终结果长度小于原串长度，说明某字符出现次数超过 `(n+1)/2`，无解。",
)

# ---------------------------------------------------------------- 10
def s_task_scheduler(t):
    ls = t.strip("\n").split("\n")
    n = int(ls[0])
    tasks = list(ls[1].split())
    cooldown = int(ls[2])
    cnt = Counter(tasks)
    if cooldown == 0:
        return f"{n}\n"
    h = [-c for c in cnt.values()]
    heapq.heapify(h)
    time = 0
    while h:
        temp = []
        for _ in range(cooldown + 1):
            if h:
                temp.append(-heapq.heappop(h) - 1)
            time += 1
            if not h and not any(temp):
                break
        for c in temp:
            if c > 0:
                heapq.heappush(h, -c)
    return f"{time}\n"


add(
    pid="heap-task-scheduler", title="任务调度器", difficulty="中等",
    tags=["堆", "优先队列", "贪心", "调度"], source="LeetCode 621", url="https://leetcode.cn/problems/task-scheduler/",
    statement="给定一组任务（用大写字母表示）和冷却时间 $n$，**同一类任务**两次执行之间必须间隔至少 $n$ 个时间单位。\n\nCPU 可以**空闲**。求执行完所有任务所需的**最少时间单位数**。",
    input_format="第一行一个整数 $m$（$1 \\le m \\le 10^4$），表示任务个数。\n\n第二行 $m$ 个大写字母，以空格分隔。\n\n第三行一个整数 $n$（$0 \\le n \\le 100$），表示冷却时间。",
    output_format="一行一个整数，表示最少所需时间。",
    constraints=["1 ≤ m ≤ 10^4", "0 ≤ n ≤ 100", "任务用大写字母表示"],
    solver=s_task_scheduler,
    specs=[("样例 1", "6\nA A A B B B\n2", 10), ("样例 2", "6\nA A A B B B\n0", 10),
           ("样例 3", "12\nA A A A A A B C D E F G\n2", 15),
           ("单任务", "1\nA\n2", 15), ("全不同", "3\nA B C\n1", 20),
           ("两个任务", "2\nA B\n2", 20), ("冷却很大", "2\nA A\n5", 20)],
    cpp=CPP_HEADER + """int main(){int m;scanf("%d",&m);
int cnt[26]={0};
for(int i=0;i<m;++i){char c[4];scanf("%s",c);++cnt[c[0]-'A'];}
int n;scanf("%d",&n);
priority_queue<int>pq;
for(int i=0;i<26;++i)if(cnt[i])pq.push(cnt[i]);
int time=0;
while(!pq.empty()){
vector<int>tmp;
for(int i=0;i<=n;++i){
if(!pq.empty()){tmp.push_back(pq.top()-1);pq.pop();}
++time;
if(pq.empty()){bool any=false;for(int v:tmp)if(v>0)any=true;
if(!any)break;}}
for(int v:tmp)if(v>0)pq.push(v);}
printf("%d\\n",time);return 0;}
""",
    hint="**大根堆 + 按轮次调度**：每一轮长度为 $n+1$（冷却窗口）。\n\n每轮从堆中取出现次数最多的任务执行（次数减 1 暂存），执行完一轮后把剩余次数大于 0 的放回堆。\n\n> **关键**：当堆空且暂存的任务都已耗尽时，可以**提前结束本轮**（CPU 不再空转）。\n\n> **另解（公式法）**：设最大频次为 $f$，频次为 $f$ 的任务有 $c$ 种，则答案是 `max(m, (f-1)*(n+1) + c)`。",
)

# ---------------------------------------------------------------- 11
def s_min_increment(t):
    n, a = arr(t)
    a.sort()
    ops = 0
    for i in range(1, n):
        if a[i] <= a[i - 1]:
            ops += a[i - 1] + 1 - a[i]
            a[i] = a[i - 1] + 1
    return f"{ops}\n"


add(
    pid="heap-min-increment-unique", title="使数组唯一的最小增量", difficulty="中等",
    tags=["数组", "排序", "贪心"], source="LeetCode 945", url="https://leetcode.cn/problems/minimum-increment-to-make-array-unique/",
    statement="每次操作可以让数组中**任意一个元素加 1**。\n\n求使数组中所有元素**互不相同**所需的**最少操作次数**。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数 $a_i$（$0 \\le a_i \\le 10^5$）。",
    output_format="一行一个整数，表示最少操作次数。",
    constraints=["1 ≤ n ≤ 10^5", "0 ≤ a_i ≤ 10^5"],
    solver=s_min_increment,
    specs=[("样例 1", "3\n1 2 2", 10), ("样例 2", "3\n3 2 1 2 1 7", 10),
           ("已互异", "3\n1 2 3", 15), ("全相同", "4\n5 5 5 5", 15),
           ("单元素", "1\n5", 20), ("含零", "3\n0 0 0", 20),
           ("两个相同", "2\n3 3", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
sort(a.begin(),a.end());
long long ops=0;
for(int i=1;i<n;++i)if(a[i]<=a[i-1]){ops+=a[i-1]+1-a[i];a[i]=a[i-1]+1;}
printf("%lld\\n",ops);return 0;}
""",
    hint="**排序后贪心**：把数组升序排序，从左往右扫描。\n\n若 `a[i] <= a[i-1]`，就把它提升到 `a[i-1] + 1`，并累加代价。\n\n> **为什么排序有效**：排序后相同的值聚在一起，处理顺序天然保证「只增不减」，避免来回调整。\n\n时间 $O(n\\log n)$。",
)

# ---------------------------------------------------------------- 12
def s_reduce_array(t):
    ls = t.strip("\n").split("\n")
    n = int(ls[0])
    a = sorted(map(int, ls[1].split()))
    cur = 1
    for i in range(1, n):
        cur = min(a[i], cur + 1)
    return f"{cur}\n"


add(
    pid="heap-reduce-array", title="减小和重新排列数组后的最大元素", difficulty="简单",
    tags=["数组", "排序", "贪心"], source="LeetCode 1846", url="https://leetcode.cn/problems/maximum-element-after-decreasing-and-rearranging/",
    statement="你可以**任意重排**数组，并**减小**任意元素的值（不能增大）。\n\n操作后要求：第一个元素为 $1$，且相邻元素之差的绝对值不超过 $1$。\n\n求操作后**最大元素的最大可能值**。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 10^5$）。\n\n第二行 $n$ 个正整数 $a_i$（$1 \\le a_i \\le 10^9$）。",
    output_format="一行一个整数，表示最大可能值。",
    constraints=["1 ≤ n ≤ 10^5", "1 ≤ a_i ≤ 10^9"],
    solver=s_reduce_array,
    specs=[("样例 1", "3\n2 2 1 2 1", 10), ("样例 2", "3\n100 1 1000", 10),
           ("单元素", "1\n5", 15), ("全为 1", "3\n1 1 1", 15),
           ("递减序列", "4\n10 9 8 7", 20), ("递增序列", "4\n1 2 3 4", 20),
           ("含大值", "2\n1000000000 1", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
sort(a.begin(),a.end());
long long cur=1;
for(int i=1;i<n;++i){if(a[i]>cur)cur=cur+1;}
printf("%lld\\n",cur);return 0;}
""",
    hint="**排序后贪心构造**：排序后，第一个元素设为 $1$，之后每个元素取 `min(a[i], 前一个 + 1)`。\n\n最终序列的最后一个元素就是答案。\n\n> **直觉**：每个位置最多比前一个多 1，且不能超过原值，所以尽量「顶格」往上取。",
)

# ---------------------------------------------------------------- 13
def s_find_k_closest(t):
    ls = t.strip("\n").split("\n")
    n, k, x = map(int, ls[0].split())
    a = list(map(int, ls[1].split()))
    h = []
    for v in a:
        heapq.heappush(h, (-abs(v - x), -v))
        if len(h) > k:
            heapq.heappop(h)
    res = sorted(-v for _, v in h)
    return " ".join(map(str, res)) + "\n"


add(
    pid="heap-find-k-closest", title="找到 K 个最接近的元素", difficulty="中等",
    tags=["堆", "优先队列", "二分查找"], source="LeetCode 658", url="https://leetcode.cn/problems/find-k-closest-elements/",
    statement="给定**升序**数组、整数 $k$ 和目标值 $x$，找出数组中**最接近 $x$ 的 $k$ 个数**。\n\n**输出要求**：结果按**升序**排列，以空格分隔。\n\n若两个数与 $x$ 的距离相同，**优先保留较小的那个**。",
    input_format="第一行三个整数 $n, k, x$（$1 \\le k \\le n \\le 10^4$，$|x| \\le 10^4$）。\n\n第二行 $n$ 个整数（升序，$|a_i| \\le 10^4$）。",
    output_format="一行 $k$ 个整数，升序排列。",
    constraints=["1 ≤ k ≤ n ≤ 10^4", "数组升序", "距离相同时保留较小值"],
    solver=s_find_k_closest,
    specs=[("样例 1", "4 2 3\n1 2 3 4", 10), ("样例 2", "4 2 3\n1 2 3 4 5", 10),
           ("k = n", "3 3 5\n1 2 3", 15), ("k = 1", "5 1 3\n1 2 3 4 5", 15),
           ("含负数", "5 2 -1\n-5 -3 -1 0 2", 20), ("距离相同", "4 2 2\n1 2 3 4", 20),
           ("全相同距离", "3 2 0\n-1 0 1", 20)],
    cpp=CPP_HEADER + """int main(){int n,k,x;scanf("%d %d %d",&n,&k,&x);
vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
priority_queue<pair<long long,long long>>pq;
for(long long v:a){
pq.push({llabs(v-x),v});
if((int)pq.size()>k)pq.pop();}
vector<long long>res;
while(!pq.empty()){res.push_back(pq.top().second);pq.pop();}
sort(res.begin(),res.end());
for(int i=0;i<k;++i){if(i)printf(" ");printf("%lld",res[i]);}
printf("\\n");return 0;}
""",
    hint="**大小为 $k$ 的大根堆**：堆中保存「当前最接近的 $k$ 个数」，按**距离**比较，堆顶是距离最远的。\n\n遇到更近的就替换堆顶。\n\n> **平局处理**：`pair<距离, 值>` 比较大小时，距离相同时会再比值——正好满足「保留较小值」的要求（堆顶是更大的那个，先被弹出）。\n\n> **更优解法**：因为是升序数组，可用**二分**找到 $x$ 的位置，再向两侧双指针扩展，$O(\\log n + k)$。",
)

# ---------------------------------------------------------------- 14
def s_meeting_rooms(t):
    ls = t.strip("\n").split("\n")
    n = int(ls[0])
    iv = [tuple(map(int, ls[i + 1].split())) for i in range(n)]
    iv.sort()
    h = []
    for s, e in iv:
        if h and h[0] <= s:
            heapq.heappop(h)
        heapq.heappush(h, e)
    return f"{len(h)}\n"


add(
    pid="heap-meeting-rooms-ii", title="会议室 II（最少会议室数）", difficulty="中等",
    tags=["堆", "优先队列", "区间", "贪心"], source="LeetCode 253", url="https://leetcode.cn/problems/meeting-rooms-ii/",
    statement="给定若干会议的时间区间 $[start, end)$，求**至少需要多少间会议室**才能安排所有会议。\n\n注意区间是**左闭右开**：一个会议在 `end` 时刻结束，另一个可以在同一时刻开始。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 10^4$）。\n\n接下来 $n$ 行，每行两个整数 $start, end$（$0 \\le start < end \\le 10^6$）。",
    output_format="一行一个整数，表示最少会议室数。",
    constraints=["1 ≤ n ≤ 10^4", "0 ≤ start < end ≤ 10^6", "区间左闭右开"],
    solver=s_meeting_rooms,
    specs=[("样例 1", "3\n0 30\n5 10\n15 20", 10), ("样例 2（无重叠）", "3\n7 10\n2 4\n1 3", 10),
           ("全重叠", "3\n1 5\n1 5\n1 5", 15), ("首尾相接", "2\n1 2\n2 3", 15),
           ("单会议", "1\n0 5", 20), ("阶梯式", "4\n1 2\n2 3\n3 4\n4 5", 20),
           ("完全包含", "2\n0 10\n2 3", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);
vector<pair<long long,long long>>v(n);
for(int i=0;i<n;++i)scanf("%lld %lld",&v[i].first,&v[i].second);
sort(v.begin(),v.end());
priority_queue<long long,vector<long long>,greater<long long>>pq;
for(auto&pr:v){
if(!pq.empty()&&pq.top()<=pr.first)pq.pop();
pq.push(pr.second);}
printf("%d\\n",(int)pq.size());return 0;}
""",
    hint="**排序 + 小根堆**：先按**开始时间**排序，小根堆里保存「正在使用的会议室的**结束时间**」。\n\n对每个会议：若堆顶（最早结束的）$\\le$ 当前开始时间，说明可以**复用**那间会议室（弹出）；然后压入当前会议的结束时间。\n\n最终堆的大小就是所需会议室数。\n\n> **关键**：用 `<=` 判断（区间左闭右开），若题目规定端点不能相接则改成 `<`。",
)

# ---------------------------------------------------------------- 15
def s_max_heap_check(t):
    n, a = arr(t)
    ok = all(a[(i - 1) // 2] >= a[i] for i in range(1, n))
    return ("YES\n" if ok else "NO\n")


add(
    pid="heap-max-heap-check", title="判断是否为大根堆", difficulty="入门",
    tags=["堆", "数组", "树"], source="堆性质检验", url="https://leetcode.cn/problems/minimum-absolute-difference-in-bst/",
    statement="给定一个按**层序**存储的完全二叉树（数组形式），判断它是否满足**大根堆性质**：\n\n**每个节点**的值都不小于它的两个孩子。\n\n是则输出 `YES`，否则 `NO`。\n\n下标规则：节点 $i$ 的孩子是 $2i+1$ 与 $2i+2$（下标从 $0$ 开始）。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数（$|a_i| \\le 10^9$）。",
    output_format="一行，输出 `YES` 或 `NO`。",
    constraints=["1 ≤ n ≤ 10^5", "|a_i| ≤ 10^9"],
    solver=s_max_heap_check,
    specs=[("样例 1（是）", "5\n9 7 5 3 1", 10), ("样例 2（不是）", "5\n9 5 7 3 1", 10),
           ("单元素", "1\n7", 15), ("全相同", "4\n5 5 5 5", 15),
           ("严格递减", "6\n6 5 4 3 2 1", 20), ("含负数", "5\n0 -1 -2 -3 -4", 20),
           ("根不是最大", "3\n1 5 2", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
bool ok=true;
for(int i=1;i<n;++i)if(a[(i-1)/2]<a[i]){ok=false;break;}
printf("%s\\n",ok?"YES":"NO");return 0;}
""",
    hint="**与「判断小根堆」对称**：对每个下标 $i \\ge 1$，检查 `a[(i-1)/2] >= a[i]`。\n\n时间 $O(n)$，空间 $O(1)$。",
)

# ---------------------------------------------------------------- 16
def s_median_window(t):
    v = numbers(t)
    n, k = v[0], v[1]
    a = v[2:2 + n]
    out = []
    for i in range(n - k + 1):
        w = sorted(a[i:i + k])
        out.append(str(w[(k - 1) // 2]))
    return " ".join(out) + "\n"


add(
    pid="heap-window-median", title="滑动窗口中位数", difficulty="困难",
    tags=["堆", "滑动窗口", "对顶堆"], source="LeetCode 480", url="https://leetcode.cn/problems/sliding-window-median/",
    statement="给定数组和窗口大小 $k$，窗口从左向右滑动，求**每个窗口的中位数**（下中位数，即排序后第 $\\lceil k/2 \\rceil$ 个）。\n\n输出为整数。",
    input_format="第一行两个整数 $n, k$（$1 \\le k \\le n \\le 2000$）。\n\n第二行 $n$ 个整数（$|a_i| \\le 10^9$）。",
    output_format="一行 $n-k+1$ 个整数，依次为各窗口的中位数。",
    constraints=["1 ≤ k ≤ n ≤ 2000", "|a_i| ≤ 10^9", "取排序后第 ceil(k/2) 个"],
    solver=s_median_window,
    specs=[("样例 1", "8 3\n1 3 -1 -3 5 3 6 7", 10), ("k = 1", "3 1\n2 1 3", 10),
           ("k = n 奇数", "5 5\n1 2 3 4 5", 15), ("k = n 偶数", "4 4\n1 2 3 4", 15),
           ("全相同", "4 2\n5 5 5 5", 20), ("含负数", "5 3\n-1 -2 -3 -4 -5", 20),
           ("递增", "5 3\n1 2 3 4 5", 20)],
    cpp=CPP_HEADER + """int main(){int n,k;scanf("%d %d",&n,&k);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
bool first=true;
for(int i=0;i+k<=n;++i){
vector<long long>w(a.begin()+i,a.begin()+i+k);
sort(w.begin(),w.end());
if(!first)printf(" ");printf("%lld",w[(k-1)/2]);first=false;}
printf("\\n");return 0;}
""",
    hint="**暴力（本题数据够用）**：对每个窗口排序后取中间元素。时间 $O(n k \\log k)$。\n\n**标准解法：对顶堆 + 惰性删除**——用大根堆和小根堆分别维护窗口的较小半与较大半，每滑动一格就插入新元素、标记过期元素，再平衡两堆。时间 $O(n\\log k)$。\n\n> **易错点**：对顶堆在滑动窗口场景下必须处理**过期元素的惰性删除**（堆顶若已滑出窗口就弹出），这是本题的最大难点。",
)


def main() -> None:
    for p in P:
        finalize(p, OUT / f"{p['id']}.json")
        total = sum(t["score"] for t in p["tests"])
        print(f"生成 {p['id']:34s} {len(p['tests'])} 测试点, 总分 {total:3d}")


if __name__ == "__main__":
    main()
