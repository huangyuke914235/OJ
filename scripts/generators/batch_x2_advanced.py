"""综合与进阶 · 批量 X2（14 道）。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from genkit import CPP_HEADER, finalize, numbers, problem  # noqa: E402

OUT = ROOT / "oj" / "data" / "problems" / "08-advanced"
P: list = []


def add(**kw):
    P.append(problem(**kw))


def arr(t):
    v = numbers(t)
    return v[0], v[1:1 + v[0]]


# ---------------------------------------------------------------- 1
def s_decode(t):
    s = t.strip().split("\n")[0].strip()
    n = len(s)
    if n == 0:
        return "0\n"
    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 0 if s[0] == "0" else 1
    for i in range(2, n + 1):
        one = int(s[i - 1])
        two = int(s[i - 2:i])
        if 1 <= one <= 9:
            dp[i] += dp[i - 1]
        if 10 <= two <= 26:
            dp[i] += dp[i - 2]
    return f"{dp[n]}\n"


add(
    pid="dp-decode-ways", title="解码方法", difficulty="中等",
    tags=["动态规划", "字符串"], source="LeetCode 91", url="https://leetcode.cn/problems/decode-ways/",
    statement="数字字符串按以下规则解码：`A`→1、`B`→2、…、`Z`→26。\n\n给定一个只含数字的字符串，求**解码方法总数**。\n\n若无法解码（如以 0 开头），输出 $0$。",
    input_format="一行一个数字字符串 $s$（$1 \\le |s| \\le 100$）。",
    output_format="一行一个整数，表示解码方法数。",
    constraints=["1 ≤ |s| ≤ 100", "仅含数字", "0 不能单独解码"],
    solver=s_decode,
    specs=[("样例 1", "12", 10), ("样例 2", "226", 10), ("以 0 开头", "06", 15),
           ("单字符", "1", 15), ("含 10", "10", 20), ("含 27", "27", 20)],
    cpp=CPP_HEADER + """int main(){string s;cin>>s;int n=s.size();
vector<long long>dp(n+1,0);
dp[0]=1;
dp[1]=(s[0]=='0')?0:1;
for(int i=2;i<=n;++i){
int one=s[i-1]-'0',two=stoi(s.substr(i-2,2));
if(one>=1&&one<=9)dp[i]+=dp[i-1];
if(two>=10&&two<=26)dp[i]+=dp[i-2];}
printf("%lld\\n",dp[n]);return 0;}
""",
    hint="**线性 DP**：`dp[i]` = 前 $i$ 个字符的解码方法数。\n\n转移：\n\n- 若 `s[i-1]` 单独成一位（$1 \\sim 9$）→ 加上 `dp[i-1]`；\n- 若 `s[i-2..i-1]` 作为两位数在 $10 \\sim 26$ 内 → 加上 `dp[i-2]`。\n\n> **易错点**：`0` 不能单独解码；以 `0` 开头直接返回 0。",
)

# ---------------------------------------------------------------- 2
def s_min_cost_climb(t):
    n, a = arr(t)
    p2, p1 = 0, 0
    for i in range(2, n + 1):
        cur = min(p1 + a[i - 1], p2 + a[i - 2])
        p2, p1 = p1, cur
    return f"{p1}\n"


add(
    pid="dp-min-cost-climbing", title="使用最小花费爬楼梯", difficulty="简单",
    tags=["动态规划", "线性DP"], source="LeetCode 746", url="https://leetcode.cn/problems/min-cost-climbing-stairs/",
    statement="数组 `cost[i]` 表示从第 $i$ 级台阶**向上爬**需要支付的费用。\n\n你可以从下标 $0$ 或 $1$ 开始，每次爬 $1$ 或 $2$ 级。\n\n求到达**楼顶**（越过最后一级）的最小花费。",
    input_format="第一行一个整数 $n$（$2 \\le n \\le 1000$）。\n\n第二行 $n$ 个非负整数（$0 \\le cost_i \\le 999$）。",
    output_format="一行一个整数，表示最小花费。",
    constraints=["2 ≤ n ≤ 1000", "0 ≤ cost_i ≤ 999"],
    solver=s_min_cost_climb,
    specs=[("样例 1", "3\n10 15 20", 10), ("样例 2", "10\n1 100 1 1 1 100 1 1 100 1", 10),
           ("全零", "3\n0 0 0", 15), ("两元素", "2\n5 10", 15),
           ("递增", "5\n1 2 3 4 5", 20), ("大值", "3\n999 999 999", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
long long p2=0,p1=0;
for(int i=2;i<=n;++i){long long cur=min(p1+a[i-1],p2+a[i-2]);p2=p1;p1=cur;}
printf("%lld\\n",p1);return 0;}
""",
    hint="**线性 DP**：`dp[i]` = 到达第 $i$ 级台阶的最小花费。\n\n`dp[i] = min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2])`。\n\n初值 `dp[0] = dp[1] = 0`（起点不花钱）。\n\n> **注意**：答案是到达**楼顶**（第 $n$ 级之后）的花费，即 `dp[n]`。",
)

