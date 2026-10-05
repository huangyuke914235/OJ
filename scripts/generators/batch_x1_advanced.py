"""综合与进阶 · 批量 X1（16 道）。"""
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
def s_fib(t):
    n = int(t.strip())
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return f"{a}\n"


add(
    pid="dp-fibonacci", title="斐波那契数列", difficulty="入门",
    tags=["动态规划", "递推"], source="LeetCode 509", url="https://leetcode.cn/problems/fibonacci-number/",
    statement="斐波那契数列定义为 $F(0)=0$、$F(1)=1$，且 $F(n) = F(n-1) + F(n-2)$。\n\n给定 $n$，求 $F(n)$。\n\n**要求**：用**滚动变量**把空间压到 $O(1)$。",
    input_format="一行一个整数 $n$（$0 \\le n \\le 90$）。",
    output_format="一行一个整数，表示 $F(n)$。",
    constraints=["0 ≤ n ≤ 90", "结果可能超出 int 范围，需用 long long"],
    solver=s_fib,
    specs=[("样例 1", "2", 10), ("样例 2", "3", 10), ("样例 3", "4", 15),
           ("n = 0", "0", 15), ("n = 1", "1", 20), ("n = 30", "30", 20),
           ("n = 90", "90", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);
long long a=0,b=1;
for(int i=0;i<n;++i){long long t=a+b;a=b;b=t;}
printf("%lld\\n",a);return 0;}
""",
    hint="**滚动变量**：只保留 `F(n-2)` 和 `F(n-1)` 两个变量，每步更新。\n\n时间 $O(n)$，空间 $O(1)$。\n\n> **易错点**：$F(90) \\approx 2.88 \\times 10^{18}$，接近 `long long` 上限（约 $9.2 \\times 10^{18}$），所以 $n \\le 90$ 是安全的；再大就需要高精度。",
)

# ---------------------------------------------------------------- 2
def s_climb(t):
    n = int(t.strip())
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return f"{a}\n"


add(
    pid="dp-climb-stairs", title="爬楼梯", difficulty="入门",
    tags=["动态规划", "递推"], source="LeetCode 70", url="https://leetcode.cn/problems/climbing-stairs/",
    statement="每次可以爬 $1$ 级或 $2$ 级台阶，问爬到第 $n$ 级共有多少种**不同的方法**。",
    input_format="一行一个整数 $n$（$1 \\le n \\le 45$）。",
    output_format="一行一个整数，表示方法数。",
    constraints=["1 ≤ n ≤ 45"],
    solver=s_climb,
    specs=[("样例 1", "2", 10), ("样例 2", "3", 10), ("n = 1", "1", 15),
           ("n = 4", "4", 15), ("n = 10", "10", 20), ("n = 45", "45", 20),
           ("n = 5", "5", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);
long long a=1,b=1;
for(int i=0;i<n;++i){long long t=a+b;a=b;b=t;}
printf("%lld\\n",a);return 0;}
""",
    hint="**状态转移**：到达第 $n$ 级的方法数 = 到达第 $n-1$ 级的方法数 + 到达第 $n-2$ 级的方法数（最后一步要么跨 1 级、要么跨 2 级）。\n\n即 `f(n) = f(n-1) + f(n-2)`，与斐波那契同构。\n\n> **易错点**：初值 `f(0) = 1`、`f(1) = 1`。",
)

# ---------------------------------------------------------------- 3
def s_rob(t):
    n, a = arr(t)
    prev2, prev1 = 0, 0
    for x in a:
        prev2, prev1 = prev1, max(prev1, prev2 + x)
    return f"{prev1}\n"


