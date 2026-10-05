"""数组与链表 · 批量 A1（14 道）。"""
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


# ---------------------------------------------------------------- 1
def s_ones(t):
    n, a = (lambda x: (x[0], x[1:]))(numbers(t))
    best = cur = 0
    for x in a:
        cur = cur + 1 if x == 1 else 0
        best = max(best, cur)
    return f"{best}\n"


add(
    pid="array-max-consecutive-ones", title="最大连续 1 的个数", difficulty="入门",
    tags=["数组", "遍历"], source="LeetCode 485", url="https://leetcode.cn/problems/max-consecutive-ones/",
    statement="给定一个只含 $0$ 和 $1$ 的数组，求其中**连续的 $1$ 的最大个数**。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数，每个为 $0$ 或 $1$。",
    output_format="一行一个整数，表示最长连续 $1$ 的个数。",
    constraints=["1 ≤ n ≤ 10^5", "元素仅为 0 或 1"],
    solver=s_ones,
    specs=[("样例 1", "6\n1 1 0 1 1 1", 10), ("样例 2（无 1）", "3\n0 0 0", 10),
           ("全为 1", "4\n1 1 1 1", 10), ("单个 1", "1\n1", 15),
           ("交替", "7\n1 0 1 0 1 0 1", 15), ("开头最长", "6\n1 1 1 0 1 1", 20),
           ("末尾最长", "6\n1 1 0 1 1 1", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);int best=0,cur=0;
for(int i=0;i<n;++i){int x;scanf("%d",&x);cur=(x==1)?cur+1:0;best=max(best,cur);}
printf("%d\\n",best);return 0;}
""",
    hint="**一次遍历**：维护 `cur`（以当前位置结尾的连续 1 个数）。遇到 1 则 `cur++`，遇到 0 则清零，每步用 `best` 记录最大值。时间 $O(n)$，空间 $O(1)$。",
)

# ---------------------------------------------------------------- 2
def s_plusone(t):
    n, a = (lambda x: (x[0], x[1:]))(numbers(t))
    for i in range(n - 1, -1, -1):
        if a[i] < 9:
            a[i] += 1
            return " ".join(map(str, a)) + "\n"
        a[i] = 0
    return "1 " + " ".join(map(str, a)) + "\n"


add(
    pid="array-plus-one", title="加一", difficulty="入门",
    tags=["数组", "模拟", "进位"], source="LeetCode 66", url="https://leetcode.cn/problems/plus-one/",
    statement="给定一个表示**非负整数**的数组，最高位在数组开头。请给这个整数**加一**，返回结果数组。\n\n例如 `[1,2,3]` 表示 123，加一后为 `[1,2,4]`。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 100$）。\n\n第二行 $n$ 个数字（$0 \\le a_i \\le 9$），表示一个非负整数，无前导零（除非该数本身为 0）。",
    output_format="一行，输出加一后的数字数组，以空格分隔。",
    constraints=["1 ≤ n ≤ 100", "0 ≤ a_i ≤ 9", "无多余前导零"],
    solver=s_plusone,
    specs=[("样例 1", "3\n1 2 3", 10), ("样例 2（进位）", "3\n1 2 9", 10),
           ("样例 3（全 9）", "3\n9 9 9", 15), ("单个 0", "1\n0", 15),
           ("单个 9", "1\n9", 15), ("末尾 9 进位", "4\n1 9 9 9", 20),
           ("无进位", "4\n5 6 7 8", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<int>a(n);
for(int i=0;i<n;++i)scanf("%d",&a[i]);
for(int i=n-1;i>=0;--i){if(a[i]<9){a[i]++;goto out;}a[i]=0;}
a.insert(a.begin(),1);
out:
for(size_t i=0;i<a.size();++i){if(i)printf(" ");printf("%d",a[i]);}
printf("\\n");return 0;}
""",
    hint="**从末尾向前处理进位**：末位加一，若小于 10 则直接返回；否则该位置 0 并继续向前。\n\n> **易错点**：若所有位都是 9（如 `[9,9,9]`），循环结束后还要在**开头插入一个 1**。",
)

