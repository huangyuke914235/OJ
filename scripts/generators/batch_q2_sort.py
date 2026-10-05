"""排序与查找 · 批量 Q2（14 道）。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from genkit import CPP_HEADER, finalize, numbers, problem  # noqa: E402

OUT = ROOT / "oj" / "data" / "problems" / "07-sort-search"
P: list = []


def add(**kw):
    P.append(problem(**kw))


def arr(t):
    v = numbers(t)
    return v[0], v[1:1 + v[0]]


def join(a):
    return " ".join(map(str, a)) + "\n"


def two(t):
    """解析「n target」+ 数组。"""
    ls = t.strip("\n").split("\n")
    n, target = map(int, ls[0].split())
    return n, target, list(map(int, ls[1].split()))


def lower_bound(a, x):
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo


# ---------------------------------------------------------------- 1
def s_lb_practice(t):
    n, x, a = two(t)
    return f"{lower_bound(a, x)}\n"


add(
    pid="search-lower-bound-practice", title="二分下界（练习）", difficulty="入门",
    tags=["二分查找", "边界"], source="LeetCode 35", url="https://leetcode.cn/problems/search-insert-position/",
    statement="给定**非递减**数组和目标值 $x$，返回**第一个不小于 $x$** 的元素下标。\n\n若所有元素都小于 $x$，返回 $n$。\n\n**要求 $O(\\log n)$**。",
    input_format="第一行两个整数 $n, x$（$1 \\le n \\le 10^5$）。\n\n第二行 $n$ 个**非递减**整数（$|a_i| \\le 10^9$）。",
    output_format="一行一个整数。",
    constraints=["1 ≤ n ≤ 10^5", "数组非递减", "要求 O(log n)"],
    solver=s_lb_practice,
    specs=[("样例 1", "5 5\n1 3 5 7 9", 10), ("全部更小", "3 100\n1 2 3", 10),
           ("第一个就满足", "4 1\n2 3 4 5", 15), ("重复元素", "6 3\n1 3 3 3 5 7", 15),
           ("单元素命中", "1 5\n5", 20), ("单元素更大", "1 5\n1", 20)],
    cpp=CPP_HEADER + """int main(){int n;long long x;scanf("%d %lld",&n,&x);
vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
int lo=0,hi=n;
while(lo<hi){int mid=lo+(hi-lo)/2;
if(a[mid]<x)lo=mid+1;else hi=mid;}
printf("%d\\n",lo);return 0;}
""",
    hint="**半开区间写法**：`hi = n`（不是 $n-1$），循环条件 `lo < hi`。\n\n`a[mid] < x` 时 `lo = mid + 1`；否则 `hi = mid`（**不能写 `mid - 1`**，因为 mid 可能就是答案）。\n\n时间 $O(\\log n)$。",
)

# ---------------------------------------------------------------- 2
def s_ub_practice(t):
    n, x, a = two(t)
    lo, hi = 0, n
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] <= x:
            lo = mid + 1
        else:
            hi = mid
    return f"{lo}\n"


add(
    pid="search-upper-bound-practice", title="二分上界（练习）", difficulty="入门",
    tags=["二分查找", "边界"], source="LeetCode 34", url="https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/",
    statement="给定**非递减**数组和目标值 $x$，返回**第一个大于 $x$** 的元素下标。\n\n若所有元素都不大于 $x$，返回 $n$。\n\n**要求 $O(\\log n)$**。",
    input_format="第一行两个整数 $n, x$（$1 \\le n \\le 10^5$）。\n\n第二行 $n$ 个**非递减**整数（$|a_i| \\le 10^9$）。",
    output_format="一行一个整数。",
    constraints=["1 ≤ n ≤ 10^5", "数组非递减", "要求 O(log n)"],
    solver=s_ub_practice,
    specs=[("样例 1", "5 5\n1 3 5 7 9", 10), ("全部不大于", "3 100\n1 2 3", 10),
           ("第一个就更大", "4 1\n2 3 4 5", 15), ("重复元素", "6 3\n1 3 3 3 5 7", 15),
           ("单元素命中", "1 5\n5", 20), ("单元素更大", "1 5\n1", 20)],
    cpp=CPP_HEADER + """int main(){int n;long long x;scanf("%d %lld",&n,&x);
vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
int lo=0,hi=n;
while(lo<hi){int mid=lo+(hi-lo)/2;
if(a[mid]<=x)lo=mid+1;else hi=mid;}
printf("%d\\n",lo);return 0;}
""",
    hint="**与下界只差一个符号**：把 `a[mid] < x` 改成 `a[mid] <= x`。\n\n> **组合用法**：`upper_bound(x) - lower_bound(x)` 就是 $x$ 在数组中的**出现次数**。",
)

# ---------------------------------------------------------------- 3
def s_count_occurrences(t):
    n, x, a = two(t)
    l = lower_bound(a, x)
    lo, hi = 0, n
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] <= x:
            lo = mid + 1
        else:
            hi = mid
    return f"{lo - l}\n"


add(
    pid="search-count-occurrences", title="统计目标值出现次数", difficulty="简单",
    tags=["二分查找", "边界"], source="LeetCode 34", url="https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/",
    statement="给定**非递减**数组和目标值 $x$，统计 $x$ 在数组中出现的**次数**。\n\n**要求 $O(\\log n)$**（不能线性扫描）。",
    input_format="第一行两个整数 $n, x$（$1 \\le n \\le 10^5$）。\n\n第二行 $n$ 个**非递减**整数（$|a_i| \\le 10^9$）。",
    output_format="一行一个整数，表示出现次数。",
    constraints=["1 ≤ n ≤ 10^5", "数组非递减", "要求 O(log n)"],
    solver=s_count_occurrences,
    specs=[("样例 1", "6 3\n1 3 3 3 5 7", 10), ("不存在", "5 4\n1 2 3 5 6", 10),
           ("全部相同", "4 5\n5 5 5 5", 15), ("单次出现", "5 3\n1 2 3 4 5", 15),
           ("单元素命中", "1 5\n5", 20), ("单元素未命中", "1 5\n6", 20)],
    cpp=CPP_HEADER + """int main(){int n;long long x;scanf("%d %lld",&n,&x);
vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
auto lb=[&](long long v){int lo=0,hi=n;
while(lo<hi){int mid=lo+(hi-lo)/2;if(a[mid]<v)lo=mid+1;else hi=mid;}return lo;};
auto ub=[&](long long v){int lo=0,hi=n;
while(lo<hi){int mid=lo+(hi-lo)/2;if(a[mid]<=v)lo=mid+1;else hi=mid;}return lo;};
printf("%d\\n",ub(x)-lb(x));return 0;}
""",
    hint="**两次二分相减**：`upper_bound(x) - lower_bound(x)` 即出现次数。\n\n时间 $O(\\log n)$。\n\n> **为什么不能线性扫描**：虽然本题数据不大，但「$O(\\log n)$ 统计出现次数」是二分边界的核心考点。",
)

# ---------------------------------------------------------------- 4
def s_sorted_check(t):
    n, a = arr(t)
    return ("YES\n" if all(a[i] <= a[i + 1] for i in range(n - 1)) else "NO\n")


add(
    pid="sort-check-sorted", title="判断数组是否已排序", difficulty="入门",
    tags=["数组", "排序"], source="排序基础", url="https://leetcode.cn/problems/sort-an-array/",
    statement="判断数组是否**非递减**。是输出 `YES`，否则 `NO`。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数（$|a_i| \\le 10^9$）。",
    output_format="一行，输出 `YES` 或 `NO`。",
    constraints=["1 ≤ n ≤ 10^5", "|a_i| ≤ 10^9"],
    solver=s_sorted_check,
    specs=[("样例 1（有序）", "5\n1 2 3 4 5", 10), ("样例 2（无序）", "3\n1 3 2", 10),
           ("单元素", "1\n7", 15), ("全相同", "4\n2 2 2 2", 15),
           ("递减", "4\n4 3 2 1", 20), ("含负数", "4\n-3 -1 0 2", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
bool ok=true;
for(int i=1;i<n;++i)if(a[i-1]>a[i]){ok=false;break;}
printf("%s\\n",ok?"YES":"NO");return 0;}
""",
    hint="**检查相邻对**：只需确认每一对相邻元素都满足 `a[i-1] <= a[i]`。\n\n时间 $O(n)$，空间 $O(1)$。",
)

