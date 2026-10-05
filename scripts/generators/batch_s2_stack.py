"""栈与队列 · 批量 S2（14 道）。"""
from __future__ import annotations

import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from genkit import CPP_HEADER, finalize, problem  # noqa: E402

OUT = ROOT / "oj" / "data" / "problems" / "02-stack-queue"
P: list = []


def add(**kw):
    P.append(problem(**kw))


def L(t):
    return t.strip("\n").split("\n")


# ---------------------------------------------------------------- 1
def s_stack_ops(t):
    ls = L(t)
    q = int(ls[0])
    st = []
    out = []
    for i in range(1, q + 1):
        p = ls[i].split()
        if p[0] == "push":
            st.append(int(p[1]))
        elif p[0] == "pop":
            out.append(str(st.pop()))
        elif p[0] == "top":
            out.append(str(st[-1]))
        elif p[0] == "size":
            out.append(str(len(st)))
        elif p[0] == "empty":
            out.append("YES" if not st else "NO")
    return ("\n".join(out) + "\n") if out else "\n"


add(
    pid="stack-basic-ops", title="栈的基本操作", difficulty="入门",
    tags=["栈", "模拟"], source="栈基础", url="https://leetcode.cn/problems/valid-parentheses/",
    statement="模拟一个栈，支持以下操作：\n\n- `push x`：把 $x$ 压栈；\n- `pop`：弹出栈顶并输出；\n- `top`：输出栈顶（不弹出）；\n- `size`：输出元素个数；\n- `empty`：空栈输出 `YES`，否则 `NO`。\n\n**保证** `pop` / `top` 只在非空栈上调用。",
    input_format="第一行一个整数 $q$（$1 \\le q \\le 10^5$）。\n\n接下来 $q$ 行，每行一个操作（$|x| \\le 10^9$）。",
    output_format="对每个有输出的操作输出一行。",
    constraints=["1 ≤ q ≤ 10^5", "|x| ≤ 10^9", "pop/top 仅在非空栈上调用"],
    solver=s_stack_ops,
    specs=[("样例 1", "5\npush 1\npush 2\ntop\npop\nsize", 10),
           ("空栈检查", "2\nempty\npush 5", 10),
           ("连续弹出", "4\npush 1\npush 2\npop\npop", 15),
           ("只看 size", "3\npush 1\npush 2\nsize", 15),
           ("含负数", "4\npush -1\npush -2\ntop\npop", 20),
           ("反复操作", "6\npush 9\npop\npush 8\ntop\nsize\nempty", 20)],
    cpp=CPP_HEADER + """int main(){int q;scanf("%d",&q);vector<long long>st;char op[16];
for(int i=0;i<q;++i){scanf("%s",op);string o=op;
if(o=="push"){long long x;scanf("%lld",&x);st.push_back(x);}
else if(o=="pop"){printf("%lld\\n",st.back());st.pop_back();}
else if(o=="top"){printf("%lld\\n",st.back());}
else if(o=="size"){printf("%d\\n",(int)st.size());}
else if(o=="empty"){printf("%s\\n",st.empty()?"YES":"NO");}}
return 0;}
""",
    hint="**栈的 LIFO 特性**：`push` 压入、`pop` 弹出最后压入的。\n\n> **易错点**：`pop` / `top` 前必须判空（本题保证不会，但工程代码要写）。",
)

# ---------------------------------------------------------------- 2
def s_queue_ops(t):
    ls = L(t)
    q = int(ls[0])
    dq = deque()
    out = []
    for i in range(1, q + 1):
        p = ls[i].split()
        if p[0] == "push":
            dq.append(int(p[1]))
        elif p[0] == "pop":
            out.append(str(dq.popleft()))
        elif p[0] == "front":
            out.append(str(dq[0]))
        elif p[0] == "back":
            out.append(str(dq[-1]))
        elif p[0] == "size":
            out.append(str(len(dq)))
        elif p[0] == "empty":
            out.append("YES" if not dq else "NO")
    return ("\n".join(out) + "\n") if out else "\n"