# ---------------------------------------------------------------- 3
def s_pivot(t):
    n, a = (lambda x: (x[0], x[1:]))(numbers(t))
    total = sum(a)
    left = 0
    for i in range(n):
        if left == total - left - a[i]:
            return f"{i}\n"
        left += a[i]
    return "-1\n"


add(
    pid="array-pivot-index", title="寻找数组的中心下标", difficulty="入门",
    tags=["数组", "前缀和"], source="LeetCode 724", url="https://leetcode.cn/problems/find-pivot-index/",
    statement="**中心下标**指满足「左侧所有元素之和 == 右侧所有元素之和」的下标。\n\n若下标在最左端，则左侧和为 $0$；在最右端则右侧和为 $0$。\n\n请返回**最靠左**的中心下标；若不存在则返回 $-1$。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 10^4$）。\n\n第二行 $n$ 个整数 $a_i$（$-1000 \\le a_i \\le 1000$）。",
    output_format="一行一个整数，表示最靠左的中心下标；不存在则输出 $-1$。",
    constraints=["1 ≤ n ≤ 10^4", "|a_i| ≤ 1000"],
    solver=s_pivot,
    specs=[("样例 1", "6\n1 7 3 6 5 6", 10), ("样例 2（不存在）", "3\n1 2 3", 10),
           ("样例 3（最左）", "3\n2 1 -1", 15), ("单元素", "1\n5", 15),
           ("全零", "5\n0 0 0 0 0", 20), ("含负数", "5\n-1 -1 0 1 1", 20),
           ("中心在末尾", "3\n1 2 0", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n);
long long total=0;
for(int i=0;i<n;++i){scanf("%lld",&a[i]);total+=a[i];}
long long left=0;
for(int i=0;i<n;++i){if(left==total-left-a[i]){printf("%d\\n",i);return 0;}left+=a[i];}
printf("-1\\n");return 0;}
""",
    hint="**前缀和**：先求出总和 `total`，再从左往右扫描，维护已扫过的 `left`。\n\n判断条件：`left == total - left - a[i]`（即左右两侧相等）。时间 $O(n)$。",
)

# ---------------------------------------------------------------- 4
def s_single(t):
    n, a = (lambda x: (x[0], x[1:]))(numbers(t))
    r = 0
    for x in a:
        r ^= x
    return f"{r}\n"


add(
    pid="array-single-number", title="只出现一次的数字", difficulty="入门",
    tags=["数组", "位运算", "异或"], source="LeetCode 136", url="https://leetcode.cn/problems/single-number/",
    statement="给定一个数组，除某个元素只出现**一次**外，其余每个元素都出现**两次**。找出这个只出现一次的元素。\n\n**要求**：线性时间、常数空间。",
    input_format="第一行一个奇数 $n$（$1 \\le n \\le 2\\times10^5-1$）。\n\n第二行 $n$ 个整数 $a_i$（$|a_i| \\le 10^9$）。",
    output_format="一行一个整数，表示只出现一次的元素。",
    constraints=["n 为奇数", "|a_i| ≤ 10^9", "要求 O(n) 时间 / O(1) 空间"],
    solver=s_single,
    specs=[("样例 1", "3\n2 2 1", 10), ("样例 2", "5\n4 1 2 1 2", 10),
           ("单元素", "1\n7", 15), ("含负数", "5\n-3 -3 5", 15),
           ("零与正负", "7\n0 1 -1 1 -1 0 9", 20), ("大数", "3\n1000000000 1000000000 -7", 20),
           ("较长", "9\n1 2 3 4 5 4 3 2 1", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);long long r=0;
for(int i=0;i<n;++i){long long x;scanf("%lld",&x);r^=x;}
printf("%lld\\n",r);return 0;}
""",
    hint="**异或的性质**：`a ^ a = 0`、`a ^ 0 = a`，且异或满足交换律与结合律。\n\n把所有数异或起来，成对出现的元素两两抵消为 0，剩下的就是只出现一次的那个。\n\n时间 $O(n)$，空间 $O(1)$。",
)

