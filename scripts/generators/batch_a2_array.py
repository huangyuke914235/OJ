"""数组与链表 · 批量 A2（16 道）。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from genkit import CPP_HEADER, finalize, numbers, problem  # noqa: E402

OUT = ROOT / "oj" / "data" / "problems" / "01-array-linkedlist"
P: list = []


def add(**kw):
    P.append(problem(**kw))


def arr(t):
    """解析「n + 数组」格式。"""
    v = numbers(t)
    return v[0], v[1:1 + v[0]]


# ---------------------------------------------------------------- 1
def s_remove_element(t):
    v = numbers(t)
    n, a, val = v[0], v[1:1 + v[0]], v[1 + v[0]]
    k = 0
    for x in a:
        if x != val:
            a[k] = x
            k += 1
    return f"{k}\n" + ((" ".join(map(str, a[:k])) + "\n") if k else "\n")


add(
    pid="array-remove-element", title="移除元素", difficulty="入门",
    tags=["数组", "双指针", "原地"], source="LeetCode 27", url="https://leetcode.cn/problems/remove-element/",
    statement="给定数组 $a$ 和值 $val$，请**原地**移除所有等于 $val$ 的元素，返回新长度 $k$。\n\n元素的**相对顺序可以改变**。结果放在数组前 $k$ 个位置。\n\n**要求空间复杂度 $O(1)$**。",
    input_format="第一行一个整数 $n$（$0 \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数。\n\n第三行一个整数 $val$。",
    output_format="第一行输出 $k$；第二行输出前 $k$ 个元素（空格分隔），$k=0$ 时输出空行。",
    constraints=["0 ≤ n ≤ 10^5", "|a_i|, |val| ≤ 10^9", "要求 O(1) 空间"],
    solver=s_remove_element,
    specs=[("样例 1", "4\n3 2 2 3\n3", 10), ("样例 2", "8\n0 1 2 2 3 0 4 2\n2", 10),
           ("全部相等", "3\n5 5 5\n5", 15), ("全部不等", "3\n1 2 3\n9", 15),
           ("单元素命中", "1\n5\n5", 15), ("单元素未命中", "1\n5\n6", 20),
           ("含负数", "5\n-1 0 -1 1 -1\n-1", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
long long val;scanf("%lld",&val);
int k=0;for(int i=0;i<n;++i)if(a[i]!=val)a[k++]=a[i];
printf("%d\\n",k);
for(int i=0;i<k;++i){if(i)printf(" ");printf("%lld",a[i]);}
printf("\\n");return 0;}
""",
    hint="**读写双指针**：`k` 指向下一个要写入的位置。遍历数组，只要元素不等于 `val` 就写到 `a[k++]`。\n\n时间 $O(n)$，空间 $O(1)$。",
)

# ---------------------------------------------------------------- 2
def s_rotate_left(t):
    v = numbers(t)
    n, k = v[0], v[1]
    a = v[2:2 + n]
    k %= n
    a = a[k:] + a[:k]
    return " ".join(map(str, a)) + "\n"


add(
    pid="array-rotate-left", title="数组循环左移 k 位", difficulty="入门",
    tags=["数组", "模拟"], source="循环移位变体", url="https://leetcode.cn/problems/rotate-array/",
    statement="把长度为 $n$ 的数组**循环左移** $k$ 位。\n\n循环左移 $k$ 位指：原数组前 $k$ 个元素整体移到末尾，其余元素前移。\n\n例如 `[1,2,3,4,5]` 左移 2 位得到 `[3,4,5,1,2]`。",
    input_format="第一行两个整数 $n, k$（$1 \\le n \\le 10^5$，$0 \\le k \\le 10^9$）。\n\n第二行 $n$ 个整数 $a_i$（$|a_i| \\le 10^9$）。",
    output_format="一行 $n$ 个整数，为左移后的数组。",
    constraints=["1 ≤ n ≤ 10^5", "0 ≤ k ≤ 10^9", "|a_i| ≤ 10^9"],
    solver=s_rotate_left,
    specs=[("样例 1", "5 2\n1 2 3 4 5", 10), ("k 为 0", "3 0\n1 2 3", 10),
           ("k 等于 n", "3 3\n1 2 3", 15), ("k 大于 n", "3 7\n1 2 3", 15),
           ("单元素", "1 5\n9", 15), ("k = n-1", "4 3\n1 2 3 4", 20),
           ("大 k", "4 1000000000\n1 2 3 4", 20)],
    cpp=CPP_HEADER + """int main(){int n;long long k;scanf("%d %lld",&n,&k);
vector<long long>a(n);for(int i=0;i<n;++i)scanf("%lld",&a[i]);
k%=n;
for(int i=0;i<n;++i){if(i)printf(" ");printf("%lld",a[(i+k)%n]);}
printf("\\n");return 0;}
""",
    hint="**取模定位**：先做 `k %= n`，左移后第 $i$ 个位置的元素是原数组的 `a[(i+k) % n]`。\n\n时间 $O(n)$，空间 $O(1)$（直接按新顺序输出，不必真的搬移）。",
)