add(
    pid="queue-basic-ops", title="队列的基本操作", difficulty="入门",
    tags=["队列", "模拟"], source="队列基础", url="https://leetcode.cn/problems/implement-queue-using-stacks/",
    statement="模拟一个队列，支持：\n\n- `push x`：入队；\n- `pop`：出队并输出队首；\n- `front`：输出队首（不出队）；\n- `back`：输出队尾；\n- `size`：输出元素个数；\n- `empty`：空队列输出 `YES`，否则 `NO`。\n\n**保证** `pop` / `front` / `back` 只在非空队列上调用。",
    input_format="第一行一个整数 $q$（$1 \\le q \\le 10^5$）。\n\n接下来 $q$ 行，每行一个操作（$|x| \\le 10^9$）。",
    output_format="对每个有输出的操作输出一行。",
    constraints=["1 ≤ q ≤ 10^5", "|x| ≤ 10^9", "pop/front/back 仅在非空队列上调用"],
    solver=s_queue_ops,
    specs=[("样例 1", "5\npush 1\npush 2\nfront\nback\npop", 10),
           ("空队列检查", "2\nempty\npush 5", 10),
           ("先进先出", "4\npush 1\npush 2\npop\npop", 15),
           ("只看 size", "3\npush 1\npush 2\nsize", 15),
           ("含负数", "4\npush -1\npush -2\nfront\nback", 20),
           ("反复操作", "6\npush 9\npop\npush 8\nfront\nsize\nempty", 20)],
    cpp=CPP_HEADER + """int main(){int q;scanf("%d",&q);deque<long long>d;char op[16];
for(int i=0;i<q;++i){scanf("%s",op);string o=op;
if(o=="push"){long long x;scanf("%lld",&x);d.push_back(x);}
else if(o=="pop"){printf("%lld\\n",d.front());d.pop_front();}
else if(o=="front"){printf("%lld\\n",d.front());}
else if(o=="back"){printf("%lld\\n",d.back());}
else if(o=="size"){printf("%d\\n",(int)d.size());}
else if(o=="empty"){printf("%s\\n",d.empty()?"YES":"NO");}}
return 0;}
""",
    hint="**队列的 FIFO 特性**：`push` 加到尾部、`pop` 从头部取出。\n\nC++ 中用 `std::queue` 或 `std::deque` 都行；本题需要访问队尾，所以用 `deque` 更方便。",
)

# ---------------------------------------------------------------- 3
def s_remove_dups_stack(t):
    n = int(t.strip().split("\n")[0])
    a = list(map(int, t.strip().split("\n")[1].split()))
    st = []
    for x in a:
        if st and st[-1] == x:
            st.pop()
        else:
            st.append(x)
    return (" ".join(map(str, st)) + "\n") if st else "\n"