# ---------------------------------------------------------------- 5
def s_missing(t):
    n, a = (lambda x: (x[0], x[1:]))(numbers(t))
    r = n
    for i in range(n):
        r ^= i ^ a[i]
    return f"{r}\n"


add(
    pid="array-missing-number", title="缺失的数字", difficulty="入门",
    tags=["数组", "位运算", "数学"], source="LeetCode 268", url="https://leetcode.cn/problems/missing-number/",
    statement="给定一个包含 $n$ 个**互不相同**整数的数组，元素取值范围为 $[0, n]$。\n\n请找出 $[0, n]$ 中**没有出现在数组里**的那个数。\n\n**要求**：线性时间、常数空间。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 10^5$）。\n\n第二行 $n$ 个互不相同的整数，范围 $[0, n]$。",
    output_format="一行一个整数，表示缺失的数字。",
    constraints=["1 ≤ n ≤ 10^5", "元素互不相同", "取值范围 [0, n]", "要求 O(1) 空间"],
    solver=s_missing,
    specs=[("样例 1", "3\n3 0 1", 10), ("样例 2", "2\n0 1", 10),
           ("样例 3", "9\n9 6 4 2 3 5 7 0 1", 15), ("缺 0", "3\n1 2 3", 15),
           ("缺 n", "3\n0 1 2", 15), ("单元素缺 0", "1\n1", 20),
           ("单元素缺 1", "1\n0", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);long long r=n;
for(int i=0;i<n;++i){long long x;scanf("%lld",&x);r^=(long long)i^x;}
printf("%lld\\n",r);return 0;}
""",
    hint="**异或法**：把 $0..n$ 与数组中的所有数一起异或。成对出现的抵消，剩下的就是缺失值。\n\n也可以**求和相减**：`n(n+1)/2 - sum(a)`，但要注意用 `long long` 防溢出。",
)

# ---------------------------------------------------------------- 6
def s_intersect(t):
    ls = t.strip("\n").split("\n")
    n, a = ls[0].split()[0], list(map(int, ls[1].split()))
    m, b = ls[0].split()[1], list(map(int, ls[2].split()))
    from collections import Counter
    ca, cb = Counter(a), Counter(b)
    res = sorted(k for k in ca if k in cb)
    return (" ".join(map(str, res)) + "\n") if res else "\n"


add(
    pid="array-intersection", title="两个数组的交集", difficulty="入门",
    tags=["数组", "哈希表", "集合"], source="LeetCode 349", url="https://leetcode.cn/problems/intersection-of-two-arrays/",
    statement="给定两个数组，求它们的**交集**。\n\n**输出要求**：结果中每个元素**只出现一次**，并按**升序**排列，以空格分隔；若无交集则输出空行。",
    input_format="第一行两个整数 $n, m$（$1 \\le n, m \\le 10^5$）。\n\n第二行 $n$ 个整数。\n\n第三行 $m$ 个整数。",
    output_format="一行，交集元素按升序排列；无交集则输出空行。",
    constraints=["1 ≤ n, m ≤ 10^5", "元素值 |a_i| ≤ 10^9", "结果去重且升序"],
    solver=s_intersect,
    specs=[("样例 1", "4 3\n1 2 2 1\n2 2", 10), ("样例 2（无交集）", "3 2\n1 2 3\n4 5", 10),
           ("完全相同", "3 3\n1 2 3\n3 2 1", 15), ("含负数", "4 4\n-1 0 1 2\n0 1 3 4", 15),
           ("单元素有交集", "1 1\n5\n5", 20), ("单元素无交集", "1 1\n5\n6", 20),
           ("多重重复", "6 5\n1 1 1 2 3 3\n1 3 3 4 5", 20)],
    cpp=CPP_HEADER + """int main(){int n,m;scanf("%d %d",&n,&m);
unordered_set<long long>s;
for(int i=0;i<n;++i){long long x;scanf("%lld",&x);s.insert(x);}
set<long long>res;
for(int i=0;i<m;++i){long long x;scanf("%lld",&x);if(s.count(x))res.insert(x);}
bool first=true;
for(long long x:res){if(!first)printf(" ");printf("%lld",x);first=false;}
printf("\\n");return 0;}
""",
    hint="**哈希集合**：把一个数组放进 `unordered_set`，再遍历另一个数组，命中就收集。\n\n用 `set` 收集结果可以自动**去重 + 升序**。时间 $O(n+m)$。",
)

# ---------------------------------------------------------------- 7
def s_twosum_hash(t):
    ls = t.strip("\n").split("\n")
    n = int(ls[0].split()[0])
    a = list(map(int, ls[1].split()))
    target = int(ls[2])
    seen = {}
    for i, x in enumerate(a):
        if target - x in seen:
            j = seen[target - x]
            return f"{j} {i}\n"
        seen.setdefault(x, i)
    return "-1\n"


add(
    pid="array-two-sum-hash", title="两数之和（哈希表）", difficulty="入门",
    tags=["数组", "哈希表"], source="LeetCode 1", url="https://leetcode.cn/problems/two-sum/",
    statement="给定一个**无序**数组和目标值 $target$，找出数组中**两个数**使它们的和等于 $target$，返回它们的**下标**。\n\n题目保证**恰好存在一组解**，且同一元素不能使用两次。\n\n返回时**较小的下标在前**。",
    input_format="第一行一个整数 $n$（$2 \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数 $a_i$（$|a_i| \\le 10^9$）。\n\n第三行一个整数 $target$。",
    output_format="一行两个整数，为两个下标（升序）。",
    constraints=["2 ≤ n ≤ 10^5", "|a_i| ≤ 10^9", "保证恰好一组解"],
    solver=s_twosum_hash,
    specs=[("样例 1", "4\n2 7 11 15\n9", 10), ("样例 2", "3\n3 2 4\n6", 10),
           ("样例 3", "2\n3 3\n6", 15), ("含负数", "4\n-3 4 3 90\n0", 15),
           ("答案在末尾", "5\n1 2 3 4 5\n9", 20), ("两元素", "2\n-1 1\n0", 20),
           ("大数", "4\n1000000000 1 -1000000000 2\n0", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
long long target;scanf("%lld",&target);
unordered_map<long long,int>seen;
for(int i=0;i<n;++i){auto it=seen.find(target-a[i]);
if(it!=seen.end()){printf("%d %d\\n",it->second,i);return 0;}seen.emplace(a[i],i);}
printf("-1\\n");return 0;}
""",
    hint="**一边遍历一边查表**：对每个 `a[i]`，先看 `target - a[i]` 是否已在哈希表里——在就找到了答案；不在就把 `a[i]` 和下标存入表。\n\n因为先查后插，天然保证不会用到同一个元素两次。时间 $O(n)$。",
)