add(
    pid="dp-house-robber", title="打家劫舍", difficulty="简单",
    tags=["动态规划", "线性DP"], source="LeetCode 198", url="https://leetcode.cn/problems/house-robber/",
    statement="一排房屋，第 $i$ 间有金额 $a_i$。**不能偷相邻的两间**（否则会触发警报）。\n\n求能偷到的**最大金额**。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 100$）。\n\n第二行 $n$ 个非负整数（$0 \\le a_i \\le 400$）。",
    output_format="一行一个整数，表示最大金额。",
    constraints=["1 ≤ n ≤ 100", "0 ≤ a_i ≤ 400"],
    solver=s_rob,
    specs=[("样例 1", "4\n1 2 3 1", 10), ("样例 2", "5\n2 7 9 3 1", 10),
           ("单间", "1\n5", 15), ("两间", "2\n2 7", 15),
           ("全零", "3\n0 0 0", 20), ("递增", "5\n1 2 3 4 5", 20),
           ("取奇数位", "5\n10 1 10 1 10", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);
long long p2=0,p1=0;
for(int i=0;i<n;++i){long long x;scanf("%lld",&x);
long long cur=max(p1,p2+x);p2=p1;p1=cur;}
printf("%lld\\n",p1);return 0;}
""",
    hint="**状态定义**：`dp[i]` = 考虑前 $i$ 间房能偷到的最大金额。\n\n**转移**：`dp[i] = max(dp[i-1], dp[i-2] + a[i])`——要么不偷第 $i$ 间，要么偷它（那就不能偷第 $i-1$ 间）。\n\n用两个滚动变量把空间压到 $O(1)$。时间 $O(n)$。",
)

# ---------------------------------------------------------------- 4
def s_rob2(t):
    n, a = arr(t)
    if n == 1:
        return f"{a[0]}\n"
    def rob(x):
        p2, p1 = 0, 0
        for v in x:
            p2, p1 = p1, max(p1, p2 + v)
        return p1
    return f"{max(rob(a[:-1]), rob(a[1:]))}\n"


add(
    pid="dp-house-robber-ii", title="打家劫舍 II（环形）", difficulty="中等",
    tags=["动态规划", "线性DP", "环形"], source="LeetCode 213", url="https://leetcode.cn/problems/house-robber-ii/",
    statement="房屋排成**一个环**（第一间和最后一间相邻），仍然不能偷相邻的两间。\n\n求最大金额。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 100$）。\n\n第二行 $n$ 个非负整数（$0 \\le a_i \\le 1000$）。",
    output_format="一行一个整数，表示最大金额。",
    constraints=["1 ≤ n ≤ 100", "0 ≤ a_i ≤ 1000"],
    solver=s_rob2,
    specs=[("样例 1", "3\n2 3 2", 10), ("样例 2", "4\n1 2 3 1", 10),
           ("单间", "1\n5", 15), ("两间", "2\n1 2", 15),
           ("三间全同", "3\n5 5 5", 20), ("四间", "4\n2 7 9 3", 20),
           ("全零", "3\n0 0 0", 20)],
    cpp=CPP_HEADER + """long long rob(vector<long long>&v){long long p2=0,p1=0;
for(long long x:v){long long c=max(p1,p2+x);p2=p1;p1=c;}return p1;}
int main(){int n;scanf("%d",&n);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
if(n==1){printf("%lld\\n",a[0]);return 0;}
vector<long long>x(a.begin(),a.end()-1),y(a.begin()+1,a.end());
printf("%lld\\n",max(rob(x),rob(y)));return 0;}
""",
    hint="**拆环成两个线性问题**：\n\n因为第一间和最后一间相邻，它们**不能同时偷**。于是分两种情况：\n\n1. **不偷最后一间** → 问题退化为 $a[0..n-2]$ 的线性打家劫舍；\n2. **不偷第一间** → 问题退化为 $a[1..n-1]$ 的线性打家劫舍。\n\n答案取两者最大值。\n\n> **易错点**：$n = 1$ 时要特判（只有一间房，直接偷）。",
)

# ---------------------------------------------------------------- 5
def s_coin(t):
    ls = t.strip("\n").split("\n")
    n, amount = map(int, ls[0].split())
    coins = list(map(int, ls[1].split()))
    INF = amount + 1
    dp = [0] + [INF] * amount
    for i in range(1, amount + 1):
        for c in coins:
            if c <= i and dp[i - c] + 1 < dp[i]:
                dp[i] = dp[i - c] + 1
    return f"{dp[amount] if dp[amount] != INF else -1}\n"


add(
    pid="dp-coin-change", title="零钱兑换（最少硬币数）", difficulty="中等",
    tags=["动态规划", "完全背包"], source="LeetCode 322", url="https://leetcode.cn/problems/coin-change/",
    statement="给定若干种硬币面额（每种**数量无限**）和目标金额，求凑出目标金额所需的**最少硬币数**。\n\n若无法凑出，输出 $-1$。",
    input_format="第一行两个整数 $n, amount$（$1 \\le n \\le 12$，$0 \\le amount \\le 10^4$）。\n\n第二行 $n$ 个正整数面额（$1 \\le c_i \\le 10^4$）。",
    output_format="一行一个整数，表示最少硬币数；无法凑出则输出 -1。",
    constraints=["1 ≤ n ≤ 12", "0 ≤ amount ≤ 10^4", "每种硬币数量无限"],
    solver=s_coin,
    specs=[("样例 1", "3 11\n1 2 5", 10), ("样例 2（无法凑出）", "1 3\n2", 10),
           ("amount = 0", "2 0\n1 2", 15), ("单种硬币可凑", "1 10\n5", 15),
           ("单种不可凑", "1 10\n3", 20), ("面额较大", "2 100\n50 30", 20),
           ("需要多枚", "3 27\n2 5 10", 20)],
    cpp=CPP_HEADER + """int main(){int n,amount;scanf("%d %d",&n,&amount);
vector<int>c(n);for(int i=0;i<n;++i)scanf("%d",&c[i]);
const int INF=1e9;
vector<int>dp(amount+1,INF);dp[0]=0;
for(int i=1;i<=amount;++i)
for(int co:c)if(co<=i&&dp[i-co]+1<dp[i])dp[i]=dp[i-co]+1;
printf("%d\\n",dp[amount]==INF?-1:dp[amount]);return 0;}
""",
    hint="**完全背包求最小值**：`dp[j]` = 凑出金额 $j$ 所需的最少硬币数。\n\n转移：`dp[j] = min(dp[j], dp[j - c] + 1)`（对每种面额 $c$ 都试一遍）。\n\n> **关键**：因为硬币**可以重复使用**，内层遍历面额时**正序**更新即可（这里外层是金额、内层是面额，天然允许重复）。\n\n> **初值**：`dp[0] = 0`，其余为 $\\infty$（表示不可达）。",
)

# ---------------------------------------------------------------- 6
def s_coin2(t):
    ls = t.strip("\n").split("\n")
    n, amount = map(int, ls[0].split())
    coins = list(map(int, ls[1].split()))
    dp = [0] * (amount + 1)
    dp[0] = 1
    for c in coins:
        for j in range(c, amount + 1):
            dp[j] += dp[j - c]
    return f"{dp[amount]}\n"


add(
    pid="dp-coin-change-ii", title="零钱兑换 II（方案数）", difficulty="中等",
    tags=["动态规划", "完全背包", "计数"], source="LeetCode 518", url="https://leetcode.cn/problems/coin-change-ii/",
    statement="给定若干种硬币面额（每种**数量无限**）和目标金额，求凑出目标金额的**方案数**。\n\n**方案数按组合计**：例如面额 `[1,2,5]` 凑 5，`1+2+2` 与 `2+1+2` 视为**同一种**方案。",
    input_format="第一行两个整数 $n, amount$（$1 \\le n \\le 300$，$0 \\le amount \\le 5000$）。\n\n第二行 $n$ 个**互不相同**的正整数面额（$1 \\le c_i \\le 5000$）。",
    output_format="一行一个整数，表示方案数。",
    constraints=["1 ≤ n ≤ 300", "0 ≤ amount ≤ 5000", "面额互不相同", "按组合计数"],
    solver=s_coin2,
    specs=[("样例 1", "3 5\n1 2 5", 10), ("样例 2（无法凑出）", "1 3\n2", 10),
           ("amount = 0", "2 0\n1 2", 15), ("单种硬币可凑", "1 10\n5", 15),
           ("单种不可凑", "1 10\n3", 20), ("两种面额", "2 5\n1 2", 20),
           ("面额较大", "2 100\n50 30", 20)],
    cpp=CPP_HEADER + """int main(){int n,amount;scanf("%d %d",&n,&amount);
vector<int>c(n);for(int i=0;i<n;++i)scanf("%d",&c[i]);
vector<long long>dp(amount+1,0);dp[0]=1;
for(int co:c)for(int j=co;j<=amount;++j)dp[j]+=dp[j-co];
printf("%lld\\n",dp[amount]);return 0;}
""",
    hint="**完全背包计数**：`dp[j]` = 凑出金额 $j$ 的**组合数**。\n\n**关键点：遍历顺序决定了「组合」还是「排列」**\n\n```\nfor (每种硬币 c)          // 外层：面额\n    for (j = c; j <= amount; ++j)   // 内层：金额正序\n        dp[j] += dp[j - c];\n```\n\n把**面额放在外层**，就能保证每种面额被「一次性批量考虑」，从而不会重复计数 `1+2` 与 `2+1`。\n\n> 若把金额放外层、面额放内层，得到的是**排列数**（即 `1+2` 与 `2+1` 算两种），那是另一道题。",
)

# ---------------------------------------------------------------- 7
def s_lps(t):
    s = t.strip("\n").split("\n")[0]
    n = len(s)
    if n == 0:
        return "0\n"
    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = 1
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2 if length > 2 else 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    return f"{dp[0][n - 1]}\n"


add(
    pid="dp-longest-palindromic-subseq", title="最长回文子序列", difficulty="中等",
    tags=["动态规划", "区间DP", "字符串"], source="LeetCode 516", url="https://leetcode.cn/problems/longest-palindromic-subsequence/",
    statement="给定一个字符串，求它的**最长回文子序列**的长度。\n\n**子序列**不要求连续，但不能改变字符的相对顺序。",
    input_format="一行一个字符串 $s$（$0 \\le |s| \\le 1000$），仅含小写英文字母。",
    output_format="一行一个整数，表示最长回文子序列的长度。",
    constraints=["0 ≤ |s| ≤ 1000", "仅小写字母", "子序列不要求连续"],
    solver=s_lps,
    specs=[("样例 1", "bbbab", 10), ("样例 2", "cbbd", 10),
           ("单字符", "a", 15), ("空串", "\n", 15),
           ("全相同", "aaaa", 20), ("已回文", "abcba", 20),
           ("无回文长度 2", "abcd", 20)],
    cpp=CPP_HEADER + """int main(){string s;getline(cin,s);
int n=s.size();
if(n==0){printf("0\\n");return 0;}
vector<vector<int>>dp(n,vector<int>(n,0));
for(int i=0;i<n;++i)dp[i][i]=1;
for(int len=2;len<=n;++len)for(int i=0;i+len-1<n;++i){
int j=i+len-1;
if(s[i]==s[j])dp[i][j]=(len>2?dp[i+1][j-1]:0)+2;
else dp[i][j]=max(dp[i+1][j],dp[i][j-1]);}
printf("%d\\n",dp[0][n-1]);return 0;}
""",
    hint="**区间 DP**：`dp[i][j]` = 子串 $s[i..j]$ 的最长回文子序列长度。\n\n转移：\n\n- 若 `s[i] == s[j]`：`dp[i][j] = dp[i+1][j-1] + 2`；\n- 否则：`dp[i][j] = max(dp[i+1][j], dp[i][j-1])`（舍弃一端）。\n\n按**区间长度**从小到大枚举。\n\n> **易错点**：长度为 2 时 `dp[i+1][j-1]` 是空区间（应视为 0），代码里用 `len > 2` 判断处理。",
)

# ---------------------------------------------------------------- 8
def s_max_square(t):
    ls = t.strip("\n").split("\n")
    r, c = map(int, ls[0].split())
    g = [list(map(int, ls[i + 1].split())) for i in range(r)]
    dp = [[0] * (c + 1) for _ in range(r + 1)]
    best = 0
    for i in range(1, r + 1):
        for j in range(1, c + 1):
            if g[i - 1][j - 1] == 1:
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
                best = max(best, dp[i][j])
    return f"{best * best}\n"


add(
    pid="dp-maximal-square", title="最大正方形", difficulty="中等",
    tags=["动态规划", "矩阵", "二维DP"], source="LeetCode 221", url="https://leetcode.cn/problems/maximal-square/",
    statement="给定一个 $0/1$ 矩阵，求其中**只包含 $1$ 的最大正方形**的**面积**。\n\n若没有 $1$，输出 $0$。",
    input_format="第一行两个整数 $r, c$（$1 \\le r, c \\le 300$）。\n\n接下来 $r$ 行，每行 $c$ 个整数（$0$ 或 $1$）。",
    output_format="一行一个整数，表示最大正方形的面积。",
    constraints=["1 ≤ r, c ≤ 300", "元素为 0 或 1"],
    solver=s_max_square,
    specs=[("样例 1", "4 5\n1 0 1 0 0\n1 0 1 1 1\n1 1 1 1 1\n1 0 0 1 0", 10),
           ("全零", "2 2\n0 0\n0 0", 10), ("全一", "3 3\n1 1 1\n1 1 1\n1 1 1", 15),
           ("单格 1", "1 1\n1", 15), ("单格 0", "1 1\n0", 20),
           ("2x2 全一", "2 2\n1 1\n1 1", 20), ("L 形", "2 2\n1 0\n1 1", 20)],
    cpp=CPP_HEADER + """int main(){int r,c;scanf("%d %d",&r,&c);
vector<vector<int>>g(r,vector<int>(c));
for(int i=0;i<r;++i)for(int j=0;j<c;++j)scanf("%d",&g[i][j]);
vector<vector<int>>dp(r+1,vector<int>(c+1,0));
int best=0;
for(int i=1;i<=r;++i)for(int j=1;j<=c;++j)
if(g[i-1][j-1]==1){
dp[i][j]=min({dp[i-1][j],dp[i][j-1],dp[i-1][j-1]})+1;
best=max(best,dp[i][j]);}
printf("%d\\n",best*best);return 0;}
""",
    hint="**状态**：`dp[i][j]` = 以 $(i,j)$ 为**右下角**的最大正方形**边长**。\n\n转移（当 `g[i][j] == 1` 时）：\n\n```\ndp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1\n```\n\n**直觉**：要以 $(i,j)$ 为右下角构成边长 $k$ 的正方形，需要上、左、左上三个位置都能构成边长 $k-1$ 的正方形——取三者最小值加一。\n\n答案 = 最大边长$^2$。",
)

# ---------------------------------------------------------------- 9
def s_unique_paths(t):
    r, c = map(int, t.strip().split())
    dp = [1] * c
    for _ in range(1, r):
        for j in range(1, c):
            dp[j] += dp[j - 1]
    return f"{dp[c - 1]}\n"


add(
    pid="dp-unique-paths", title="不同路径", difficulty="中等",
    tags=["动态规划", "矩阵", "组合数学"], source="LeetCode 62", url="https://leetcode.cn/problems/unique-paths/",
    statement="一个机器人位于 $r \\times c$ 网格的左上角，每次只能**向右或向下**移动一格。\n\n求到达右下角的**不同路径数**。",
    input_format="一行两个整数 $r, c$（$1 \\le r, c \\le 20$）。",
    output_format="一行一个整数，表示路径数。",
    constraints=["1 ≤ r, c ≤ 20"],
    solver=s_unique_paths,
    specs=[("样例 1", "3 7", 10), ("样例 2", "3 2", 10),
           ("单行", "1 5", 15), ("单列", "5 1", 15),
           ("单格", "1 1", 20), ("方阵 5", "5 5", 20),
           ("最大", "20 20", 20)],
    cpp=CPP_HEADER + """int main(){int r,c;scanf("%d %d",&r,&c);
vector<long long>dp(c,1);
for(int i=1;i<r;++i)for(int j=1;j<c;++j)dp[j]+=dp[j-1];
printf("%lld\\n",dp[c-1]);return 0;}
""",
    hint="**二维 DP（滚动成一维）**：`dp[i][j]` = 到达 $(i,j)$ 的路径数 = `dp[i-1][j] + dp[i][j-1]`（只能从上面或左边来）。\n\n用一维数组滚动：初始全为 1（第一行只有一种走法），之后 `dp[j] += dp[j-1]`。\n\n> **组合解法**：总共要走 $r-1$ 步向下、$c-1$ 步向右，答案是 $\\binom{r+c-2}{r-1}$。\n\n> **注意**：$20 \\times 20$ 时结果约 $3.5 \\times 10^{10}$，要用 `long long`。",
)

# ---------------------------------------------------------------- 10
def s_min_path(t):
    ls = t.strip("\n").split("\n")
    r, c = map(int, ls[0].split())
    g = [list(map(int, ls[i + 1].split())) for i in range(r)]
    dp = [[0] * c for _ in range(r)]
    dp[0][0] = g[0][0]
    for j in range(1, c):
        dp[0][j] = dp[0][j - 1] + g[0][j]
    for i in range(1, r):
        dp[i][0] = dp[i - 1][0] + g[i][0]
        for j in range(1, c):
            dp[i][j] = min(dp[i - 1][j], dp[i][j - 1]) + g[i][j]
    return f"{dp[r - 1][c - 1]}\n"


add(
    pid="dp-min-path-sum", title="最小路径和", difficulty="中等",
    tags=["动态规划", "矩阵", "二维DP"], source="LeetCode 64", url="https://leetcode.cn/problems/minimum-path-sum/",
    statement="给定一个非负整数矩阵，从**左上角**走到**右下角**，每次只能向右或向下移动一格。\n\n求路径上所有数字之和的**最小值**。",
    input_format="第一行两个整数 $r, c$（$1 \\le r, c \\le 200$）。\n\n接下来 $r$ 行，每行 $c$ 个非负整数（$0 \\le v \\le 200$）。",
    output_format="一行一个整数，表示最小路径和。",
    constraints=["1 ≤ r, c ≤ 200", "0 ≤ v ≤ 200"],
    solver=s_min_path,
    specs=[("样例 1", "3 3\n1 3 1\n1 5 1\n4 2 1", 10),
           ("单格", "1 1\n5", 10), ("单行", "1 3\n1 2 3", 15),
           ("单列", "3 1\n1\n2\n3", 15), ("全零", "2 2\n0 0\n0 0", 20),
           ("方阵 3", "3 3\n1 1 1\n1 1 1\n1 1 1", 20),
           ("含大值", "2 2\n9 9\n9 1", 20)],
    cpp=CPP_HEADER + """int main(){int r,c;scanf("%d %d",&r,&c);
vector<vector<long long>>g(r,vector<long long>(c));
for(int i=0;i<r;++i)for(int j=0;j<c;++j)scanf("%lld",&g[i][j]);
vector<vector<long long>>dp(r,vector<long long>(c,0));
dp[0][0]=g[0][0];
for(int j=1;j<c;++j)dp[0][j]=dp[0][j-1]+g[0][j];
for(int i=1;i<r;++i){dp[i][0]=dp[i-1][0]+g[i][0];
for(int j=1;j<c;++j)dp[i][j]=min(dp[i-1][j],dp[i][j-1])+g[i][j];}
printf("%lld\\n",dp[r-1][c-1]);return 0;}
""",
    hint="**与「不同路径」同框架**，只是把「计数」换成「取最小值」：\n\n`dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + g[i][j]`。\n\n> **易错点**：**第一行和第一列要单独初始化**（它们只有一条路径），不能直接用上面的转移式。",
)

# ---------------------------------------------------------------- 11
def s_triangle(t):
    ls = t.strip("\n").split("\n")
    n = int(ls[0])
    tri = [list(map(int, ls[i + 1].split())) for i in range(n)]
    dp = tri[-1][:]
    for i in range(n - 2, -1, -1):
        for j in range(i + 1):
            dp[j] = min(dp[j], dp[j + 1]) + tri[i][j]
    return f"{dp[0]}\n"


add(
    pid="dp-triangle", title="三角形最小路径和", difficulty="中等",
    tags=["动态规划", "二维DP", "空间优化"], source="LeetCode 120", url="https://leetcode.cn/problems/triangle/",
    statement="给定一个三角形（第 $i$ 行有 $i$ 个数），从**顶部**出发走到**底部**。\n\n每一步只能移动到下一行的**相邻**位置（下标相同或下标 +1）。\n\n求路径上数字之和的**最小值**。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 200$）。\n\n接下来 $n$ 行，第 $i$ 行有 $i$ 个整数（$|v| \\le 10^4$）。",
    output_format="一行一个整数，表示最小路径和。",
    constraints=["1 ≤ n ≤ 200", "|v| ≤ 10^4"],
    solver=s_triangle,
    specs=[("样例 1", "4\n2\n3 4\n6 5 7\n4 1 8 3", 10),
           ("单行", "1\n5", 10), ("两行", "2\n1\n2 3", 15),
           ("全相同", "3\n1\n1 1\n1 1 1", 15), ("含负数", "3\n-1\n2 3\n1 -5 4", 20),
           ("递增", "3\n1\n2 3\n4 5 6", 20), ("四行", "4\n-10\n1 2\n3 4 5\n6 7 8 9", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);
vector<vector<long long>>t(n);
for(int i=0;i<n;++i){t[i].resize(i+1);
for(int j=0;j<=i;++j)scanf("%lld",&t[i][j]);}
vector<long long>dp=t[n-1];
for(int i=n-2;i>=0;--i)for(int j=0;j<=i;++j)
dp[j]=min(dp[j],dp[j+1])+t[i][j];
printf("%lld\\n",dp[0]);return 0;}
""",
    hint="**自底向上 + 一维滚动**：`dp[j]` 表示从 $(i,j)$ 出发到底部的最小路径和。\n\n从**最后一行**开始（`dp` 初值就是最后一行），逐层往上：\n\n```\ndp[j] = min(dp[j], dp[j+1]) + triangle[i][j]\n```\n\n**为什么自底向上**：顶部只有一个起点，自顶向下要处理多个终点；自底向上则每层只需更新到 `dp[0]`，天然得到答案。\n\n空间 $O(n)$。",
)

