"""生成「栈与队列」分类的第二批题目。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from genkit import build_tests, finalize, numbers  # noqa: E402

OUT = ROOT / "oj" / "data" / "problems" / "02-stack-queue"


# ============================================================ 1. 最小栈
def solve_min_stack(text: str) -> str:
    """辅助栈同步维护当前最小值。"""
    ls = text.strip("\n").split("\n")
    q = int(ls[0])
    st, mn = [], []
    out = []
    for i in range(1, q + 1):
        p = ls[i].split()
        op = p[0]
        if op == "push":
            x = int(p[1])
            st.append(x)
            mn.append(x if not mn else min(mn[-1], x))
        elif op == "pop":
            st.pop()
            mn.pop()
        elif op == "top":
            out.append(str(st[-1]))
        elif op == "getMin":
            out.append(str(mn[-1]))
    return ("\n".join(out) + "\n") if out else "\n"


MS_SPECS = [
    ("样例 1", "5\npush 5\npush 3\ngetMin\ntop\npop", 10),
    ("样例 2（弹掉最小）", "6\npush 2\npush 1\ngetMin\npop\ngetMin\ntop", 10),
    ("单元素", "3\npush 7\ngetMin\ntop", 10),
    ("递增入栈", "6\npush 1\npush 2\npush 3\ngetMin\ntop\npop", 15),
    ("递减入栈", "6\npush 3\npush 2\npush 1\ngetMin\ntop\npop", 15),
    ("含负数", "6\npush -1\npush -5\npush 0\ngetMin\ntop\npop", 20),
    ("反复查询", "8\npush 4\ngetMin\npush 4\ngetMin\ntop\npop\ngetMin\npop", 20),
]


def build_min_stack() -> dict:
    tests = build_tests(MS_SPECS, solve_min_stack)
    return {
        "id": "stack-min-stack",
        "title": "最小栈",
        "difficulty": "简单",
        "tags": ["栈", "设计", "辅助栈"],
        "source": {
            "name": "LeetCode 155 / 剑指 Offer 30",
            "url": "https://leetcode.cn/problems/min-stack/",
        },
        "statement": (
            "设计一个支持 `push`、`pop`、`top` 操作，并能在**常数时间**内检索到最小元素的栈。\n\n"
            "- `push x`：将元素 $x$ 压入栈；\n"
            "- `pop`：删除栈顶元素；\n"
            "- `top`：获取栈顶元素；\n"
            "- `getMin`：获取栈中的最小元素。\n\n"
            "**要求所有操作的时间复杂度都是 $O(1)$**。"
        ),
        "input_format": (
            "第一行一个整数 $q$（$1 \\le q \\le 2 \\times 10^5$），表示操作数。\n\n"
            "接下来 $q$ 行，每行一个操作。其中 $|x| \\le 10^9$。\n\n"
            "**保证在栈非空时才调用 `pop` / `top` / `getMin`**。"
        ),
        "output_format": "对每个 `top` 和 `getMin` 操作，输出一行对应的结果。",
        "constraints": ["1 ≤ q ≤ 2×10^5", "|x| ≤ 10^9", "pop/top/getMin 仅在非空栈上调用", "所有操作 O(1)"],
        "samples": [
            {"input": "5\npush 5\npush 3\ngetMin\ntop\npop\n", "output": "3\n3\n",
             "explain": "压入 5、3 后最小值为 3，栈顶也是 3；弹出栈顶 3。"},
            {"input": "6\npush 2\npush 1\ngetMin\npop\ngetMin\ntop\n", "output": "1\n2\n2\n",
             "explain": "最小值为 1；弹出 1 之后最小值变回 2，栈顶也是 2。"},
        ],
        "hint": (
            "**辅助栈**：再开一个栈 `mn`，与主栈 `st` **同步**记录「当前栈内最小值」。\n\n"
            "- `push x`：`st` 压入 $x$；`mn` 压入 `min(mn.top(), x)`（若 `mn` 为空则直接压 $x$）；\n"
            "- `pop`：两个栈同时弹出；\n"
            "- `getMin`：直接返回 `mn` 的栈顶。\n\n"
            "关键在于 `mn` 与 `st` 的**高度始终一致**，这样弹出时不需要额外判断。"
            "所有操作都是 $O(1)$。"
        ),
        "starter_code": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <vector>\n"
                "#include <cstring>\n\n"
                "// TODO: 用辅助栈同步维护最小值\n\n"
                "int main() {\n"
                "    int q;\n"
                "    scanf(\"%d\", &q);\n"
                "    for (int i = 0; i < q; ++i) {\n"
                "        char op[16];\n"
                "        scanf(\"%s\", op);\n"
                "        if (strcmp(op, \"push\") == 0) {\n"
                "            long long x; scanf(\"%lld\", &x);\n"
                "            // TODO\n"
                "        } else if (strcmp(op, \"pop\") == 0) {\n"
                "            // TODO\n"
                "        } else if (strcmp(op, \"top\") == 0) {\n"
                "            // TODO: 输出栈顶\n"
                "        } else if (strcmp(op, \"getMin\") == 0) {\n"
                "            // TODO: 输出最小值\n"
                "        }\n"
                "    }\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "tests": tests,
        "reference": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <vector>\n"
                "#include <cstring>\n"
                "#include <algorithm>\n\n"
                "std::vector<long long> st, mn;\n\n"
                "int main() {\n"
                "    int q;\n"
                "    scanf(\"%d\", &q);\n"
                "    for (int i = 0; i < q; ++i) {\n"
                "        char op[16];\n"
                "        scanf(\"%s\", op);\n"
                "        if (strcmp(op, \"push\") == 0) {\n"
                "            long long x; scanf(\"%lld\", &x);\n"
                "            st.push_back(x);\n"
                "            mn.push_back(mn.empty() ? x : std::min(mn.back(), x));\n"
                "        } else if (strcmp(op, \"pop\") == 0) {\n"
                "            st.pop_back();\n"
                "            mn.pop_back();\n"
                "        } else if (strcmp(op, \"top\") == 0) {\n"
                "            printf(\"%lld\\n\", st.back());\n"
                "        } else if (strcmp(op, \"getMin\") == 0) {\n"
                "            printf(\"%lld\\n\", mn.back());\n"
                "        }\n"
                "    }\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "time_limit": 2.0,
    }


# ============================================================ 2. 每日温度
def solve_daily_temperatures(text: str) -> str:
    """单调栈：找右侧第一个更大元素的距离。"""
    nums = numbers(text)
    n, t = nums[0], nums[1:1 + nums[0]]
    res = [0] * n
    st = []
    for i in range(n):
        while st and t[st[-1]] < t[i]:
            j = st.pop()
            res[j] = i - j
        st.append(i)
    return " ".join(map(str, res)) + "\n"


DT_SPECS = [
    ("样例 1", "8\n73 74 75 71 69 72 76 73", 10),
    ("样例 2（递减）", "5\n30 25 20 15 10", 10),
    ("单元素", "1\n50", 10),
    ("递增", "5\n10 20 30 40 50", 15),
    ("全相同", "4\n7 7 7 7", 15),
    ("交替", "6\n1 3 2 4 3 5", 20),
    ("含负数", "6\n-5 -3 -4 -1 -2 0", 20),
]


def build_daily_temperatures() -> dict:
    tests = build_tests(DT_SPECS, solve_daily_temperatures)
    return {
        "id": "stack-daily-temperatures",
        "title": "每日温度",
        "difficulty": "中等",
        "tags": ["栈", "单调栈"],
        "source": {
            "name": "LeetCode 739 / 单调栈经典",
            "url": "https://leetcode.cn/problems/daily-temperatures/",
        },
        "statement": (
            "给定一个整数数组 $t$，表示连续若干天的温度。\n\n"
            "对每一天 $i$，请计算**至少需要等待多少天**才会出现一个更高的温度。"
            "若之后都不会更高，则答案为 $0$。\n\n"
            "**要求：时间复杂度 $O(n)$**。"
        ),
        "input_format": "第一行一个整数 $n$（$1 \\le n \\le 2 \\times 10^5$）。\n\n第二行 $n$ 个整数 $t_i$（$-10^9 \\le t_i \\le 10^9$）。",
        "output_format": "一行 $n$ 个整数，依次为每一天需要等待的天数，以空格分隔。",
        "constraints": ["1 ≤ n ≤ 2×10^5", "|t_i| ≤ 10^9", "要求 O(n) 算法"],
        "samples": [
            {"input": "8\n73 74 75 71 69 72 76 73\n", "output": "1 1 4 2 1 1 0 0\n",
             "explain": "第 1 天(73)等 1 天到 74；第 3 天(75)要等 4 天到 76；第 7 天(76)之后没有更高温度，为 0。"},
            {"input": "5\n30 25 20 15 10\n", "output": "0 0 0 0 0\n",
             "explain": "温度严格递减，之后都不会更高，全部为 0。"},
        ],
        "hint": (
            "**单调栈**：维护一个栈存**下标**，栈内对应的温度从栈底到栈顶**单调递减**。\n\n"
            "从左到右扫描第 $i$ 天：当栈非空且栈顶下标的温度 $< t_i$ 时，"
            "栈顶那一天「等待的天数」就是 $i - j$，弹出它；重复直到不满足。然后把 $i$ 压栈。\n\n"
            "每个下标最多入栈、出栈各一次，因此总时间 $O(n)$。\n\n"
            "> 这与「下一个更大元素」是同一个模板，只是记录的不是值而是**下标之差**。"
        ),
        "starter_code": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <vector>\n\n"
                "int main() {\n"
                "    int n;\n"
                "    scanf(\"%d\", &n);\n"
                "    std::vector<long long> t(n);\n"
                "    for (int i = 0; i < n; ++i) scanf(\"%lld\", &t[i]);\n\n"
                "    std::vector<int> res(n, 0);\n"
                "    std::vector<int> stk;\n"
                "    // TODO: 单调栈求解\n\n"
                "    for (int i = 0; i < n; ++i) {\n"
                "        if (i) printf(\" \");\n"
                "        printf(\"%d\", res[i]);\n"
                "    }\n"
                "    printf(\"\\n\");\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "tests": tests,
        "reference": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <vector>\n\n"
                "int main() {\n"
                "    int n;\n"
                "    scanf(\"%d\", &n);\n"
                "    std::vector<long long> t(n);\n"
                "    for (int i = 0; i < n; ++i) scanf(\"%lld\", &t[i]);\n\n"
                "    std::vector<int> res(n, 0);\n"
                "    std::vector<int> stk;\n"
                "    for (int i = 0; i < n; ++i) {\n"
                "        while (!stk.empty() && t[stk.back()] < t[i]) {\n"
                "            int j = stk.back();\n"
                "            stk.pop_back();\n"
                "            res[j] = i - j;\n"
                "        }\n"
                "        stk.push_back(i);\n"
                "    }\n\n"
                "    for (int i = 0; i < n; ++i) {\n"
                "        if (i) printf(\" \");\n"
                "        printf(\"%d\", res[i]);\n"
                "    }\n"
                "    printf(\"\\n\");\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "time_limit": 2.0,
    }


# ============================================================ 3. 逆波兰表达式求值
def solve_rpn(text: str) -> str:
    """后缀表达式求值：遇操作数入栈，遇运算符弹两个算完再入栈。"""
    tokens = text.split()
    st = []
    for tk in tokens:
        if tk in ("+", "-", "*", "/"):
            b = st.pop()
            a = st.pop()
            if tk == "+":
                st.append(a + b)
            elif tk == "-":
                st.append(a - b)
            elif tk == "*":
                st.append(a * b)
            else:
                # 向零取整
                q = abs(a) // abs(b)
                st.append(q if (a >= 0) == (b >= 0) else -q)
        else:
            st.append(int(tk))
    return f"{st[-1]}\n"


RPN_SPECS = [
    ("样例 1", "2 1 + 3 *", 10),
    ("样例 2（除法）", "4 13 5 / +", 10),
    ("单数字", "42", 10),
    ("纯加法", "1 2 3 4 + + +", 15),
    ("纯乘法", "2 3 4 * *", 15),
    ("含负数", "-5 3 -", 20),
    ("混合运算", "10 6 9 3 + -11 * / * 17 + 5 +", 20),
]


def build_rpn() -> dict:
    tests = build_tests(RPN_SPECS, solve_rpn)
    return {
        "id": "stack-eval-rpn",
        "title": "逆波兰表达式求值",
        "difficulty": "简单",
        "tags": ["栈", "表达式求值"],
        "source": {
            "name": "LeetCode 150 / 后缀表达式",
            "url": "https://leetcode.cn/problems/evaluate-reverse-polish-notation/",
        },
        "statement": (
            "给定一个**逆波兰表达式**（后缀表达式），求它的值。\n\n"
            "合法的运算符包括 `+`、`-`、`*`、`/`。每个操作数可以是整数或另一个表达式。\n\n"
            "**注意**：\n"
            "- 两个整数之间的除法总是**向零截断**（例如 `6 / -4 = -1`，`-7 / 2 = -3`）；\n"
            "- 表达式保证合法，不会出现除以 $0$ 的情况。"
        ),
        "input_format": "一行，若干个以空格分隔的 token，依次为操作数或运算符。操作数范围 $|x| \\le 10^4$。",
        "output_format": "一行，输出表达式的值。",
        "constraints": ["token 数 ≤ 10^4", "|操作数| ≤ 10^4", "除法向零截断", "保证表达式合法且无除零"],
        "samples": [
            {"input": "2 1 + 3 *\n", "output": "9\n",
             "explain": "先算 `2 + 1 = 3`，再算 `3 * 3 = 9`。"},
            {"input": "4 13 5 / +\n", "output": "6\n",
             "explain": "先算 `13 / 5 = 2`（向零截断），再算 `4 + 2 = 6`。"},
        ],
        "hint": (
            "**栈**：从左到右扫描 token。\n\n"
            "- 遇到操作数：压栈；\n"
            "- 遇到运算符：弹出**两个**操作数，先弹出的是**右**操作数 $b$，后弹出的是**左**操作数 $a$，"
            "计算 $a \\; op \\; b$，把结果压栈。\n\n"
            "扫描结束后栈中只剩一个数，就是答案。\n\n"
            "> **易错点**：减法和除法**不满足交换律**，弹出顺序反了结果就完全错误。"
            "另外 C++ 的 `/` 对整数本来就是向零截断，直接用即可。"
        ),
        "starter_code": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <vector>\n"
                "#include <string>\n"
                "#include <iostream>\n\n"
                "int main() {\n"
                "    std::string tk;\n"
                "    std::vector<long long> st;\n"
                "    while (std::cin >> tk) {\n"
                "        if (tk == \"+\" || tk == \"-\" || tk == \"*\" || tk == \"/\") {\n"
                "            // TODO: 弹出两个操作数计算后压栈\n"
                "        } else {\n"
                "            st.push_back(std::stoll(tk));\n"
                "        }\n"
                "    }\n"
                "    printf(\"%lld\\n\", st.back());\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "tests": tests,
        "reference": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <vector>\n"
                "#include <string>\n"
                "#include <iostream>\n\n"
                "int main() {\n"
                "    std::string tk;\n"
                "    std::vector<long long> st;\n"
                "    while (std::cin >> tk) {\n"
                "        if (tk == \"+\" || tk == \"-\" || tk == \"*\" || tk == \"/\") {\n"
                "            long long b = st.back(); st.pop_back();\n"
                "            long long a = st.back(); st.pop_back();\n"
                "            long long r = 0;\n"
                "            if (tk == \"+\") r = a + b;\n"
                "            else if (tk == \"-\") r = a - b;\n"
                "            else if (tk == \"*\") r = a * b;\n"
                "            else r = a / b;              // C++ 整数除法即向零截断\n"
                "            st.push_back(r);\n"
                "        } else {\n"
                "            st.push_back(std::stoll(tk));\n"
                "        }\n"
                "    }\n"
                "    printf(\"%lld\\n\", st.back());\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "time_limit": 2.0,
    }


# ============================================================ 4. 删除相邻重复项
def solve_remove_adjacent(text: str) -> str:
    """栈：栈顶与当前字符相同则弹出，否则压入。"""
    ls = text.strip("\n").split("\n")
    s = ls[0] if ls else ""
    st = []
    for c in s:
        if st and st[-1] == c:
            st.pop()
        else:
            st.append(c)
    return ("".join(st) + "\n") if st else "\n"


RA_SPECS = [
    ("样例 1", "abbaca", 10),
    ("样例 2（全消）", "abba", 10),
    ("单字符", "a", 10),
    ("无重复", "abcd", 15),
    ("全部相同", "aaaa", 15),
    ("三段相消", "aabccbdd", 20),
    ("大小写敏感", "aAbbAc", 20),
]


def build_remove_adjacent() -> dict:
    tests = build_tests(RA_SPECS, solve_remove_adjacent)
    return {
        "id": "stack-remove-adjacent-duplicates",
        "title": "删除字符串中所有相邻重复项",
        "difficulty": "简单",
        "tags": ["栈", "字符串"],
        "source": {
            "name": "LeetCode 1047 / 栈的应用",
            "url": "https://leetcode.cn/problems/remove-all-adjacent-duplicates-in-string/",
        },
        "statement": (
            "给定一个字符串 $s$，重复地**删除其中所有相邻且相同的字符对**，直到无法继续删除为止。\n\n"
            "返回最终得到的字符串。\n\n"
            "**注意**：删除操作可能产生新的相邻重复项，需要反复处理。"
            "例如 `abbaca` → 删 `bb` 得 `aaca` → 删 `aa` 得 `ca`。"
        ),
        "input_format": "一行一个字符串 $s$（$1 \\le |s| \\le 10^5$），仅含大小写英文字母。",
        "output_format": "一行，输出删除完毕后的字符串。若结果为空串，输出一个空行。",
        "constraints": ["1 ≤ |s| ≤ 10^5", "仅含大小写英文字母"],
        "samples": [
            {"input": "abbaca\n", "output": "ca\n",
             "explain": "删掉 `bb` 得到 `aaca`，再删掉 `aa` 得到 `ca`。"},
            {"input": "abba\n", "output": "\n",
             "explain": "删掉 `bb` 得到 `aa`，再删掉 `aa` 得到空串。"},
        ],
        "hint": (
            "**栈**：从左到右扫描字符。\n\n"
            "- 若栈非空且**栈顶字符与当前字符相同**，说明形成了一对相邻重复，弹出栈顶（相当于删除这对）；\n"
            "- 否则把当前字符压栈。\n\n"
            "扫描结束后，栈中剩下的字符按从栈底到栈顶的顺序就是答案。\n\n"
            "**为什么正确**：栈顶始终代表「处理完前缀后剩下的最后一个字符」，"
            "删除后新的栈顶自然与前缀的下一个字符比较，从而正确处理「删了又产生新重复」的情况。"
            "时间 $O(n)$，空间 $O(n)$。"
        ),
        "starter_code": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <cstring>\n\n"
                "char s[100005];\n"
                "char stk[100005];\n\n"
                "int main() {\n"
                "    if (!fgets(s, sizeof(s), stdin)) { printf(\"\\n\"); return 0; }\n"
                "    int len = (int)strlen(s);\n"
                "    while (len > 0 && (s[len - 1] == '\\n' || s[len - 1] == '\\r')) s[--len] = 0;\n\n"
                "    int top = 0;\n"
                "    // TODO: 用栈消除相邻重复项\n\n"
                "    stk[top] = 0;\n"
                "    printf(\"%s\\n\", stk);\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "tests": tests,
        "reference": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <cstring>\n\n"
                "char s[100005];\n"
                "char stk[100005];\n\n"
                "int main() {\n"
                "    if (!fgets(s, sizeof(s), stdin)) { printf(\"\\n\"); return 0; }\n"
                "    int len = (int)strlen(s);\n"
                "    while (len > 0 && (s[len - 1] == '\\n' || s[len - 1] == '\\r')) s[--len] = 0;\n\n"
                "    int top = 0;\n"
                "    for (int i = 0; i < len; ++i) {\n"
                "        if (top > 0 && stk[top - 1] == s[i]) --top;   // 消除一对\n"
                "        else stk[top++] = s[i];\n"
                "    }\n"
                "    stk[top] = 0;\n"
                "    printf(\"%s\\n\", stk);\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "time_limit": 2.0,
    }


def main() -> None:
    builders = [
        build_min_stack,
        build_daily_temperatures,
        build_rpn,
        build_remove_adjacent,
    ]
    for b in builders:
        prob = b()
        path = finalize(prob, OUT / f"{prob['id']}.json")
        total = sum(t["score"] for t in prob["tests"])
        print(f"生成 {prob['id']:38s} {len(prob['tests'])} 测试点, 总分 {total:3d}  -> {path.name}")


if __name__ == "__main__":
    main()
