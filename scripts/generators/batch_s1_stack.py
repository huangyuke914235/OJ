"""栈与队列 · 批量 S1（16 道）。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from genkit import CPP_HEADER, finalize, numbers, problem  # noqa: E402

OUT = ROOT / "oj" / "data" / "problems" / "02-stack-queue"
P: list = []


def add(**kw):
    P.append(problem(**kw))


def L(t):
    return t.strip("\n").split("\n")


def arr(t):
    v = numbers(t)
    return v[0], v[1:1 + v[0]]


# ---------------------------------------------------------------- 1
def s_baseball(t):
    ls = L(t)
    n = int(ls[0])
    st = []
    for i in range(1, n + 1):
        op = ls[i].strip()
        if op == "+":
            st.append(st[-1] + st[-2])
        elif op == "D":
            st.append(st[-1] * 2)
        elif op == "C":
            st.pop()
        else:
            st.append(int(op))
    return f"{sum(st)}\n"


add(
    pid="stack-baseball-game", title="棒球比赛", difficulty="简单",
    tags=["栈", "模拟"], source="LeetCode 682", url="https://leetcode.cn/problems/baseball-game/",
    statement="记录一场棒球比赛的得分。每行是一条操作：\n\n- 整数 $x$：本轮得 $x$ 分；\n- `+`：本轮得分等于**前两轮有效得分之和**；\n- `D`：本轮得分等于**上一轮有效得分的两倍**；\n- `C`：**作废**上一轮得分（把它删掉）。\n\n求所有有效得分的总和。\n\n**保证** `+`、`D`、`C` 出现时前面有足够的历史记录。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 1000$）。\n\n接下来 $n$ 行，每行一条操作（整数 $|x| \\le 3\\times10^4$，或 `+` / `D` / `C`）。",
    output_format="一行一个整数，表示所有有效得分的总和。",
    constraints=["1 ≤ n ≤ 1000", "|x| ≤ 3×10^4", "操作保证合法"],
    solver=s_baseball,
    specs=[("样例 1", "5\n5\n2\nC\nD\n+", 10), ("样例 2", "7\n5\n-2\n4\nC\nD\n9\n+", 10),
           ("全为整数", "3\n1\n2\n3", 15), ("含作废", "3\n5\nC\n3", 15),
           ("单操作", "1\n7", 20), ("含负数", "4\n-1\n-2\nD\n+", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>st;char buf[32];
for(int i=0;i<n;++i){scanf("%s",buf);string op=buf;
if(op=="+")st.push_back(st[st.size()-1]+st[st.size()-2]);
else if(op=="D")st.push_back(st.back()*2);
else if(op=="C")st.pop_back();
else st.push_back(stoll(op));}
long long s=0;for(long long x:st)s+=x;
printf("%lld\\n",s);return 0;}
""",
    hint="**栈模拟**：整数入栈；`+` 用栈顶两个相加后入栈；`D` 用栈顶乘 2 入栈；`C` 弹出栈顶。\n\n最后求和。时间 $O(n)$。",
)

# ---------------------------------------------------------------- 2
def s_backspace(t):
    ls = L(t)
    a, b = ls[0], ls[1]
    def build(s):
        st = []
        for c in s:
            if c == "#":
                if st:
                    st.pop()
            else:
                st.append(c)
        return "".join(st)
    return ("YES\n" if build(a) == build(b) else "NO\n")


add(
    pid="stack-backspace-compare", title="比较含退格的字符串", difficulty="简单",
    tags=["栈", "字符串", "双指针"], source="LeetCode 844", url="https://leetcode.cn/problems/backspace-string-compare/",
    statement="`#` 表示**退格**（删除前一个字符）。给定两个字符串，判断它们经过退格处理后是否**相等**。\n\n若某个 `#` 前面没有字符，则它什么也不做。\n\n相等输出 `YES`，否则 `NO`。",
    input_format="第一行一个字符串 $a$。\n\n第二行一个字符串 $b$。\n\n两串长度均不超过 $2\\times10^5$，仅含小写字母与 `#`。",
    output_format="一行，输出 `YES` 或 `NO`。",
    constraints=["|a|, |b| ≤ 2×10^5", "仅含小写字母与 #"],
    solver=s_backspace,
    specs=[("样例 1（相等）", "ab#c\nad#c", 10), ("样例 2（相等）", "ab##\nc#d#", 10),
           ("样例 3（不等）", "a#c\nb", 15), ("全为退格", "###\n#", 15),
           ("无退格", "abc\nabc", 20), ("末尾退格", "abc#\nab", 20),
           ("两串都空", "#\n#", 20)],
    cpp=CPP_HEADER + """string build(const string&s){string st;
for(char c:s){if(c=='#'){if(!st.empty())st.pop_back();}else st.push_back(c);}
return st;}
int main(){string a,b;cin>>a>>b;
printf("%s\\n",build(a)==build(b)?"YES":"NO");return 0;}
""",
    hint="**用栈模拟退格**：遇到普通字符入栈，遇到 `#` 且栈非空就弹出。\n\n把两个串都处理完再比较即可。时间 $O(n)$，空间 $O(n)$。\n\n> **进阶**：可以从**后往前**用双指针 + 退格计数做到 $O(1)$ 空间。",
)