# ---------------------------------------------------------------- 12
def s_word_break(t):
    ls = t.strip("\n").split("\n")
    s = ls[0].strip()
    n = int(ls[1])
    words = [ls[i + 2].strip() for i in range(n)]
    ws = set(words)
    L = len(s)
    dp = [False] * (L + 1)
    dp[0] = True
    for i in range(1, L + 1):
        for j in range(i):
            if dp[j] and s[j:i] in ws:
                dp[i] = True
                break
    return ("YES\n" if dp[L] else "NO\n")


add(
    pid="dp-word-break", title="单词拆分", difficulty="中等",
    tags=["动态规划", "字符串", "哈希表"], source="LeetCode 139", url="https://leetcode.cn/problems/word-break/",
    statement="给定一个字符串和一个单词字典，判断字符串**能否**被拆分成字典中单词的**拼接**。\n\n字典中的单词**可以重复使用**。\n\n能则输出 `YES`，否则 `NO`。",
    input_format="第一行一个字符串 $s$（$1 \\le |s| \\le 300$），仅含小写字母。\n\n第二行一个整数 $n$（$1 \\le n \\le 1000$）。\n\n接下来 $n$ 行，每行一个单词（仅小写字母）。",
    output_format="一行，输出 `YES` 或 `NO`。",
    constraints=["1 ≤ |s| ≤ 300", "1 ≤ n ≤ 1000", "字典单词可重复使用"],
    solver=s_word_break,
    specs=[("样例 1（可以）", "leetcode\n2\nleet\ncode", 10),
           ("样例 2（可以，可重复使用）", "applepenapple\n2\napple\npen", 10),
           ("单字符命中", "a\n1\na", 15), ("单字符未命中", "a\n1\nb", 15),
           ("可重复使用", "aaaa\n2\na\naa", 20), ("无法拆分", "abcd\n2\nab\ncde", 20),
           ("整串即单词", "abc\n1\nabc", 20)],
    cpp=CPP_HEADER + """int main(){string s;cin>>s;int n;cin>>n;
unordered_set<string>ws;
for(int i=0;i<n;++i){string w;cin>>w;ws.insert(w);}
int L=s.size();vector<bool>dp(L+1,false);dp[0]=true;
for(int i=1;i<=L;++i)for(int j=0;j<i;++j)
if(dp[j]&&ws.count(s.substr(j,i-j))){dp[i]=true;break;}
printf("%s\\n",dp[L]?"YES":"NO");return 0;}
""",
    hint="**状态**：`dp[i]` = 字符串的**前 $i$ 个字符**能否被拆分。\n\n转移：对每个 $i$，枚举切分点 $j$，若 `dp[j]` 为真**且** `s[j..i-1]` 在字典中，则 `dp[i]` 为真。\n\n用**哈希集合**存字典，查询 $O(1)$。时间 $O(n^2)$。\n\n> **优化**：枚举 $j$ 时可以只考虑「长度不超过字典最长单词」的范围，或改用**字典树（Trie）** 加速匹配。",
)

