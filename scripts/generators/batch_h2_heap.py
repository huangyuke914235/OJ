"""堆与优先队列 · 批量 H2（14 道）。"""
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


def join(a):
    return " ".join(map(str, a)) + "\n"


# ---------------------------------------------------------------- 1
def s_kth_largest_stream_offline(t):
    ls = t.strip("\n").split("\n")
    n, k = map(int, ls[0].split())
    a = list(map(int, ls[1].split()))
    s = sorted(a, reverse=True)
    return f"{s[k - 1]}\n"


add(
    pid="heap-kth-largest-sort", title="第 K 大元素（排序解法）", difficulty="入门",
    tags=["堆", "排序", "Top-K"], source="LeetCode 215", url="https://leetcode.cn/problems/kth-largest-element-in-an-array/",
    statement="给定数组和整数 $k$，求数组中**第 $k$ 大**的元素。\n\n> 本题用于对比：直接排序取第 $k$ 个（$O(n\\log n)$）与用堆（$O(n\\log k)$）的差异。",
    input_format="第一行两个整数 $n, k$（$1 \\le k \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数（$|a_i| \\le 10^9$）。",
    output_format="一行一个整数。",
    constraints=["1 ≤ k ≤ n ≤ 10^5", "|a_i| ≤ 10^9"],
    solver=s_kth_largest_stream_offline,
    specs=[("样例 1", "6 2\n3 2 1 5 6 4", 10), ("k = 1", "3 1\n3 2 1", 10),
           ("k = n", "4 4\n1 2 3 4", 15), ("全相同", "4 2\n5 5 5 5", 15),
           ("含负数", "5 3\n-1 -2 -3 -4 -5", 20), ("单元素", "1 1\n7", 20)],
    cpp=CPP_HEADER + """int main(){int n,k;scanf("%d %d",&n,&k);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
sort(a.rbegin(),a.rend());
printf("%lld\\n",a[k-1]);return 0;}
""",
    hint="**排序解法**：降序排序后取第 $k$ 个。时间 $O(n\\log n)$。\n\n> **堆解法更优**：维护大小为 $k$ 的**小根堆**，时间 $O(n\\log k)$、空间 $O(k)$，适合 $n$ 很大而 $k$ 很小、或数据流场景。",
)

