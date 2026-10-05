"""排序与查找 · 批量 Q1（16 道）。"""
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


# ---------------------------------------------------------------- 1
def s_insertion(t):
    n, a = arr(t)
    for i in range(1, n):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return join(a)


add(
    pid="sort-insertion", title="插入排序", difficulty="入门",
    tags=["排序", "插入排序"], source="经典排序", url="https://leetcode.cn/problems/sort-an-array/",
    statement="用**插入排序**把数组升序排列并输出。\n\n插入排序的思路：把数组分成「已排序前缀」和「未排序后缀」，每次取后缀的第一个元素，在已排序部分从后往前找到它该插入的位置。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 5000$）。\n\n第二行 $n$ 个整数（$|a_i| \\le 10^9$）。",
    output_format="一行 $n$ 个整数，升序排列。",
    constraints=["1 ≤ n ≤ 5000", "|a_i| ≤ 10^9"],
    solver=s_insertion,
    specs=[("样例 1", "5\n3 1 4 1 5", 10), ("已有序", "4\n1 2 3 4", 10),
           ("逆序", "4\n4 3 2 1", 15), ("单元素", "1\n7", 15),
           ("全相同", "4\n2 2 2 2", 20), ("含负数", "5\n-1 0 -3 2 -2", 20),
           ("两元素", "2\n5 3", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
for(int i=1;i<n;++i){long long key=a[i];int j=i-1;
while(j>=0&&a[j]>key){a[j+1]=a[j];--j;}
a[j+1]=key;}
for(int i=0;i<n;++i){if(i)printf(" ");printf("%lld",a[i]);}
printf("\\n");return 0;}
""",
    hint="**插入排序**：`a[0..i-1]` 已有序，把 `a[i]` 插入到正确位置（从后往前比较并后移）。\n\n时间 $O(n^2)$，空间 $O(1)$，**稳定**。\n\n> **优点**：数组**近乎有序**时接近 $O(n)$，实际表现常优于快排。",
)

# ---------------------------------------------------------------- 2
def s_bubble(t):
    n, a = arr(t)
    for i in range(n):
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return join(a)


add(
    pid="sort-bubble", title="冒泡排序", difficulty="入门",
    tags=["排序", "冒泡排序"], source="经典排序", url="https://leetcode.cn/problems/sort-an-array/",
    statement="用**冒泡排序**把数组升序排列并输出。\n\n冒泡排序的思路：每轮从头到尾比较相邻元素，逆序就交换——这样每轮能把当前最大的元素「冒」到末尾。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 2000$）。\n\n第二行 $n$ 个整数（$|a_i| \\le 10^9$）。",
    output_format="一行 $n$ 个整数，升序排列。",
    constraints=["1 ≤ n ≤ 2000", "|a_i| ≤ 10^9"],
    solver=s_bubble,
    specs=[("样例 1", "5\n3 1 4 1 5", 10), ("已有序", "4\n1 2 3 4", 10),
           ("逆序", "4\n4 3 2 1", 15), ("单元素", "1\n7", 15),
           ("全相同", "4\n2 2 2 2", 20), ("含负数", "5\n-1 0 -3 2 -2", 20),
           ("两元素", "2\n5 3", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
for(int i=0;i<n;++i)for(int j=0;j+1<n-i;++j)
if(a[j]>a[j+1])swap(a[j],a[j+1]);
for(int i=0;i<n;++i){if(i)printf(" ");printf("%lld",a[i]);}
printf("\\n");return 0;}
""",
    hint="**冒泡排序**：每轮把最大的元素「冒」到未排序区间的末尾。\n\n时间 $O(n^2)$，空间 $O(1)$，**稳定**。\n\n> **优化**：若某一轮没有发生任何交换，说明已经有序，可提前退出。",
)

# ---------------------------------------------------------------- 3
def s_selection(t):
    n, a = arr(t)
    for i in range(n):
        m = i
        for j in range(i + 1, n):
            if a[j] < a[m]:
                m = j
        a[i], a[m] = a[m], a[i]
    return join(a)


add(
    pid="sort-selection", title="选择排序", difficulty="入门",
    tags=["排序", "选择排序"], source="经典排序", url="https://leetcode.cn/problems/sort-an-array/",
    statement="用**选择排序**把数组升序排列并输出。\n\n选择排序的思路：每轮在未排序区间中找到最小元素，与区间第一个元素交换。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 2000$）。\n\n第二行 $n$ 个整数（$|a_i| \\le 10^9$）。",
    output_format="一行 $n$ 个整数，升序排列。",
    constraints=["1 ≤ n ≤ 2000", "|a_i| ≤ 10^9"],
    solver=s_selection,
    specs=[("样例 1", "5\n3 1 4 1 5", 10), ("已有序", "4\n1 2 3 4", 10),
           ("逆序", "4\n4 3 2 1", 15), ("单元素", "1\n7", 15),
           ("全相同", "4\n2 2 2 2", 20), ("含负数", "5\n-1 0 -3 2 -2", 20),
           ("两元素", "2\n5 3", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
for(int i=0;i<n;++i){int m=i;
for(int j=i+1;j<n;++j)if(a[j]<a[m])m=j;
swap(a[i],a[m]);}
for(int i=0;i<n;++i){if(i)printf(" ");printf("%lld",a[i]);}
printf("\\n");return 0;}
""",
    hint="**选择排序**：每轮选最小值放到区间开头。\n\n时间 $O(n^2)$，空间 $O(1)$，**不稳定**（交换可能打乱相等元素的相对顺序）。\n\n> **优点**：交换次数最少（最多 $n-1$ 次），适合「写操作代价高」的场景。",
)

# ---------------------------------------------------------------- 4
def s_merge_sort(t):
    n, a = arr(t)
    def ms(lo, hi):
        if hi - lo <= 1:
            return
        mid = (lo + hi) // 2
        ms(lo, mid)
        ms(mid, hi)
        tmp = []
        i, j = lo, mid
        while i < mid and j < hi:
            if a[i] <= a[j]:
                tmp.append(a[i]); i += 1
            else:
                tmp.append(a[j]); j += 1
        tmp.extend(a[i:mid])
        tmp.extend(a[j:hi])
        a[lo:hi] = tmp
    ms(0, n)
    return join(a)


add(
    pid="sort-merge", title="归并排序", difficulty="中等",
    tags=["排序", "归并排序", "分治"], source="经典排序", url="https://leetcode.cn/problems/sort-an-array/",
    statement="用**归并排序**把数组升序排列并输出。\n\n归并排序的思路：把数组不断二分，直到每段只有一个元素，再两两合并有序段。\n\n**要求**：时间 $O(n\\log n)$。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数（$|a_i| \\le 10^9$）。",
    output_format="一行 $n$ 个整数，升序排列。",
    constraints=["1 ≤ n ≤ 10^5", "|a_i| ≤ 10^9", "要求 O(n log n)", "稳定排序"],
    solver=s_merge_sort,
    specs=[("样例 1", "5\n3 1 4 1 5", 10), ("已有序", "4\n1 2 3 4", 10),
           ("逆序", "4\n4 3 2 1", 15), ("单元素", "1\n7", 15),
           ("全相同", "4\n2 2 2 2", 20), ("含负数", "6\n-1 0 -3 2 -2 5", 20),
           ("两元素", "2\n5 3", 20)],
    cpp=CPP_HEADER + """vector<long long>a,tmp;
void ms(int lo,int hi){
if(hi-lo<=1)return;
int mid=(lo+hi)/2;
ms(lo,mid);ms(mid,hi);
int i=lo,j=mid,k=lo;
while(i<mid&&j<hi){if(a[i]<=a[j])tmp[k++]=a[i++];else tmp[k++]=a[j++];}
while(i<mid)tmp[k++]=a[i++];
while(j<hi)tmp[k++]=a[j++];
for(int t=lo;t<hi;++t)a[t]=tmp[t];}
int main(){int n;scanf("%d",&n);a.resize(n);tmp.resize(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
ms(0,n);
for(int i=0;i<n;++i){if(i)printf(" ");printf("%lld",a[i]);}
printf("\\n");return 0;}
""",
    hint="**分治三步**：\n\n1. **分**：把区间对半分；\n2. **治**：递归排序左右两半；\n3. **合**：把两个有序段归并成一个（双指针比较取小）。\n\n时间 $O(n\\log n)$，空间 $O(n)$，**稳定**。\n\n> **归并的副产品**：合并时可以顺便统计**逆序对**（见另一道题）。",
)

# ---------------------------------------------------------------- 5
def s_counting_sort(t):
    n, a = arr(t)
    cnt = {}
    for x in a:
        cnt[x] = cnt.get(x, 0) + 1
    res = []
    for k in sorted(cnt):
        res.extend([k] * cnt[k])
    return join(res)


add(
    pid="sort-counting", title="计数排序", difficulty="简单",
    tags=["排序", "计数排序", "非比较排序"], source="经典排序", url="https://leetcode.cn/problems/sort-an-array/",
    statement="用**计数排序**把数组升序排列并输出。\n\n计数排序的思路：统计每个值出现的次数，再按值从小到大依次输出。\n\n**要求**：时间 $O(n + V)$（$V$ 为值域大小），**非比较排序**。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数（$0 \\le a_i \\le 10^4$）。",
    output_format="一行 $n$ 个整数，升序排列。",
    constraints=["1 ≤ n ≤ 10^5", "0 ≤ a_i ≤ 10^4", "值域较小，适合计数排序"],
    solver=s_counting_sort,
    specs=[("样例 1", "5\n3 1 4 1 5", 10), ("已有序", "4\n1 2 3 4", 10),
           ("逆序", "4\n4 3 2 1", 15), ("单元素", "1\n7", 15),
           ("全相同", "4\n2 2 2 2", 20), ("含 0", "5\n0 3 0 1 0", 20),
           ("跨度大", "4\n0 0 10000 10000", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);
const int MAXV=10000;
vector<int>cnt(MAXV+1,0);
for(int i=0;i<n;++i){int x;scanf("%d",&x);++cnt[x];}
bool first=true;
for(int v=0;v<=MAXV;++v)for(int k=0;k<cnt[v];++k){
if(!first)printf(" ");printf("%d",v);first=false;}
printf("\\n");return 0;}
""",
    hint="**计数排序**：\n\n1. 开一个大小为值域的计数数组；\n2. 遍历原数组，`cnt[a[i]]++`；\n3. 按值从小到大，把每个值输出 `cnt[v]` 次。\n\n时间 $O(n + V)$，空间 $O(V)$。\n\n> **适用条件**：值域不能太大（否则计数数组开不下）。值域大时改用**基数排序**。\n\n> **稳定性**：上面的写法天然稳定（按值输出，同值保持原序）。",
)

# ---------------------------------------------------------------- 6
def s_by_parity(t):
    n, a = arr(t)
    even = [x for x in a if x % 2 == 0]
    odd = [x for x in a if x % 2 != 0]
    return join(even + odd)


add(
    pid="sort-by-parity", title="按奇偶排序数组", difficulty="入门",
    tags=["数组", "双指针", "排序"], source="LeetCode 905", url="https://leetcode.cn/problems/sort-array-by-parity/",
    statement="给定一个整数数组，把所有**偶数**移到前面、**奇数**移到后面。\n\n**要求**：两部分的**相对顺序可以任意**。\n\n> 本题约定输出**保持偶数和奇数各自的原始相对顺序**（便于判题唯一）。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 5000$）。\n\n第二行 $n$ 个整数（$0 \\le a_i \\le 5000$）。",
    output_format="一行 $n$ 个整数，偶数在前、奇数在后。",
    constraints=["1 ≤ n ≤ 5000", "0 ≤ a_i ≤ 5000", "保持各自相对顺序"],
    solver=s_by_parity,
    specs=[("样例 1", "4\n3 1 2 4", 10), ("全偶", "3\n2 4 6", 10),
           ("全奇", "3\n1 3 5", 15), ("单元素偶", "1\n2", 15),
           ("单元素奇", "1\n3", 20), ("含 0", "4\n0 1 2 3", 20),
           ("交替", "6\n1 2 3 4 5 6", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<int>a(n);
for(int i=0;i<n;++i)scanf("%d",&a[i]);
bool first=true;
for(int pass=0;pass<2;++pass)
for(int i=0;i<n;++i)
if((pass==0&&a[i]%2==0)||(pass==1&&a[i]%2!=0)){
if(!first)printf(" ");printf("%d",a[i]);first=false;}
printf("\\n");return 0;}
""",
    hint="**两趟扫描**：第一趟输出所有偶数，第二趟输出所有奇数。\n\n时间 $O(n)$，空间 $O(1)$（直接输出，不必真的移动）。\n\n> **原地版（双指针）**：`l` 从左找奇数、`r` 从右找偶数，交换——但那样会打乱相对顺序。",
)

# ---------------------------------------------------------------- 7
def s_squares(t):
    n, a = arr(t)
    res = sorted(x * x for x in a)
    return join(res)


add(
    pid="sort-squares", title="有序数组的平方", difficulty="简单",
    tags=["数组", "双指针", "排序"], source="LeetCode 977", url="https://leetcode.cn/problems/squares-of-a-sorted-array/",
    statement="给定一个**非递减**数组（可能含负数），把每个元素**平方**后，按**升序**输出。\n\n**进阶**：用**双指针**在 $O(n)$ 内完成（不用排序）。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 10^4$）。\n\n第二行 $n$ 个整数（非递减，$|a_i| \\le 10^4$）。",
    output_format="一行 $n$ 个整数，为平方后的升序序列。",
    constraints=["1 ≤ n ≤ 10^4", "数组非递减", "|a_i| ≤ 10^4", "建议 O(n)"],
    solver=s_squares,
    specs=[("样例 1", "5\n-4 -1 0 3 10", 10), ("样例 2", "5\n-7 -3 2 3 11", 10),
           ("全负", "3\n-3 -2 -1", 15), ("全正", "3\n1 2 3", 15),
           ("单元素", "1\n-5", 20), ("含零", "5\n-2 -1 0 1 2", 20),
           ("两端对称", "4\n-3 -2 2 3", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
vector<long long>res(n);
int l=0,r=n-1;
for(int k=n-1;k>=0;--k){
if(llabs(a[l])>llabs(a[r])){res[k]=a[l]*a[l];++l;}
else{res[k]=a[r]*a[r];--r;}}
for(int i=0;i<n;++i){if(i)printf(" ");printf("%lld",res[i]);}
printf("\\n");return 0;}
""",
    hint="**双指针从两端向中间**：数组非递减，平方后的最大值一定出现在**两端**（绝对值最大的地方）。\n\n用 `l`、`r` 分别指向两端，每次比较 `|a[l]|` 与 `|a[r]|`，把较大的平方值填到结果数组的**末尾**，然后移动那一侧的指针。\n\n时间 $O(n)$，空间 $O(n)$。",
)

# ---------------------------------------------------------------- 8
def s_relative_ranks(t):
    n, a = arr(t)
    order = sorted(range(n), key=lambda i: -a[i])
    res = [""] * n
    medals = {0: "Gold Medal", 1: "Silver Medal", 2: "Bronze Medal"}
    for rank, idx in enumerate(order):
        res[idx] = medals.get(rank, str(rank + 1))
    return " ".join(res) + "\n"


add(
    pid="sort-relative-ranks", title="相对名次", difficulty="简单",
    tags=["数组", "排序", "哈希表"], source="LeetCode 506", url="https://leetcode.cn/problems/relative-ranks/",
    statement="给定各选手的得分，输出每个选手的**名次**。\n\n**输出格式**：前 3 名分别输出 `Gold Medal`、`Silver Medal`、`Bronze Medal`，其余输出名次数字（如 `4`）。\n\n得分**互不相同**。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 10^4$）。\n\n第二行 $n$ 个互不相同的整数（$0 \\le a_i \\le 10^6$）。",
    output_format="一行 $n$ 个名次标记，以空格分隔（顺序与输入一致）。",
    constraints=["1 ≤ n ≤ 10^4", "得分互不相同"],
    solver=s_relative_ranks,
    specs=[("样例 1", "5\n5 4 3 2 1", 10), ("样例 2", "5\n10 3 8 9 4", 10),
           ("单元素", "1\n100", 15), ("两元素", "2\n1 2", 15),
           ("三元素", "3\n3 1 2", 20), ("四元素", "4\n4 3 2 1", 20),
           ("乱序", "6\n7 1 5 3 9 2", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
vector<int>idx(n);for(int i=0;i<n;++i)idx[i]=i;
sort(idx.begin(),idx.end(),[&](int x,int y){return a[x]>a[y];});
vector<string>res(n);
for(int r=0;r<n;++r){
if(r==0)res[idx[r]]="Gold Medal";
else if(r==1)res[idx[r]]="Silver Medal";
else if(r==2)res[idx[r]]="Bronze Medal";
else res[idx[r]]=to_string(r+1);}
for(int i=0;i<n;++i){if(i)printf(" ");printf("%s",res[i].c_str());}
printf("\\n");return 0;}
""",
    hint="**排序下标**：把下标按得分降序排序，得到名次顺序；再把名次写回对应下标。\n\n> **易错点**：排序的是**下标**而不是得分本身——否则无法知道名次属于哪个选手。",
)

# ---------------------------------------------------------------- 9
def s_height_checker(t):
    n, a = arr(t)
    s = sorted(a)
    return f"{sum(1 for i in range(n) if a[i] != s[i])}\n"


add(
    pid="sort-height-checker", title="高度检查器", difficulty="入门",
    tags=["数组", "排序"], source="LeetCode 1051", url="https://leetcode.cn/problems/height-checker/",
    statement="给定一个身高数组，把它**升序排列**后，统计**有多少个位置**上的身高与原来不同。\n\n输出这个数量。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 100$）。\n\n第二行 $n$ 个整数（$1 \\le a_i \\le 100$）。",
    output_format="一行一个整数，表示位置不同的个数。",
    constraints=["1 ≤ n ≤ 100", "1 ≤ a_i ≤ 100"],
    solver=s_height_checker,
    specs=[("样例 1", "6\n1 1 4 2 1 3", 10), ("样例 2", "5\n5 1 2 3 4", 10),
           ("样例 3（已有序）", "5\n1 2 3 4 5", 15), ("全相同", "3\n2 2 2", 15),
           ("单元素", "1\n5", 20), ("完全逆序", "4\n4 3 2 1", 20),
           ("两元素", "2\n2 1", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<int>a(n),s;
for(int i=0;i<n;++i){scanf("%d",&a[i]);s.push_back(a[i]);}
sort(s.begin(),s.end());
int c=0;for(int i=0;i<n;++i)if(a[i]!=s[i])++c;
printf("%d\\n",c);return 0;}
""",
    hint="**排序后逐位比较**：把原数组复制一份排序，然后逐位对比，统计不同的位置数。\n\n时间 $O(n\\log n)$。",
)

# ---------------------------------------------------------------- 10
def s_insert_position(t):
    ls = t.strip("\n").split("\n")
    n, target = map(int, ls[0].split())
    a = list(map(int, ls[1].split()))
    lo, hi = 0, n
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return f"{lo}\n"


add(
    pid="search-insert-position", title="搜索插入位置", difficulty="入门",
    tags=["二分查找", "数组"], source="LeetCode 35", url="https://leetcode.cn/problems/search-insert-position/",
    statement="给定一个**无重复、升序**数组和目标值 $target$，若存在则返回其下标；\n\n若不存在，返回它**按顺序插入**后应有的下标。\n\n**要求 $O(\\log n)$**。",
    input_format="第一行两个整数 $n, target$（$1 \\le n \\le 10^4$）。\n\n第二行 $n$ 个**严格递增**的整数（$|a_i| \\le 10^4$）。",
    output_format="一行一个整数，表示下标。",
    constraints=["1 ≤ n ≤ 10^4", "数组严格递增", "|a_i| ≤ 10^4", "要求 O(log n)"],
    solver=s_insert_position,
    specs=[("样例 1（存在）", "4 5\n1 3 5 6", 10),
           ("样例 2（插入中间）", "4 2\n1 3 5 6", 10),
           ("样例 3（插入末尾）", "4 7\n1 3 5 6", 15),
           ("插入开头", "4 0\n1 3 5 6", 15), ("单元素命中", "1 5\n5", 20),
           ("单元素插入前", "1 3\n5", 20), ("单元素插入后", "1 7\n5", 20)],
    cpp=CPP_HEADER + """int main(){int n;long long target;scanf("%d %lld",&n,&target);
vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
int lo=0,hi=n;
while(lo<hi){int mid=lo+(hi-lo)/2;
if(a[mid]<target)lo=mid+1;else hi=mid;}
printf("%d\\n",lo);return 0;}
""",
    hint="**等价于 `lower_bound`**：求第一个不小于 $target$ 的位置。\n\n半开区间写法：`a[mid] < target` 时 `lo = mid + 1`，否则 `hi = mid`。\n\n结果 `lo` 既可能是「找到的下标」，也可能是「应插入的位置」——两者天然统一。",
)

# ---------------------------------------------------------------- 11
def s_peak(t):
    n, a = arr(t)
    lo, hi = 0, n - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] > a[mid + 1]:
            hi = mid
        else:
            lo = mid + 1
    return f"{lo}\n"


add(
    pid="search-peak-element", title="寻找峰值", difficulty="中等",
    tags=["二分查找", "数组"], source="LeetCode 162", url="https://leetcode.cn/problems/find-peak-element/",
    statement="**峰值**指**严格大于**左右相邻元素的元素。\n\n给定数组（边界外视为 $-\\infty$），返回**任意一个**峰值的下标。\n\n**要求 $O(\\log n)$**。\n\n> 为保证判题唯一：本题约定返回**最靠左**的峰值下标。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 1000$）。\n\n第二行 $n$ 个**互不相同**的整数（$|a_i| \\le 10^9$）。",
    output_format="一行一个整数，表示峰值下标。",
    constraints=["1 ≤ n ≤ 1000", "元素互不相同", "要求 O(log n)"],
    solver=s_peak,
    specs=[("样例 1", "4\n1 2 3 1", 10), ("样例 2", "7\n1 2 1 3 5 6 4", 10),
           ("单元素", "1\n5", 15), ("递增", "4\n1 2 3 4", 15),
           ("递减", "4\n4 3 2 1", 20), ("两元素递增", "2\n1 2", 20),
           ("两元素递减", "2\n2 1", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
int lo=0,hi=n-1;
while(lo<hi){int mid=lo+(hi-lo)/2;
if(a[mid]>a[mid+1])hi=mid;else lo=mid+1;}
printf("%d\\n",lo);return 0;}
""",
    hint="**二分找「上升沿」**：比较 `a[mid]` 与 `a[mid+1]`：\n\n- 若 `a[mid] > a[mid+1]`，说明右侧在下降，**峰值一定在 `mid` 或更左** → `hi = mid`；\n- 否则右侧在上升，**峰值一定在 `mid` 右侧** → `lo = mid + 1`。\n\n> **直觉**：只要沿着「往上走」的方向前进，一定能走到某个峰值（因为边界外是 $-\\infty$）。",
)

# ---------------------------------------------------------------- 12
def s_first_last(t):
    ls = t.strip("\n").split("\n")
    n, target = map(int, ls[0].split())
    a = list(map(int, ls[1].split()))
    def lower(x):
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            if a[mid] < x:
                lo = mid + 1
            else:
                hi = mid
        return lo
    def upper(x):
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            if a[mid] <= x:
                lo = mid + 1
            else:
                hi = mid
        return lo
    l = lower(target)
    r = upper(target) - 1
    if l > r:
        return "-1 -1\n"
    return f"{l} {r}\n"


add(
    pid="search-first-last", title="查找元素的第一个和最后一个位置", difficulty="中等",
    tags=["二分查找", "数组"], source="LeetCode 34", url="https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/",
    statement="给定**非递减**数组和目标值 $target$，返回它在数组中**第一次和最后一次出现**的下标。\n\n若不存在，输出 `-1 -1`。\n\n**要求 $O(\\log n)$**。",
    input_format="第一行两个整数 $n, target$（$1 \\le n \\le 10^5$）。\n\n第二行 $n$ 个**非递减**整数（$|a_i| \\le 10^9$）。",
    output_format="一行两个整数，为起始与结束下标；不存在则输出 `-1 -1`。",
    constraints=["1 ≤ n ≤ 10^5", "数组非递减", "|a_i| ≤ 10^9", "要求 O(log n)"],
    solver=s_first_last,
    specs=[("样例 1", "6 8\n5 7 7 8 8 10", 10),
           ("样例 2（不存在）", "6 6\n5 7 7 8 8 10", 10),
           ("全相同命中", "4 5\n5 5 5 5", 15), ("全相同未命中", "4 5\n1 1 1 1", 15),
           ("单元素命中", "1 7\n7", 20), ("单元素未命中", "1 7\n8", 20),
           ("重复在两端", "5 1\n1 1 2 3 4", 20)],
    cpp=CPP_HEADER + """int main(){int n;long long target;scanf("%d %lld",&n,&target);
vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
auto lower=[&](long long x){int lo=0,hi=n;
while(lo<hi){int mid=lo+(hi-lo)/2;if(a[mid]<x)lo=mid+1;else hi=mid;}return lo;};
auto upper=[&](long long x){int lo=0,hi=n;
while(lo<hi){int mid=lo+(hi-lo)/2;if(a[mid]<=x)lo=mid+1;else hi=mid;}return lo;};
int l=lower(target),r=upper(target)-1;
if(l>r)printf("-1 -1\\n");else printf("%d %d\\n",l,r);
return 0;}
""",
    hint="**两次二分**：\n\n- `lower_bound(target)` 给出**第一个 $\ge target$** 的位置，即起点；\n- `upper_bound(target) - 1` 给出**最后一个 $\le target$** 的位置，即终点。\n\n若起点 > 终点，说明不存在。\n\n时间 $O(\\log n)$。",
)

# ---------------------------------------------------------------- 13
def s_single_sorted(t):
    n, a = arr(t)
    lo, hi = 0, n - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if mid % 2 == 1:
            mid -= 1
        if a[mid] == a[mid + 1]:
            lo = mid + 2
        else:
            hi = mid
    return f"{a[lo]}\n"


add(
    pid="search-single-element", title="有序数组中的单一元素", difficulty="中等",
    tags=["二分查找", "数组", "位运算"], source="LeetCode 540", url="https://leetcode.cn/problems/single-element-in-a-sorted-array/",
    statement="给定一个**已排序**数组，其中每个元素都出现**两次**，只有一个元素出现**一次**。\n\n找出这个元素。\n\n**要求 $O(\\log n)$**。",
    input_format="第一行一个**奇数** $n$（$1 \\le n \\le 10^5$）。\n\n第二行 $n$ 个非递减整数（$|a_i| \\le 10^9$），保证恰好一个元素出现一次。",
    output_format="一行一个整数，表示只出现一次的元素。",
    constraints=["n 为奇数", "|a_i| ≤ 10^9", "恰好一个元素出现一次", "要求 O(log n)"],
    solver=s_single_sorted,
    specs=[("样例 1", "7\n1 1 2 3 3 4 4", 10),
           ("样例 2", "3\n3 3 7 7 10 11 11", 10),
           ("单元素", "1\n7", 15), ("唯一在开头", "5\n1 2 2 3 3", 15),
           ("唯一在末尾", "5\n1 1 2 2 3", 20), ("含负数", "5\n-3 -3 -1 0 0", 20),
           ("三元素", "3\n1 2 2", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
int lo=0,hi=n-1;
while(lo<hi){int mid=lo+(hi-lo)/2;
if(mid%2==1)--mid;
if(a[mid]==a[mid+1])lo=mid+2;else hi=mid;}
printf("%lld\\n",a[lo]);return 0;}
""",
    hint="**利用「成对」的规律二分**：在单一元素**之前**，所有成对元素的下标是 `(偶数, 奇数)`；**之后**则变成 `(奇数, 偶数)`。\n\n做法：把 `mid` 调整到**偶数**位置，然后比较 `a[mid]` 与 `a[mid+1]`：\n\n- 相等 → 单一元素在右侧，`lo = mid + 2`；\n- 不等 → 单一元素在 `mid` 或左侧，`hi = mid`。\n\n时间 $O(\\log n)$。\n\n> **另解**：把所有元素异或起来（$O(n)$），或利用「前缀下标和的奇偶性」。",
)

# ---------------------------------------------------------------- 14
def s_perimeter(t):
    n, a = arr(t)
    a = sorted(a, reverse=True)
    for i in range(n - 2):
        if a[i] < a[i + 1] + a[i + 2]:
            return f"{a[i] + a[i + 1] + a[i + 2]}\n"
    return "0\n"


add(
    pid="sort-largest-perimeter", title="三角形的最大周长", difficulty="简单",
    tags=["数组", "排序", "贪心"], source="LeetCode 976", url="https://leetcode.cn/problems/largest-perimeter-triangle/",
    statement="给定边长数组，从中选出 **3 条边**组成三角形，求**最大周长**。\n\n若无法组成任何三角形，输出 $0$。\n\n**组成条件**：任意两边之和大于第三边。",
    input_format="第一行一个整数 $n$（$3 \\le n \\le 10^4$）。\n\n第二行 $n$ 个正整数（$1 \\le a_i \\le 10^6$）。",
    output_format="一行一个整数，表示最大周长；无法组成三角形则输出 0。",
    constraints=["3 ≤ n ≤ 10^4", "1 ≤ a_i ≤ 10^6"],
    solver=s_perimeter,
    specs=[("样例 1", "4\n2 1 2", 10), ("样例 2（无法组成）", "3\n1 2 1", 10),
           ("样例 3", "4\n3 2 3 4", 15), ("全相同", "3\n5 5 5", 15),
           ("退化三角形", "3\n1 1 2", 20), ("大边优先", "5\n1 1 1 100 100", 20),
           ("多个候选", "6\n2 3 4 5 6 7", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
sort(a.rbegin(),a.rend());
for(int i=0;i+2<n;++i)
if(a[i]<a[i+1]+a[i+2]){printf("%lld\\n",a[i]+a[i+1]+a[i+2]);return 0;}
printf("0\\n");return 0;}
""",
    hint="**排序后贪心**：把边长**降序**排序，从最大的开始，检查连续三条能否组成三角形。\n\n**为什么只需检查相邻三条**：若 `a[i] >= a[i+1] + a[i+2]`，那么 `a[i]` 与任何更小的两条边都无法组成三角形，所以可以直接跳过 `a[i]`。\n\n时间 $O(n\\log n)$。",
)

# ---------------------------------------------------------------- 15
def s_kth_missing(t):
    ls = t.strip("\n").split("\n")
    n, k = map(int, ls[0].split())
    a = list(map(int, ls[1].split()))
    lo, hi = 0, n
    while lo < hi:
        mid = (lo + hi) // 2
        # a[mid] 之前缺失的正整数个数
        if a[mid] - mid - 1 < k:
            lo = mid + 1
        else:
            hi = mid
    return f"{lo + k}\n"


add(
    pid="search-kth-missing", title="第 K 个缺失的正整数", difficulty="简单",
    tags=["二分查找", "数组"], source="LeetCode 1539", url="https://leetcode.cn/problems/kth-missing-positive-number/",
    statement="给定一个**严格递增**的正整数数组，找出其中**第 $k$ 个缺失的正整数**。\n\n例如 `[2,3,4,7,11]` 中缺失的正整数依次是 `1,5,6,8,9,...`，第 2 个是 5。",
    input_format="第一行两个整数 $n, k$（$1 \\le n \\le 1000$，$1 \\le k \\le 1000$）。\n\n第二行 $n$ 个**严格递增**的正整数（$1 \\le a_i \\le 1000$）。",
    output_format="一行一个整数，表示第 $k$ 个缺失的正整数。",
    constraints=["1 ≤ n, k ≤ 1000", "数组严格递增", "元素为正整数"],
    solver=s_kth_missing,
    specs=[("样例 1", "5 2\n2 3 4 7 11", 10), ("样例 2", "4 5\n1 2 3 4", 10),
           ("样例 3", "2 3\n1 2", 15), ("从 1 开始无缺失", "3 1\n1 2 3", 15),
           ("首位缺失", "3 1\n2 3 4", 20), ("k 很大", "3 1000\n1 2 3", 20),
           ("单元素", "1 1\n2", 20)],
    cpp=CPP_HEADER + """int main(){int n,k;scanf("%d %d",&n,&k);vector<int>a(n);
for(int i=0;i<n;++i)scanf("%d",&a[i]);
int lo=0,hi=n;
while(lo<hi){int mid=lo+(hi-lo)/2;
if(a[mid]-mid-1<k)lo=mid+1;else hi=mid;}
printf("%d\\n",lo+k);return 0;}
""",
    hint="**关键观察**：在排好序的数组中，下标 `i` 处**前面缺失的正整数个数**是 `a[i] - i - 1`（因为前 $i+1$ 个数本该是 $1 \\sim a[i]$，实际有 $i+1$ 个）。\n\n用二分找**第一个**满足 `a[i] - i - 1 >= k` 的位置 `lo`，答案就是 `lo + k`。\n\n> **直觉**：到 `lo` 为止已有 `lo` 个不缺失的数，所以第 $k$ 个缺失值就是 `lo + k`。",
)

# ---------------------------------------------------------------- 16
def s_merge_intervals_count(t):
    ls = t.strip("\n").split("\n")
    n = int(ls[0])
    iv = [tuple(map(int, ls[i + 1].split())) for i in range(n)]
    iv.sort()
    cnt = 0
    cur_end = -1
    for s, e in iv:
        if s > cur_end:
            cnt += 1
            cur_end = e
        else:
            cur_end = max(cur_end, e)
    return f"{cnt}\n"


def _nonoverlap(t):
    ls = t.strip("\n").split("\n")
    n = int(ls[0])
    iv = [tuple(map(int, ls[i + 1].split())) for i in range(n)]
    iv.sort()
    keep = 0
    cur_end = None
    for s, e in iv:
        if cur_end is None or s >= cur_end:
            keep += 1
            cur_end = e
        else:
            cur_end = min(cur_end, e)
    return n - keep


add(
    pid="sort-non-overlapping", title="无重叠区间（最少删除数）", difficulty="中等",
    tags=["贪心", "区间", "排序"], source="LeetCode 435", url="https://leetcode.cn/problems/non-overlapping-intervals/",
    statement="给定若干区间 $[start, end]$，请删除**最少数量**的区间，使得剩下的区间**互不重叠**。\n\n**不重叠**指前一个区间的**结束**不大于后一个区间的**开始**（端点可以相接）。\n\n输出最少需要删除的区间数。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 10^5$）。\n\n接下来 $n$ 行，每行两个整数 $start, end$（$start \\le end$，$|start|, |end| \\le 10^9$）。",
    output_format="一行一个整数，表示最少删除数。",
    constraints=["1 ≤ n ≤ 10^5", "start ≤ end", "端点相接视为不重叠"],
    solver=lambda t: f"{_nonoverlap(t)}\n",
    specs=[("样例 1", "4\n1 2\n2 3\n3 4\n1 3", 10),
           ("样例 2", "3\n1 2\n1 2\n1 2", 10),
           ("样例 3", "2\n1 2\n2 3", 15), ("单区间", "1\n1 5", 15),
           ("全不重叠", "3\n1 2\n3 4\n5 6", 20), ("全重叠", "3\n1 10\n2 3\n4 5", 20),
           ("端点相接", "3\n1 2\n2 3\n3 4", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);
vector<pair<long long,long long>>v(n);
for(int i=0;i<n;++i)scanf("%lld %lld",&v[i].first,&v[i].second);
sort(v.begin(),v.end());
long long curEnd=LLONG_MIN;int keep=0;
for(auto&pr:v){
if(pr.first>=curEnd){++keep;curEnd=pr.second;}
else curEnd=min(curEnd,pr.second);}
printf("%d\\n",n-keep);return 0;}
""",
    hint="**按结束时间贪心**：先按**开始时间**排序（本题实现用 `curEnd` 跟踪当前保留区间的结束时间）。\n\n逐个考虑区间：若它的开始 $\\ge$ `curEnd`，说明不重叠，**保留**并更新 `curEnd`；否则必然重叠，需要删除——但**要保留结束更早的那个**（`curEnd = min(curEnd, end)`），这样给后面留出更多空间。\n\n答案 = 总数 − 保留数。\n\n> **更标准的写法**：直接按**结束时间升序**排序，然后贪心选择「结束最早且不与已选重叠」的区间。",
)


def _nonoverlap(t):
    ls = t.strip("\n").split("\n")
    n = int(ls[0])
    iv = [tuple(map(int, ls[i + 1].split())) for i in range(n)]
    iv.sort()
    keep = 0
    cur_end = None
    for s, e in iv:
        if cur_end is None or s >= cur_end:
            keep += 1
            cur_end = e
        else:
            cur_end = min(cur_end, e)
    return n - keep


def main() -> None:
    for p in P:
        finalize(p, OUT / f"{p['id']}.json")
        total = sum(t["score"] for t in p["tests"])
        print(f"生成 {p['id']:34s} {len(p['tests'])} 测试点, 总分 {total:3d}")


if __name__ == "__main__":
    main()