# ---------------------------------------------------------------- 8
def s_dup(t):
    n, a = (lambda x: (x[0], x[1:]))(numbers(t))
    return ("YES\n" if len(set(a)) < n else "NO\n")


add(
    pid="array-contains-duplicate", title="存在重复元素", difficulty="入门",
    tags=["数组", "哈希表", "排序"], source="LeetCode 217", url="https://leetcode.cn/problems/contains-duplicate/",
    statement="判断数组中是否存在**重复元素**。存在输出 `YES`，否则输出 `NO`。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数 $a_i$（$|a_i| \\le 10^9$）。",
    output_format="一行，输出 `YES` 或 `NO`。",
    constraints=["1 ≤ n ≤ 10^5", "|a_i| ≤ 10^9"],
    solver=s_dup,
    specs=[("样例 1（有重复）", "4\n1 2 3 1", 10), ("样例 2（无重复）", "4\n1 2 3 4", 10),
           ("单元素", "1\n7", 15), ("两元素相同", "2\n5 5", 15),
           ("两元素不同", "2\n5 6", 15), ("含负数重复", "5\n-1 -2 -3 -1 0", 20),
           ("全部相同", "4\n9 9 9 9", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);unordered_set<long long>s;bool dup=false;
for(int i=0;i<n;++i){long long x;scanf("%lld",&x);if(!s.insert(x).second)dup=true;}
printf("%s\\n",dup?"YES":"NO");return 0;}
""",
    hint="**哈希集合**：边插入边判断是否已存在。\n\n也可以**先排序再检查相邻元素**（$O(n\\log n)$，空间 $O(1)$，但会修改原数组）。",
)

# ---------------------------------------------------------------- 9
def s_stock(t):
    n, a = (lambda x: (x[0], x[1:]))(numbers(t))
    best = 0
    low = a[0]
    for x in a:
        low = min(low, x)
        best = max(best, x - low)
    return f"{best}\n"


add(
    pid="array-best-time-stock", title="买卖股票的最佳时机", difficulty="简单",
    tags=["数组", "贪心"], source="LeetCode 121", url="https://leetcode.cn/problems/best-time-to-buy-and-sell-stock/",
    statement="给定一支股票每天的价格，你只能选择**某一天买入**、并在**之后的某一天卖出**（一次交易）。\n\n求能获得的最大利润；若无法获利则返回 $0$。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数 $p_i$（$0 \\le p_i \\le 10^4$），表示每天价格。",
    output_format="一行一个整数，表示最大利润。",
    constraints=["1 ≤ n ≤ 10^5", "0 ≤ p_i ≤ 10^4", "只能买卖一次"],
    solver=s_stock,
    specs=[("样例 1", "6\n7 1 5 3 6 4", 10), ("样例 2（下跌）", "5\n7 6 4 3 1", 10),
           ("单元素", "1\n5", 15), ("单调上涨", "4\n1 2 3 4", 15),
           ("最低在最后", "4\n5 4 3 2", 20), ("含 0", "4\n0 3 1 4", 20),
           ("两元素上涨", "2\n1 5", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);
long long low=1e18,best=0;
for(int i=0;i<n;++i){long long x;scanf("%lld",&x);
low=min(low,x);best=max(best,x-low);}
printf("%lld\\n",best);return 0;}
""",
    hint="**一次遍历**：维护「到目前为止的历史最低价 `low`」，对每天计算 `price - low` 并更新最大值。\n\n关键点：**先更新最低价再算利润**，保证卖出日不早于买入日。时间 $O(n)$。",
)