# ---------------------------------------------------------------- 2
def s_kth_largest_quickselect(t):
    ls = t.strip("\n").split("\n")
    n, k = map(int, ls[0].split())
    a = list(map(int, ls[1].split()))
    target = n - k        # 升序下第 k 大 = 下标 n-k
    lo, hi = 0, n - 1
    while lo <= hi:
        pivot = a[(lo + hi) // 2]
        i, j = lo, hi
        while i <= j:
            while a[i] < pivot:
                i += 1
            while a[j] > pivot:
                j -= 1
            if i <= j:
                a[i], a[j] = a[j], a[i]
                i += 1
                j -= 1
        if target <= j:
            hi = j
        elif target >= i:
            lo = i
        else:
            break
    return f"{a[target]}\n"


add(
    pid="heap-kth-largest-quickselect", title="第 K 大元素（快速选择）", difficulty="中等",
    tags=["快速选择", "分治", "Top-K"], source="LeetCode 215", url="https://leetcode.cn/problems/kth-largest-element-in-an-array/",
    statement="给定数组和整数 $k$，求**第 $k$ 大**的元素。\n\n**要求**：用**快速选择**算法，平均时间 $O(n)$，不需要完整排序。",
    input_format="第一行两个整数 $n, k$（$1 \\le k \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数（$|a_i| \\le 10^9$）。",
    output_format="一行一个整数。",
    constraints=["1 ≤ k ≤ n ≤ 10^5", "|a_i| ≤ 10^9", "平均 O(n)"],
    solver=s_kth_largest_quickselect,
    specs=[("样例 1", "6 2\n3 2 1 5 6 4", 10), ("k = 1", "3 1\n3 2 1", 10),
           ("k = n", "4 4\n1 2 3 4", 15), ("全相同", "4 2\n5 5 5 5", 15),
           ("含负数", "5 3\n-1 -2 -3 -4 -5", 20), ("单元素", "1 1\n7", 20)],
    cpp=CPP_HEADER + """int main(){int n,k;scanf("%d %d",&n,&k);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
int target=n-k,lo=0,hi=n-1;
while(lo<=hi){
long long p=a[(lo+hi)/2];
int i=lo,j=hi;
while(i<=j){
while(a[i]<p)++i;
while(a[j]>p)--j;
if(i<=j){swap(a[i],a[j]);++i;--j;}}
if(target<=j)hi=j;else if(target>=i)lo=i;else break;}
printf("%lld\\n",a[target]);return 0;}
""",
    hint="**快速选择（Quickselect）**：\n\n1. 选定一个基准，把数组**划分为「小于基准」和「大于基准」两部分**；\n2. 若目标下标落在某一侧，**只递归那一侧**——另一侧完全不用管。\n\n因为每次平均能排除一半，总时间 $O(n)$。\n\n> **易错点**：基准要**随机化**（本题取中间位置），否则有序输入会退化成 $O(n^2)$。",
)

# ---------------------------------------------------------------- 3
def s_merge_k_lists(t):
    ls = t.strip("\n").split("\n")
    k = int(ls[0])
    arrs = []
    for i in range(k):
        parts = ls[i + 1].split()
        arrs.append(list(map(int, parts[1:])) if parts else [])
    h = []
    for i, a in enumerate(arrs):
        if a:
            heapq.heappush(h, (a[0], i, 0))
    res = []
    while h:
        v, i, j = heapq.heappop(h)
        res.append(v)
        if j + 1 < len(arrs[i]):
            heapq.heappush(h, (arrs[i][j + 1], i, j + 1))
    return join(res)


add(
    pid="heap-merge-k-lists", title="合并 K 个有序数组（小根堆）", difficulty="中等",
    tags=["堆", "优先队列", "多路归并"], source="LeetCode 23", url="https://leetcode.cn/problems/merge-k-sorted-lists/",
    statement="给定 $k$ 个**非递减**数组，把它们合并为一个非递减数组并输出。\n\n**要求**：用小根堆做多路归并，时间 $O(N\\log k)$（$N$ 为元素总数）。",
    input_format="第一行一个整数 $k$（$1 \\le k \\le 100$）。\n\n接下来 $k$ 行，每行先是一个整数 $m_i$（该数组长度），随后 $m_i$ 个整数（非递减）。",
    output_format="一行，合并后的非递减序列。",
    constraints=["1 ≤ k ≤ 100", "每个数组非递减", "元素总数 ≤ 10^4"],
    solver=s_merge_k_lists,
    specs=[("样例 1", "3\n3 1 4 5\n2 1 3\n3 2 6 7", 10),
           ("单数组", "1\n3 1 2 3", 10),
           ("含空数组", "3\n0\n2 1 2\n0", 15),
           ("全空", "2\n0\n0", 15),
           ("全相同", "2\n2 1 1\n2 1 1", 20),
           ("含负数", "2\n2 -3 -1\n2 -2 0", 20)],
    cpp=CPP_HEADER + """int main(){int k;scanf("%d",&k);
vector<vector<long long>>arr(k);
for(int i=0;i<k;++i){int m;scanf("%d",&m);arr[i].resize(m);
for(int j=0;j<m;++j)scanf("%lld",&arr[i][j]);}
priority_queue<tuple<long long,int,int>,vector<tuple<long long,int,int>>,greater<>>pq;
for(int i=0;i<k;++i)if(!arr[i].empty())pq.push({arr[i][0],i,0});
bool first=true;
while(!pq.empty()){auto [v,i,j]=pq.top();pq.pop();
if(!first)printf(" ");printf("%lld",v);first=false;
if(j+1<(int)arr[i].size())pq.push({arr[i][j+1],i,j+1});}
printf("\\n");return 0;}
""",
    hint="**多路归并**：小根堆中存 `(值, 数组编号, 该数组内下标)`。\n\n每次弹出堆顶（全局最小值）输出，然后**把同一数组的下一个元素压入堆**。\n\n> **为什么比两两合并快**：两两合并是 $O(Nk)$，多路归并是 $O(N\\log k)$。",
)

# ---------------------------------------------------------------- 4
def s_k_closest_small(t):
    ls = t.strip("\n").split("\n")
    n, k = map(int, ls[0].split())
    a = list(map(int, ls[1].split()))
    # 小根堆：堆顶是「已保留的 k 个中最小」的，超出 k 就弹掉最小的
    h = []
    for x in a:
        heapq.heappush(h, x)
        if len(h) > k:
            heapq.heappop(h)
    res = sorted(h)
    return join(res)


add(
    pid="heap-k-largest-values", title="最大的 K 个数", difficulty="简单",
    tags=["堆", "优先队列", "Top-K"], source="Top-K 变体", url="https://leetcode.cn/problems/kth-largest-element-in-an-array/",
    statement="给定数组和整数 $k$，找出其中**最大的 $k$ 个数**，按**升序**输出。\n\n**要求**：用小根堆维护，时间 $O(n\\log k)$。",
    input_format="第一行两个整数 $n, k$（$1 \\le k \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数（$|a_i| \\le 10^9$）。",
    output_format="一行 $k$ 个整数，升序排列。",
    constraints=["1 ≤ k ≤ n ≤ 10^5", "|a_i| ≤ 10^9", "要求 O(n log k)"],
    solver=s_k_closest_small,
    specs=[("样例 1", "6 2\n3 2 1 5 6 4", 10), ("k = 1", "3 1\n3 2 1", 10),
           ("k = n", "4 4\n1 2 3 4", 15), ("全相同", "4 2\n5 5 5 5", 15),
           ("含负数", "5 2\n-1 -2 -3 -4 -5", 20), ("单元素", "1 1\n7", 20)],
    cpp=CPP_HEADER + """int main(){int n,k;scanf("%d %d",&n,&k);
priority_queue<long long,vector<long long>,greater<long long>>pq;
for(int i=0;i<n;++i){long long x;scanf("%lld",&x);pq.push(x);
if((int)pq.size()>k)pq.pop();}
vector<long long>r;while(!pq.empty()){r.push_back(pq.top());pq.pop();}
sort(r.begin(),r.end());
for(int i=0;i<k;++i){if(i)printf(" ");printf("%lld",r[i]);}
printf("\\n");return 0;}
""",
    hint="**大小为 $k$ 的小根堆**：堆顶是「当前最大的 $k$ 个数」中**最小**的那个。\n\n遇到比堆顶大的元素就替换堆顶。最后堆中就是最大的 $k$ 个数，排序后输出。\n\n> **对比**：「第 $k$ 大」只需输出堆顶；「最大的 $k$ 个」要把堆内全部输出。",
)

# ---------------------------------------------------------------- 5
def s_priority_queue_sim(t):
    ls = t.strip("\n").split("\n")
    q = int(ls[0])
    h = []
    out = []
    for i in range(1, q + 1):
        p = ls[i].split()
        if p[0] == "push":
            heapq.heappush(h, int(p[1]))
        elif p[0] == "pop":
            out.append(str(heapq.heappop(h)))
        elif p[0] == "top":
            out.append(str(h[0]))
        elif p[0] == "size":
            out.append(str(len(h)))
    return ("\n".join(out) + "\n") if out else "\n"


add(
    pid="heap-priority-queue-ops", title="小根堆的操作模拟", difficulty="入门",
    tags=["堆", "优先队列", "模拟"], source="堆基础", url="https://leetcode.cn/problems/kth-largest-element-in-an-array/",
    statement="模拟一个小根堆（优先队列），支持：\n\n- `push x`：插入 $x$；\n- `pop`：弹出并输出**最小值**；\n- `top`：输出最小值（不弹出）；\n- `size`：输出元素个数。\n\n**保证** `pop` / `top` 只在非空堆上调用。",
    input_format="第一行一个整数 $q$（$1 \\le q \\le 10^5$）。\n\n接下来 $q$ 行，每行一个操作（$|x| \\le 10^9$）。",
    output_format="对每个有输出的操作输出一行。",
    constraints=["1 ≤ q ≤ 10^5", "|x| ≤ 10^9", "pop/top 仅在非空堆上调用"],
    solver=s_priority_queue_sim,
    specs=[("样例 1", "5\npush 3\npush 1\ntop\npop\nsize", 10),
           ("递增插入", "4\npush 1\npush 2\npush 3\npop", 10),
           ("递减插入", "4\npush 3\npush 2\npush 1\npop", 15),
           ("只查询", "3\npush 5\ntop\nsize", 15),
           ("含负数", "4\npush -1\npush -2\ntop\npop", 20),
           ("反复操作", "6\npush 9\npop\npush 8\ntop\nsize\npop", 20)],
    cpp=CPP_HEADER + """int main(){int q;scanf("%d",&q);
priority_queue<long long,vector<long long>,greater<long long>>pq;char op[16];
for(int i=0;i<q;++i){scanf("%s",op);string o=op;
if(o=="push"){long long x;scanf("%lld",&x);pq.push(x);}
else if(o=="pop"){printf("%lld\\n",pq.top());pq.pop();}
else if(o=="top"){printf("%lld\\n",pq.top());}
else if(o=="size"){printf("%d\\n",(int)pq.size());}}
return 0;}
""",
    hint="**小根堆**：`top()` / `pop()` 得到的都是当前**最小值**。\n\nC++ 用 `priority_queue<T, vector<T>, greater<T>>`；Python 的 `heapq` 本身就是小根堆。\n\n> **大根堆**：C++ 去掉 `greater` 即可；Python 要存**负数**。",
)

# ---------------------------------------------------------------- 6
def s_max_heap_ops(t):
    ls = t.strip("\n").split("\n")
    q = int(ls[0])
    h = []
    out = []
    for i in range(1, q + 1):
        p = ls[i].split()
        if p[0] == "push":
            heapq.heappush(h, -int(p[1]))
        elif p[0] == "pop":
            out.append(str(-heapq.heappop(h)))
        elif p[0] == "top":
            out.append(str(-h[0]))
        elif p[0] == "size":
            out.append(str(len(h)))
    return ("\n".join(out) + "\n") if out else "\n"


add(
    pid="heap-max-heap-ops", title="大根堆的操作模拟", difficulty="入门",
    tags=["堆", "优先队列", "模拟"], source="堆基础", url="https://leetcode.cn/problems/kth-largest-element-in-an-array/",
    statement="模拟一个**大根堆**，支持 `push x`、`pop`（输出最大值）、`top`（输出最大值）、`size`。\n\n**保证** `pop` / `top` 只在非空堆上调用。",
    input_format="第一行一个整数 $q$（$1 \\le q \\le 10^5$）。\n\n接下来 $q$ 行，每行一个操作（$|x| \\le 10^9$）。",
    output_format="对每个有输出的操作输出一行。",
    constraints=["1 ≤ q ≤ 10^5", "|x| ≤ 10^9", "pop/top 仅在非空堆上调用"],
    solver=s_max_heap_ops,
    specs=[("样例 1", "5\npush 3\npush 1\ntop\npop\nsize", 10),
           ("递增插入", "4\npush 1\npush 2\npush 3\npop", 10),
           ("递减插入", "4\npush 3\npush 2\npush 1\npop", 15),
           ("只查询", "3\npush 5\ntop\nsize", 15),
           ("含负数", "4\npush -1\npush -2\ntop\npop", 20),
           ("反复操作", "6\npush 9\npop\npush 8\ntop\nsize\npop", 20)],
    cpp=CPP_HEADER + """int main(){int q;scanf("%d",&q);
priority_queue<long long>pq;char op[16];
for(int i=0;i<q;++i){scanf("%s",op);string o=op;
if(o=="push"){long long x;scanf("%lld",&x);pq.push(x);}
else if(o=="pop"){printf("%lld\\n",pq.top());pq.pop();}
else if(o=="top"){printf("%lld\\n",pq.top());}
else if(o=="size"){printf("%d\\n",(int)pq.size());}}
return 0;}
""",
    hint="**大根堆**：`top()` / `pop()` 得到当前**最大值**。\n\nC++ 的 `priority_queue<long long>` **默认就是大根堆**；Python 的 `heapq` 是小根堆，需**存负数**来模拟。",
)

# ---------------------------------------------------------------- 7
def s_k_smallest_values(t):
    ls = t.strip("\n").split("\n")
    n, k = map(int, ls[0].split())
    a = list(map(int, ls[1].split()))
    h = []
    for x in a:
        heapq.heappush(h, -x)
        if len(h) > k:
            heapq.heappop(h)
    res = sorted(-x for x in h)
    return join(res)


add(
    pid="heap-k-smallest-values", title="最小的 K 个数", difficulty="简单",
    tags=["堆", "优先队列", "Top-K"], source="Top-K 变体", url="https://leetcode.cn/problems/kth-largest-element-in-an-array/",
    statement="给定数组和整数 $k$，找出其中**最小的 $k$ 个数**，按**升序**输出。\n\n**要求**：用**大根堆**维护，时间 $O(n\\log k)$。",
    input_format="第一行两个整数 $n, k$（$1 \\le k \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数（$|a_i| \\le 10^9$）。",
    output_format="一行 $k$ 个整数，升序排列。",
    constraints=["1 ≤ k ≤ n ≤ 10^5", "|a_i| ≤ 10^9", "要求 O(n log k)"],
    solver=s_k_smallest_values,
    specs=[("样例 1", "6 2\n3 2 1 5 6 4", 10), ("k = 1", "3 1\n3 2 1", 10),
           ("k = n", "4 4\n1 2 3 4", 15), ("全相同", "4 2\n5 5 5 5", 15),
           ("含负数", "5 2\n-1 -2 -3 -4 -5", 20), ("单元素", "1 1\n7", 20)],
    cpp=CPP_HEADER + """int main(){int n,k;scanf("%d %d",&n,&k);
priority_queue<long long>pq;
for(int i=0;i<n;++i){long long x;scanf("%lld",&x);pq.push(x);
if((int)pq.size()>k)pq.pop();}
vector<long long>r;while(!pq.empty()){r.push_back(pq.top());pq.pop();}
sort(r.begin(),r.end());
for(int i=0;i<k;++i){if(i)printf(" ");printf("%lld",r[i]);}
printf("\\n");return 0;}
""",
    hint="**大小为 $k$ 的大根堆**：堆中保存「当前最小的 $k$ 个数」，堆顶是其中**最大**的。\n\n遇到比堆顶小的元素就替换堆顶。最后堆中就是最小的 $k$ 个数，排序后输出。\n\n> **对比**：「最大的 $k$ 个」用**小根堆**，方向正好相反。",
)

# ---------------------------------------------------------------- 8
def s_heap_sort_desc(t):
    n = int(t.strip().split("\n")[0])
    a = list(map(int, t.strip().split("\n")[1].split()))
    h = [-x for x in a]
    heapq.heapify(h)
    res = [-heapq.heappop(h) for _ in range(n)]
    return join(res)


add(
    pid="heap-sort-desc", title="堆排序（降序）", difficulty="简单",
    tags=["堆", "排序"], source="经典堆排序", url="https://leetcode.cn/problems/sort-an-array/",
    statement="用**堆排序**把数组**降序**排列并输出。\n\n**要求**：时间 $O(n\\log n)$。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数（$|a_i| \\le 10^9$）。",
    output_format="一行 $n$ 个整数，降序排列。",
    constraints=["1 ≤ n ≤ 10^5", "|a_i| ≤ 10^9", "要求 O(n log n)"],
    solver=s_heap_sort_desc,
    specs=[("样例 1", "5\n3 1 4 1 5", 10), ("已有序", "4\n1 2 3 4", 10),
           ("逆序", "4\n4 3 2 1", 15), ("单元素", "1\n7", 15),
           ("全相同", "4\n2 2 2 2", 20), ("含负数", "5\n-1 0 -3 2 -2", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
priority_queue<long long>pq(a.begin(),a.end());
bool first=true;
while(!pq.empty()){if(!first)printf(" ");printf("%lld",pq.top());pq.pop();first=false;}
printf("\\n");return 0;}
""",
    hint="**大根堆逐个弹出**：把元素放入**大根堆**，反复弹出堆顶——弹出顺序就是降序。\n\n时间 $O(n\\log n)$（建堆 $O(n)$ + $n$ 次弹出）。",
)

# ---------------------------------------------------------------- 9
def s_min_cost_hire_small(t):
    ls = t.strip("\n").split("\n")
    n, k = map(int, ls[0].split())
    a = list(map(int, ls[1].split()))
    # 大根堆保留「最小的 k 个」，被弹出来的就是最大的 n-k 个，累加它们
    h = []
    total = 0
    for x in a:
        heapq.heappush(h, -x)
        if len(h) > k:
            total += -heapq.heappop(h)
    return f"{total}\n"


add(
    pid="heap-min-cost-remove", title="删除最小的 K 个数后的总和", difficulty="简单",
    tags=["堆", "优先队列", "Top-K"], source="Top-K 变体", url="https://leetcode.cn/problems/kth-largest-element-in-an-array/",
    statement="给定数组和整数 $k$，**删除其中最小的 $k$ 个数**，求剩余元素之和。\n\n**要求**：用小根堆维护最小的 $k$ 个，时间 $O(n\\log k)$。",
    input_format="第一行两个整数 $n, k$（$1 \\le k \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数（$|a_i| \\le 10^9$）。",
    output_format="一行一个整数，表示剩余元素之和。",
    constraints=["1 ≤ k ≤ n ≤ 10^5", "|a_i| ≤ 10^9"],
    solver=s_min_cost_hire_small,
    specs=[("样例 1", "5 2\n3 1 4 1 5", 10), ("k = 1", "3 1\n3 2 1", 10),
           ("k = n", "4 4\n1 2 3 4", 15), ("全相同", "4 2\n5 5 5 5", 15),
           ("含负数", "5 2\n-1 -2 -3 -4 -5", 20), ("单元素", "1 1\n7", 20)],
    cpp=CPP_HEADER + """int main(){int n,k;scanf("%d %d",&n,&k);
priority_queue<long long>pq;long long total=0;
for(int i=0;i<n;++i){long long x;scanf("%lld",&x);
pq.push(x);
if((int)pq.size()>k)total+=pq.top(),pq.pop();}
printf("%lld\\n",total);return 0;}
""",
    hint="**大小为 $k$ 的大根堆**：堆中保存「当前最小的 $k$ 个数」，堆顶是其中最大的。\n\n当堆大小超过 $k$ 时，弹出的元素就是「被排除在最小的 $k$ 个之外」的，累加它们即可。\n\n> **等价说法**：答案是「总和 − 最小的 $k$ 个数之和」。",
)

# ---------------------------------------------------------------- 10
def s_ugly_number(t):
    n = int(t.strip())
    h = [1]
    seen = {1}
    cur = 1
    for _ in range(n):
        cur = heapq.heappop(h)
        for f in (2, 3, 5):
            v = cur * f
            if v not in seen:
                seen.add(v)
                heapq.heappush(h, v)
    return f"{cur}\n"


add(
    pid="heap-ugly-number", title="丑数 II", difficulty="中等",
    tags=["堆", "优先队列", "数学"], source="LeetCode 264", url="https://leetcode.cn/problems/ugly-number-ii/",
    statement="**丑数**指只含质因子 $2$、$3$、$5$ 的正整数（$1$ 也是丑数）。\n\n求第 $n$ 个丑数（按从小到大排序）。",
    input_format="一行一个整数 $n$（$1 \\le n \\le 1690$）。",
    output_format="一行一个整数，表示第 $n$ 个丑数。",
    constraints=["1 ≤ n ≤ 1690", "丑数只含质因子 2、3、5"],
    solver=s_ugly_number,
    specs=[("样例 1", "10", 10), ("n = 1", "1", 10), ("n = 2", "2", 15),
           ("n = 7", "7", 15), ("n = 100", "100", 20), ("n = 1690", "1690", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);
priority_queue<long long,vector<long long>,greater<long long>>pq;
set<long long>seen;pq.push(1);seen.insert(1);
long long cur=1;
for(int i=0;i<n;++i){cur=pq.top();pq.pop();
for(long long f:{2LL,3LL,5LL}){
long long v=cur*f;
if(!seen.count(v)){seen.insert(v);pq.push(v);}}}
printf("%lld\\n",cur);return 0;}
""",
    hint="**小根堆 + 去重**：\n\n1. 初始把 1 放入小根堆；\n2. 每次弹出堆顶（当前最小丑数），**把它乘 2、3、5 后的结果压入堆**；\n3. 用集合**去重**（否则 6 会由 2×3 和 3×2 重复产生）。\n\n第 $n$ 次弹出的就是第 $n$ 个丑数。\n\n> **另解（三指针 DP）**：维护三个指针分别指向「×2」「×3」「×5」的位置，每次取三者最小值推进，时间 $O(n)$、空间 $O(n)$，是本题最优解。",
)

# ---------------------------------------------------------------- 11
def s_min_meeting_rooms(t):
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
    pid="heap-meeting-rooms-min", title="最少会议室数", difficulty="中等",
    tags=["堆", "优先队列", "区间"], source="LeetCode 253", url="https://leetcode.cn/problems/meeting-rooms-ii/",
    statement="给定若干会议时间区间 $[start, end)$，求**至少需要多少间会议室**。\n\n区间**左闭右开**：会议在 `end` 时刻结束，另一场可以在同一时刻开始。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 10^4$）。\n\n接下来 $n$ 行，每行两个整数 $start, end$（$0 \\le start < end \\le 10^6$）。",
    output_format="一行一个整数，表示最少会议室数。",
    constraints=["1 ≤ n ≤ 10^4", "0 ≤ start < end ≤ 10^6", "区间左闭右开"],
    solver=s_min_meeting_rooms,
    specs=[("样例 1", "3\n0 30\n5 10\n15 20", 10), ("无重叠", "3\n7 10\n2 4\n1 3", 10),
           ("全重叠", "3\n1 5\n1 5\n1 5", 15), ("首尾相接", "2\n1 2\n2 3", 15),
           ("单会议", "1\n0 5", 20), ("阶梯式", "4\n1 2\n2 3\n3 4\n4 5", 20)],
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
    hint="**排序 + 小根堆**：按开始时间排序，小根堆保存「正在进行的会议的结束时间」。\n\n对每场会议：若堆顶（最早结束的）**不大于**当前开始时间，可以**复用**那间会议室；然后压入当前会议的结束时间。\n\n最终堆的大小即所需会议室数。",
)

# ---------------------------------------------------------------- 12
def s_heap_top_k_words(t):
    ls = t.strip("\n").split("\n")
    n, k = map(int, ls[0].split())
    words = ls[1].split()
    cnt = Counter(words)
    items = sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))
    return " ".join(w for w, _ in items[:k]) + "\n"