add(
    pid="stack-remove-adjacent-nums", title="删除相邻重复的数字", difficulty="入门",
    tags=["栈", "数组"], source="栈的应用", url="https://leetcode.cn/problems/remove-all-adjacent-duplicates-in-string/",
    statement="给定一个整数数组，**反复删除相邻且相等**的一对元素，直到无法继续。\n\n输出最终剩下的数组（保持原顺序）。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数（$|a_i| \\le 10^9$）。",
    output_format="一行，剩余元素（空格分隔）。若全部删完则输出空行。",
    constraints=["1 ≤ n ≤ 10^5", "|a_i| ≤ 10^9"],
    solver=s_remove_dups_stack,
    specs=[("样例 1", "5\n1 2 2 3 3", 10), ("全删完", "4\n1 1 2 2", 10),
           ("无相邻重复", "3\n1 2 3", 15), ("单元素", "1\n5", 15),
           ("连锁删除", "6\n1 1 1 2 2 1", 20), ("含负数", "4\n-1 -1 2 2", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>st;
for(int i=0;i<n;++i){long long x;scanf("%lld",&x);
if(!st.empty()&&st.back()==x)st.pop_back();else st.push_back(x);}
for(size_t i=0;i<st.size();++i){if(i)printf(" ");printf("%lld",st[i]);}
printf("\\n");return 0;}
""",
    hint="**栈**：从左到右扫描，若**栈顶与当前元素相同**就弹出（消除一对），否则压入。\n\n> **为什么正确**：消除后新的栈顶会自动与前缀的下一个元素比较，从而处理连锁消除。",
)

# ---------------------------------------------------------------- 4
def s_prev_greater(t):
    n = int(t.strip().split("\n")[0])
    a = list(map(int, t.strip().split("\n")[1].split()))
    res = [-1] * n
    st = []
    for i in range(n):
        while st and a[st[-1]] <= a[i]:
            st.pop()
        res[i] = a[st[-1]] if st else -1
        st.append(i)
    return " ".join(map(str, res)) + "\n"


add(
    pid="stack-prev-greater", title="上一个更大元素", difficulty="简单",
    tags=["栈", "单调栈"], source="单调栈变体", url="https://leetcode.cn/problems/next-greater-element-i/",
    statement="对数组中每个位置 $i$，求**它左侧第一个比它大**的元素值；不存在则输出 $-1$。\n\n**要求 $O(n)$**。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 2\\times10^5$）。\n\n第二行 $n$ 个整数（$|a_i| \\le 10^9$）。",
    output_format="一行 $n$ 个整数。",
    constraints=["1 ≤ n ≤ 2×10^5", "|a_i| ≤ 10^9", "要求 O(n)"],
    solver=s_prev_greater,
    specs=[("样例 1", "5\n3 1 4 2 5", 10), ("递增", "4\n1 2 3 4", 10),
           ("递减", "4\n4 3 2 1", 15), ("全相同", "3\n5 5 5", 15),
           ("单元素", "1\n7", 20), ("含负数", "5\n-1 0 -2 3 -5", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n),res(n,-1);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
vector<int>st;
for(int i=0;i<n;++i){
while(!st.empty()&&a[st.back()]<=a[i])st.pop_back();
res[i]=st.empty()?-1:a[st.back()];
st.push_back(i);}
for(int i=0;i<n;++i){if(i)printf(" ");printf("%lld",res[i]);}
printf("\\n");return 0;}
""",
    hint="**单调栈（递减）**：维护一个**递减**的栈（存下标）。处理 `i` 时先把栈中所有**小于等于** `a[i]` 的弹出——它们不可能再成为后面元素的「左大值」。\n\n弹完后栈顶就是左侧第一个更大的元素。\n\n> **对比**：「上一个更小元素」维护**递增**栈，用 `>=` 弹出。",
)

# ---------------------------------------------------------------- 5
def s_min_remove_brackets(t):
    s = t.strip("\n").split("\n")[0]
    open_cnt = 0
    unmatched_right = 0
    for c in s:
        if c == "(":
            open_cnt += 1
        elif c == ")":
            if open_cnt:
                open_cnt -= 1
            else:
                unmatched_right += 1
    return f"{unmatched_right + open_cnt}\n"


add(
    pid="stack-min-remove-brackets", title="最少需要删除的括号数", difficulty="简单",
    tags=["栈", "字符串"], source="LeetCode 1249", url="https://leetcode.cn/problems/minimum-remove-to-make-valid-parentheses/",
    statement="给定一个只含 `(` 和 `)` 的字符串，求**最少需要删除多少个字符**才能使它成为合法的括号序列。",
    input_format="一行一个字符串 $s$（$0 \\le |s| \\le 10^5$），仅含 `(` 和 `)`。",
    output_format="一行一个整数，表示最少删除数。",
    constraints=["0 ≤ |s| ≤ 10^5", "仅含圆括号"],
    solver=s_min_remove_brackets,
    specs=[("样例 1", "())", 10), ("样例 2", "(((", 10), ("空串", "\n", 15),
           ("已合法", "()()", 15), ("全右括号", ")))", 20), ("交错", "())(()", 20)],
    cpp=CPP_HEADER + """int main(){string s;getline(cin,s);
int open=0,ans=0;
for(char c:s){
if(c=='(')++open;
else if(c==')'){if(open)--open;else ++ans;}}
printf("%d\\n",ans+open);return 0;}
""",
    hint="**贪心计数**：\n\n- 遇到 `(`：`open++`；\n- 遇到 `)`：若 `open > 0` 则配对（`open--`），否则这个右括号**必须删除**（`ans++`）。\n\n扫描结束后，**剩余的未配对左括号也要删除**，所以答案是 `ans + open`。\n\n时间 $O(n)$。",
)

# ---------------------------------------------------------------- 6
def s_reverse_stack(t):
    ls = L(t)
    n = int(ls[0])
    st = list(map(int, ls[1].split()))
    return " ".join(map(str, st[::-1])) + "\n"


add(
    pid="stack-reverse", title="逆序输出栈中元素", difficulty="入门",
    tags=["栈", "数组"], source="栈基础", url="https://leetcode.cn/problems/valid-parentheses/",
    statement="给定一个栈（按**从栈底到栈顶**的顺序给出元素），请**从栈顶到栈底**依次输出所有元素。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数，按**栈底到栈顶**顺序给出（$|a_i| \\le 10^9$）。",
    output_format="一行 $n$ 个整数，按**栈顶到栈底**顺序。",
    constraints=["1 ≤ n ≤ 10^5", "|a_i| ≤ 10^9"],
    solver=s_reverse_stack,
    specs=[("样例 1", "3\n1 2 3", 10), ("单元素", "1\n7", 10),
           ("含负数", "4\n-1 0 1 2", 15), ("全相同", "3\n5 5 5", 15),
           ("两元素", "2\n1 2", 20), ("大数组", "5\n1 2 3 4 5", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
for(int i=n-1;i>=0;--i){if(i<n-1)printf(" ");printf("%lld",a[i]);}
printf("\\n");return 0;}
""",
    hint="**栈顶就是数组末尾**：按栈底到栈顶给出的序列，逆序输出即可得到栈顶到栈底。\n\n时间 $O(n)$。",
)

# ---------------------------------------------------------------- 7
def s_bracket_depth(t):
    s = t.strip("\n").split("\n")[0]
    cur = best = 0
    for c in s:
        if c == "(":
            cur += 1
            best = max(best, cur)
        elif c == ")":
            cur -= 1
    return f"{best}\n"


add(
    pid="stack-bracket-depth", title="括号的最大嵌套深度", difficulty="入门",
    tags=["栈", "字符串"], source="LeetCode 1614", url="https://leetcode.cn/problems/maximum-nesting-depth-of-the-parentheses/",
    statement="给定一个**合法**的括号字符串（可能夹杂其他字符，忽略即可），求它的**最大嵌套深度**。\n\n嵌套深度指同一时刻未闭合的左括号数量的最大值。",
    input_format="一行一个字符串 $s$（$0 \\le |s| \\le 100$），保证其中的括号是**合法**序列。",
    output_format="一行一个整数，表示最大嵌套深度。",
    constraints=["0 ≤ |s| ≤ 100", "括号序列合法"],
    solver=s_bracket_depth,
    specs=[("样例 1", "(1+(2*3)+((8)/4))+1", 10), ("样例 2", "(1)+((2))+(((3)))", 10),
           ("空串", "\n", 15), ("无括号", "abc", 15),
           ("单层", "()", 20), ("深层", "(((())))", 20)],
    cpp=CPP_HEADER + """int main(){string s;getline(cin,s);
int cur=0,best=0;
for(char c:s){if(c=='('){++cur;best=max(best,cur);}else if(c==')')--cur;}
printf("%d\\n",best);return 0;}
""",
    hint="**计数即可**：遇到 `(` 深度加一，遇到 `)` 深度减一，全程记录最大值。\n\n非括号字符直接忽略。时间 $O(n)$。",
)

# ---------------------------------------------------------------- 8
def s_deque_ops(t):
    ls = L(t)
    q = int(ls[0])
    dq = deque()
    out = []
    for i in range(1, q + 1):
        p = ls[i].split()
        if p[0] == "push_front":
            dq.appendleft(int(p[1]))
        elif p[0] == "push_back":
            dq.append(int(p[1]))
        elif p[0] == "pop_front":
            out.append(str(dq.popleft()))
        elif p[0] == "pop_back":
            out.append(str(dq.pop()))
        elif p[0] == "front":
            out.append(str(dq[0]))
        elif p[0] == "back":
            out.append(str(dq[-1]))
        elif p[0] == "size":
            out.append(str(len(dq)))
    return ("\n".join(out) + "\n") if out else "\n"


add(
    pid="deque-basic-ops", title="双端队列的基本操作", difficulty="入门",
    tags=["队列", "双端队列", "模拟"], source="双端队列", url="https://leetcode.cn/problems/design-circular-deque/",
    statement="模拟一个**双端队列**，支持：\n\n- `push_front x` / `push_back x`：在队首 / 队尾插入 $x$；\n- `pop_front` / `pop_back`：从队首 / 队尾删除并输出；\n- `front` / `back`：输出队首 / 队尾；\n- `size`：输出元素个数。\n\n**保证**删除与查询操作只在非空队列上调用。",
    input_format="第一行一个整数 $q$（$1 \\le q \\le 10^5$）。\n\n接下来 $q$ 行，每行一个操作（$|x| \\le 10^9$）。",
    output_format="对每个有输出的操作输出一行。",
    constraints=["1 ≤ q ≤ 10^5", "|x| ≤ 10^9", "删除/查询仅在非空队列上调用"],
    solver=s_deque_ops,
    specs=[("样例 1", "6\npush_back 1\npush_front 2\nfront\nback\npop_front\npop_back", 10),
           ("只从前面操作", "4\npush_front 1\npush_front 2\nfront\nsize", 10),
           ("只从后面操作", "4\npush_back 1\npush_back 2\nback\nsize", 15),
           ("交替插入", "4\npush_back 1\npush_front 2\npop_back\npop_front", 15),
           ("单元素", "3\npush_back 5\nfront\nback", 20),
           ("含负数", "4\npush_front -1\npush_back -2\nfront\nback", 20)],
    cpp=CPP_HEADER + """int main(){int q;scanf("%d",&q);deque<long long>d;char op[16];
for(int i=0;i<q;++i){scanf("%s",op);string o=op;
if(o=="push_front"){long long x;scanf("%lld",&x);d.push_front(x);}
else if(o=="push_back"){long long x;scanf("%lld",&x);d.push_back(x);}
else if(o=="pop_front"){printf("%lld\\n",d.front());d.pop_front();}
else if(o=="pop_back"){printf("%lld\\n",d.back());d.pop_back();}
else if(o=="front"){printf("%lld\\n",d.front());}
else if(o=="back"){printf("%lld\\n",d.back());}
else if(o=="size"){printf("%d\\n",(int)d.size());}}
return 0;}
""",
    hint="**双端队列**两端都能高效插入删除。\n\nC++ 用 `std::deque`；Python 用 `collections.deque`。\n\n> **用途**：单调队列（滑动窗口最值）就依赖双端队列的两端操作。",
)

# ---------------------------------------------------------------- 9
def s_validate_stack_seq(t):
    ls = L(t)
    n = int(ls[0])
    pushed = list(map(int, ls[1].split()))
    popped = list(map(int, ls[2].split()))
    st = []
    j = 0
    for x in pushed:
        st.append(x)
        while st and j < n and st[-1] == popped[j]:
            st.pop()
            j += 1
    return ("YES\n" if j == n else "NO\n")


add(
    pid="stack-validate-sequence", title="验证栈序列", difficulty="中等",
    tags=["栈", "模拟"], source="LeetCode 946", url="https://leetcode.cn/problems/validate-stack-sequences/",
    statement="给定两个序列 $pushed$（入栈顺序）和 $popped$（出栈顺序），判断 $popped$ 是否**可能是** $pushed$ 的合法出栈序列。\n\n是则输出 `YES`，否则 `NO`。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 1000$）。\n\n第二行 $n$ 个整数（入栈顺序）。\n\n第三行 $n$ 个整数（出栈顺序）。",
    output_format="一行，输出 `YES` 或 `NO`。",
    constraints=["1 ≤ n ≤ 1000", "两序列都是同一组数的排列"],
    solver=s_validate_stack_seq,
    specs=[("样例 1（合法）", "5\n1 2 3 4 5\n4 5 3 2 1", 10),
           ("样例 2（非法）", "5\n1 2 3 4 5\n4 3 5 1 2", 10),
           ("升序出栈", "3\n1 2 3\n1 2 3", 15), ("降序出栈", "3\n1 2 3\n3 2 1", 15),
           ("单元素", "1\n1\n1", 20), ("非法", "3\n1 2 3\n3 1 2", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);
vector<int>a(n),b(n);
for(int i=0;i<n;++i)scanf("%d",&a[i]);
for(int i=0;i<n;++i)scanf("%d",&b[i]);
vector<int>st;int j=0;
for(int x:a){st.push_back(x);
while(!st.empty()&&j<n&&st.back()==b[j]){st.pop_back();++j;}}
printf("%s\\n",j==n?"YES":"NO");return 0;}
""",
    hint="**模拟入栈过程**：按 $pushed$ 的顺序入栈，**每入栈一个就检查栈顶是否等于 $popped$ 的下一个待出元素**——是就不断弹出。\n\n最后若 $popped$ 全部被匹配完，说明合法。\n\n时间 $O(n)$。",
)

# ---------------------------------------------------------------- 10
def s_monotonic_queue_max_k(t):
    ls = L(t)
    n, k = map(int, ls[0].split())
    a = list(map(int, ls[1].split()))
    dq = deque()
    res = []
    for i in range(n):
        while dq and a[dq[-1]] <= a[i]:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            res.append(a[dq[0]])
    return " ".join(map(str, res)) + "\n"


add(
    pid="queue-window-max-again", title="滑动窗口最大值（单调队列练习）", difficulty="中等",
    tags=["队列", "单调队列", "滑动窗口"], source="单调队列", url="https://leetcode.cn/problems/sliding-window-maximum/",
    statement="给定数组和窗口大小 $k$，求每个窗口内的**最大值**。\n\n**要求 $O(n)$**。",
    input_format="第一行两个整数 $n, k$（$1 \\le k \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数（$|a_i| \\le 10^9$）。",
    output_format="一行 $n-k+1$ 个整数。",
    constraints=["1 ≤ k ≤ n ≤ 10^5", "|a_i| ≤ 10^9", "要求 O(n)"],
    solver=s_monotonic_queue_max_k,
    specs=[("样例 1", "8 3\n1 3 -1 -3 5 3 6 7", 10), ("k = 1", "4 1\n5 2 9 1", 10),
           ("k = n", "4 4\n5 2 9 1", 15), ("递增", "5 3\n1 2 3 4 5", 15),
           ("递减", "5 3\n5 4 3 2 1", 20), ("全相同", "4 2\n3 3 3 3", 20)],
    cpp=CPP_HEADER + """int main(){int n,k;scanf("%d %d",&n,&k);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
deque<int>dq;bool first=true;
for(int i=0;i<n;++i){
while(!dq.empty()&&a[dq.back()]<=a[i])dq.pop_back();
dq.push_back(i);
if(dq.front()<=i-k)dq.pop_front();
if(i>=k-1){if(!first)printf(" ");printf("%lld",a[dq.front()]);first=false;}}
printf("\\n");return 0;}
""",
    hint="**单调队列**：双端队列存**下标**，保持对应值**递减**。\n\n1. 队尾弹出所有比新元素小的；\n2. 新元素入队；\n3. 队首若滑出窗口则弹出；\n4. 队首就是当前窗口最大值。\n\n时间 $O(n)$。",
)

# ---------------------------------------------------------------- 11
def s_two_stacks_queue_ops(t):
    ls = L(t)
    q = int(ls[0])
    in_st, out_st = [], []
    res = []
    for i in range(1, q + 1):
        p = ls[i].split()
        if p[0] == "push":
            in_st.append(int(p[1]))
        elif p[0] in ("pop", "peek"):
            if not out_st:
                while in_st:
                    out_st.append(in_st.pop())
            res.append(str(out_st.pop() if p[0] == "pop" else out_st[-1]))
    return ("\n".join(res) + "\n") if res else "\n"


add(
    pid="queue-two-stacks-ops", title="用两个栈实现队列（操作模拟）", difficulty="中等",
    tags=["栈", "队列", "设计"], source="LeetCode 232", url="https://leetcode.cn/problems/implement-queue-using-stacks/",
    statement="用两个栈模拟队列，支持 `push x`、`pop`、`peek`。\n\n输出所有 `pop` 和 `peek` 的结果。\n\n**保证** `pop` / `peek` 只在非空队列上调用。",
    input_format="第一行一个整数 $q$（$1 \\le q \\le 10^5$）。\n\n接下来 $q$ 行，每行一个操作（$|x| \\le 10^9$）。",
    output_format="对每个 `pop` / `peek` 输出一行。",
    constraints=["1 ≤ q ≤ 10^5", "|x| ≤ 10^9", "pop/peek 仅在非空队列上调用"],
    solver=s_two_stacks_queue_ops,
    specs=[("样例 1", "5\npush 1\npush 2\npeek\npop\npeek", 10),
           ("连续弹出", "4\npush 1\npush 2\npop\npop", 10),
           ("交替", "6\npush 1\npop\npush 2\npop\npush 3\npeek", 15),
           ("只 peek", "3\npush 5\npush 6\npeek", 15),
           ("含负数", "4\npush -1\npush -2\npop\npeek", 20),
           ("大量入队", "6\npush 1\npush 2\npush 3\npop\npop\npop", 20)],
    cpp=CPP_HEADER + """int main(){int q;scanf("%d",&q);
vector<long long>in,out;char op[16];
for(int i=0;i<q;++i){scanf("%s",op);string o=op;
if(o=="push"){long long x;scanf("%lld",&x);in.push_back(x);}
else{if(out.empty()){while(!in.empty()){out.push_back(in.back());in.pop_back();}}
if(o=="pop"){printf("%lld\\n",out.back());out.pop_back();}
else printf("%lld\\n",out.back());}}
return 0;}
""",
    hint="**两个栈分工**：`in` 负责入队，`out` 负责出队。\n\n出队时若 `out` 为空，就把 `in` **全部倒入** `out`（顺序自然反转）。\n\n> **摊还分析**：每个元素最多被倒一次，所以 $q$ 次操作总共 $O(q)$。",
)

# ---------------------------------------------------------------- 12
def s_histogram_area_small(t):
    ls = L(t)
    n = int(ls[0])
    a = list(map(int, ls[1].split()))
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
    pid="stack-histogram-area", title="柱状图中的最大矩形（练习）", difficulty="困难",
    tags=["栈", "单调栈"], source="LeetCode 84", url="https://leetcode.cn/problems/largest-rectangle-in-histogram/",
    statement="给定柱状图各柱子的高度（宽度均为 1），求能勾勒出的**最大矩形面积**。\n\n**要求 $O(n)$**。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 10^5$）。\n\n第二行 $n$ 个非负整数（$0 \\le h_i \\le 10^4$）。",
    output_format="一行一个整数。",
    constraints=["1 ≤ n ≤ 10^5", "0 ≤ h_i ≤ 10^4", "要求 O(n)"],
    solver=s_histogram_area_small,
    specs=[("样例 1", "6\n2 1 5 6 2 3", 10), ("单柱", "1\n5", 10),
           ("全相同", "4\n3 3 3 3", 15), ("含 0", "3\n1 0 1", 15),
           ("递增", "4\n1 2 3 4", 20), ("递减", "4\n4 3 2 1", 20)],
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
    hint="**单调栈 + 哨兵**：在数组末尾追加高度 0 的哨兵，这样循环结束时能弹出栈内全部元素。\n\n当遇到比栈顶矮的柱子时，栈顶的**右边界**（当前下标）和**左边界**（栈中下一个元素）都确定了，可以计算面积。\n\n> **宽度公式**：`i - left - 1`。",
)

# ---------------------------------------------------------------- 13
def s_132(t):
    ls = L(t)
    n = int(ls[0])
    a = list(map(int, ls[1].split()))
    st = []
    third = float("-inf")
    for x in reversed(a):
        if x < third:
            return "YES\n"
        while st and st[-1] < x:
            third = st.pop()
        st.append(x)
    return "NO\n"


add(
    pid="stack-132-pattern", title="132 模式", difficulty="中等",
    tags=["栈", "单调栈"], source="LeetCode 456", url="https://leetcode.cn/problems/132-pattern/",
    statement="判断数组中是否存在下标 $i < j < k$ 使得 $a_i < a_k < a_j$（即「132 模式」）。\n\n存在输出 `YES`，否则 `NO`。\n\n**要求 $O(n)$**。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 2\\times10^5$）。\n\n第二行 $n$ 个整数（$|a_i| \\le 10^9$）。",
    output_format="一行，输出 `YES` 或 `NO`。",
    constraints=["1 ≤ n ≤ 2×10^5", "|a_i| ≤ 10^9", "要求 O(n)"],
    solver=s_132,
    specs=[("样例 1（存在）", "4\n1 2 3 4", 10),
           ("样例 2（不存在）", "4\n3 1 4 2", 10),
           ("样例 3（不存在）", "4\n-1 3 2 0", 15),
           ("单元素", "1\n1", 15), ("递增三元", "3\n1 3 2", 20),
           ("递减", "4\n4 3 2 1", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);vector<long long>a(n);
for(int i=0;i<n;++i)scanf("%lld",&a[i]);
vector<long long>st;long long third=LLONG_MIN;
for(int i=n-1;i>=0;--i){
if(a[i]<third){printf("YES\\n");return 0;}
while(!st.empty()&&st.back()<a[i]){third=st.back();st.pop_back();}
st.push_back(a[i]);}
printf("NO\\n");return 0;}
""",
    hint="**从右往左扫描 + 单调栈**：\n\n维护一个**递减**的栈，并记录一个变量 `third`（表示「已经找到的、可以作为 $a_k$ 的最大值」）。\n\n对每个 $x = a[i]$：\n\n1. 若 `x < third`，说明找到了 $a_i < a_k < a_j$ → 成功；\n2. 否则，把栈中所有比 $x$ 小的弹出，**每弹出一个就用它更新 `third`**（它比 $x$ 小，可以当 $a_k$）；\n3. 把 $x$ 压栈。\n\n时间 $O(n)$。",
)

# ---------------------------------------------------------------- 14
def s_bracket_score_small(t):
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
    pid="stack-bracket-score-again", title="括号分数（练习）", difficulty="中等",
    tags=["栈", "字符串"], source="LeetCode 856", url="https://leetcode.cn/problems/score-of-parentheses/",
    statement="给定合法括号串，按规则计算分数：\n\n- `()` 得 1 分；\n- `AB` 得 $A + B$ 分；\n- `(A)` 得 $2A$ 分。",
    input_format="一行一个平衡的括号字符串（$2 \\le |s| \\le 5\\times10^4$）。",
    output_format="一行一个整数。",
    constraints=["2 ≤ |s| ≤ 5×10^4", "保证平衡"],
    solver=s_bracket_score_small,
    specs=[("样例 1", "()", 10), ("嵌套", "(())", 10), ("并列", "()()", 15),
           ("混合", "(()(()))", 15), ("深层", "(((())))", 20), ("多个并列", "()()()()", 20)],
    cpp=CPP_HEADER + """int main(){string s;cin>>s;vector<long long>st;st.push_back(0);
for(char c:s){
if(c=='(')st.push_back(0);
else{long long v=st.back();st.pop_back();st.back()+=max(2*v,1LL);}}
printf("%lld\\n",st.back());return 0;}
""",
    hint="**栈存每层累计分数**：遇 `(` 压入 0；遇 `)` 弹出内层分数 $v$，把 `max(2v, 1)` 加到外层。\n\n`v = 0` 表示这是空括号 `()`，得 1 分；否则得 $2v$ 分。\n\n时间 $O(n)$。",
)


def main() -> None:
    for p in P:
        finalize(p, OUT / f"{p['id']}.json")
        total = sum(t["score"] for t in p["tests"])
        print(f"生成 {p['id']:36s} {len(p['tests'])} 测试点, 总分 {total:3d}")


if __name__ == "__main__":
    main()