# ---------------------------------------------------------------- 5
def s_dedupe_sorted(t):
    n, a = arr(t)
    out = []
    for x in a:
        if not out or out[-1] != x:
            out.append(x)
    return join(out) if out else "\n"


add(
    pid="sort-dedupe-sorted", title="有序数组去重（输出结果）", difficulty="入门",
    tags=["数组", "双指针", "排序"], source="LeetCode 26", url="https://leetcode.cn/problems/remove-duplicates-from-sorted-array/",
    statement="给定**非递减**数组，输出去重后的数组（每个值只保留一次，保持升序）。",
    input_format="第一行一个整数 $n$（$0 \\le n \\le 10^5$）。\n\n第二行 $n$ 个**非递减**整数（$|a_i| \\le 10^9$），$n=0$ 时为空行。",
    output_format="一行，去重后的数组；空数组输出空行。",
    constraints=["0 ≤ n ≤ 10^5", "数组非递减"],
    solver=s_dedupe_sorted,
    specs=[("样例 1", "5\n1 1 2 2 3", 10), ("无重复", "4\n1 2 3 4", 10),
           ("全相同", "4\n7 7 7 7", 15), ("空数组", "0\n", 15),
           ("单元素", "1\n5", 20), ("含负数", "5\n-3 -3 -1 0 0", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>r;
for(int i=0;i<n;++i){long long x;scanf("%lld",&x);
if(r.empty()||r.back()!=x)r.push_back(x);}
for(size_t i=0;i<r.size();++i){if(i)printf(" ");printf("%lld",r[i]);}
printf("\\n");return 0;}
""",
    hint="**边读边去重**：因为数组有序，相同的值必然相邻，只需保留「与上一个不同」的元素。\n\n时间 $O(n)$。",
)

# ---------------------------------------------------------------- 6
def s_min_abs_diff(t):
    n, a = arr(t)
    a = sorted(a)
    best = min(a[i + 1] - a[i] for i in range(n - 1))
    return f"{best}\n"


add(
    pid="sort-min-abs-diff", title="有序数组中的最小绝对差", difficulty="简单",
    tags=["数组", "排序"], source="LeetCode 1200", url="https://leetcode.cn/problems/minimum-absolute-difference/",
    statement="给定数组，求**任意两个元素之间绝对值差的最小值**。",
    input_format="第一行一个整数 $n$（$2 \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数（$|a_i| \\le 10^9$）。",
    output_format="一行一个整数，表示最小绝对差。",
    constraints=["2 ≤ n ≤ 10^5", "|a_i| ≤ 10^9"],
    solver=s_min_abs_diff,
    specs=[("样例 1", "4\n4 2 1 3", 10), ("含重复", "3\n1 3 1", 10),
           ("两元素", "2\n5 3", 15), ("含负数", "4\n-1 -5 2 3", 15),
           ("全相同", "3\n7 7 7", 20), ("大跨度", "3\n1 100 10000", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
sort(a.begin(),a.end());
long long best=LLONG_MAX;
for(int i=1;i<n;++i)best=min(best,a[i]-a[i-1]);
printf("%lld\\n",best);return 0;}
""",
    hint="**排序后看相邻**：绝对值差最小的两个元素，排序后必然**相邻**。\n\n所以排序后扫描相邻差值即可。时间 $O(n\\log n)$。\n\n> **为什么**：若 $x \\le y \\le z$，则 $z - x = (z-y) + (y-x) \\ge \\max(z-y, y-x)$，跨元素不可能比相邻更近。",
)

# ---------------------------------------------------------------- 7
def s_contains_dup_sort(t):
    n, a = arr(t)
    a = sorted(a)
    ok = any(a[i] == a[i + 1] for i in range(n - 1))
    return ("YES\n" if ok else "NO\n")


add(
    pid="sort-contains-dup", title="存在重复元素（排序解法）", difficulty="入门",
    tags=["数组", "排序"], source="LeetCode 217", url="https://leetcode.cn/problems/contains-duplicate/",
    statement="判断数组中是否存在重复元素。存在输出 `YES`，否则 `NO`。\n\n> 本题用**排序**解决（$O(n\\log n)$），对比哈希解法（$O(n)$）。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数（$|a_i| \\le 10^9$）。",
    output_format="一行，输出 `YES` 或 `NO`。",
    constraints=["1 ≤ n ≤ 10^5", "|a_i| ≤ 10^9"],
    solver=s_contains_dup_sort,
    specs=[("样例 1（有重复）", "4\n1 2 3 1", 10), ("样例 2（无重复）", "4\n1 2 3 4", 10),
           ("单元素", "1\n7", 15), ("两元素相同", "2\n5 5", 15),
           ("含负数重复", "5\n-1 -2 -3 -1 0", 20), ("全相同", "4\n9 9 9 9", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
sort(a.begin(),a.end());
bool dup=false;
for(int i=1;i<n;++i)if(a[i]==a[i-1]){dup=true;break;}
printf("%s\\n",dup?"YES":"NO");return 0;}
""",
    hint="**排序后看相邻**：排序后若存在重复，重复元素必然相邻。\n\n时间 $O(n\\log n)$，空间 $O(1)$（不算排序本身的开销）。\n\n> **对比哈希法**：时间 $O(n)$ 但空间 $O(n)$；排序法反之。",
)

# ---------------------------------------------------------------- 8
def s_merge_sorted_inplace(t):
    ls = t.strip("\n").split("\n")
    n, m = map(int, ls[0].split())
    a = list(map(int, ls[1].split()))
    b = list(map(int, ls[2].split()))
    i, j = n - 1, m - 1
    k = n + m - 1
    res = [0] * (n + m)
    while j >= 0:
        if i >= 0 and a[i] > b[j]:
            res[k] = a[i]
            i -= 1
        else:
            res[k] = b[j]
            j -= 1
        k -= 1
    while i >= 0:
        res[k] = a[i]
        i -= 1
        k -= 1
    return join(res)


add(
    pid="sort-merge-inplace", title="合并两个有序数组（从后往前）", difficulty="简单",
    tags=["数组", "双指针", "归并"], source="LeetCode 88", url="https://leetcode.cn/problems/merge-sorted-array/",
    statement="给定两个**非递减**数组 $A$（长 $n$）和 $B$（长 $m$），合并成一个非递减数组并输出。\n\n> **技巧**：经典做法是**从后往前**比较，避免搬移元素（$O(1)$ 额外空间）。本题只需输出合并结果。",
    input_format="第一行两个整数 $n, m$（$1 \\le n, m \\le 10^5$）。\n\n第二行 $n$ 个非递减整数。\n\n第三行 $m$ 个非递减整数。",
    output_format="一行 $n+m$ 个整数，非递减。",
    constraints=["1 ≤ n, m ≤ 10^5", "两数组非递减"],
    solver=s_merge_sorted_inplace,
    specs=[("样例 1", "3 3\n1 2 3\n2 5 6", 10), ("全部 A 更小", "3 2\n1 2 3\n4 5", 10),
           ("全部 B 更小", "2 3\n4 5\n1 2 3", 15), ("含重复", "3 3\n1 1 2\n1 2 2", 15),
           ("含负数", "2 2\n-3 -1\n-2 0", 20), ("单元素", "1 1\n1\n2", 20)],
    cpp=CPP_HEADER + """int main(){int n,m;scanf("%d %d",&n,&m);
vector<long long>a(n),b(m);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
for(int i=0;i<m;++i)scanf("%lld",&b[i]);
vector<long long>r(n+m);
int i=n-1,j=m-1,k=n+m-1;
while(j>=0){if(i>=0&&a[i]>b[j])r[k--]=a[i--];else r[k--]=b[j--];}
while(i>=0)r[k--]=a[i--];
for(int t=0;t<n+m;++t){if(t)printf(" ");printf("%lld",r[t]);}
printf("\\n");return 0;}
""",
    hint="**从后往前归并**：两个指针分别指向 $A$ 和 $B$ 的**末尾**，每次把较大的放到结果数组的末尾。\n\n> **为什么从后往前**：若 $A$ 后面有足够空位，从后往前填就**不会覆盖还没处理的 $A$ 元素**，从而做到 $O(1)$ 额外空间。\n\n时间 $O(n+m)$。",
)

# ---------------------------------------------------------------- 9
def s_binary_search_count(t):
    n, x, a = two(t)
    lo, hi = 0, n - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if a[mid] == x:
            return "YES\n"
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return "NO\n"


add(
    pid="search-exists", title="二分查找（判断存在）", difficulty="入门",
    tags=["二分查找"], source="LeetCode 704", url="https://leetcode.cn/problems/binary-search/",
    statement="给定**严格递增**数组和目标值 $x$，判断 $x$ 是否存在于数组中。\n\n存在输出 `YES`，否则 `NO`。\n\n**要求 $O(\\log n)$**。",
    input_format="第一行两个整数 $n, x$（$1 \\le n \\le 10^5$）。\n\n第二行 $n$ 个**严格递增**整数（$|a_i| \\le 10^9$）。",
    output_format="一行，输出 `YES` 或 `NO`。",
    constraints=["1 ≤ n ≤ 10^5", "数组严格递增", "要求 O(log n)"],
    solver=s_binary_search_count,
    specs=[("样例 1（存在）", "6 9\n-1 0 3 5 9 12", 10),
           ("样例 2（不存在）", "6 2\n-1 0 3 5 9 12", 10),
           ("单元素命中", "1 5\n5", 15), ("单元素未命中", "1 5\n6", 15),
           ("首元素命中", "4 1\n1 3 5 7", 20), ("末元素命中", "4 7\n1 3 5 7", 20)],
    cpp=CPP_HEADER + """int main(){int n;long long x;scanf("%d %lld",&n,&x);
vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
int lo=0,hi=n-1;bool found=false;
while(lo<=hi){int mid=lo+(hi-lo)/2;
if(a[mid]==x){found=true;break;}
if(a[mid]<x)lo=mid+1;else hi=mid-1;}
printf("%s\\n",found?"YES":"NO");return 0;}
""",
    hint="**闭区间写法**：`lo = 0`、`hi = n-1`，循环条件 `lo <= hi`，边界更新用 `mid ± 1`。\n\n时间 $O(\\log n)$。\n\n> **与半开区间写法的区别**：闭区间用 `<=` 和 `mid±1`；半开区间用 `<` 和 `hi = mid`。**两种都可以，但不要混用**。",
)

# ---------------------------------------------------------------- 10
def s_sort_by_freq(t):
    from collections import Counter
    n, a = arr(t)
    cnt = Counter(a)
    a = sorted(a, key=lambda x: (cnt[x], -x))   # 频率升序，同频按值降序
    return join(a)


add(
    pid="sort-by-frequency", title="按频率升序排序", difficulty="中等",
    tags=["数组", "排序", "哈希表"], source="LeetCode 1636", url="https://leetcode.cn/problems/sort-array-by-increasing-frequency/",
    statement="给定数组，按**元素出现频率升序**排序；频率相同时，按**元素值降序**排列。\n\n输出排序后的数组。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 100$）。\n\n第二行 $n$ 个整数（$-100 \\le a_i \\le 100$）。",
    output_format="一行 $n$ 个整数。",
    constraints=["1 ≤ n ≤ 100", "−100 ≤ a_i ≤ 100", "频率相同按值降序"],
    solver=s_sort_by_freq,
    specs=[("样例 1", "6\n1 1 2 2 2 3", 10), ("全相同", "3\n5 5 5", 10),
           ("全不同", "3\n1 2 3", 15), ("两两相同", "4\n2 2 1 1", 15),
           ("含负数", "5\n-1 -1 2 3 3", 20), ("单元素", "1\n7", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<int>a(n);
unordered_map<int,int>c;
for(int i=0;i<n;++i){scanf("%d",&a[i]);++c[a[i]];}
sort(a.begin(),a.end(),[&](int x,int y){
if(c[x]!=c[y])return c[x]<c[y];
return x>y;});
for(int i=0;i<n;++i){if(i)printf(" ");printf("%d",a[i]);}
printf("\\n");return 0;}
""",
    hint="**哈希计数 + 自定义排序**：先统计频率，再按「频率升序，频率相同则值降序」排序。\n\n> **易错点**：`sort` 的比较函数必须是**严格弱序**——写成 `<=` 或 `>=` 会导致未定义行为（可能崩溃）。\n\n时间 $O(n\\log n)$。",
)

# ---------------------------------------------------------------- 11
def s_kth_largest_sort(t):
    ls = t.strip("\n").split("\n")
    n, k = map(int, ls[0].split())
    a = list(map(int, ls[1].split()))
    a.sort(reverse=True)
    return f"{a[k - 1]}\n"


add(
    pid="sort-kth-largest", title="排序求第 K 大", difficulty="入门",
    tags=["排序", "数组"], source="LeetCode 215", url="https://leetcode.cn/problems/kth-largest-element-in-an-array/",
    statement="给定数组和整数 $k$，用**排序**求第 $k$ 大的元素。",
    input_format="第一行两个整数 $n, k$（$1 \\le k \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数（$|a_i| \\le 10^9$）。",
    output_format="一行一个整数。",
    constraints=["1 ≤ k ≤ n ≤ 10^5", "|a_i| ≤ 10^9"],
    solver=s_kth_largest_sort,
    specs=[("样例 1", "6 2\n3 2 1 5 6 4", 10), ("k = 1", "3 1\n3 2 1", 10),
           ("k = n", "4 4\n1 2 3 4", 15), ("全相同", "4 2\n5 5 5 5", 15),
           ("含负数", "5 3\n-1 -2 -3 -4 -5", 20), ("单元素", "1 1\n7", 20)],
    cpp=CPP_HEADER + """int main(){int n,k;scanf("%d %d",&n,&k);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
sort(a.rbegin(),a.rend());
printf("%lld\\n",a[k-1]);return 0;}
""",
    hint="**降序排序取第 $k$ 个**：时间 $O(n\\log n)$。\n\n> **对比**：用堆是 $O(n\\log k)$，用快速选择平均 $O(n)$。",
)

# ---------------------------------------------------------------- 12
def s_sort_stability_demo(t):
    ls = t.strip("\n").split("\n")
    n = int(ls[0])
    items = [tuple(map(int, ls[i + 1].split())) for i in range(n)]
    items.sort(key=lambda p: p[0])       # 稳定排序，只按第一个键
    return "\n".join(f"{a} {b}" for a, b in items) + "\n"


add(
    pid="sort-stable-demo", title="稳定排序（按首键排序）", difficulty="简单",
    tags=["排序", "稳定性"], source="排序性质", url="https://leetcode.cn/problems/sort-an-array/",
    statement="给定 $n$ 个数对 $(key, id)$，请按 **$key$ 升序**排列。\n\n**要求**：$key$ 相同的数对**保持原有的相对顺序**（即必须使用**稳定排序**）。\n\n每行输出一个数对。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 10^4$）。\n\n接下来 $n$ 行，每行两个整数 $key, id$（$|key| \\le 10^9$，$id$ 互不相同）。",
    output_format="共 $n$ 行，每行 `key id`。",
    constraints=["1 ≤ n ≤ 10^4", "id 互不相同", "必须稳定排序"],
    solver=s_sort_stability_demo,
    specs=[("样例 1", "4\n2 1\n1 2\n2 3\n1 4", 10), ("全相同 key", "3\n5 1\n5 2\n5 3", 10),
           ("单元素", "1\n7 1", 15), ("已有序", "3\n1 1\n2 2\n3 3", 15),
           ("逆序 key", "3\n3 1\n2 2\n1 3", 20), ("含负数", "4\n-1 1\n0 2\n-1 3\n0 4", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);
vector<pair<long long,long long>>v(n);
for(int i=0;i<n;++i)scanf("%lld %lld",&v[i].first,&v[i].second);
stable_sort(v.begin(),v.end(),[](const auto&a,const auto&b){return a.first<b.first;});
for(int i=0;i<n;++i)printf("%lld %lld\\n",v[i].first,v[i].second);
return 0;}
""",
    hint="**稳定排序**：C++ 用 `std::stable_sort`，Python 的 `sort` **本身就是稳定的**。\n\n> **哪些排序是稳定的**：插入、冒泡、归并、计数排序稳定；快排、堆排、选择排序**不稳定**。\n\n> **应用**：多关键字排序时，可以先按次要键排、再按主要键**稳定**排序，从而避免写复杂的多键比较。",
)

# ---------------------------------------------------------------- 13
def s_search_sqrt_int(t):
    n = int(t.strip())
    if n < 2:
        return f"{n}\n"
    lo, hi = 1, n
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid * mid <= n:
            lo = mid
        else:
            hi = mid - 1
    return f"{lo}\n"


add(
    pid="search-sqrt-practice", title="平方根（二分答案练习）", difficulty="简单",
    tags=["二分答案", "数学"], source="LeetCode 69", url="https://leetcode.cn/problems/sqrtx/",
    statement="给定非负整数 $n$，求 $\\lfloor\\sqrt{n}\\rfloor$（平方根的整数部分）。\n\n**禁止**使用 `sqrt` 等库函数。\n\n**要求 $O(\\log n)$**。",
    input_format="一行一个整数 $n$（$0 \\le n \\le 2^{31}-1$）。",
    output_format="一行一个整数。",
    constraints=["0 ≤ n ≤ 2^31−1", "禁止使用 sqrt", "要求 O(log n)"],
    solver=s_search_sqrt_int,
    specs=[("样例 1", "4", 10), ("样例 2", "8", 10), ("零", "0", 15),
           ("一", "1", 15), ("完全平方", "144", 20), ("大数", "2147483647", 20)],
    cpp=CPP_HEADER + """int main(){long long n;scanf("%lld",&n);
if(n<2){printf("%lld\\n",n);return 0;}
long long lo=1,hi=n;
while(lo<hi){long long mid=lo+(hi-lo+1)/2;
if(mid*mid<=n)lo=mid;else hi=mid-1;}
printf("%lld\\n",lo);return 0;}
""",
    hint="**二分答案**：答案 $x$ 满足「$x^2 \\le n$」单调，在 $[0, n]$ 上二分。\n\n> **两个易错点**：\n> 1. 中点要**上取整**（`(lo+hi+1)/2`），否则会死循环；\n> 2. $n$ 可达 $2^{31}-1$，`mid*mid` 会溢出 `int`，**必须用 `long long`**。",
)

# ---------------------------------------------------------------- 14
def s_sort_diagonal(t):
    ls = t.strip("\n").split("\n")
    r, c = map(int, ls[0].split())
    g = [list(map(int, ls[i + 1].split())) for i in range(r)]
    for d in range(r + c - 1):
        cells = [(i, d - i) for i in range(r) if 0 <= d - i < c]
        vals = sorted(g[i][j] for i, j in cells)
        for (i, j), v in zip(cells, vals):
            g[i][j] = v
    return "\n".join(" ".join(map(str, row)) for row in g) + "\n"


add(
    pid="sort-matrix-diagonal", title="将矩阵对角线排序", difficulty="中等",
    tags=["矩阵", "排序", "模拟"], source="LeetCode 1329", url="https://leetcode.cn/problems/sort-the-matrix-diagonally/",
    statement="给定矩阵，把**每条从左上到右下的对角线**上的元素**升序排序**。\n\n输出排序后的矩阵。",
    input_format="第一行两个整数 $r, c$（$1 \\le r, c \\le 100$）。\n\n接下来 $r$ 行，每行 $c$ 个整数（$|v| \\le 100$）。",
    output_format="共 $r$ 行，为排序后的矩阵。",
    constraints=["1 ≤ r, c ≤ 100", "|v| ≤ 100"],
    solver=s_sort_diagonal,
    specs=[("样例 1", "3 3\n3 3 1\n2 2 1\n1 1 1", 10),
           ("单元素", "1 1\n5", 10), ("单行", "1 3\n3 1 2", 15),
           ("单列", "3 1\n3\n1\n2", 15), ("已有序", "2 2\n1 2\n3 4", 20),
           ("全相同", "2 2\n5 5\n5 5", 20)],
    cpp=CPP_HEADER + """int main(){int r,c;scanf("%d %d",&r,&c);
vector<vector<long long>>g(r,vector<long long>(c));
for(int i=0;i<r;++i)for(int j=0;j<c;++j)scanf("%lld",&g[i][j]);
for(int d=0;d<r+c-1;++d){
vector<long long>v;vector<pair<int,int>>pos;
for(int i=0;i<r;++i){int j=d-i;
if(j<0||j>=c)continue;
pos.push_back({i,j});v.push_back(g[i][j]);}
sort(v.begin(),v.end());
for(size_t k=0;k<pos.size();++k)g[pos[k].first][pos[k].second]=v[k];}
for(int i=0;i<r;++i){for(int j=0;j<c;++j){if(j)printf(" ");printf("%lld",g[i][j]);}printf("\\n");}
return 0;}
""",
    hint="**按对角线编号分组**：同一条「左上→右下」对角线上的元素满足 `i - j` 为定值，或者用 `i + j` 统一编号。\n\n对每条对角线收集元素、排序、再写回。\n\n时间 $O(rc \\cdot \\log(\\max(r,c)))$。",
)


def main() -> None:
    for p in P:
        finalize(p, OUT / f"{p['id']}.json")
        total = sum(t["score"] for t in p["tests"])
        print(f"生成 {p['id']:34s} {len(p['tests'])} 测试点, 总分 {total:3d}")


if __name__ == "__main__":
    main()