# ---------------------------------------------------------------- 10
def s_transpose(t):
    ls = t.strip("\n").split("\n")
    r, c = map(int, ls[0].split())
    g = [list(map(int, ls[i + 1].split())) for i in range(r)]
    out = [" ".join(str(g[i][j]) for i in range(r)) for j in range(c)]
    return "\n".join(out) + "\n"


add(
    pid="matrix-transpose", title="矩阵转置", difficulty="入门",
    tags=["矩阵", "数组", "模拟"], source="LeetCode 867", url="https://leetcode.cn/problems/transpose-matrix/",
    statement="给定一个 $r \\times c$ 的矩阵，返回它的**转置**矩阵（$c \\times r$）。\n\n转置即把原矩阵的第 $i$ 行变成新矩阵的第 $i$ 列。",
    input_format="第一行两个整数 $r, c$（$1 \\le r, c \\le 1000$）。\n\n接下来 $r$ 行，每行 $c$ 个整数（$|v| \\le 10^9$）。",
    output_format="共 $c$ 行，每行 $r$ 个整数，为转置后的矩阵。",
    constraints=["1 ≤ r, c ≤ 1000", "|v| ≤ 10^9"],
    solver=s_transpose,
    specs=[("样例 1", "2 3\n1 2 3\n4 5 6", 10), ("单元素", "1 1\n5", 10),
           ("单行", "1 3\n1 2 3", 15), ("单列", "3 1\n1\n2\n3", 15),
           ("方阵", "3 3\n1 2 3\n4 5 6\n7 8 9", 20),
           ("含负数", "2 2\n-1 2\n3 -4", 20)],
    cpp=CPP_HEADER + """int main(){int r,c;scanf("%d %d",&r,&c);
vector<vector<long long>>g(r,vector<long long>(c));
for(int i=0;i<r;++i)for(int j=0;j<c;++j)scanf("%lld",&g[i][j]);
for(int j=0;j<c;++j){for(int i=0;i<r;++i){if(i)printf(" ");printf("%lld",g[i][j]);}printf("\\n");}
return 0;}
""",
    hint="**双重循环交换下标**：新矩阵的第 $j$ 行就是原矩阵的第 $j$ 列。\n\n输出时外层遍历列、内层遍历行即可。时间 $O(rc)$。",
)