# ---------------------------------------------------------------- 3
def s_max_avg(t):
    v = numbers(t)
    n, k = v[0], v[1]
    a = v[2:2 + n]
    s = sum(a[:k])
    best = s
    for i in range(k, n):
        s += a[i] - a[i - k]
        best = max(best, s)
    return f"{best / k:.5f}\n"


add(
    pid="array-max-average-subarray", title="长度为 k 的子数组最大平均数", difficulty="简单",
    tags=["数组", "滑动窗口"], source="LeetCode 643", url="https://leetcode.cn/problems/maximum-average-subarray-i/",
    statement="给定数组和整数 $k$，找出**长度恰好为 $k$** 的连续子数组，使其**平均数最大**，输出这个最大平均数。\n\n结果保留 **5 位小数**。",
    input_format="第一行两个整数 $n, k$（$1 \\le k \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数 $a_i$（$|a_i| \\le 10^4$）。",
    output_format="一行，最大平均数，保留 5 位小数。",
    constraints=["1 ≤ k ≤ n ≤ 10^5", "|a_i| ≤ 10^4"],
    solver=s_max_avg,
    specs=[("样例 1", "6 4\n1 12 -5 -6 50 3", 10), ("样例 2", "1 1\n5", 10),
           ("全相同", "4 2\n3 3 3 3", 15), ("含负数", "5 2\n-1 -2 -3 -4 -5", 15),
           ("k = n", "3 3\n1 2 3", 20), ("最大在末尾", "5 2\n1 1 1 1 100", 20)],
    cpp=CPP_HEADER + """int main(){int n,k;scanf("%d %d",&n,&k);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
long long s=0;for(int i=0;i<k;++i)s+=a[i];
long long best=s;
for(int i=k;i<n;++i){s+=a[i]-a[i-k];best=max(best,s);}
printf("%.5f\\n",(double)best/k);return 0;}
""",
    hint="**定长滑动窗口**：先算出前 $k$ 个元素的和，之后每次右移一格：`s += a[i] - a[i-k]`。\n\n用**整数求和**再最后除，避免浮点误差累积。时间 $O(n)$。",
)

# ---------------------------------------------------------------- 4
def s_max_subarray_len(t):
    v = numbers(t)
    n, target = v[0], v[1]
    a = v[2:2 + n]
    left = 0
    s = 0
    best = n + 1                      # 用 > n 表示「不存在」
    for right in range(n):
        s += a[right]
        while s >= target:            # 和达到 target 就开始收缩
            best = min(best, right - left + 1)
            s -= a[left]
            left += 1
    return f"{0 if best > n else best}\n"


add(
    pid="array-min-size-subarray", title="长度最小的子数组", difficulty="中等",
    tags=["数组", "滑动窗口", "双指针"], source="LeetCode 209", url="https://leetcode.cn/problems/minimum-size-subarray-sum/",
    statement="给定一个**正整数**数组和目标值 $target$，找出**和 $\\ge target$** 的**最短连续子数组**，返回其长度。\n\n若不存在这样的子数组，返回 $0$。\n\n**要求 $O(n)$**。",
    input_format="第一行两个整数 $n, target$（$1 \\le n \\le 10^5$，$1 \\le target \\le 10^9$）。\n\n第二行 $n$ 个正整数 $a_i$（$1 \\le a_i \\le 10^4$）。",
    output_format="一行一个整数，表示最短长度；不存在则输出 0。",
    constraints=["1 ≤ n ≤ 10^5", "1 ≤ a_i ≤ 10^4", "1 ≤ target ≤ 10^9", "要求 O(n)"],
    solver=s_max_subarray_len,
    specs=[("样例 1", "6 7\n2 3 1 2 4 3", 10), ("样例 2（不存在）", "3 100\n1 1 1", 10),
           ("单元素命中", "1 5\n5", 15), ("单元素未命中", "1 3\n5", 15),
           ("整个数组才够", "4 10\n1 2 3 4", 20), ("最短在末尾", "5 4\n1 1 1 1 4", 20),
           ("含等于", "3 6\n1 2 3", 20)],
    cpp=CPP_HEADER + """int main(){int n;long long target;scanf("%d %lld",&n,&target);
vector<long long>a(n);for(int i=0;i<n;++i)scanf("%lld",&a[i]);
int left=0,best=1e9;long long s=0;
for(int right=0;right<n;++right){s+=a[right];
while(s>=target){best=min(best,right-left+1);s-=a[left++];}}
printf("%d\\n",best==1e9?0:best);return 0;}
""",
    hint="**滑动窗口**：右指针扩张累加和；当和 $\\ge target$ 时，用 while 收缩左指针并**同时更新答案**。\n\n因为元素都是正整数，窗口和关于左右端点单调，所以 $O(n)$。\n\n> **易错点**：答案是「收缩时」更新，且要取最小长度。",
)