# ---------------------------------------------------------------- 3
def s_max_circular(t):
    n, a = arr(t)
    def kadane(x):
        best = cur = x[0]
        for v in x[1:]:
            cur = max(v, cur + v)
            best = max(best, cur)
        return best
    total = sum(a)
    if all(x < 0 for x in a):
        return f"{max(a)}\n"
    # 最大子数组 = max(不跨环, 总和 - 最小子数组)
    min_cur = min_best = a[0]
    for v in a[1:]:
        min_cur = min(v, min_cur + v)
        min_best = min(min_best, min_cur)
    return f"{max(kadane(a), total - min_best)}\n"


add(
    pid="dp-max-subarray-circular", title="环形子数组的最大和", difficulty="中等",
    tags=["动态规划", "Kadane", "环形"], source="LeetCode 918", url="https://leetcode.cn/problems/maximum-sum-circular-subarray/",
    statement="给定一个**环形**数组（首尾相接），求**非空连续子数组**的最大和。\n\n> **提示**：结果要么「不跨过首尾」（普通最大子段和），要么「跨过首尾」（等于「总和 − 最小子段和」）。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 3\\times10^4$）。\n\n第二行 $n$ 个整数（$|a_i| \\le 10^4$）。",
    output_format="一行一个整数，表示最大子数组和。",
    constraints=["1 ≤ n ≤ 3×10^4", "|a_i| ≤ 10^4", "子数组非空"],
    solver=s_max_circular,
    specs=[("样例 1", "3\n1 -2 3 -2", 10), ("样例 2", "3\n5 -3 5", 10),
           ("单元素", "1\n-1", 15), ("全正", "3\n1 2 3", 15),
           ("全负", "3\n-3 -2 -1", 20), ("跨环", "4\n3 -1 2 -1", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
auto kadane=[&](bool mx){long long best=a[0],cur=a[0];
for(int i=1;i<n;++i){
if(mx)cur=max(a[i],cur+a[i]);else cur=min(a[i],cur+a[i]);
if(mx)best=max(best,cur);else best=min(best,cur);}
return best;};
long long total=0;for(long long x:a)total+=x;
long long mx=kadane(true),mn=kadane(false);
long long ans=mx;
if(total-mn!=0)ans=max(ans,total-mn);
bool allNeg=true;for(long long x:a)if(x>=0)allNeg=false;
if(allNeg)ans=mx;
printf("%lld\\n",ans);return 0;}
""",
    hint="**两种情况取最大**：\n\n1. **不跨环**：直接求普通的最大子段和（Kadane）；\n2. **跨环**：等价于「总和 − **最小**子段和」（把中间那段挖掉，剩下两端接起来）。\n\n> **易错点**：若数组**全为负数**，第 2 种情况会得到「总和 − 最小子段和 = 0」（空数组），这是非法的。此时答案就是最大子段和（即最大的那个负数）。",
)

# ---------------------------------------------------------------- 4
def s_integer_break(t):
    n = int(t.strip())
    if n <= 3:
        return f"{n - 1}\n"
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        best = i
        for j in range(1, i):
            best = max(best, dp[j] * (i - j))
        dp[i] = best
    return f"{dp[n]}\n"


add(
    pid="dp-integer-break", title="整数拆分", difficulty="中等",
    tags=["动态规划", "数学"], source="LeetCode 343", url="https://leetcode.cn/problems/integer-break/",
    statement="给定正整数 $n$，把它拆成**至少两个**正整数之和，使它们的**乘积最大**。\n\n输出最大乘积。",
    input_format="一行一个整数 $n$（$2 \\le n \\le 58$）。",
    output_format="一行一个整数。",
    constraints=["2 ≤ n ≤ 58"],
    solver=s_integer_break,
    specs=[("样例 1", "2", 10), ("样例 2", "10", 10), ("n = 3", "3", 15),
           ("n = 4", "4", 15), ("n = 20", "20", 20), ("n = 58", "58", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);
if(n<=3){printf("%d\\n",n-1);return 0;}
vector<long long>dp(n+1,0);dp[1]=1;
for(int i=2;i<=n;++i){long long best=i;
for(int j=1;j<i;++j)best=max(best,dp[j]*(i-j));
dp[i]=best;}
printf("%lld\\n",dp[n]);return 0;}
""",
    hint="**线性 DP**：`dp[i]` = 把 $i$ 拆分后的最大乘积。\n\n转移：`dp[i] = max(dp[j] * (i - j))`，$j$ 从 $1$ 到 $i-1$。\n\n> **数学结论**：最优拆法是**尽量拆成 3**（余 1 时把 3+1 换成 2+2）。所以 $n \\le 3$ 时答案是 $n-1$，否则按此规律可直接算出。",
)

# ---------------------------------------------------------------- 5
def s_tribonacci(t):
    n = int(t.strip())
    a, b, c = 0, 1, 1
    if n == 0:
        return "0\n"
    if n == 1:
        return "1\n"
    for _ in range(n - 2):
        a, b, c = b, c, a + b + c
    return f"{c}\n"


add(
    pid="dp-tribonacci", title="第 N 个泰波那契数", difficulty="入门",
    tags=["动态规划", "递推"], source="LeetCode 1137", url="https://leetcode.cn/problems/n-th-tribonacci-number/",
    statement="泰波那契数列：$T_0 = 0$，$T_1 = 1$，$T_2 = 1$，且 $T_n = T_{n-1} + T_{n-2} + T_{n-3}$。\n\n给定 $n$，求 $T_n$。",
    input_format="一行一个整数 $n$（$0 \\le n \\le 37$）。",
    output_format="一行一个整数。",
    constraints=["0 ≤ n ≤ 37"],
    solver=s_tribonacci,
    specs=[("样例 1", "4", 10), ("样例 2", "25", 10), ("n = 0", "0", 15),
           ("n = 1", "1", 15), ("n = 2", "1", 20), ("n = 37", "37", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);
long long a=0,b=1,c=1;
if(n==0){printf("0\\n");return 0;}
if(n==1){printf("1\\n");return 0;}
for(int i=0;i<n-2;++i){long long t=a+b+c;a=b;b=c;c=t;}
printf("%lld\\n",c);return 0;}
""",
    hint="**滚动三个变量**：`T(n) = T(n-1) + T(n-2) + T(n-3)`，只需保留最近三项。\n\n时间 $O(n)$，空间 $O(1)$。",
)

# ---------------------------------------------------------------- 6
def s_min_cost_tickets(t):
    ls = t.strip("\n").split("\n")
    n = int(ls[0])
    days = list(map(int, ls[1].split()))
    costs = list(map(int, ls[2].split()))
    last = days[-1]
    is_travel = set(days)
    INF = 10 ** 9
    dp = [0] * (last + 1)
    for d in range(1, last + 1):
        if d not in is_travel:
            dp[d] = dp[d - 1]
            continue
        c1 = dp[d - 1] + costs[0]
        c7 = dp[max(0, d - 7)] + costs[1]
        c30 = dp[max(0, d - 30)] + costs[2]
        dp[d] = min(c1, c7, c30)
    return f"{dp[last]}\n"


add(
    pid="dp-min-cost-tickets", title="最低票价", difficulty="中等",
    tags=["动态规划", "线性DP"], source="LeetCode 983", url="https://leetcode.cn/problems/minimum-cost-for-tickets/",
    statement="你要在指定的日期出行。有三种票：\n\n- 1 日票 `costs[0]`；\n- 7 日票 `costs[1]`；\n- 30 日票 `costs[2]`。\n\n票在**购买当天起**的对应天数内有效。求完成所有出行日的**最低总花费**。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 365$），表示出行天数。\n\n第二行 $n$ 个**严格递增**的整数，表示出行日期（$1 \\le d \\le 365$）。\n\n第三行三个整数 $costs_1, costs_7, costs_{30}$（$1 \\le \\cdot \\le 1000$）。",
    output_format="一行一个整数，表示最低总花费。",
    constraints=["1 ≤ n ≤ 365", "日期严格递增", "票价 ≤ 1000"],
    solver=s_min_cost_tickets,
    specs=[("样例 1", "6\n1 4 6 7 8 20\n2 7 15", 10),
           ("样例 2", "10\n1 2 3 4 5 6 7 8 9 10\n2 7 15", 10),
           ("单日", "1\n1\n2 7 15", 15), ("全年", "3\n1 200 365\n5 20 50", 15),
           ("连续多日", "5\n1 2 3 4 5\n3 10 30", 20),
           ("稀疏出行", "3\n1 100 365\n10 50 100", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);
vector<int>days(n);for(int i=0;i<n;++i)scanf("%d",&days[i]);
int c1,c7,c30;scanf("%d %d %d",&c1,&c7,&c30);
int last=days[n-1];
vector<bool>travel(last+1,false);
for(int d:days)travel[d]=true;
vector<long long>dp(last+1,0);
for(int d=1;d<=last;++d){
if(!travel[d]){dp[d]=dp[d-1];continue;}
dp[d]=min({dp[d-1]+c1,dp[max(0,d-7)]+c7,dp[max(0,d-30)]+c30});}
printf("%lld\\n",dp[last]);return 0;}
""",
    hint="**按天递推**：`dp[d]` = 覆盖到第 $d$ 天的最低花费。\n\n- 若第 $d$ 天不出行：`dp[d] = dp[d-1]`；\n- 否则：`dp[d] = min(dp[d-1] + cost1, dp[d-7] + cost7, dp[d-30] + cost30)`（下标取 $\\max(0, \\cdot)$）。\n\n时间 $O(\\text{最后一天})$。",
)

# ---------------------------------------------------------------- 7
def s_pair_chain(t):
    ls = t.strip("\n").split("\n")
    n = int(ls[0])
    ps = [tuple(map(int, ls[i + 1].split())) for i in range(n)]
    ps.sort(key=lambda p: p[1])
    cnt = 0
    cur = float("-inf")
    for a, b in ps:
        if a > cur:
            cnt += 1
            cur = b
    return f"{cnt}\n"


add(
    pid="dp-max-length-pair-chain", title="最长数对链", difficulty="中等",
    tags=["动态规划", "贪心", "区间"], source="LeetCode 646", url="https://leetcode.cn/problems/maximum-length-of-pair-chain/",
    statement="给定若干数对 $(a, b)$（$a < b$）。若数对 $B$ 的 $a$ **严格大于**数对 $A$ 的 $b$，"
              "则称 $B$ 可以接在 $A$ 后面。\n\n求能构成的最长数对链的长度。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 1000$）。\n\n接下来 $n$ 行，每行两个整数 $a, b$（$a < b$，$|a|, |b| \\le 10^9$）。",
    output_format="一行一个整数，表示最长链长度。",
    constraints=["1 ≤ n ≤ 1000", "a < b", "接续条件为严格大于"],
    solver=s_pair_chain,
    specs=[("样例 1", "5\n1 2\n2 3\n3 4\n1 3\n4 5", 10),
           ("样例 2", "3\n1 2\n7 8\n4 5", 10), ("单数对", "1\n1 2", 15),
           ("全部可接", "3\n1 2\n3 4\n5 6", 15), ("全部冲突", "3\n1 10\n2 10\n3 10", 20),
           ("含负数", "3\n-5 -4\n-3 -2\n-1 0", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);
vector<pair<long long,long long>>v(n);
for(int i=0;i<n;++i)scanf("%lld %lld",&v[i].first,&v[i].second);
sort(v.begin(),v.end(),[](const auto&a,const auto&b){return a.second<b.second;});
int cnt=0;long long cur=LLONG_MIN;
for(auto&p:v)if(p.first>cur){++cnt;cur=p.second;}
printf("%d\\n",cnt);return 0;}
""",
    hint="**贪心（按右端点排序）**：把所有数对按**右端点 $b$ 升序**排序，然后依次尝试接续：若当前数对的 $a$ **大于**已选链的末尾 $b$，就选它并更新末尾。\n\n> **为什么贪心正确**：右端点越小，给后面留的空间越大——这是经典的**区间调度**贪心。\n\n> **DP 解法**：按 $a$ 排序后求「最长递增子序列」式的 DP，$O(n^2)$，但贪心 $O(n\\log n)$ 更优。",
)

# ---------------------------------------------------------------- 8
def s_arith_slices(t):
    n, a = arr(t)
    total = 0
    cur = 0
    for i in range(2, n):
        if a[i] - a[i - 1] == a[i - 1] - a[i - 2]:
            cur += 1
            total += cur
        else:
            cur = 0
    return f"{total}\n"


add(
    pid="dp-arithmetic-slices", title="等差数列划分", difficulty="中等",
    tags=["动态规划", "数组"], source="LeetCode 413", url="https://leetcode.cn/problems/arithmetic-slices/",
    statement="若一个数组的**相邻元素之差都相等**，则称它是**等差**的。\n\n给定数组，求其中**等差连续子数组**的个数（长度至少为 3）。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 5000$）。\n\n第二行 $n$ 个整数（$|a_i| \\le 10^4$）。",
    output_format="一行一个整数。",
    constraints=["1 ≤ n ≤ 5000", "|a_i| ≤ 10^4", "子数组长度 ≥ 3"],
    solver=s_arith_slices,
    specs=[("样例 1", "4\n1 2 3 4", 10), ("样例 2", "1\n1", 10),
           ("无等差", "3\n1 2 4", 15), ("全相同", "4\n5 5 5 5", 15),
           ("长等差", "6\n1 2 3 4 5 6", 20), ("两段等差", "6\n1 2 3 5 7 9", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
long long total=0,cur=0;
for(int i=2;i<n;++i){
if(a[i]-a[i-1]==a[i-1]-a[i-2]){++cur;total+=cur;}
else cur=0;}
printf("%lld\\n",total);return 0;}
""",
    hint="**滚动 DP**：`cur` = 以 $i$ 结尾的等差子数组个数。\n\n若 `a[i]-a[i-1] == a[i-1]-a[i-2]`，则 `cur++`；否则 `cur = 0`。每步把 `cur` 累加到答案。\n\n> **直觉**：以 $i$ 结尾的等差子数组，长度从 3 到 $\\text{cur}+2$ 共 `cur` 个。\n\n时间 $O(n)$，空间 $O(1)$。",
)

# ---------------------------------------------------------------- 9
def s_delete_earn(t):
    n, a = arr(t)
    if n == 0:
        return "0\n"
    mx = max(a)
    cnt = [0] * (mx + 1)
    for x in a:
        cnt[x] += x
    p2, p1 = 0, 0
    for v in cnt:
        p2, p1 = p1, max(p1, p2 + v)
    return f"{p1}\n"


add(
    pid="dp-delete-and-earn", title="删除并获得点数", difficulty="中等",
    tags=["动态规划", "打家劫舍"], source="LeetCode 740", url="https://leetcode.cn/problems/delete-and-earn/",
    statement="每次操作：选择任意一个数 $x$，获得 $x$ 点，然后**删除所有等于 $x-1$ 和 $x+1$ 的数**。\n\n求能获得的**最大点数**。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 2\\times10^4$）。\n\n第二行 $n$ 个正整数（$1 \\le a_i \\le 10^4$）。",
    output_format="一行一个整数。",
    constraints=["1 ≤ n ≤ 2×10^4", "1 ≤ a_i ≤ 10^4"],
    solver=s_delete_earn,
    specs=[("样例 1", "3\n3 4 2", 10), ("样例 2", "6\n2 2 3 3 3 4", 10),
           ("单元素", "1\n5", 15), ("连续值", "3\n1 2 3", 15),
           ("含重复", "5\n2 2 2 2 2", 20), ("两端值", "4\n1 1 100 100", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);
int mx=0;vector<int>a(n);
for(int i=0;i<n;++i){scanf("%d",&a[i]);mx=max(mx,a[i]);}
vector<long long>cnt(mx+1,0);
for(int x:a)cnt[x]+=x;
long long p2=0,p1=0;
for(int v=0;v<=mx;++v){long long cur=max(p1,p2+cnt[v]);p2=p1;p1=cur;}
printf("%lld\\n",p1);return 0;}
""",
    hint="**转化为打家劫舍**：\n\n先把相同值的点数合并——`cnt[x] = x × (x 的出现次数)`。\n\n于是问题变成：在序列 `cnt[1], cnt[2], ..., cnt[maxV]` 上做打家劫舍（**不能选相邻的**）。\n\n> **为什么等价**：选了 $x$ 就不能选 $x-1$ 和 $x+1$，正是「不能取相邻」的约束。\n\n时间 $O(n + \\text{maxV})$。",
)

# ---------------------------------------------------------------- 10
def s_lc_substring(t):
    ls = t.strip("\n").split("\n")
    a, b = ls[0].strip(), ls[1].strip()
    m = len(b)
    prev = [0] * (m + 1)
    best = 0
    for i in range(1, len(a) + 1):
        cur = [0] * (m + 1)
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1] + 1
                best = max(best, cur[j])
        prev = cur
    return f"{best}\n"


add(
    pid="dp-longest-common-substring", title="最长公共子串", difficulty="中等",
    tags=["动态规划", "字符串", "二维DP"], source="最长公共子串", url="https://leetcode.cn/problems/maximum-length-of-repeated-subarray/",
    statement="给定两个字符串，求它们的**最长公共子串**（**必须连续**）的长度。",
    input_format="第一行一个字符串 $a$。\n\n第二行一个字符串 $b$。\n\n长度均不超过 $1000$，仅含小写字母。",
    output_format="一行一个整数。",
    constraints=["|a|, |b| ≤ 1000", "仅小写字母", "子串必须连续"],
    solver=s_lc_substring,
    specs=[("样例 1", "abcde\nabfde", 10), ("无公共", "abc\ndef", 10),
           ("完全相同", "abc\nabc", 15), ("单字符匹配", "a\nab", 15),
           ("长匹配", "abcdefg\nxyzcdef", 20), ("重复字符", "aaaa\naa", 20)],
    cpp=CPP_HEADER + """int main(){string a,b;cin>>a>>b;
int n=a.size(),m=b.size();
vector<int>prev(m+1,0),cur(m+1,0);int best=0;
for(int i=1;i<=n;++i){
fill(cur.begin(),cur.end(),0);
for(int j=1;j<=m;++j)if(a[i-1]==b[j-1]){
cur[j]=prev[j-1]+1;best=max(best,cur[j]);}
prev=cur;}
printf("%d\\n",best);return 0;}
""",
    hint="**与 LCS 的区别**：最长公共**子串**要求**连续**。\n\n`dp[i][j]` = 「以 $a[i-1]$ 和 $b[j-1]$ **结尾**」的最长公共子串长度。\n\n- 若 `a[i-1] == b[j-1]`：`dp[i][j] = dp[i-1][j-1] + 1`；\n- **否则 `dp[i][j] = 0`**（关键区别！LCS 那里是取 max）。\n\n答案要取**整个过程中的最大值**，不是 `dp[n][m]`。",
)

# ---------------------------------------------------------------- 11
def s_01_knapsack_basic(t):
    ls = t.strip("\n").split("\n")
    n, W = map(int, ls[0].split())
    dp = [0] * (W + 1)
    for i in range(1, n + 1):
        w, v = map(int, ls[i].split())
        for j in range(W, w - 1, -1):
            if dp[j - w] + v > dp[j]:
                dp[j] = dp[j - w] + v
    return f"{dp[W]}\n"


add(
    pid="dp-01-knapsack-basic", title="0-1 背包（基础）", difficulty="中等",
    tags=["动态规划", "0-1背包"], source="经典背包问题", url="https://www.luogu.com.cn/problem/P1048",
    statement="有 $n$ 件物品和一个容量 $W$ 的背包。第 $i$ 件物品重量 $w_i$、价值 $v_i$，**每件最多选一次**。\n\n求最大总价值。",
    input_format="第一行两个整数 $n, W$（$1 \\le n \\le 1000$，$0 \\le W \\le 1000$）。\n\n接下来 $n$ 行，每行两个整数 $w_i, v_i$（$1 \\le w_i \\le 1000$，$0 \\le v_i \\le 1000$）。",
    output_format="一行一个整数。",
    constraints=["1 ≤ n, W ≤ 1000", "每件物品最多选一次"],
    solver=s_01_knapsack_basic,
    specs=[("样例 1", "3 5\n1 2\n2 3\n3 4", 10), ("容量为 0", "2 0\n1 5\n2 3", 10),
           ("装不下任何", "2 1\n5 10\n6 20", 15), ("全都能装", "2 10\n1 5\n2 6", 15),
           ("重量等于容量", "1 5\n5 10", 20), ("需取舍", "4 6\n2 3\n3 4\n4 5\n1 1", 20)],
    cpp=CPP_HEADER + """int main(){int n,W;scanf("%d %d",&n,&W);
vector<long long>dp(W+1,0);
for(int i=0;i<n;++i){int w;long long v;scanf("%d %lld",&w,&v);
for(int j=W;j>=w;--j)dp[j]=max(dp[j],dp[j-w]+v);}
printf("%lld\\n",dp[W]);return 0;}
""",
    hint="**一维滚动数组**：`dp[j]` = 容量为 $j$ 时的最大价值。\n\n对每件物品，容量 **从大到小**遍历：`dp[j] = max(dp[j], dp[j-w] + v)`。\n\n> **为什么必须倒序**：倒序保证 `dp[j-w]` 还是「没考虑当前物品」的旧值，从而每件物品只用一次。\n\n> **对比完全背包**：完全背包要**正序**。",
)

# ---------------------------------------------------------------- 12
def s_count_palindromic(t):
    s = t.strip("\n").split("\n")[0]
    n = len(s)
    cnt = 0
    for center in range(2 * n - 1):
        l = center // 2
        r = l + center % 2
        while l >= 0 and r < n and s[l] == s[r]:
            cnt += 1
            l -= 1
            r += 1
    return f"{cnt}\n"


add(
    pid="dp-count-palindromic-substrings", title="回文子串数目", difficulty="中等",
    tags=["字符串", "中心扩展", "动态规划"], source="LeetCode 647", url="https://leetcode.cn/problems/palindromic-substrings/",
    statement="给定一个字符串，统计其中**回文子串**的个数。\n\n**位置不同**的子串即使内容相同也分别计数。",
    input_format="一行一个字符串 $s$（$1 \\le |s| \\le 1000$），仅含小写字母。",
    output_format="一行一个整数。",
    constraints=["1 ≤ |s| ≤ 1000", "仅小写字母"],
    solver=s_count_palindromic,
    specs=[("样例 1", "abc", 10), ("样例 2", "aaa", 10), ("单字符", "a", 15),
           ("两相同", "aa", 15), ("全相同", "aaaa", 20), ("混合", "ababa", 20)],
    cpp=CPP_HEADER + """int main(){string s;cin>>s;int n=s.size();
long long cnt=0;
for(int c=0;c<2*n-1;++c){
int l=c/2,r=l+c%2;
while(l>=0&&r<n&&s[l]==s[r]){++cnt;--l;++r;}}
printf("%lld\\n",cnt);return 0;}
""",
    hint="**中心扩展法**：回文子串的中心有 $2n-1$ 个（$n$ 个单字符中心 + $n-1$ 个双字符中心）。\n\n对每个中心向两侧扩展，只要字符相同就计数并继续。\n\n> **编码技巧**：用 `center` 从 $0$ 到 $2n-2$，令 `l = center/2`、`r = l + center%2`——`center` 为偶数时是单字符中心，奇数时是双字符中心。\n\n时间 $O(n^2)$。",
)

# ---------------------------------------------------------------- 13
def s_jump_game(t):
    n, a = arr(t)
    reach = 0
    for i in range(n):
        if i > reach:
            return "NO\n"
        reach = max(reach, i + a[i])
    return "YES\n"


add(
    pid="dp-jump-game", title="跳跃游戏（能否到达）", difficulty="中等",
    tags=["贪心", "数组"], source="LeetCode 55", url="https://leetcode.cn/problems/jump-game/",
    statement="数组 `a[i]` 表示从位置 $i$ 最多能向右跳多少步。\n\n从下标 $0$ 出发，判断能否到达**最后一个下标**。\n\n能输出 `YES`，否则 `NO`。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 10^4$）。\n\n第二行 $n$ 个非负整数（$0 \\le a_i \\le 10^5$）。",
    output_format="一行，输出 `YES` 或 `NO`。",
    constraints=["1 ≤ n ≤ 10^4", "0 ≤ a_i ≤ 10^5"],
    solver=s_jump_game,
    specs=[("样例 1（能）", "5\n2 3 1 1 4", 10), ("样例 2（不能）", "5\n3 2 1 0 4", 10),
           ("单元素", "1\n0", 15), ("全零多元素", "3\n0 0 0", 15),
           ("一步到位", "2\n1 0", 20), ("含零", "4\n1 0 1 0", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
long long reach=0;
for(int i=0;i<n;++i){
if(i>reach){printf("NO\\n");return 0;}
reach=max(reach,(long long)i+a[i]);}
printf("YES\\n");return 0;}
""",
    hint="**贪心维护最远可达位置**：`reach` = 当前能到达的最远下标。\n\n从左到右扫描，若 `i > reach` 说明位置 $i$ **不可达**，直接失败；否则用 `i + a[i]` 更新 `reach`。\n\n时间 $O(n)$，空间 $O(1)$。\n\n> **直觉**：只要当前位置可达，就能「借力」跳到更远——不需要关心具体怎么跳。",
)

# ---------------------------------------------------------------- 14
def s_jump_game_ii(t):
    n, a = arr(t)
    jumps = 0
    cur_end = 0
    farthest = 0
    for i in range(n - 1):
        farthest = max(farthest, i + a[i])
        if i == cur_end:
            jumps += 1
            cur_end = farthest
    return f"{jumps}\n"


add(
    pid="dp-jump-game-ii", title="跳跃游戏 II（最少步数）", difficulty="中等",
    tags=["贪心", "数组", "BFS"], source="LeetCode 45", url="https://leetcode.cn/problems/jump-game-ii/",
    statement="数组 `a[i]` 表示从位置 $i$ 最多能向右跳多少步。**保证**能到达最后一个下标。\n\n求到达最后一个下标的**最少跳跃次数**。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 10^4$）。\n\n第二行 $n$ 个非负整数（$0 \\le a_i \\le 10^5$）。",
    output_format="一行一个整数，表示最少跳跃次数。",
    constraints=["1 ≤ n ≤ 10^4", "0 ≤ a_i ≤ 10^5", "保证可达"],
    solver=s_jump_game_ii,
    specs=[("样例 1", "5\n2 3 1 1 4", 10), ("单元素", "1\n0", 10),
           ("两元素", "2\n1 0", 15), ("全一跳", "4\n1 1 1 1", 15),
           ("大跳跃", "5\n10 0 0 0 0", 20), ("需两步", "3\n2 1 0", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
int jumps=0,curEnd=0;long long farthest=0;
for(int i=0;i<n-1;++i){
farthest=max(farthest,(long long)i+a[i]);
if(i==curEnd){++jumps;curEnd=farthest;}}
printf("%d\\n",jumps);return 0;}
""",
    hint="**贪心（类似 BFS 分层）**：\n\n维护三个量：`jumps`（已跳次数）、`curEnd`（当前这一跳能覆盖的右边界）、`farthest`（下一跳能到达的最远处）。\n\n扫描到 `i == curEnd` 时，说明当前这一跳的范围用完了，必须**再跳一次**：`jumps++`、`curEnd = farthest`。\n\n> **注意**：循环只需到 $n-2$（到达最后一个下标时不需要再跳）。\n\n时间 $O(n)$，空间 $O(1)$。",
)


def main() -> None:
    for p in P:
        finalize(p, OUT / f"{p['id']}.json")
        total = sum(t["score"] for t in p["tests"])
        print(f"生成 {p['id']:38s} {len(p['tests'])} 测试点, 总分 {total:3d}")


if __name__ == "__main__":
    main()