# ---------------------------------------------------------------- 11
def s_reshape(t):
    ls = t.strip("\n").split("\n")
    r, c, nr, nc = map(int, ls[0].split())
    flat = []
    for i in range(r):
        flat.extend(map(int, ls[i + 1].split()))
    if r * c != nr * nc:
        return "NO\n"
    out = [" ".join(str(flat[i * nc + j]) for j in range(nc)) for i in range(nr)]
    return "YES\n" + "\n".join(out) + "\n"


add(
    pid="matrix-reshape", title="重塑矩阵", difficulty="入门",
    tags=["矩阵", "数组", "模拟"], source="LeetCode 566", url="https://leetcode.cn/problems/reshape-the-matrix/",
    statement="给定一个 $r \\times c$ 的矩阵和目标尺寸 $nr \\times nc$。\n\n若两者**元素总数相同**，则按**行优先顺序**把矩阵重塑为 $nr \\times nc$ 并输出；否则输出 `NO`。\n\n行优先顺序指：先读第一行，再读第二行……",
    input_format="第一行四个整数 $r, c, nr, nc$（$1 \\le r,c,nr,nc \\le 1000$）。\n\n接下来 $r$ 行，每行 $c$ 个整数（$|v| \\le 10^9$）。",
    output_format="若可重塑，第一行输出 `YES`，随后 $nr$ 行输出新矩阵；否则只输出一行 `NO`。",
    constraints=["1 ≤ r,c,nr,nc ≤ 1000", "|v| ≤ 10^9"],
    solver=s_reshape,
    specs=[("样例 1", "2 2 1 4\n1 2\n3 4", 10), ("样例 2（不可重塑）", "2 2 2 4\n1 2\n3 4", 10),
           ("样例 3", "4 2 2 4\n1 2\n3 4\n5 6\n7 8", 15),
           ("单元素", "1 1 1 1\n5", 15), ("转成单列", "2 3 6 1\n1 2 3\n4 5 6", 20),
           ("转成单行", "3 2 1 6\n1 2\n3 4\n5 6", 20)],
    cpp=CPP_HEADER + """int main(){int r,c,nr,nc;scanf("%d %d %d %d",&r,&c,&nr,&nc);
vector<long long>f;f.reserve(r*c);
for(int i=0;i<r;++i)for(int j=0;j<c;++j){long long x;scanf("%lld",&x);f.push_back(x);}
if(r*c!=nr*nc){printf("NO\\n");return 0;}
printf("YES\\n");
for(int i=0;i<nr;++i){for(int j=0;j<nc;++j){if(j)printf(" ");printf("%lld",f[i*nc+j]);}printf("\\n");}
return 0;}
""",
    hint="**展平再重排**：先把矩阵按行优先读成一维数组，再按新的列数 `nc` 切分。\n\n先判断 `r*c == nr*nc`，不等直接输出 `NO`。时间 $O(rc)$。",
)