# ---------------------------------------------------------------- 3
def s_remove_k_digits(t):
    ls = L(t)
    num = ls[0].strip()
    k = int(ls[1])
    st = []
    for c in num:
        while k > 0 and st and st[-1] > c:
            st.pop()
            k -= 1
        st.append(c)
    while k > 0 and st:
        st.pop()
        k -= 1
    res = "".join(st).lstrip("0")
    return (res + "\n") if res else "0\n"


add(
    pid="stack-remove-k-digits", title="移掉 K 位数字", difficulty="中等",
    tags=["栈", "单调栈", "贪心"], source="LeetCode 402", url="https://leetcode.cn/problems/remove-k-digits/",
    statement="给定一个以字符串表示的非负整数 $num$ 和整数 $k$，移除其中 $k$ 个数字，使剩下的数字**尽可能小**。\n\n输出这个最小的数。若结果为空或全为前导零，输出 `0`。",
    input_format="第一行一个数字字符串 $num$（长度 $1 \\le |num| \\le 10^5$，无前导零，除非为 \"0\"）。\n\n第二行一个整数 $k$（$0 \\le k \\le |num|$）。",
    output_format="一行，移除 $k$ 位后的最小数字。",
    constraints=["1 ≤ |num| ≤ 10^5", "0 ≤ k ≤ |num|", "num 无多余前导零"],
    solver=s_remove_k_digits,
    specs=[("样例 1", "1432219\n3", 10), ("样例 2", "10200\n1", 10),
           ("样例 3（全删）", "10\n2", 15), ("k = 0", "12345\n0", 15),
           ("单调递增", "12345\n2", 15), ("全相同", "1111\n2", 20),
           ("前导零", "100200\n1", 20)],
    cpp=CPP_HEADER + """int main(){string num;int k;cin>>num>>k;
string st;
for(char c:num){while(k>0&&!st.empty()&&st.back()>c){st.pop_back();--k;}st.push_back(c);}
while(k>0&&!st.empty()){st.pop_back();--k;}
size_t i=0;while(i<st.size()&&st[i]=='0')++i;
string r=st.substr(i);
printf("%s\\n",r.empty()?"0":r.c_str());return 0;}
""",
    hint="**单调栈 + 贪心**：从左到右扫描，只要「栈顶比当前数字大」且「还有删除额度」，就弹出栈顶——因为把更大的高位删掉能让数更小。\n\n扫完后若还有额度，从**末尾**继续删（此时序列已非递减）。\n\n最后**去掉前导零**；若结果为空则输出 `0`。",
)

# ---------------------------------------------------------------- 4
def s_asteroid(t):
    n, a = arr(t)
    st = []
    for x in a:
        alive = True
        while alive and x < 0 and st and st[-1] > 0:
            if st[-1] < -x:
                st.pop()
            elif st[-1] == -x:
                st.pop()
                alive = False
            else:
                alive = False
        if alive:
            st.append(x)
    return (" ".join(map(str, st)) + "\n") if st else "\n"