# ---------------------------------------------------------------- 13
def s_partition(t):
    n, a = arr(t)
    total = sum(a)
    if total % 2:
        return "NO\n"
    half = total // 2
    dp = [False] * (half + 1)
    dp[0] = True
    for x in a:
        for j in range(half, x - 1, -1):
            if dp[j - x]:
                dp[j] = True
    return ("YES\n" if dp[half] else "NO\n")


add(
    pid="dp-partition-equal", title="分割等和子集", difficulty="中等",
    tags=["动态规划", "0-1背包", "子集和"], source="LeetCode 416", url="https://leetcode.cn/problems/partition-equal-subset-sum/",
    statement="给定一个正整数数组，判断能否把它分成**两个子集**，使得两个子集的**元素和相等**。\n\n能则输出 `YES`，否则 `NO`。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 200$）。\n\n第二行 $n$ 个正整数（$1 \\le a_i \\le 100$）。",
    output_format="一行，输出 `YES` 或 `NO`。",
    constraints=["1 ≤ n ≤ 200", "1 ≤ a_i ≤ 100", "元素为正整数"],
    solver=s_partition,
    specs=[("样例 1（可以）", "4\n1 5 11 5", 10), ("样例 2（不可以）", "3\n1 2 5", 10),
           ("单元素", "1\n5", 15), ("两元素相等", "2\n3 3", 15),
           ("两元素不等", "2\n3 4", 20), ("全相同偶数个", "4\n2 2 2 2", 20),
           ("和为奇数", "3\n1 2 4", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<int>a(n);
int total=0;for(int i=0;i<n;++i){scanf("%d",&a[i]);total+=a[i];}
if(total%2){printf("NO\\n");return 0;}
int half=total/2;
vector<bool>dp(half+1,false);dp[0]=true;
for(int x:a)for(int j=half;j>=x;--j)if(dp[j-x])dp[j]=true;
printf("%s\\n",dp[half]?"YES":"NO");return 0;}
""",
    hint="**转化为 0-1 背包**：若总和为奇数，直接 `NO`；否则目标变成「能否用数组中的元素凑出 `total/2`」。\n\n`dp[j]` = 能否凑出和 $j$。对每个元素，**容量倒序**遍历（保证每个元素只用一次）：\n\n```\nfor (int j = half; j >= x; --j) if (dp[j-x]) dp[j] = true;\n```\n\n> **易错点**：内层必须**倒序**！正序会让同一个元素被重复使用，退化成完全背包。",
)

# ---------------------------------------------------------------- 14
def s_target_sum(t):
    ls = t.strip("\n").split("\n")
    n, target = map(int, ls[0].split())
    a = list(map(int, ls[1].split()))
    total = sum(a)
    # 设加号部分和为 P，则 P - (total-P) = target → P = (total+target)/2
    if (total + target) % 2 or abs(target) > total:
        return "0\n"
    half = (total + target) // 2
    dp = [0] * (half + 1)
    dp[0] = 1
    for x in a:
        for j in range(half, x - 1, -1):
            dp[j] += dp[j - x]
    return f"{dp[half]}\n"


add(
    pid="dp-target-sum", title="目标和", difficulty="中等",
    tags=["动态规划", "0-1背包", "计数"], source="LeetCode 494", url="https://leetcode.cn/problems/target-sum/",
    statement="给定一个非负整数数组和目标值 $target$，给每个数前面添加 `+` 或 `-`，使表达式结果等于 $target$。\n\n求共有多少种**不同的添加方式**。",
    input_format="第一行两个整数 $n, target$（$1 \\le n \\le 20$，$|target| \\le 1000$）。\n\n第二行 $n$ 个非负整数（$0 \\le a_i \\le 1000$）。",
    output_format="一行一个整数，表示方案数。",
    constraints=["1 ≤ n ≤ 20", "|target| ≤ 1000", "0 ≤ a_i ≤ 1000"],
    solver=s_target_sum,
    specs=[("样例 1", "5 3\n1 1 1 1 1", 10), ("样例 2", "1 1\n1", 10),
           ("无法达成", "1 2\n1", 15), ("全零 target 0", "3 0\n0 0 0", 15),
           ("单元素 0", "1 0\n0", 20), ("含零混合", "3 1\n0 1 1", 20),
           ("target 为负", "2 -1\n1 1", 20)],
    cpp=CPP_HEADER + """int main(){int n,target;scanf("%d %d",&n,&target);
vector<int>a(n);int total=0;
for(int i=0;i<n;++i){scanf("%d",&a[i]);total+=a[i];}
if((total+target)%2||abs(target)>total){printf("0\\n");return 0;}
int half=(total+target)/2;
vector<long long>dp(half+1,0);dp[0]=1;
for(int x:a)for(int j=half;j>=x;--j)dp[j]+=dp[j-x];
printf("%lld\\n",dp[half]);return 0;}
""",
    hint="**转化为子集和计数**：设取 `+` 的元素之和为 $P$，则取 `-` 的元素之和为 $total - P$。\n\n要求 $P - (total - P) = target$，解得 $P = \\dfrac{total + target}{2}$。\n\n于是问题变成「从数组中选出若干元素，使它们的和恰好为 $P$ 的方案数」——标准的 **0-1 背包计数**。\n\n> **易错点**：\n> 1. `(total + target)` 必须为**偶数**，否则无解；\n> 2. `|target| > total` 时无解；\n> 3. 内层容量仍要**倒序**。",
)

# ---------------------------------------------------------------- 15
def s_rod(t):
    ls = t.strip("\n").split("\n")
    n = int(ls[0])
    p = list(map(int, ls[1].split()))
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        best = p[i - 1]
        for j in range(1, i):
            best = max(best, dp[j] + dp[i - j])
        dp[i] = best
    return f"{dp[n]}\n"


add(
    pid="dp-rod-cutting", title="钢条切割", difficulty="中等",
    tags=["动态规划", "完全背包"], source="经典 DP 问题", url="https://leetcode.cn/problems/coin-change/",
    statement="一根长度为 $n$ 的钢条，价格表给出长度 $1 \\sim n$ 的钢条各自的价格 $p_i$。\n\n把钢条切割成若干段（可以不切）出售，求**最大收益**。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 1000$）。\n\n第二行 $n$ 个正整数 $p_i$（$1 \\le p_i \\le 10^4$），表示长度 $i$ 的钢条价格。",
    output_format="一行一个整数，表示最大收益。",
    constraints=["1 ≤ n ≤ 1000", "1 ≤ p_i ≤ 10^4"],
    solver=s_rod,
    specs=[("样例 1", "4\n1 5 8 9", 10), ("样例 2", "5\n2 5 7 8 10", 10),
           ("单长度", "1\n5", 15), ("整根最划算", "3\n1 2 100", 15),
           ("递减价格", "4\n10 5 3 1", 20), ("全相同价格", "4\n5 5 5 5", 20),
           ("长度 7", "7\n1 5 8 9 10 17 17", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>p(n+1);
for(int i=1;i<=n;++i)scanf("%lld",&p[i]);
vector<long long>dp(n+1,0);
for(int i=1;i<=n;++i){
long long best=p[i];
for(int j=1;j<i;++j)best=max(best,dp[j]+dp[i-j]);
dp[i]=best;}
printf("%lld\\n",dp[n]);return 0;}
""",
    hint="**状态**：`dp[i]` = 长度为 $i$ 的钢条能获得的最大收益。\n\n**转移**：`dp[i] = max(p[i], max over j<i of dp[j] + dp[i-j])`。\n\n含义是「要么整根不切（得 $p_i$），要么切成两段 $j$ 和 $i-j$ 分别求最优」。\n\n> **更简洁的写法**：`dp[i] = max(p[j] + dp[i-j])`（$1 \\le j \\le i$）——枚举**第一刀**的长度，剩余部分递归求解。两种写法等价。",
)

# ---------------------------------------------------------------- 16
def s_perfect_squares(t):
    n = int(t.strip())
    dp = [0] + [10 ** 9] * n
    for i in range(1, n + 1):
        j = 1
        while j * j <= i:
            dp[i] = min(dp[i], dp[i - j * j] + 1)
            j += 1
    return f"{dp[n]}\n"


add(
    pid="dp-perfect-squares", title="完全平方数", difficulty="中等",
    tags=["动态规划", "完全背包", "数学"], source="LeetCode 279", url="https://leetcode.cn/problems/perfect-squares/",
    statement="给定正整数 $n$，求**最少**用几个**完全平方数**（如 $1, 4, 9, 16, \\dots$）之和表示出 $n$。\n\n每个平方数**可以重复使用**。",
    input_format="一行一个整数 $n$（$1 \\le n \\le 10^4$）。",
    output_format="一行一个整数，表示最少个数。",
    constraints=["1 ≤ n ≤ 10^4"],
    solver=s_perfect_squares,
    specs=[("样例 1", "12", 10), ("样例 2", "13", 10), ("n = 1", "1", 15),
           ("完全平方数", "16", 15), ("质数", "7", 20), ("较大", "10000", 20),
           ("n = 2", "2", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);
const int INF=1e9;
vector<int>dp(n+1,INF);dp[0]=0;
for(int i=1;i<=n;++i)
for(int j=1;j*j<=i;++j)dp[i]=min(dp[i],dp[i-j*j]+1);
printf("%d\\n",dp[n]);return 0;}
""",
    hint="**完全背包求最小值**：`dp[i]` = 表示 $i$ 所需的最少平方数个数。\n\n转移：对所有满足 $j^2 \\le i$ 的 $j$，`dp[i] = min(dp[i], dp[i - j*j] + 1)`。\n\n时间 $O(n\\sqrt{n})$。\n\n> **数学结论（四平方和定理）**：任何正整数都能表示为**至多 4 个**平方数之和，所以答案只会是 1、2、3、4。可以用这个性质做 $O(\\sqrt{n})$ 的判定，但 DP 更通用。",
)


def main() -> None:
    for p in P:
        finalize(p, OUT / f"{p['id']}.json")
        total = sum(t["score"] for t in p["tests"])
        print(f"生成 {p['id']:34s} {len(p['tests'])} 测试点, 总分 {total:3d}")


if __name__ == "__main__":
    main()
