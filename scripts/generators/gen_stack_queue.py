"""生成「栈与队列」分类的题目。

每道题的测试数据都由其参考实现（Python 版，与 C++ 参考解算法一致）生成，
从而保证输出与参考解严格一致。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from genkit import build_tests, finalize, numbers  # noqa: E402

OUT = ROOT / "oj" / "data" / "problems" / "02-stack-queue"


# ============================================================ 1. 括号匹配
def solve_brackets(text: str) -> str:
    """经典栈应用：判断括号序列是否合法。"""
    ls = text.strip("\n").split("\n")
    s = ls[0].strip() if ls else ""
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return "NO\n"
    return "YES\n" if not stack else "NO\n"


BRACKETS_SPECS = [
    ("样例 1（合法）", "()[]{}", 10),
    ("样例 2（非法）", "([)]", 10),
    ("空串", "", 10),
    ("单种括号", "((()))", 10),
    ("缺少右括号", "((", 15),
    ("多余的右括号", "())", 15),
    ("嵌套很深", "(" * 50 + ")" * 50, 15),
    ("交错但合法", "{[()]}[()]", 15),
]
# 修正：空串输入需要至少一个空行
BRACKETS_SPECS = [
    ("样例 1（合法）", "()[]{}", 10),
    ("样例 2（非法）", "([)]", 10),
    ("空串", "\n", 10),
    ("单种括号", "((()))", 10),
    ("缺少右括号", "((", 15),
    ("多余的右括号", "())", 15),
    ("嵌套很深", "(" * 50 + ")" * 50, 15),
    ("交错但合法", "{[()]}[()]", 15),
]

# ============================================================ 2. 单调栈：下一个更大元素
def solve_next_greater(text: str) -> str:
    nums = numbers(text)
    n, a = nums[0], nums[1:1 + nums[0]]
    res = [-1] * n
    stack = []  # 存下标，值单调递减
    for i, x in enumerate(a):
        while stack and a[stack[-1]] < x:
            res[stack.pop()] = x
        stack.append(i)
    return " ".join(map(str, res)) + "\n"


NGE_SPECS = [
    ("样例 1", "4\n2 1 2 4 3", 10),
    ("样例 2（递减）", "5\n5 4 3 2 1", 10),
    ("单元素", "1\n7", 10),
    ("全相同", "4\n3 3 3 3", 15),
    ("递增", "5\n1 2 3 4 5", 15),
    ("含负数", "6\n-3 -1 -2 0 -5 -4", 20),
    ("交替", "7\n1 3 2 4 3 5 4", 20),
]

# ============================================================ 3. 用栈实现队列
def solve_stack_queue(text: str) -> str:
    """模拟用两个栈实现队列的入队/出队操作。

    题面保证 pop/peek 只在非空队列上调用，因此这里不做空队列兜底输出。
    """
    ls = text.strip("\n").split("\n")
    q = int(ls[0]) if ls and ls[0].strip() else 0
    in_st, out_st = [], []
    out_lines = []
    for i in range(1, q + 1):
        parts = ls[i].split()
        if parts[0] == "push":
            in_st.append(int(parts[1]))
        elif parts[0] in ("pop", "peek"):
            # 惰性搬运：out 为空时把 in 全部倒过来
            if not out_st:
                while in_st:
                    out_st.append(in_st.pop())
            if parts[0] == "pop":
                out_lines.append(str(out_st.pop()))
            else:
                out_lines.append(str(out_st[-1]))
        elif parts[0] == "size":
            out_lines.append(str(len(in_st) + len(out_st)))
    return ("\n".join(out_lines) + "\n") if out_lines else "\n"


STACK_QUEUE_SPECS = [
    ("样例 1", "5\npush 1\npush 2\npeek\npop\nsize", 10),
    ("样例 2（连续入队弹出）", "6\npush 5\npop\npush 7\npop\npush 9\npeek", 10),
    ("入队后全出队", "6\npush 1\npush 2\npush 3\npop\npop\npop", 15),
    ("反复交替", "6\npush 1\npop\npush 2\npop\npush 3\npop", 15),
    ("部分出队再入队", "7\npush 1\npush 2\npop\npush 3\npeek\nsize\npop", 20),
    ("只有 size", "2\npush 5\nsize", 10),
    ("大量入队后查询", "6\npush 9\npush 8\npush 7\nsize\npeek\npop", 20),
]


def build_brackets() -> dict:
    tests = build_tests(BRACKETS_SPECS, solve_brackets)
    return {
        "id": "stack-bracket-match",
        "title": "括号匹配",
        "difficulty": "入门",
        "tags": ["栈", "字符串", "括号匹配"],
        "source": {
            "name": "LeetCode 20 / 栈的经典应用",
            "url": "https://leetcode.cn/problems/valid-parentheses/",
        },
        "statement": (
            "给定一个只包含字符 `(`、`)`、`[`、`]`、`{`、`}` 的字符串 $s$，"
            "判断它是否是**合法的括号序列**。\n\n"
            "合法序列的定义：\n"
            "1. 左括号必须用**相同类型**的右括号闭合；\n"
            "2. 左括号必须以**正确的顺序**闭合。\n\n"
            "这是栈（Stack）最经典的应用场景。"
        ),
        "input_format": "一行一个字符串 $s$（$0 \\le |s| \\le 10^5$），仅包含上述六种括号字符。$s$ 可能为空串。",
        "output_format": "一行，若 $s$ 是合法括号序列输出 `YES`，否则输出 `NO`。",
        "constraints": ["0 ≤ |s| ≤ 10^5", "仅含 ()[]{} 六种字符"],
        "samples": [
            {"input": "()[]{}\n", "output": "YES\n", "explain": "三种括号各自配对，整体合法。"},
            {"input": "([)]\n", "output": "NO\n", "explain": "`(` 被 `]` 关闭，顺序错误。"},
        ],
        "hint": (
            "**核心思路**：遇到左括号就压栈；遇到右括号时，检查栈顶是否为对应的左括号——"
            "是则弹出，不是（或栈为空）则说明非法。\n\n"
            "扫描结束后，栈必须为空才算合法。时间 $O(n)$，空间 $O(n)$。"
        ),
        "starter_code": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <cstring>\n\n"
                "char s[100005];\n"
                "char stk[100005];\n\n"
                "int main() {\n"
                "    if (!fgets(s, sizeof(s), stdin)) { printf(\"YES\\n\"); return 0; }\n"
                "    int top = 0;\n"
                "    int len = (int)strlen(s);\n"
                "    for (int i = 0; i < len; ++i) {\n"
                "        char c = s[i];\n"
                "        // TODO: 用栈判断括号序列是否合法\n"
                "    }\n"
                "    printf(\"%s\\n\", top == 0 ? \"YES\" : \"NO\");\n"
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
                "    if (!fgets(s, sizeof(s), stdin)) { printf(\"YES\\n\"); return 0; }\n"
                "    int top = 0;\n"
                "    int len = (int)strlen(s);\n"
                "    int ok = 1;\n"
                "    for (int i = 0; i < len; ++i) {\n"
                "        char c = s[i];\n"
                "        if (c == '(' || c == '[' || c == '{') {\n"
                "            stk[top++] = c;\n"
                "        } else if (c == ')' || c == ']' || c == '}') {\n"
                "            char need = (c == ')') ? '(' : (c == ']' ? '[' : '{');\n"
                "            if (top == 0 || stk[top - 1] != need) { ok = 0; break; }\n"
                "            --top;\n"
                "        }\n"
                "    }\n"
                "    if (top != 0) ok = 0;\n"
                "    printf(\"%s\\n\", ok ? \"YES\" : \"NO\");\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "time_limit": 2.0,
    }


def build_nge() -> dict:
    tests = build_tests(NGE_SPECS, solve_next_greater)
    return {
        "id": "stack-next-greater-element",
        "title": "下一个更大元素",
        "difficulty": "中等",
        "tags": ["栈", "单调栈"],
        "source": {
            "name": "LeetCode 739 / 496 单调栈经典",
            "url": "https://leetcode.cn/problems/daily-temperatures/",
        },
        "statement": (
            "给定一个长度为 $n$ 的整数数组 $a_1, a_2, \\dots, a_n$。\n\n"
            "对每个位置 $i$，求**它右侧第一个比 $a_i$ 大的元素**：即最小的 $j > i$ 满足 $a_j > a_i$。"
            "若不存在这样的 $j$，则答案为 $-1$。\n\n"
            "请输出这 $n$ 个答案。\n\n"
            "**要求：时间复杂度 $O(n)$**。朴素双重循环是 $O(n^2)$，在 $n = 2 \\times 10^5$ 时会超时。"
        ),
        "input_format": "第一行一个整数 $n$（$1 \\le n \\le 2 \\times 10^5$）。\n\n第二行 $n$ 个整数 $a_i$（$|a_i| \\le 10^9$）。",
        "output_format": "一行 $n$ 个整数，依次为每个位置的答案，以空格分隔。",
        "constraints": ["1 ≤ n ≤ 2×10^5", "|a_i| ≤ 10^9", "要求 O(n) 算法"],
        "samples": [
            {"input": "4\n2 1 2 4\n", "output": "4 2 4 -1\n",
             "explain": "a_1=2 右侧第一个更大的是 4；a_2=1 右侧第一个更大的是 2；a_3=2 右侧第一个更大的是 4；a_4=4 无更大值，输出 -1。"},
            {"input": "5\n5 4 3 2 1\n", "output": "-1 -1 -1 -1 -1\n",
             "explain": "严格递减，每个元素右侧都没有更大的值。"},
        ],
        "hint": (
            "**单调栈**：维护一个栈，栈中存**下标**，对应的值从栈底到栈顶**单调递减**。\n\n"
            "从左到右扫描，对当前元素 $a_i$：当栈非空且栈顶元素的值 $< a_i$ 时，"
            "栈顶元素的答案就是 $a_i$，弹出它；重复此过程，然后把 $i$ 压栈。\n\n"
            "每个元素最多入栈、出栈各一次，因此总时间 $O(n)$。"
        ),
        "starter_code": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <vector>\n\n"
                "int main() {\n"
                "    int n;\n"
                "    scanf(\"%d\", &n);\n"
                "    std::vector<long long> a(n);\n"
                "    for (int i = 0; i < n; ++i) scanf(\"%lld\", &a[i]);\n\n"
                "    std::vector<long long> res(n, -1);\n"
                "    std::vector<int> stk;\n"
                "    // TODO: 单调栈求解\n\n"
                "    for (int i = 0; i < n; ++i) {\n"
                "        if (i) printf(\" \");\n"
                "        printf(\"%lld\", res[i]);\n"
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
                "    std::vector<long long> a(n);\n"
                "    for (int i = 0; i < n; ++i) scanf(\"%lld\", &a[i]);\n\n"
                "    std::vector<long long> res(n, -1);\n"
                "    std::vector<int> stk;\n"
                "    for (int i = 0; i < n; ++i) {\n"
                "        while (!stk.empty() && a[stk.back()] < a[i]) {\n"
                "            res[stk.back()] = a[i];\n"
                "            stk.pop_back();\n"
                "        }\n"
                "        stk.push_back(i);\n"
                "    }\n"
                "    for (int i = 0; i < n; ++i) {\n"
                "        if (i) printf(\" \");\n"
                "        printf(\"%lld\", res[i]);\n"
                "    }\n"
                "    printf(\"\\n\");\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "time_limit": 2.0,
    }


def build_stack_queue() -> dict:
    tests = build_tests(STACK_QUEUE_SPECS, solve_stack_queue)
    return {
        "id": "queue-with-two-stacks",
        "title": "用两个栈实现队列",
        "difficulty": "简单",
        "tags": ["栈", "队列", "设计"],
        "source": {
            "name": "LeetCode 232 / 剑指 Offer 09",
            "url": "https://leetcode.cn/problems/implement-queue-using-stacks/",
        },
        "statement": (
            "请用**两个栈**实现一个队列，支持以下操作：\n\n"
            "- `push x`：把元素 $x$ 加入队尾；\n"
            "- `pop`：删除并返回队首元素；\n"
            "- `peek`：返回队首元素（不删除）；\n"
            "- `size`：返回当前队列中元素个数。\n\n"
            "要求所有操作的**均摊时间复杂度为 $O(1)$**。"
        ),
        "input_format": (
            "第一行一个整数 $q$（$1 \\le q \\le 2 \\times 10^5$），表示操作总数。\n\n"
            "接下来 $q$ 行，每行一个操作，格式如上所述。其中 $|x| \\le 10^9$。\n\n"
            "**保证队列非空时才会调用 `pop` / `peek`**，因此无需处理越界情况。"
        ),
        "output_format": "对每个 `pop`、`peek`、`size` 操作，输出一行对应的结果。",
        "constraints": ["1 ≤ q ≤ 2×10^5", "|x| ≤ 10^9", "pop/peek 仅在非空队列上调用"],
        "samples": [
            {"input": "5\npush 1\npush 2\npeek\npop\nsize\n", "output": "1\n1\n1\n",
             "explain": "依次执行：入队 1、入队 2；`peek` 返回队首 1；`pop` 删掉队首 1；`size` 返回剩余的 1 个元素。"},
            {"input": "6\npush 5\npop\npush 7\npop\npush 9\npeek\n", "output": "5\n7\n9\n",
             "explain": "元素始终先进先出：5 被弹出，7 被弹出，最后队首是 9。"},
        ],
        "hint": (
            "设两个栈为 `in` 和 `out`：\n\n"
            "- `push`：直接压入 `in`；\n"
            "- `pop` / `peek`：若 `out` 为空，把 `in` 中所有元素依次弹出并压入 `out`"
            "（这样顺序就反过来了，`out` 的栈顶即为队首），然后操作 `out`。\n\n"
            "**均摊分析**：每个元素最多被搬运一次，因此 $q$ 次操作总共 $O(q)$。"
        ),
        "starter_code": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <vector>\n"
                "#include <cstring>\n\n"
                "// TODO: 定义两个栈，实现队列\n\n"
                "int main() {\n"
                "    int q;\n"
                "    scanf(\"%d\", &q);\n"
                "    for (int i = 0; i < q; ++i) {\n"
                "        char op[16];\n"
                "        scanf(\"%s\", op);\n"
                "        if (strcmp(op, \"push\") == 0) {\n"
                "            long long x;\n"
                "            scanf(\"%lld\", &x);\n"
                "            // TODO\n"
                "        } else if (strcmp(op, \"pop\") == 0) {\n"
                "            // TODO\n"
                "        } else if (strcmp(op, \"peek\") == 0) {\n"
                "            // TODO\n"
                "        } else if (strcmp(op, \"size\") == 0) {\n"
                "            // TODO\n"
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
                "#include <cstring>\n\n"
                "std::vector<long long> in, out;\n\n"
                "int main() {\n"
                "    int q;\n"
                "    scanf(\"%d\", &q);\n"
                "    for (int i = 0; i < q; ++i) {\n"
                "        char op[16];\n"
                "        scanf(\"%s\", op);\n"
                "        if (strcmp(op, \"push\") == 0) {\n"
                "            long long x;\n"
                "            scanf(\"%lld\", &x);\n"
                "            in.push_back(x);\n"
                "        } else if (strcmp(op, \"pop\") == 0) {\n"
                "            if (out.empty()) {\n"
                "                while (!in.empty()) { out.push_back(in.back()); in.pop_back(); }\n"
                "            }\n"
                "            printf(\"%lld\\n\", out.back());\n"
                "            out.pop_back();\n"
                "        } else if (strcmp(op, \"peek\") == 0) {\n"
                "            if (out.empty()) {\n"
                "                while (!in.empty()) { out.push_back(in.back()); in.pop_back(); }\n"
                "            }\n"
                "            printf(\"%lld\\n\", out.back());\n"
                "        } else if (strcmp(op, \"size\") == 0) {\n"
                "            printf(\"%d\\n\", (int)(in.size() + out.size()));\n"
                "        }\n"
                "    }\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "time_limit": 2.0,
    }


def main() -> None:
    builders = [build_brackets, build_nge, build_stack_queue]
    for b in builders:
        prob = b()
        path = finalize(prob, OUT / f"{prob['id']}.json")
        total = sum(t["score"] for t in prob["tests"])
        print(f"生成 {prob['id']:32s} {len(prob['tests'])} 测试点, 总分 {total}  -> {path.name}")


if __name__ == "__main__":
    main()