add(
    pid="heap-top-k-words", title="前 K 个高频单词", difficulty="中等",
    tags=["堆", "优先队列", "哈希表"], source="LeetCode 692", url="https://leetcode.cn/problems/top-k-frequent-words/",
    statement="给定一组单词和整数 $k$，返回**出现频率最高的 $k$ 个单词**。\n\n**输出要求**：按「频率降序；频率相同则字典序升序」排列，以空格分隔。",
    input_format="第一行两个整数 $n, k$（$1 \\le k \\le$ 不同单词数 $\\le n \\le 10^4$）。\n\n第二行 $n$ 个小写字母单词，以空格分隔。",
    output_format="一行 $k$ 个单词。",
    constraints=["1 ≤ n ≤ 10^4", "仅小写字母", "按 (频率降序, 字典序升序) 输出"],
    solver=s_heap_top_k_words,
    specs=[("样例 1", "6 2\ni love leetcode i love coding", 10),
           ("全不同", "3 2\na b c", 10), ("全相同", "3 1\na a a", 15),
           ("频率相同", "4 3\nb a d c", 15),
           ("混合", "8 2\nthe the a a b b c d", 20),
           ("k 等于总数", "3 3\nx y z", 20)],
    cpp=CPP_HEADER + """int main(){int n,k;scanf("%d %d",&n,&k);
unordered_map<string,int>c;
for(int i=0;i<n;++i){string w;cin>>w;++c[w];}
vector<pair<string,int>>v(c.begin(),c.end());
sort(v.begin(),v.end(),[](const auto&a,const auto&b){
if(a.second!=b.second)return a.second>b.second;
return a.first<b.first;});
for(int i=0;i<k;++i){if(i)printf(" ");printf("%s",v[i].first.c_str());}
printf("\\n");return 0;}
""",
    hint="**哈希计数 + 双关键字排序**：\n\n1. 用哈希表统计每个单词的频率；\n2. 按「频率**降序**，频率相同则单词**字典序升序**」排序，取前 $k$ 个。\n\n> **易错点**：必须写成**双关键字**比较，只比频率会导致输出顺序不稳定。\n\n> **堆解法**：维护大小为 $k$ 的堆，比较规则反过来（频率低、字典序大的优先被弹出），时间 $O(n\\log k)$。",
)