add(
    pid="stack-asteroid-collision", title="行星碰撞", difficulty="中等",
    tags=["栈", "模拟"], source="LeetCode 735", url="https://leetcode.cn/problems/asteroid-collision/",
    statement="给定一个数组表示一排行星。正数表示**向右**飞，负数表示**向左**飞，绝对值是大小。\n\n相向而行的行星会碰撞：**小的爆炸**；若**大小相同，两个都爆炸**。同向的永不相撞。\n\n求碰撞结束后剩下的行星（按原顺序）。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 10^4$）。\n\n第二行 $n$ 个非零整数 $a_i$（$1 \\le |a_i| \\le 1000$）。",
    output_format="一行，剩余行星的大小（空格分隔）。若全部爆炸则输出空行。",
    constraints=["1 ≤ n ≤ 10^4", "1 ≤ |a_i| ≤ 1000", "元素非零"],
    solver=s_asteroid,
    specs=[("样例 1", "3\n5 10 -5", 10), ("样例 2（全爆）", "2\n8 -8", 10),
           ("样例 3", "3\n10 2 -5", 15), ("同向不撞", "3\n1 2 3", 15),
           ("全向左", "3\n-1 -2 -3", 15), ("嵌套碰撞", "4\n-2 -1 1 2", 20),
           ("一个吃掉多个", "4\n10 -5 -8 -3", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>st;
for(int i=0;i<n;++i){long long x;scanf("%lld",&x);bool alive=true;
while(alive&&x<0&&!st.empty()&&st.back()>0){
if(st.back()<-x)st.pop_back();
else if(st.back()==-x){st.pop_back();alive=false;}
else alive=false;}
if(alive)st.push_back(x);}
for(size_t i=0;i<st.size();++i){if(i)printf(" ");printf("%lld",st[i]);}
printf("\\n");return 0;}
""",
    hint="**栈模拟**：只有「栈顶向右（正）+ 当前向左（负）」才可能碰撞。\n\n用 while 循环处理连锁碰撞：当前行星较小则弹出栈顶继续比；相等则双双消失；栈顶较小则当前行星存活继续比。\n\n> **易错点**：`alive` 标记很重要——当前行星可能在碰撞中消失，此时**不能入栈**。",
)

# ---------------------------------------------------------------- 5
def s_decode_string(t):
    s = t.strip("\n").split("\n")[0]
    st = []
    cur = ""
    num = 0
    for c in s:
        if c.isdigit():
            num = num * 10 + int(c)
        elif c == "[":
            st.append((cur, num))
            cur = ""
            num = 0
        elif c == "]":
            prev, k = st.pop()
            cur = prev + cur * k
        else:
            cur += c
    return f"{cur}\n"


add(
    pid="stack-decode-string", title="字符串解码", difficulty="中等",
    tags=["栈", "字符串", "递归"], source="LeetCode 394", url="https://leetcode.cn/problems/decode-string/",
    statement="给定一个编码字符串，按规则解码。规则为 `k[encoded]`，表示方括号内的内容**重复 $k$ 次**。\n\n可以嵌套，例如 `3[a2[c]]` 解码为 `accaccacc`。\n\n输入保证合法，数字只表示重复次数（不会出现 0）。",
    input_format="一行一个字符串（长度 $1 \\le |s| \\le 10^4$），仅含小写字母、数字和方括号。",
    output_format="一行，解码后的字符串。",
    constraints=["1 ≤ |s| ≤ 10^4", "输入保证合法", "重复次数 ≥ 1"],
    solver=s_decode_string,
    specs=[("样例 1", "3[a]2[bc]", 10), ("样例 2（嵌套）", "3[a2[c]]", 10),
           ("样例 3", "2[abc]3[cd]ef", 15), ("无编码", "abc", 15),
           ("单字符重复", "10[z]", 20), ("多层嵌套", "2[a2[b2[c]]]", 20)],
    cpp=CPP_HEADER + """int main(){string s;cin>>s;vector<pair<string,int>>st;
string cur;int num=0;
for(char c:s){
if(isdigit((unsigned char)c))num=num*10+(c-'0');
else if(c=='['){st.push_back({cur,num});cur="";num=0;}
else if(c==']'){auto pr=st.back();st.pop_back();
string t2;for(int i=0;i<pr.second;++i)t2+=cur;cur=pr.first+t2;}
else cur+=c;}
printf("%s\\n",cur.c_str());return 0;}
""",
    hint="**双栈 / 栈存上下文**：\n\n- 遇到数字：累积 `num`；\n- 遇到 `[`：把**当前的字符串与数字**压栈，然后清空它们，开始处理括号内部；\n- 遇到 `]`：弹出「之前的字符串 + 重复次数」，把当前内容重复 $k$ 次后**拼到之前的字符串后面**；\n- 遇到字母：追加到当前字符串。\n\n时间 $O(输出长度)$。",
)

# ---------------------------------------------------------------- 6
def s_simplify_path(t):
    p = t.strip("\n").split("\n")[0]
    st = []
    for part in p.split("/"):
        if part == "" or part == ".":
            continue
        if part == "..":
            if st:
                st.pop()
        else:
            st.append(part)
    return "/" + "/".join(st) + "\n"


add(
    pid="stack-simplify-path", title="简化路径", difficulty="中等",
    tags=["栈", "字符串"], source="LeetCode 71", url="https://leetcode.cn/problems/simplify-path/",
    statement="给定一个 Unix 风格绝对路径，把它简化为**规范路径**。规则：\n\n- 以 `/` 开头，且目录之间只有一个 `/`；\n- `.` 表示当前目录（忽略）；\n- `..` 表示上级目录（若已在根则忽略）；\n- 结果**不以 `/` 结尾**（除非就是根 `/`）。",
    input_format="一行一个字符串（长度 $1 \\le |s| \\le 3000$），为合法路径。",
    output_format="一行，简化后的规范路径。",
    constraints=["1 ≤ |s| ≤ 3000", "输入为合法路径"],
    solver=s_simplify_path,
    specs=[("样例 1", "/home/", 10), ("样例 2", "/../", 10),
           ("样例 3", "/home//foo/", 15), ("样例 4", "/a/./b/../../c/", 15),
           ("根目录", "/", 20), ("多点", "/...", 20), ("连续上级", "/a/b/c/../../../..", 20)],
    cpp=CPP_HEADER + """int main(){string p;cin>>p;vector<string>st;
string cur;
auto flush=[&](){if(cur==".."){if(!st.empty())st.pop_back();}
else if(cur!=""&&cur!=".")st.push_back(cur);cur="";};
for(char c:p){if(c=='/')flush();else cur+=c;}
flush();
string r;
for(auto&x:st)r+="/"+x;
if(r.empty())r="/";
printf("%s\\n",r.c_str());return 0;}
""",
    hint="**栈按段处理**：把路径按 `/` 切成若干段，逐段判断：\n\n- 空段或 `.`：忽略；\n- `..`：弹出栈顶（栈非空时）；\n- 其他：压栈。\n\n最后用 `/` 连接栈中所有段，并在最前面补一个 `/`。\n\n> **易错点**：`...` 是合法目录名，不是 `..`——只能精确匹配。",
)

# ---------------------------------------------------------------- 7
def s_largest_rect(t):
    n, a = arr(t)
    st = []
    best = 0
    for i in range(n + 1):
        h = a[i] if i < n else 0
        while st and a[st[-1]] > h:
            j = st.pop()
            left = st[-1] if st else -1
            best = max(best, a[j] * (i - left - 1))
        st.append(i)
    return f"{best}\n"


add(
    pid="stack-largest-rectangle", title="柱状图中最大的矩形", difficulty="困难",
    tags=["栈", "单调栈"], source="LeetCode 84", url="https://leetcode.cn/problems/largest-rectangle-in-histogram/",
    statement="给定 $n$ 个非负整数表示柱状图中各柱子的高度（每根柱子宽度为 $1$），求能勾勒出的**最大矩形面积**。\n\n**要求 $O(n)$**。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 10^5$）。\n\n第二行 $n$ 个非负整数 $h_i$（$0 \\le h_i \\le 10^4$）。",
    output_format="一行一个整数，表示最大矩形面积。",
    constraints=["1 ≤ n ≤ 10^5", "0 ≤ h_i ≤ 10^4", "要求 O(n)"],
    solver=s_largest_rect,
    specs=[("样例 1", "6\n2 1 5 6 2 3", 10), ("单柱子", "1\n5", 10),
           ("全相同", "4\n3 3 3 3", 15), ("含 0", "3\n1 0 1", 15),
           ("递增", "4\n1 2 3 4", 20), ("递减", "4\n4 3 2 1", 20),
           ("全零", "3\n0 0 0", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n+1,0);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
vector<int>st;long long best=0;
for(int i=0;i<=n;++i){
while(!st.empty()&&a[st.back()]>a[i]){
int j=st.back();st.pop_back();
int left=st.empty()?-1:st.back();
best=max(best,a[j]*(i-left-1));}
st.push_back(i);}
printf("%lld\\n",best);return 0;}
""",
    hint="**单调栈**：维护一个**递增**的栈（存下标）。当遇到比栈顶矮的柱子时，说明栈顶柱子的**右边界**确定了（当前下标），而**左边界**就是它下面那个元素——于是可以计算以它为高的最大矩形。\n\n> **技巧**：在数组末尾**追加一个高度 0 的哨兵**，这样循环结束时能把栈内所有元素都弹出来处理，省去收尾逻辑。\n\n> **易错点**：宽度是 `i - left - 1`（left 是栈中下一个元素的下标，即左边第一个更矮的位置）。",
)

# ---------------------------------------------------------------- 8
def s_trap(t):
    n, a = arr(t)
    st = []
    res = 0
    for i in range(n):
        while st and a[st[-1]] < a[i]:
            mid = st.pop()
            if not st:
                break
            h = min(a[st[-1]], a[i]) - a[mid]
            w = i - st[-1] - 1
            res += h * w
        st.append(i)
    return f"{res}\n"


add(
    pid="stack-trapping-rain", title="接雨水", difficulty="困难",
    tags=["栈", "单调栈", "双指针"], source="LeetCode 42", url="https://leetcode.cn/problems/trapping-rain-water/",
    statement="给定 $n$ 个非负整数表示宽度为 $1$ 的柱子高度，求下雨后这些柱子之间能接住多少单位的雨水。\n\n**要求 $O(n)$**。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 2\\times10^4$）。\n\n第二行 $n$ 个非负整数 $h_i$（$0 \\le h_i \\le 10^5$）。",
    output_format="一行一个整数，表示能接住的雨水总量。",
    constraints=["1 ≤ n ≤ 2×10^4", "0 ≤ h_i ≤ 10^5", "要求 O(n)"],
    solver=s_trap,
    specs=[("样例 1", "12\n0 1 0 2 1 0 1 3 2 1 2 1", 10), ("单柱", "1\n5", 10),
           ("递增", "4\n1 2 3 4", 15), ("递减", "4\n4 3 2 1", 15),
           ("全平", "4\n3 3 3 3", 20), ("中间凹陷", "5\n5 0 0 0 5", 20),
           ("全零", "3\n0 0 0", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
vector<int>st;long long res=0;
for(int i=0;i<n;++i){
while(!st.empty()&&a[st.back()]<a[i]){
int mid=st.back();st.pop_back();
if(st.empty())break;
long long h=min(a[st.back()],a[i])-a[mid];
long long w=i-st.back()-1;
res+=h*w;}
st.push_back(i);}
printf("%lld\\n",res);return 0;}
""",
    hint="**单调栈（按行计算）**：维护一个**递减**的栈。当遇到比栈顶高的柱子时，栈顶形成一个「凹槽底部」，它左边是 `st[-1]`、右边是当前柱子，于是可以计算这一层的水量。\n\n高度取 `min(左柱, 右柱) - 凹槽底`，宽度是 `i - left - 1`。\n\n> **另一种经典解法**是**双指针**（$O(1)$ 空间）：维护左右两侧已知的最大高度，从较矮的一侧向内推进并累加水量。",
)

# ---------------------------------------------------------------- 9
def s_prev_smaller(t):
    n, a = arr(t)
    res = [-1] * n
    st = []
    for i in range(n):
        while st and a[st[-1]] >= a[i]:
            st.pop()
        res[i] = a[st[-1]] if st else -1
        st.append(i)
    return " ".join(map(str, res)) + "\n"


add(
    pid="stack-prev-smaller", title="上一个更小元素", difficulty="简单",
    tags=["栈", "单调栈"], source="单调栈基础变体", url="https://leetcode.cn/problems/next-greater-element-i/",
    statement="对数组中每个位置 $i$，求**它左侧第一个比它小**的元素值。\n\n若不存在，输出 $-1$。\n\n**要求 $O(n)$**。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 2\\times10^5$）。\n\n第二行 $n$ 个整数 $a_i$（$|a_i| \\le 10^9$）。",
    output_format="一行 $n$ 个整数，为每个位置的答案。",
    constraints=["1 ≤ n ≤ 2×10^5", "|a_i| ≤ 10^9", "要求 O(n)"],
    solver=s_prev_smaller,
    specs=[("样例 1", "5\n3 1 4 2 5", 10), ("递增", "4\n1 2 3 4", 10),
           ("递减", "4\n4 3 2 1", 15), ("全相同", "3\n5 5 5", 15),
           ("单元素", "1\n7", 20), ("含负数", "5\n-1 0 -2 3 -5", 20),
           ("锯齿", "6\n2 5 1 4 3 6", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n),res(n,-1);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
vector<int>st;
for(int i=0;i<n;++i){
while(!st.empty()&&a[st.back()]>=a[i])st.pop_back();
res[i]=st.empty()?-1:a[st.back()];
st.push_back(i);}
for(int i=0;i<n;++i){if(i)printf(" ");printf("%lld",res[i]);}
printf("\\n");return 0;}
""",
    hint="**单调栈（从左往右）**：维护一个**递增**的栈（存下标）。处理 `i` 时，先把栈中所有**大于等于** `a[i]` 的元素弹掉——它们不可能再成为后面任何元素的「左小值」。\n\n弹完后，栈顶就是左侧第一个更小的元素。\n\n> **易错点**：这里用 `>=` 弹出，因为要找**严格更小**的元素。",
)

# ---------------------------------------------------------------- 10
def s_next_smaller(t):
    n, a = arr(t)
    res = [-1] * n
    st = []
    for i in range(n):
        while st and a[st[-1]] > a[i]:
            res[st.pop()] = a[i]
        st.append(i)
    return " ".join(map(str, res)) + "\n"


add(
    pid="stack-next-smaller", title="下一个更小元素", difficulty="简单",
    tags=["栈", "单调栈"], source="单调栈基础变体", url="https://leetcode.cn/problems/next-greater-element-i/",
    statement="对数组中每个位置 $i$，求**它右侧第一个比它小**的元素值。\n\n若不存在，输出 $-1$。\n\n**要求 $O(n)$**。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 2\\times10^5$）。\n\n第二行 $n$ 个整数 $a_i$（$|a_i| \\le 10^9$）。",
    output_format="一行 $n$ 个整数，为每个位置的答案。",
    constraints=["1 ≤ n ≤ 2×10^5", "|a_i| ≤ 10^9", "要求 O(n)"],
    solver=s_next_smaller,
    specs=[("样例 1", "5\n3 1 4 2 5", 10), ("递增", "4\n1 2 3 4", 10),
           ("递减", "4\n4 3 2 1", 15), ("全相同", "3\n5 5 5", 15),
           ("单元素", "1\n7", 20), ("含负数", "5\n-1 0 -2 3 -5", 20),
           ("锯齿", "6\n2 5 1 4 3 6", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n),res(n,-1);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
vector<int>st;
for(int i=0;i<n;++i){
while(!st.empty()&&a[st.back()]>a[i]){res[st.back()]=a[i];st.pop_back();}
st.push_back(i);}
for(int i=0;i<n;++i){if(i)printf(" ");printf("%lld",res[i]);}
printf("\\n");return 0;}
""",
    hint="**单调栈（从左往右）**：维护一个**递增**的栈（存下标）。\n\n新元素 `a[i]` 比栈顶小时，说明栈顶元素的「右小值」就是 `a[i]`——于是不断弹出并记录答案。\n\n这与「下一个更大元素」是同一个模板，只是比较方向相反。",
)

# ---------------------------------------------------------------- 11
def s_queue_stack(t):
    ls = L(t)
    q = int(ls[0])
    dq = []
    out = []
    for i in range(1, q + 1):
        p = ls[i].split()
        op = p[0]
        if op == "push":
            dq.append(int(p[1]))
        elif op == "pop":
            out.append(str(dq.pop()))
        elif op == "top":
            out.append(str(dq[-1]))
        elif op == "empty":
            out.append("YES" if not dq else "NO")
    return ("\n".join(out) + "\n") if out else "\n"


add(
    pid="queue-implement-stack", title="用队列实现栈", difficulty="简单",
    tags=["队列", "设计", "栈"], source="LeetCode 225", url="https://leetcode.cn/problems/implement-stack-using-queues/",
    statement="请用**队列**实现一个栈，支持：\n\n- `push x`：压入 $x$；\n- `pop`：弹出并返回栈顶；\n- `top`：返回栈顶（不弹出）；\n- `empty`：若栈为空输出 `YES`，否则 `NO`。\n\n**保证 `pop` / `top` 只在非空栈上调用**。",
    input_format="第一行一个整数 $q$（$1 \\le q \\le 10^5$）。\n\n接下来 $q$ 行，每行一个操作。$|x| \\le 10^9$。",
    output_format="对每个 `pop` / `top` / `empty` 操作输出一行结果。",
    constraints=["1 ≤ q ≤ 10^5", "|x| ≤ 10^9", "pop/top 仅在非空栈上调用"],
    solver=s_queue_stack,
    specs=[("样例 1", "5\npush 1\npush 2\ntop\npop\nempty", 10),
           ("样例 2", "6\npush 5\npop\npush 7\ntop\npop\nempty", 10),
           ("单元素", "2\npush 9\ntop", 15), ("全部弹完", "4\npush 1\npush 2\npop\npop", 15),
           ("反复操作", "6\npush 1\npop\npush 2\npop\npush 3\nempty", 20),
           ("只看 empty", "2\npush 1\nempty", 20)],
    cpp=CPP_HEADER + """int main(){int q;scanf("%d",&q);deque<long long>d;char op[16];
for(int i=0;i<q;++i){scanf("%s",op);string o=op;
if(o=="push"){long long x;scanf("%lld",&x);d.push_back(x);}
else if(o=="pop"){printf("%lld\\n",d.back());d.pop_back();}
else if(o=="top"){printf("%lld\\n",d.back());}
else if(o=="empty"){printf("%s\\n",d.empty()?"YES":"NO");}}
return 0;}
""",
    hint="**用一个队列实现栈**：压入元素后，把队列中**前面的所有元素依次出队再入队**，这样新元素就转到了队首。\n\n于是 `pop` / `top` 都只需操作队首。压入 $O(n)$，弹出 $O(1)$。\n\n> 也可以用**两个队列**：`push` 直接进 `q1`；`pop` 时把 `q1` 前 $n-1$ 个元素搬到 `q2`，弹出剩下的那个，再交换两队列。",
)

# ---------------------------------------------------------------- 12
def s_circular_queue(t):
    ls = L(t)
    k, q = map(int, ls[0].split())
    buf = []
    out = []
    for i in range(1, q + 1):
        p = ls[i].split()
        op = p[0]
        if op == "enQueue":
            if len(buf) < k:
                buf.append(int(p[1]))
                out.append("YES")
            else:
                out.append("NO")
        elif op == "deQueue":
            if buf:
                buf.pop(0)
                out.append("YES")
            else:
                out.append("NO")
        elif op == "Front":
            out.append(str(buf[0]) if buf else "-1")
        elif op == "Rear":
            out.append(str(buf[-1]) if buf else "-1")
        elif op == "isEmpty":
            out.append("YES" if not buf else "NO")
        elif op == "isFull":
            out.append("YES" if len(buf) == k else "NO")
    return ("\n".join(out) + "\n") if out else "\n"


add(
    pid="queue-circular-design", title="设计循环队列", difficulty="中等",
    tags=["队列", "设计", "数组"], source="LeetCode 622", url="https://leetcode.cn/problems/design-circular-queue/",
    statement="设计一个**循环队列**，容量固定为 $k$，支持：\n\n- `enQueue x`：入队，成功输出 `YES`，队满输出 `NO`；\n- `deQueue`：出队，成功输出 `YES`，队空输出 `NO`；\n- `Front`：返回队首（空返回 `-1`）；\n- `Rear`：返回队尾（空返回 `-1`）；\n- `isEmpty` / `isFull`：输出 `YES` / `NO`。",
    input_format="第一行两个整数 $k, q$（$1 \\le k \\le 1000$，$1 \\le q \\le 3000$）。\n\n接下来 $q$ 行，每行一个操作。",
    output_format="对每个有返回值的操作输出一行。",
    constraints=["1 ≤ k ≤ 1000", "1 ≤ q ≤ 3000"],
    solver=s_circular_queue,
    specs=[("样例 1", "3 12\nenQueue 1\nenQueue 2\nenQueue 3\nenQueue 4\nRear\nisFull\ndeQueue\nenQueue 4\nRear\nFront\nisEmpty\nisFull", 10),
           ("样例 2（空队列）", "2 4\nFront\nRear\nisEmpty\ndeQueue", 10),
           ("容量 1", "1 5\nenQueue 5\nenQueue 6\nFront\nRear\nisFull", 15),
           ("反复进出", "2 8\nenQueue 1\nenQueue 2\ndeQueue\nenQueue 3\ndeQueue\ndeQueue\ndeQueue\nisEmpty", 20),
           ("只查询", "2 3\nisEmpty\nisFull\nFront", 20)],
    cpp=CPP_HEADER + """int main(){int k,q;scanf("%d %d",&k,&q);
deque<long long>d;char op[32];
for(int i=0;i<q;++i){scanf("%s",op);string o=op;
if(o=="enQueue"){long long x;scanf("%lld",&x);
if((int)d.size()<k){d.push_back(x);printf("YES\\n");}else printf("NO\\n");}
else if(o=="deQueue"){if(!d.empty()){d.pop_front();printf("YES\\n");}else printf("NO\\n");}
else if(o=="Front"){printf("%lld\\n",d.empty()?-1LL:d.front());}
else if(o=="Rear"){printf("%lld\\n",d.empty()?-1LL:d.back());}
else if(o=="isEmpty"){printf("%s\\n",d.empty()?"YES":"NO");}
else if(o=="isFull"){printf("%s\\n",(int)d.size()==k?"YES":"NO");}}
return 0;}
""",
    hint="**用固定数组 + 双下标实现**：维护 `head`（队首位置）、`tail`（下一个可写位置）和 `size`。\n\n入队：`buf[tail] = x; tail = (tail + 1) % k; size++`；出队：`head = (head + 1) % k; size--`。\n\n> **易错点**：必须单独维护 `size`（或留一个空位），否则「队空」与「队满」时 `head == tail`，无法区分。",
)

# ---------------------------------------------------------------- 13
def s_win_min(t):
    v = numbers(t)
    n, k = v[0], v[1]
    a = v[2:2 + n]
    from collections import deque
    dq = deque()
    res = []
    for i in range(n):
        while dq and a[dq[-1]] >= a[i]:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            res.append(a[dq[0]])
    return " ".join(map(str, res)) + "\n"


add(
    pid="queue-window-min", title="滑动窗口最小值", difficulty="中等",
    tags=["队列", "单调队列", "滑动窗口"], source="单调队列经典", url="https://leetcode.cn/problems/sliding-window-maximum/",
    statement="给定数组和窗口大小 $k$，窗口从最左端滑到最右端（每次右移一格），求**每个窗口内的最小值**。\n\n**要求 $O(n)$**。",
    input_format="第一行两个整数 $n, k$（$1 \\le k \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数 $a_i$（$|a_i| \\le 10^9$）。",
    output_format="一行 $n-k+1$ 个整数，依次为各窗口的最小值。",
    constraints=["1 ≤ k ≤ n ≤ 10^5", "|a_i| ≤ 10^9", "要求 O(n)"],
    solver=s_win_min,
    specs=[("样例 1", "8 3\n1 3 -1 -3 5 3 6 7", 10), ("k = 1", "3 1\n2 1 3", 10),
           ("k = n", "4 4\n5 2 9 1", 15), ("递增", "5 3\n1 2 3 4 5", 15),
           ("递减", "5 3\n5 4 3 2 1", 20), ("全相同", "4 2\n3 3 3 3", 20),
           ("含负数", "6 2\n-1 -3 2 -4 5 -2", 20)],
    cpp=CPP_HEADER + """int main(){int n,k;scanf("%d %d",&n,&k);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
deque<int>dq;bool first=true;
for(int i=0;i<n;++i){
while(!dq.empty()&&a[dq.back()]>=a[i])dq.pop_back();
dq.push_back(i);
if(dq.front()<=i-k)dq.pop_front();
if(i>=k-1){if(!first)printf(" ");printf("%lld",a[dq.front()]);first=false;}}
printf("\\n");return 0;}
""",
    hint="**单调队列**：用双端队列存**下标**，保持队列内对应的值**单调递增**（求最小值）。\n\n1. 队尾弹出所有比新元素**大或等**的（它们不可能再成为最小值）；\n2. 新元素入队；\n3. 队首若已滑出窗口（`<= i - k`）则弹出；\n4. 窗口成形后，队首就是最小值。\n\n> **易错点**：队列里必须存**下标**，否则无法判断是否滑出窗口。",
)

# ---------------------------------------------------------------- 14
def s_longest_valid_paren(t):
    s = t.strip("\n").split("\n")[0]
    st = [-1]
    best = 0
    for i, c in enumerate(s):
        if c == "(":
            st.append(i)
        else:
            st.pop()
            if not st:
                st.append(i)
            else:
                best = max(best, i - st[-1])
    return f"{best}\n"


add(
    pid="stack-longest-valid-paren", title="最长有效括号", difficulty="困难",
    tags=["栈", "字符串", "动态规划"], source="LeetCode 32", url="https://leetcode.cn/problems/longest-valid-parentheses/",
    statement="给定一个只含 `(` 和 `)` 的字符串，求**最长的有效括号子串**的长度。\n\n有效括号子串指连续的、括号正确配对的子串。",
    input_format="一行一个字符串 $s$（$0 \\le |s| \\le 3\\times10^4$），仅含 `(` 和 `)`。",
    output_format="一行一个整数，表示最长有效括号子串的长度。",
    constraints=["0 ≤ |s| ≤ 3×10^4", "仅含圆括号"],
    solver=s_longest_valid_paren,
    specs=[("样例 1", "(()", 10), ("样例 2", ")()())", 10),
           ("空串", "\n", 15), ("全合法", "()()", 15),
           ("全左括号", "((((", 20), ("全右括号", "))))", 20),
           ("嵌套", "((()))", 20)],
    cpp=CPP_HEADER + """int main(){string s;getline(cin,s);
vector<int>st;st.push_back(-1);int best=0;
for(int i=0;i<(int)s.size();++i){
if(s[i]=='(')st.push_back(i);
else{st.pop_back();
if(st.empty())st.push_back(i);
else best=max(best,i-st.back());}}
printf("%d\\n",best);return 0;}
""",
    hint="**栈存下标**：栈底放一个 $-1$ 作为「最后一个未匹配位置的哨兵」。\n\n- 遇到 `(`：压入下标；\n- 遇到 `)`：弹出栈顶。若栈变空，说明当前 `)` 无法匹配，把它的下标压入作为新哨兵；否则当前有效长度为 `i - st.top()`。\n\n时间 $O(n)$。",
)

# ---------------------------------------------------------------- 15
def s_score_paren(t):
    s = t.strip("\n").split("\n")[0]
    st = [0]
    for c in s:
        if c == "(":
            st.append(0)
        else:
            v = st.pop()
            st[-1] += max(2 * v, 1)
    return f"{st[0]}\n"


add(
    pid="stack-score-of-parentheses", title="括号的分数", difficulty="中等",
    tags=["栈", "字符串"], source="LeetCode 856", url="https://leetcode.cn/problems/score-of-parentheses/",
    statement="给定一个**平衡**的括号字符串，按以下规则计算分数：\n\n- `()` 得 $1$ 分；\n- 两个相邻的平衡串 `AB` 得 $A + B$ 分；\n- 嵌套的平衡串 `(A)` 得 $2 \\times A$ 分。\n\n输出总分。",
    input_format="一行一个平衡的括号字符串（$2 \\le |s| \\le 5\\times10^4$）。",
    output_format="一行一个整数，表示分数。",
    constraints=["2 ≤ |s| ≤ 5×10^4", "保证括号平衡"],
    solver=s_score_paren,
    specs=[("样例 1", "()", 10), ("样例 2", "(())", 10),
           ("样例 3", "()()", 15), ("样例 4", "(()(()))", 15),
           ("深层嵌套", "(((())))", 20), ("多个并列", "()()()()", 20),
           ("混合", "(())()(()())", 20)],
    cpp=CPP_HEADER + """int main(){string s;cin>>s;vector<long long>st;st.push_back(0);
for(char c:s){
if(c=='(')st.push_back(0);
else{long long v=st.back();st.pop_back();
st.back()+=max(2*v,1LL);}}
printf("%lld\\n",st.back());return 0;}
""",
    hint="**栈 + 分数累加**：栈中每个元素代表「当前这一层已经累计的分数」。\n\n- 遇到 `(`：压入 $0$，进入新的一层；\n- 遇到 `)`：弹出内层分数 $v$，**若 $v = 0$ 说明是空括号 `()`，得 1 分；否则得 $2v$ 分**，加到外层上。\n\n`max(2*v, 1)` 这个写法正好统一了两种情形。时间 $O(n)$。",
)

# ---------------------------------------------------------------- 16
def s_stack_permutation(t):
    ls = L(t)
    n = int(ls[0])
    a = list(map(int, ls[1].split()))
    st = []
    nxt = 1
    for x in a:
        while nxt <= x:
            st.append(nxt)
            nxt += 1
        if st and st[-1] == x:
            st.pop()
        else:
            return "NO\n"
    return "YES\n"


add(
    pid="stack-permutation-check", title="栈序列合法性判断", difficulty="中等",
    tags=["栈", "模拟"], source="经典栈判断题", url="https://leetcode.cn/problems/validate-stack-sequences/",
    statement="把 $1, 2, \\dots, n$ 依次压入一个栈（压入顺序固定），在任意时刻可以弹出栈顶。\n\n给定一个弹出序列，判断它**是否可能是合法的出栈序列**。是则输出 `YES`，否则 `NO`。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数，为 $1 \\sim n$ 的一个排列（出栈序列）。",
    output_format="一行，输出 `YES` 或 `NO`。",
    constraints=["1 ≤ n ≤ 10^5", "给定序列是 1..n 的排列"],
    solver=s_stack_permutation,
    specs=[("样例 1（合法）", "5\n4 5 3 2 1", 10), ("样例 2（非法）", "5\n4 3 5 1 2", 10),
           ("升序", "4\n1 2 3 4", 15), ("降序", "4\n4 3 2 1", 15),
           ("单元素", "1\n1", 20), ("交替", "4\n2 1 4 3", 20),
           ("另一个非法", "3\n3 1 2", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<int>a(n);
for(int i=0;i<n;++i)scanf("%d",&a[i]);
vector<int>st;int nxt=1;bool ok=true;
for(int x:a){
while(nxt<=x)st.push_back(nxt++);
if(!st.empty()&&st.back()==x)st.pop_back();
else{ok=false;break;}}
printf("%s\\n",ok?"YES":"NO");return 0;}
""",
    hint="**贪心模拟**：用一个变量 `nxt` 表示「下一个待压入的数」（从 $1$ 开始）。\n\n对出栈序列中的每个目标值 $x$：\n1. 不断把 `nxt` 压栈并递增，直到 `nxt > x`；\n2. 此时若栈顶恰好是 $x$，弹出（合法）；否则说明无法产生该出栈序列，判定 `NO`。\n\n时间 $O(n)$。",
)


def main() -> None:
    for p in P:
        finalize(p, OUT / f"{p['id']}.json")
        total = sum(t["score"] for t in p["tests"])
        print(f"生成 {p['id']:34s} {len(p['tests'])} 测试点, 总分 {total:3d}")


if __name__ == "__main__":
    main()