# ---------------------------------------------------------------- 12
def s_spiral(t):
    ls = t.strip("\n").split("\n")
    r, c = map(int, ls[0].split())
    g = [list(map(int, ls[i + 1].split())) for i in range(r)]
    top, bot, left, right = 0, r - 1, 0, c - 1
    res = []
    while top <= bot and left <= right:
        for j in range(left, right + 1):
            res.append(g[top][j])
        top += 1
        for i in range(top, bot + 1):
            res.append(g[i][right])
        right -= 1
        if top <= bot:
            for j in range(right, left - 1, -1):
                res.append(g[bot][j])
            bot -= 1
        if left <= right:
            for i in range(bot, top - 1, -1):
                res.append(g[i][left])
            left += 1
    return " ".join(map(str, res)) + "\n"


add(
    pid="matrix-spiral-order", title="螺旋矩阵", difficulty="中等",
    tags=["矩阵", "模拟", "边界"], source="LeetCode 54", url="https://leetcode.cn/problems/spiral-matrix/",
    statement="给定一个 $r \\times c$ 的矩阵，按**顺时针螺旋顺序**返回其中所有元素。\n\n螺旋顺序：先从左到右走完顶行，再从上到下走完右列，再从右到左走完底行，再从下到上走完左列，然后向内收缩，重复直到取完。",
    input_format="第一行两个整数 $r, c$（$1 \\le r, c \\le 500$）。\n\n接下来 $r$ 行，每行 $c$ 个整数（$|v| \\le 10^9$）。",
    output_format="一行，按螺旋顺序输出全部元素，以空格分隔。",
    constraints=["1 ≤ r, c ≤ 500", "|v| ≤ 10^9"],
    solver=s_spiral,
    specs=[("样例 1", "3 3\n1 2 3\n4 5 6\n7 8 9", 10),
           ("样例 2", "3 4\n1 2 3 4\n5 6 7 8\n9 10 11 12", 10),
           ("单行", "1 4\n1 2 3 4", 15), ("单列", "4 1\n1\n2\n3\n4", 15),
           ("单元素", "1 1\n9", 15), ("方阵 4", "4 4\n1 2 3 4\n5 6 7 8\n9 10 11 12\n13 14 15 16", 20),
           ("2 行 3 列", "2 3\n1 2 3\n4 5 6", 20)],
    cpp=CPP_HEADER + """int main(){int r,c;scanf("%d %d",&r,&c);
vector<vector<long long>>g(r,vector<long long>(c));
for(int i=0;i<r;++i)for(int j=0;j<c;++j)scanf("%lld",&g[i][j]);
int top=0,bot=r-1,left=0,right=c-1;bool first=true;
auto pr=[&](long long v){if(!first)printf(" ");printf("%lld",v);first=false;};
while(top<=bot&&left<=right){
for(int j=left;j<=right;++j)pr(g[top][j]); ++top;
for(int i=top;i<=bot;++i)pr(g[i][right]); --right;
if(top<=bot){for(int j=right;j>=left;--j)pr(g[bot][j]); --bot;}
if(left<=right){for(int i=bot;i>=top;--i)pr(g[i][left]); ++left;}
}
printf("\\n");return 0;}
""",
    hint="**四边界收缩法**：维护 `top / bot / left / right` 四个边界。\n\n依次走「顶行 → 右列 → 底行 → 左列」，每走完一条边就收缩对应边界。\n\n> **最关键的易错点**：走完顶行后**必须判断 `top <= bot` 再走底行**，否则在「单行」或「非方阵」时会把同一行重复输出。",
)

# ---------------------------------------------------------------- 13
def s_diag(t):
    ls = t.strip("\n").split("\n")
    n = int(ls[0])
    g = [list(map(int, ls[i + 1].split())) for i in range(n)]
    s = 0
    for i in range(n):
        s += g[i][i]
        if i != n - 1 - i:
            s += g[i][n - 1 - i]
    return f"{s}\n"