# ---------------------------------------------------------------- 13
def s_sliding_window_median_small(t):
    ls = t.strip("\n").split("\n")
    n, k = map(int, ls[0].split())
    a = list(map(int, ls[1].split()))
    out = []
    for i in range(n - k + 1):
        w = sorted(a[i:i + k])
        out.append(str(w[(k - 1) // 2]))
    return " ".join(out) + "\n"


add(
    pid="heap-window-median-basic", title="窗口内的中位数（基础版）", difficulty="简单",
    tags=["堆", "滑动窗口", "排序"], source="LeetCode 480 简化版", url="https://leetcode.cn/problems/sliding-window-median/",
    statement="给定数组和窗口大小 $k$，求每个窗口内的**中位数**（下中位数，即排序后第 $\\lceil k/2 \\rceil$ 个）。\n\n> 本题数据规模较小，直接对每个窗口排序即可；大规模场景需用**对顶堆 + 惰性删除**。",
    input_format="第一行两个整数 $n, k$（$1 \\le k \\le n \\le 2000$）。\n\n第二行 $n$ 个整数（$|a_i| \\le 10^9$）。",
    output_format="一行 $n-k+1$ 个整数。",
    constraints=["1 ≤ k ≤ n ≤ 2000", "|a_i| ≤ 10^9"],
    solver=s_sliding_window_median_small,
    specs=[("样例 1", "8 3\n1 3 -1 -3 5 3 6 7", 10), ("k = 1", "3 1\n2 1 3", 10),
           ("k = n", "5 5\n1 2 3 4 5", 15), ("全相同", "4 2\n5 5 5 5", 15),
           ("含负数", "5 3\n-1 -2 -3 -4 -5", 20), ("递增", "5 3\n1 2 3 4 5", 20)],
    cpp=CPP_HEADER + """int main(){int n,k;scanf("%d %d",&n,&k);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
bool first=true;
for(int i=0;i+k<=n;++i){
vector<long long>w(a.begin()+i,a.begin()+i+k);
sort(w.begin(),w.end());
if(!first)printf(" ");printf("%lld",w[(k-1)/2]);first=false;}
printf("\\n");return 0;}
""",
    hint="**暴力解法**：对每个窗口排序后取中间元素，时间 $O(nk\\log k)$。\n\n> **对顶堆解法**：大根堆存较小的一半、小根堆存较大的一半，每滑动一格就插入新元素并平衡两堆；**难点在于处理滑出窗口的元素的惰性删除**。",
)

# ---------------------------------------------------------------- 14
def s_kth_smallest_matrix(t):
    ls = t.strip("\n").split("\n")
    r, c, k = map(int, ls[0].split())
    g = [list(map(int, ls[i + 1].split())) for i in range(r)]
    h = []
    for i in range(min(r, k)):
        heapq.heappush(h, (g[i][0], i, 0))
    val = 0
    for _ in range(k):
        val, i, j = heapq.heappop(h)
        if j + 1 < c:
            heapq.heappush(h, (g[i][j + 1], i, j + 1))
    return f"{val}\n"


add(
    pid="heap-kth-smallest-matrix", title="有序矩阵中第 K 小的元素", difficulty="中等",
    tags=["堆", "优先队列", "矩阵"], source="LeetCode 378", url="https://leetcode.cn/problems/kth-smallest-element-in-a-sorted-matrix/",
    statement="给定一个 $r \\times c$ 矩阵，**每行每列都升序**。\n\n求矩阵中**第 $k$ 小**的元素。\n\n**要求**：用小根堆做多路归并，时间 $O(k\\log r)$。",
    input_format="第一行三个整数 $r, c, k$（$1 \\le r, c \\le 200$，$1 \\le k \\le rc$）。\n\n接下来 $r$ 行，每行 $c$ 个整数（每行每列均非递减）。",
    output_format="一行一个整数。",
    constraints=["1 ≤ r, c ≤ 200", "1 ≤ k ≤ rc", "每行每列非递减"],
    solver=s_kth_smallest_matrix,
    specs=[("样例 1", "3 3 5\n1 5 9\n10 11 13\n12 13 15", 10),
           ("k = 1", "2 2 1\n1 2\n3 4", 10), ("k = rc", "2 2 4\n1 2\n3 4", 15),
           ("单行", "1 4 2\n1 2 3 4", 15), ("单列", "4 1 3\n1\n2\n3\n4", 20),
           ("全相同", "2 2 3\n5 5\n5 5", 20)],
    cpp=CPP_HEADER + """int main(){int r,c,k;scanf("%d %d %d",&r,&c,&k);
vector<vector<long long>>g(r,vector<long long>(c));
for(int i=0;i<r;++i)for(int j=0;j<c;++j)scanf("%lld",&g[i][j]);
priority_queue<tuple<long long,int,int>,vector<tuple<long long,int,int>>,greater<>>pq;
for(int i=0;i<min(r,k);++i)pq.push({g[i][0],i,0});
long long val=0;
for(int t=0;t<k;++t){auto [v,i,j]=pq.top();pq.pop();val=v;
if(j+1<c)pq.push({g[i][j+1],i,j+1});}
printf("%lld\\n",val);return 0;}
""",
    hint="**多路归并**：把每一行看作一个有序序列，用**小根堆**做多路归并。\n\n堆中存 `(值, 行号, 列号)`，每次弹出最小值后把**同一行的下一个元素**压入。弹出第 $k$ 次时的值就是答案。\n\n> **剪枝**：只需把前 $\\min(r, k)$ 行的首元素入堆（第 $k+1$ 行之后的首元素不可能进入前 $k$ 小）。\n\n> **另解（二分）**：对答案值二分，统计矩阵中 $\\le mid$ 的元素个数，做到 $O(n\\log(\\text{值域}))$。",
)


def main() -> None:
    for p in P:
        finalize(p, OUT / f"{p['id']}.json")
        total = sum(t["score"] for t in p["tests"])
        print(f"生成 {p['id']:38s} {len(p['tests'])} 测试点, 总分 {total:3d}")


if __name__ == "__main__":
    main()