# ---------------------------------------------------------------- 5
def s_move_neg(t):
    n, a = arr(t)
    pos = [x for x in a if x >= 0]
    neg = [x for x in a if x < 0]
    res = pos + neg
    return " ".join(map(str, res)) + "\n"


add(
    pid="array-move-negatives", title="将负数移到数组末尾", difficulty="入门",
    tags=["数组", "双指针", "分区"], source="分区问题变体", url="https://leetcode.cn/problems/move-zeroes/",
    statement="给定一个整数数组，请把**所有负数移到数组末尾**，同时保持**非负数之间**和**负数之间**原有的相对顺序。\n\n**要求**：原地操作，空间 $O(1)$。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数 $a_i$（$|a_i| \\le 10^9$）。",
    output_format="一行 $n$ 个整数，为移动后的数组。",
    constraints=["1 ≤ n ≤ 10^5", "|a_i| ≤ 10^9", "要求 O(1) 空间"],
    solver=s_move_neg,
    specs=[("样例 1", "5\n-1 2 -3 4 -5", 10), ("全非负", "3\n1 2 3", 10),
           ("全负", "3\n-1 -2 -3", 15), ("零的处理", "4\n0 -1 0 -2", 15),
           ("单元素正", "1\n5", 20), ("单元素负", "1\n-5", 20),
           ("交错", "6\n1 -1 2 -2 3 -3", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
vector<long long>t(n);int k=0;
for(int i=0;i<n;++i)if(a[i]>=0)t[k++]=a[i];
for(int i=0;i<n;++i)if(a[i]<0)t[k++]=a[i];
for(int i=0;i<n;++i){if(i)printf(" ");printf("%lld",t[i]);}
printf("\\n");return 0;}
""",
    hint="**两趟扫描 + 临时数组**：先收集所有非负数，再收集所有负数。\n\n注意 **$0$ 属于非负数**（按题面「负数移到末尾」的定义）。\n\n> 若要严格 $O(1)$ 空间，需要用类似插入排序的稳定分区，代价是 $O(n^2)$；本题数据规模下用临时数组即可。",
)

# ---------------------------------------------------------------- 6
def s_merge_two_sorted_arrays(t):
    ls = t.strip("\n").split("\n")
    n, m = map(int, ls[0].split())
    a = list(map(int, ls[1].split())) if n else []
    b = list(map(int, ls[2].split())) if m else []
    i = j = 0
    res = []
    while i < n and j < m:
        if a[i] <= b[j]:
            res.append(a[i]); i += 1
        else:
            res.append(b[j]); j += 1
    res.extend(a[i:]); res.extend(b[j:])
    return " ".join(map(str, res)) + "\n"


add(
    pid="array-merge-two-sorted", title="合并两个有序数组", difficulty="入门",
    tags=["数组", "双指针", "归并"], source="LeetCode 88", url="https://leetcode.cn/problems/merge-sorted-array/",
    statement="给定两个**非递减**数组 $A$（长 $n$）与 $B$（长 $m$），把它们合并为一个**非递减**数组并输出。",
    input_format="第一行两个整数 $n, m$（$0 \\le n, m \\le 10^5$）。\n\n第二行 $n$ 个整数（非递减），$n=0$ 时为空行。\n\n第三行 $m$ 个整数（非递减），$m=0$ 时为空行。",
    output_format="一行 $n+m$ 个整数，为合并后的非递减序列。",
    constraints=["0 ≤ n, m ≤ 10^5", "两数组均非递减", "|a_i| ≤ 10^9"],
    solver=s_merge_two_sorted_arrays,
    specs=[("样例 1", "3 3\n1 2 3\n2 5 6", 10), ("其中一个为空", "3 0\n1 2 3\n", 10),
           ("两个都空", "0 0\n\n", 15), ("全部 A 更小", "3 2\n1 2 3\n4 5", 15),
           ("全部 B 更小", "2 3\n4 5\n1 2 3", 20), ("含重复", "3 3\n1 1 2\n1 2 2", 20),
           ("含负数", "2 2\n-3 -1\n-2 0", 20)],
    cpp=CPP_HEADER + """int main(){int n,m;scanf("%d %d",&n,&m);
vector<long long>a(n),b(m);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
for(int i=0;i<m;++i)scanf("%lld",&b[i]);
vector<long long>r;r.reserve(n+m);
int i=0,j=0;
while(i<n&&j<m){if(a[i]<=b[j])r.push_back(a[i++]);else r.push_back(b[j++]);}
while(i<n)r.push_back(a[i++]);
while(j<m)r.push_back(b[j++]);
for(size_t k=0;k<r.size();++k){if(k)printf(" ");printf("%lld",r[k]);}
printf("\\n");return 0;}
""",
    hint="**双指针归并**：两个指针分别指向两数组开头，每次取较小的那个放入结果并前移。\n\n某一方取完后，把另一方剩余部分直接接上。时间 $O(n+m)$。\n\n> 这与归并排序的 merge 步骤完全相同。",
)

# ---------------------------------------------------------------- 7
def s_third_max(t):
    n, a = arr(t)
    top = sorted(set(a), reverse=True)
    return f"{top[2] if len(top) >= 3 else top[0]}\n"


add(
    pid="array-third-max", title="第三大的数", difficulty="简单",
    tags=["数组", "排序", "去重"], source="LeetCode 414", url="https://leetcode.cn/problems/third-maximum-number/",
    statement="给定一个数组，返回其中**第三大的数**（按**去重后**的降序计）。\n\n若不同值的个数不足 3 个，则返回**最大的那个数**。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 10^4$）。\n\n第二行 $n$ 个整数 $a_i$（$|a_i| \\le 2^{31}-1$）。",
    output_format="一行一个整数，为第三大的数（不足三个不同值时返回最大值）。",
    constraints=["1 ≤ n ≤ 10^4", "|a_i| ≤ 2^31−1", "按去重后的降序计"],
    solver=s_third_max,
    specs=[("样例 1", "3\n3 2 1", 10), ("样例 2（不足三个）", "2\n1 2", 10),
           ("样例 3（有重复）", "5\n2 2 3 1", 15), ("全相同", "3\n5 5 5", 15),
           ("单元素", "1\n7", 15), ("含负数", "4\n-1 -2 -3 -4", 20),
           ("正好三个", "3\n10 20 30", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);set<long long>s;
for(int i=0;i<n;++i){long long x;scanf("%lld",&x);s.insert(x);}
auto it=s.rbegin();
if(s.size()<3)printf("%lld\\n",*it);
else{advance(it,2);printf("%lld\\n",*it);}
return 0;}
""",
    hint="**去重 + 排序**：用 `set` 自动去重并保持有序，再从大到小取第 3 个。\n\n> **易错点**：必须**先去重**再数——`[2,2,3,1]` 去重后是 `{1,2,3}`，第三大是 1，而不是 2。\n> 另外「不足三个不同值」时要返回**最大值**，不是返回 0 或报错。",
)

# ---------------------------------------------------------------- 8
def s_degree(t):
    from collections import Counter
    n, a = arr(t)
    cnt = Counter(a)
    deg = max(cnt.values())
    res = n
    for v, c in cnt.items():
        if c != deg:
            continue
        idx = [i for i, x in enumerate(a) if x == v]
        res = min(res, idx[-1] - idx[0] + 1)
    return f"{res}\n"


add(
    pid="array-degree", title="数组的度", difficulty="简单",
    tags=["数组", "哈希表"], source="LeetCode 697", url="https://leetcode.cn/problems/degree-of-an-array/",
    statement="数组的**度**定义为「任一元素出现次数的最大值」。\n\n请找出数组中**度相同**的**最短连续子数组**，返回它的长度。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 5\\times10^4$）。\n\n第二行 $n$ 个整数 $a_i$（$|a_i| \\le 5\\times10^4$）。",
    output_format="一行一个整数，表示最短连续子数组的长度。",
    constraints=["1 ≤ n ≤ 5×10^4", "|a_i| ≤ 5×10^4"],
    solver=s_degree,
    specs=[("样例 1", "5\n1 2 2 3 1", 10), ("样例 2", "7\n1 2 2 3 1 4 2", 10),
           ("单元素", "1\n5", 15), ("全部相同", "4\n7 7 7 7", 15),
           ("含负数", "6\n-1 -1 2 2 3 3", 20), ("两个同度值", "8\n1 1 2 2 3 3 4 4", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n);
unordered_map<long long,int>cnt,first;unordered_map<long long,int>last;
int deg=0;
for(int i=0;i<n;++i){scanf("%lld",&a[i]);
if(!first.count(a[i]))first[a[i]]=i;
last[a[i]]=i;deg=max(deg,++cnt[a[i]]);}
int best=n;
for(auto&kv:cnt)if(kv.second==deg)best=min(best,last[kv.first]-first[kv.first]+1);
printf("%d\\n",best);return 0;}
""",
    hint="**三次统计**：用哈希表分别记录每个值的**出现次数**、**首次位置**、**末次位置**。\n\n先求出度 `deg`，再对所有出现次数等于 `deg` 的值计算 `last - first + 1`，取最小值。\n\n时间 $O(n)$。",
)

# ---------------------------------------------------------------- 9
def s_longest_harmonious(t):
    from collections import Counter
    n, a = arr(t)
    cnt = Counter(a)
    best = 0
    for v in cnt:
        if v + 1 in cnt:
            best = max(best, cnt[v] + cnt[v + 1])
    return f"{best}\n"


add(
    pid="array-harmonious", title="最长和谐子序列", difficulty="简单",
    tags=["数组", "哈希表", "计数"], source="LeetCode 594", url="https://leetcode.cn/problems/longest-harmonious-subsequence/",
    statement="**和谐子序列**指元素**最大值与最小值之差恰好为 1** 的子序列（不要求连续）。\n\n求最长的和谐子序列的**长度**；不存在则输出 $0$。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 2\\times10^4$）。\n\n第二行 $n$ 个整数 $a_i$（$-10^9 \\le a_i \\le 10^9$）。",
    output_format="一行一个整数，表示最长和谐子序列的长度。",
    constraints=["1 ≤ n ≤ 2×10^4", "|a_i| ≤ 10^9", "子序列不要求连续"],
    solver=s_longest_harmonious,
    specs=[("样例 1", "5\n1 3 2 2 5 2 3 7", 10), ("样例 2（无和谐）", "3\n1 1 1 1", 10),
           ("单元素", "1\n5", 15), ("恰好一对", "2\n1 2", 15),
           ("含负数", "6\n-1 0 0 1 1 1", 20), ("多组相邻值", "8\n1 1 2 2 2 3 3 4", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);unordered_map<long long,int>c;
for(int i=0;i<n;++i){long long x;scanf("%lld",&x);++c[x];}
int best=0;
for(auto&kv:c)if(c.count(kv.first+1))best=max(best,kv.second+c[kv.first+1]);
printf("%d\\n",best);return 0;}
""",
    hint="**计数 + 相邻配对**：因为子序列不要求连续，只需关心「每个值有多少个」。\n\n统计频次后，对每个值 $v$ 检查 $v+1$ 是否存在，若存在则候选长度为 `cnt[v] + cnt[v+1]`，取最大值。\n\n时间 $O(n)$。",
)

# ---------------------------------------------------------------- 10
def s_summary_ranges(t):
    n, a = arr(t)
    res = []
    i = 0
    while i < n:
        j = i
        while j + 1 < n and a[j + 1] == a[j] + 1:
            j += 1
        res.append(str(a[i]) if i == j else f"{a[i]}->{a[j]}")
        i = j + 1
    return " ".join(res) + "\n"


add(
    pid="array-summary-ranges", title="汇总区间", difficulty="简单",
    tags=["数组", "区间", "模拟"], source="LeetCode 228", url="https://leetcode.cn/problems/summary-ranges/",
    statement="给定一个**无重复**且**已升序**的数组，把其中连续的整数段汇总为区间。\n\n格式：单个元素输出它本身；连续多元素输出 `起点->终点`。多个区间用空格分隔。",
    input_format="第一行一个整数 $n$（$0 \\le n \\le 10^5$）。\n\n第二行 $n$ 个**严格递增**的整数（$|a_i| \\le 10^9$），$n=0$ 时为空行。",
    output_format="一行，各区间以空格分隔。无元素时输出空行。",
    constraints=["0 ≤ n ≤ 10^5", "数组严格递增", "|a_i| ≤ 10^9"],
    solver=s_summary_ranges,
    specs=[("样例 1", "6\n0 1 2 4 5 7", 10), ("样例 2", "4\n0 2 3 4 6 8 9", 10),
           ("全连续", "5\n1 2 3 4 5", 15), ("全不连续", "4\n1 3 5 7", 15),
           ("单元素", "1\n5", 15), ("空数组", "0\n", 20),
           ("含负数", "4\n-3 -2 -1 5", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
bool first=true;
for(int i=0;i<n;){
int j=i;while(j+1<n&&a[j+1]==a[j]+1)++j;
if(!first)printf(" ");first=false;
if(i==j)printf("%lld",a[i]);else printf("%lld->%lld",a[i],a[j]);
i=j+1;}
printf("\\n");return 0;}
""",
    hint="**一趟扫描找连续段**：从 `i` 出发，只要 `a[j+1] == a[j] + 1` 就继续右扩，扩不动了就输出这一段。\n\n时间 $O(n)$。注意 $n=0$ 时要输出空行。",
)

# ---------------------------------------------------------------- 11
def s_pascals_triangle(t):
    n = int(t.strip())
    if n <= 0:
        return "\n"
    rows = [[1]]
    for i in range(1, n):
        prev = rows[-1]
        cur = [1] + [prev[j] + prev[j + 1] for j in range(len(prev) - 1)] + [1]
        rows.append(cur)
    return "\n".join(" ".join(map(str, r)) for r in rows) + "\n"


add(
    pid="array-pascals-triangle", title="杨辉三角", difficulty="入门",
    tags=["数组", "递推", "模拟"], source="LeetCode 118", url="https://leetcode.cn/problems/pascals-triangle/",
    statement="给定行数 $n$，输出杨辉三角的前 $n$ 行。\n\n杨辉三角的规则：每行首尾都是 $1$，中间每个数等于它**左上方**与**正上方**两数之和。",
    input_format="一行一个整数 $n$（$0 \\le n \\le 30$）。",
    output_format="共 $n$ 行，第 $i$ 行有 $i$ 个数，以空格分隔。$n=0$ 时输出空行。",
    constraints=["0 ≤ n ≤ 30"],
    solver=s_pascals_triangle,
    specs=[("样例 1", "5", 10), ("样例 2", "1", 10), ("0 行", "0", 15),
           ("2 行", "2", 15), ("10 行", "10", 20), ("30 行", "30", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);
vector<vector<long long>>t;
for(int i=0;i<n;++i){vector<long long>r(i+1,1);
for(int j=1;j<i;++j)r[j]=t[i-1][j-1]+t[i-1][j];
t.push_back(r);}
for(auto&r:t){for(size_t j=0;j<r.size();++j){if(j)printf(" ");printf("%lld",r[j]);}printf("\\n");}
if(n==0)printf("\\n");
return 0;}
""",
    hint="**逐行递推**：第 $i$ 行有 $i$ 个元素，首尾为 1，中间 `r[j] = 上一行[j-1] + 上一行[j]`。\n\n时间 $O(n^2)$。\n\n> **易错点**：$n=0$ 时要输出一个空行，不能什么都不输出。",
)

# ---------------------------------------------------------------- 12
def s_duplicate_zero(t):
    n, a = arr(t)
    res = []
    for x in a:
        res.append(x)
        if x == 0:
            res.append(0)
    return " ".join(map(str, res[:n])) + "\n"


add(
    pid="array-duplicate-zeros", title="复写零", difficulty="简单",
    tags=["数组", "双指针", "原地"], source="LeetCode 1089", url="https://leetcode.cn/problems/duplicate-zeros/",
    statement="给定一个长度固定的数组，将其中每个 $0$ **复写一遍**（即每个 $0$ 后面再插入一个 $0$），其余元素**右移**。\n\n超出原数组长度的元素被丢弃。请**原地**修改数组。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 10^4$）。\n\n第二行 $n$ 个整数 $a_i$（$0 \\le a_i \\le 10^4$）。",
    output_format="一行 $n$ 个整数，为复写后的数组。",
    constraints=["1 ≤ n ≤ 10^4", "0 ≤ a_i ≤ 10^4", "长度保持不变"],
    solver=s_duplicate_zero,
    specs=[("样例 1", "8\n1 0 2 3 0 4 5 0", 10), ("无零", "3\n1 2 3", 10),
           ("全零", "4\n0 0 0 0", 15), ("单元素零", "1\n0", 15),
           ("单元素非零", "1\n5", 15), ("零在开头", "5\n0 1 2 3 4", 20),
           ("零在末尾", "5\n1 2 3 4 0", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<int>a(n);
for(int i=0;i<n;++i)scanf("%d",&a[i]);
vector<int>r;
for(int i=0;i<n&&(int)r.size()<n;++i){r.push_back(a[i]);
if(a[i]==0&&(int)r.size()<n)r.push_back(0);}
for(int i=0;i<n;++i){if(i)printf(" ");printf("%d",r[i]);}
printf("\\n");return 0;}
""",
    hint="**先构造再截断**：从左到右把元素写入结果，遇到 $0$ 就多写一个 $0$，写满 $n$ 个就停止。\n\n> **易错点**：每写一个都要判断是否已达长度上限，否则会多写。",
)

# ---------------------------------------------------------------- 13
def s_list_palindrome(t):
    n, a = arr(t)
    return ("YES\n" if a == a[::-1] else "NO\n")


add(
    pid="list-palindrome", title="回文链表", difficulty="简单",
    tags=["链表", "双指针", "栈"], source="LeetCode 234", url="https://leetcode.cn/problems/palindrome-linked-list/",
    statement="判断一个单链表的节点值序列是否为**回文**。是则输出 `YES`，否则输出 `NO`。",
    input_format="第一行一个整数 $n$（$0 \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数，按从头到尾顺序给出节点值（$|v| \\le 10^9$），$n=0$ 时为空行。",
    output_format="一行，输出 `YES` 或 `NO`。空链表视为回文，输出 `YES`。",
    constraints=["0 ≤ n ≤ 10^5", "|v| ≤ 10^9"],
    solver=s_list_palindrome,
    specs=[("样例 1（是）", "4\n1 2 2 1", 10), ("样例 2（否）", "2\n1 2", 10),
           ("单节点", "1\n7", 15), ("空链表", "0\n", 15),
           ("全相同", "4\n5 5 5 5", 20), ("奇数长度回文", "5\n1 2 3 2 1", 20),
           ("含负数", "4\n-1 0 0 -1", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
bool ok=true;for(int i=0,j=n-1;i<j;++i,--j)if(a[i]!=a[j]){ok=false;break;}
printf("%s\\n",ok?"YES":"NO");return 0;}
""",
    hint="**相向双指针**：从两端向中间逐对比较。\n\n> 在真实链表上不能随机访问，标准做法是「**快慢指针找中点 → 反转后半段 → 比较 → 恢复**」。\n> 本题以数组形式给出链表，用双指针即可。",
)

# ---------------------------------------------------------------- 14
def s_remove_dup_sorted_list(t):
    n, a = arr(t)
    out = []
    for x in a:
        if not out or out[-1] != x:
            out.append(x)
    return ((" ".join(map(str, out)) + "\n") if out else "\n")


add(
    pid="list-remove-duplicates", title="删除排序链表中的重复元素", difficulty="入门",
    tags=["链表", "双指针"], source="LeetCode 83", url="https://leetcode.cn/problems/remove-duplicates-from-sorted-list/",
    statement="给定一个**已升序**的单链表，删除所有重复元素，使每个值**只出现一次**。\n\n输出删除后的链表节点值序列。",
    input_format="第一行一个整数 $n$（$0 \\le n \\le 10^5$）。\n\n第二行 $n$ 个**非递减**整数，$n=0$ 时为空行。",
    output_format="一行，删除重复后的节点值序列（空格分隔）。空链表输出空行。",
    constraints=["0 ≤ n ≤ 10^5", "链表非递减", "|v| ≤ 10^9"],
    solver=s_remove_dup_sorted_list,
    specs=[("样例 1", "5\n1 1 2", 10), ("样例 2", "7\n1 1 2 3 3", 10),
           ("无重复", "3\n1 2 3", 15), ("全相同", "4\n7 7 7 7", 15),
           ("空链表", "0\n", 15), ("单节点", "1\n5", 20),
           ("含负数", "5\n-3 -3 -1 0 0", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a;
for(int i=0;i<n;++i){long long x;scanf("%lld",&x);if(a.empty()||a.back()!=x)a.push_back(x);}
for(size_t i=0;i<a.size();++i){if(i)printf(" ");printf("%lld",a[i]);}
printf("\\n");return 0;}
""",
    hint="**与「有序数组去重」同思路**：因为链表已有序，相同的值必然相邻。\n\n只需保留「与上一个不同」的元素。时间 $O(n)$。",
)

# ---------------------------------------------------------------- 15
def s_odd_even_list(t):
    n, a = arr(t)
    odd = a[0::2]
    even = a[1::2]
    res = odd + even
    return ((" ".join(map(str, res)) + "\n") if res else "\n")


add(
    pid="list-odd-even", title="奇偶链表", difficulty="中等",
    tags=["链表", "双指针"], source="LeetCode 328", url="https://leetcode.cn/problems/odd-even-linked-list/",
    statement="给定单链表，把所有**奇数位置**的节点排在前面、**偶数位置**的节点排在后面，保持各自的相对顺序。\n\n位置从 $1$ 开始计数（第 1 个节点是奇数位置）。\n\n**要求**：原地操作，空间 $O(1)$。",
    input_format="第一行一个整数 $n$（$0 \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数，$n=0$ 时为空行。",
    output_format="一行，重排后的节点值序列（空格分隔）。空链表输出空行。",
    constraints=["0 ≤ n ≤ 10^5", "|v| ≤ 10^9", "要求 O(1) 空间"],
    solver=s_odd_even_list,
    specs=[("样例 1", "5\n1 2 3 4 5", 10), ("样例 2", "7\n2 1 3 5 6 4 7", 10),
           ("单节点", "1\n7", 15), ("两节点", "2\n1 2", 15),
           ("空链表", "0\n", 20), ("偶数个", "4\n1 2 3 4", 20),
           ("含负数", "5\n-1 -2 -3 -4 -5", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
bool first=true;
for(int p=0;p<2;++p)for(int i=p;i<n;i+=2){if(!first)printf(" ");printf("%lld",a[i]);first=false;}
printf("\\n");return 0;}
""",
    hint="**分成两条链再拼接**：用两个指针分别把奇数位置和偶数位置的节点串起来，最后把偶数链接到奇数链尾部。\n\n> **易错点**：偶数指针前进时要注意 `even->next` 可能为空，需先判空再取 `next`。",
)

# ---------------------------------------------------------------- 16
def s_swap_pairs(t):
    n, a = arr(t)
    b = a[:]
    for i in range(0, n - 1, 2):
        b[i], b[i + 1] = b[i + 1], b[i]
    return ((" ".join(map(str, b)) + "\n") if b else "\n")


add(
    pid="list-swap-pairs", title="两两交换链表中的节点", difficulty="中等",
    tags=["链表", "指针操作"], source="LeetCode 24", url="https://leetcode.cn/problems/swap-nodes-in-pairs/",
    statement="给定单链表，**两两交换**其中相邻的节点，返回交换后的链表。\n\n若节点总数为奇数，最后一个节点保持不动。\n\n**要求**：不能只交换节点内的值，必须实际调整指针（本题以序列形式给出结果）。",
    input_format="第一行一个整数 $n$（$0 \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数，$n=0$ 时为空行。",
    output_format="一行，交换后的节点值序列（空格分隔）。空链表输出空行。",
    constraints=["0 ≤ n ≤ 10^5", "|v| ≤ 10^9"],
    solver=s_swap_pairs,
    specs=[("样例 1", "4\n1 2 3 4", 10), ("奇数个", "3\n1 2 3", 10),
           ("单节点", "1\n1", 15), ("两节点", "2\n1 2", 15),
           ("空链表", "0\n", 20), ("五节点", "5\n1 2 3 4 5", 20),
           ("含负数", "4\n-1 -2 -3 -4", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
for(int i=0;i+1<n;i+=2)swap(a[i],a[i+1]);
for(int i=0;i<n;++i){if(i)printf(" ");printf("%lld",a[i]);}
printf("\\n");return 0;}
""",
    hint="**哑结点 + 三指针**：加 `dummy` 消除头结点特判，每轮用 `prev / first / second` 三个指针完成一次交换：\n\n```\nprev->next = second;\nfirst->next = second->next;\nsecond->next = first;\nprev = first;\n```\n\n> **易错点**：交换顺序不能乱——必须先让 `prev` 指向 `second`，否则链会断。",
)


def main() -> None:
    for p in P:
        finalize(p, OUT / f"{p['id']}.json")
        total = sum(t["score"] for t in p["tests"])
        print(f"生成 {p['id']:34s} {len(p['tests'])} 测试点, 总分 {total:3d}")


if __name__ == "__main__":
    main()