add(
    pid="matrix-diagonal-sum", title="矩阵对角线元素的和", difficulty="入门",
    tags=["矩阵", "模拟"], source="LeetCode 1572", url="https://leetcode.cn/problems/matrix-diagonal-sum/",
    statement="给定一个 $n \\times n$ 方阵，求**主对角线**与**副对角线**上所有元素之和。\n\n若某元素同时位于两条对角线上（即矩阵中心），**只计算一次**。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 500$）。\n\n接下来 $n$ 行，每行 $n$ 个整数（$|v| \\le 10^9$）。",
    output_format="一行一个整数，表示两条对角线元素之和。",
    constraints=["1 ≤ n ≤ 500", "|v| ≤ 10^9", "中心元素只算一次"],
    solver=s_diag,
    specs=[("样例 1", "3\n1 2 3\n4 5 6\n7 8 9", 10), ("单元素", "1\n5", 10),
           ("2 阶", "2\n1 2\n3 4", 15), ("4 阶", "4\n1 1 1 1\n1 1 1 1\n1 1 1 1\n1 1 1 1", 15),
           ("含负数", "3\n-1 2 3\n4 -5 6\n7 8 -9", 20),
           ("5 阶", "5\n1 2 3 4 5\n6 7 8 9 10\n11 12 13 14 15\n16 17 18 19 20\n21 22 23 24 25", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);long long s=0;
for(int i=0;i<n;++i)for(int j=0;j<n;++j){long long x;scanf("%lld",&x);
if(i==j)s+=x; if(i+j==n-1&&i!=j)s+=x;}
printf("%lld\\n",s);return 0;}
""",
    hint="**边读边累加**：主对角线元素满足 `i == j`，副对角线满足 `i + j == n - 1`。\n\n> **易错点**：当 $n$ 为奇数时中心元素被两条对角线同时覆盖，要加 `i != j` 条件避免重复计算。",
)

# ---------------------------------------------------------------- 14
def s_max_pair(t):
    n, a = (lambda x: (x[0], x[1:]))(numbers(t))
    a = sorted(a, reverse=True)
    return f"{a[0] * a[1]}\n"


add(
    pid="array-max-product-pair", title="数组中两元素的最大乘积", difficulty="入门",
    tags=["数组", "排序", "贪心"], source="LeetCode 1464", url="https://leetcode.cn/problems/maximum-product-of-two-elements-in-an-array/",
    statement="给定一个整数数组，选出**两个不同的元素**使它们的乘积最大，输出这个乘积。",
    input_format="第一行一个整数 $n$（$2 \\le n \\le 500$）。\n\n第二行 $n$ 个整数 $a_i$（$1 \\le a_i \\le 1000$）。",
    output_format="一行一个整数，表示最大乘积。",
    constraints=["2 ≤ n ≤ 500", "1 ≤ a_i ≤ 1000"],
    solver=s_max_pair,
    specs=[("样例 1", "4\n3 4 5 2", 10), ("样例 2", "4\n1 5 4 5", 10),
           ("两元素", "2\n3 7", 15), ("全部相同", "3\n5 5 5", 15),
           ("最小值组合", "5\n1 2 3 4 1000", 20), ("含大值", "4\n1000 999 1 2", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);
long long m1=0,m2=0;
for(int i=0;i<n;++i){long long x;scanf("%lld",&x);
if(x>m1){m2=m1;m1=x;}else if(x>m2)m2=x;}
printf("%lld\\n",m1*m2);return 0;}
""",
    hint="**只需找出最大的两个数**。可以排序后取前两个，也可以一次遍历维护「最大值」和「次大值」。\n\n时间 $O(n)$（不排序），空间 $O(1)$。",
)


def main() -> None:
    for p in P:
        path = finalize(p, OUT / f"{p['id']}.json")
        total = sum(t["score"] for t in p["tests"])
        print(f"生成 {p['id']:32s} {len(p['tests'])} 测试点, 总分 {total:3d}")


if __name__ == "__main__":
    main()
