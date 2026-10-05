"""生成「数组与链表」分类的第二批题目。

测试数据全部由参考实现（Python，与 C++ 参考解算法一致）生成。
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from genkit import build_tests, finalize, numbers  # noqa: E402

OUT = ROOT / "oj" / "data" / "problems" / "01-array-linkedlist"


# ============================================================ 1. 有序数组去重
def solve_remove_duplicates(text: str) -> str:
    """双指针原地去重：slow 指向已确定的最后一个唯一元素。"""
    nums = numbers(text)
    n, a = nums[0], nums[1:1 + nums[0]]
    if n == 0:
        return "0\n\n"
    slow = 0
    for fast in range(1, n):
        if a[fast] != a[slow]:
            slow += 1
            a[slow] = a[fast]
    k = slow + 1
    return f"{k}\n" + " ".join(map(str, a[:k])) + "\n"


RD_SPECS = [
    ("样例 1", "5\n1 1 2 2 3", 10),
    ("样例 2（无重复）", "4\n1 2 3 4", 10),
    ("全相同", "5\n7 7 7 7 7", 15),
    ("单元素", "1\n5", 10),
    ("含负数", "6\n-3 -3 -1 0 0 2", 15),
    ("仅两种值", "8\n1 1 1 1 2 2 2 2", 15),
    ("长重复段", "10\n1 1 1 2 2 3 3 3 3 4", 25),
]


def build_remove_duplicates() -> dict:
    tests = build_tests(RD_SPECS, solve_remove_duplicates)
    return {
        "id": "array-remove-duplicates",
        "title": "有序数组去重",
        "difficulty": "入门",
        "tags": ["数组", "双指针", "原地"],
        "source": {
            "name": "LeetCode 26 / 双指针原地压缩",
            "url": "https://leetcode.cn/problems/remove-duplicates-from-sorted-array/",
        },
        "statement": (
            "给定一个**非递减**数组 $a$，请**原地**删除重复元素，使得每个元素只出现一次，"
            "并返回去重后的新长度 $k$。\n\n"
            "去重后的结果应放在数组的**前 $k$ 个位置**，其余位置的内容无关紧要。\n\n"
            "**要求：空间复杂度 $O(1)$**，不能额外开一个数组。"
        ),
        "input_format": "第一行一个整数 $n$（$0 \\le n \\le 2 \\times 10^5$）。\n\n第二行 $n$ 个整数 $a_i$，保证非递减（$|a_i| \\le 10^9$）。当 $n=0$ 时第二行为空行。",
        "output_format": "第一行输出新长度 $k$。\n\n第二行输出去重后的前 $k$ 个元素，以空格分隔。若 $k=0$ 则输出一个空行。",
        "constraints": ["0 ≤ n ≤ 2×10^5", "|a_i| ≤ 10^9", "数组非递减", "要求 O(1) 额外空间"],
        "samples": [
            {"input": "5\n1 1 2 2 3\n", "output": "3\n1 2 3\n",
             "explain": "去重后得到 `[1, 2, 3]`，新长度为 3。"},
            {"input": "5\n7 7 7 7 7\n", "output": "1\n7\n",
             "explain": "所有元素相同，去重后只剩一个 `7`。"},
        ],
        "hint": (
            "**读写双指针**：`slow` 指向「已确认的唯一序列」的末尾，`fast` 负责扫描。\n\n"
            "当 `a[fast] != a[slow]` 时，说明遇到了新值，把 `slow` 前移一位并写入 `a[fast]`。\n\n"
            "因为数组已经有序，相同的元素必然相邻，所以只需比较 `a[fast]` 与 `a[slow]`。\n"
            "时间 $O(n)$，空间 $O(1)$。"
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
                "    // TODO: 用读写双指针原地去重\n"
                "    int k = n;\n\n"
                "    printf(\"%d\\n\", k);\n"
                "    for (int i = 0; i < k; ++i) {\n"
                "        if (i) printf(\" \");\n"
                "        printf(\"%lld\", a[i]);\n"
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
                "    int k = 0;\n"
                "    for (int fast = 0; fast < n; ++fast) {\n"
                "        if (k == 0 || a[fast] != a[k - 1]) {\n"
                "            a[k++] = a[fast];\n"
                "        }\n"
                "    }\n\n"
                "    printf(\"%d\\n\", k);\n"
                "    for (int i = 0; i < k; ++i) {\n"
                "        if (i) printf(\" \");\n"
                "        printf(\"%lld\", a[i]);\n"
                "    }\n"
                "    printf(\"\\n\");\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "time_limit": 2.0,
    }


# ============================================================ 2. 移动零
def solve_move_zeroes(text: str) -> str:
    """读写指针：把非零元素依次写到前面，剩余位置补零。"""
    nums = numbers(text)
    n, a = nums[0], nums[1:1 + nums[0]]
    slow = 0
    for fast in range(n):
        if a[fast] != 0:
            a[slow] = a[fast]
            slow += 1
    for i in range(slow, n):
        a[i] = 0
    return " ".join(map(str, a)) + "\n"


MZ_SPECS = [
    ("样例 1", "5\n0 1 0 3 12", 10),
    ("样例 2（无零）", "4\n1 2 3 4", 10),
    ("全零", "3\n0 0 0", 15),
    ("零在前", "4\n0 0 1 2", 15),
    ("零在后", "4\n1 2 0 0", 15),
    ("含负数", "6\n-1 0 -2 0 -3 0", 20),
    ("交替", "7\n0 1 0 2 0 3 0", 25),
]


def build_move_zeroes() -> dict:
    tests = build_tests(MZ_SPECS, solve_move_zeroes)
    return {
        "id": "array-move-zeroes",
        "title": "移动零",
        "difficulty": "入门",
        "tags": ["数组", "双指针", "原地"],
        "source": {
            "name": "LeetCode 283 / 读写指针",
            "url": "https://leetcode.cn/problems/move-zeroes/",
        },
        "statement": (
            "给定一个整数数组 $a$，请将所有 $0$ 移动到数组的**末尾**，同时保持**非零元素的相对顺序**。\n\n"
            "**要求**：必须**原地**操作，不能复制整个数组；空间复杂度 $O(1)$。"
        ),
        "input_format": "第一行一个整数 $n$（$0 \\le n \\le 2 \\times 10^5$）。\n\n第二行 $n$ 个整数 $a_i$（$|a_i| \\le 10^9$）。当 $n=0$ 时第二行为空行。",
        "output_format": "一行 $n$ 个整数，为移动零之后的数组，以空格分隔。若 $n=0$ 输出一个空行。",
        "constraints": ["0 ≤ n ≤ 2×10^5", "|a_i| ≤ 10^9", "要求 O(1) 额外空间"],
        "samples": [
            {"input": "5\n0 1 0 3 12\n", "output": "1 3 12 0 0\n",
             "explain": "非零元素 `1 3 12` 保持原顺序移到前面，两个零移到末尾。"},
            {"input": "3\n0 0 0\n", "output": "0 0 0\n",
             "explain": "全是零，移动后不变。"},
        ],
        "hint": (
            "**读写双指针**：`slow` 指向「下一个非零元素应该放的位置」，`fast` 负责扫描。\n\n"
            "遇到非零元素就写到 `a[slow]` 并把 `slow` 前移；扫描结束后，把 `slow` 到末尾的"
            "位置全部置为 $0$。\n\n"
            "时间 $O(n)$，空间 $O(1)$。"
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
                "    // TODO: 用读写双指针把非零元素前移，末尾补零\n\n"
                "    for (int i = 0; i < n; ++i) {\n"
                "        if (i) printf(\" \");\n"
                "        printf(\"%lld\", a[i]);\n"
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
                "    int slow = 0;\n"
                "    for (int fast = 0; fast < n; ++fast) {\n"
                "        if (a[fast] != 0) a[slow++] = a[fast];\n"
                "    }\n"
                "    while (slow < n) a[slow++] = 0;\n\n"
                "    for (int i = 0; i < n; ++i) {\n"
                "        if (i) printf(\" \");\n"
                "        printf(\"%lld\", a[i]);\n"
                "    }\n"
                "    printf(\"\\n\");\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "time_limit": 2.0,
    }


# ============================================================ 3. 链表的中间结点
def solve_middle_node(text: str) -> str:
    """快慢指针：快指针走两步，慢指针走一步。偶数个时返回第二个中间结点。"""
    nums = numbers(text)
    n, a = nums[0], nums[1:1 + nums[0]]
    if n == 0:
        return "\n"
    slow = 0
    fast = 0
    while fast + 1 < n:
        slow += 1
        fast += 2
    return f"{a[slow]}\n"


MN_SPECS = [
    ("样例 1（奇数）", "5\n1 2 3 4 5", 10),
    ("样例 2（偶数）", "6\n1 2 3 4 5 6", 10),
    ("单节点", "1\n42", 10),
    ("两节点", "2\n1 2", 15),
    ("三节点", "3\n7 8 9", 15),
    ("含负数", "7\n-3 -2 -1 0 1 2 3", 20),
    ("四节点", "4\n10 20 30 40", 20),
]


def build_middle_node() -> dict:
    tests = build_tests(MN_SPECS, solve_middle_node)
    return {
        "id": "list-middle-node",
        "title": "链表的中间结点",
        "difficulty": "入门",
        "tags": ["链表", "快慢指针"],
        "source": {
            "name": "LeetCode 876 / 快慢指针",
            "url": "https://leetcode.cn/problems/middle-of-the-linked-list/",
        },
        "statement": (
            "给定一个单链表的头结点，请返回它的**中间结点**。\n\n"
            "若有**两个**中间结点（即链表长度为偶数），则返回**第二个**中间结点。\n\n"
            "**要求**：只能遍历链表一次，空间复杂度 $O(1)$。"
        ),
        "input_format": "第一行一个整数 $n$（$0 \\le n \\le 2 \\times 10^5$），表示链表长度。\n\n第二行 $n$ 个整数，按从头到尾的顺序给出节点值 $v_i$（$|v_i| \\le 10^9$）。当 $n=0$ 时第二行为空行。",
        "output_format": "一行，输出中间结点的值。若 $n=0$ 输出一个空行。",
        "constraints": ["0 ≤ n ≤ 2×10^5", "|v_i| ≤ 10^9", "只能遍历一次", "要求 O(1) 空间"],
        "samples": [
            {"input": "5\n1 2 3 4 5\n", "output": "3\n",
             "explain": "长度为 5（奇数），中间结点是第 3 个，值为 3。"},
            {"input": "6\n1 2 3 4 5 6\n", "output": "4\n",
             "explain": "长度为 6（偶数），有两个中间结点（3 和 4），返回第二个，即 4。"},
        ],
        "hint": (
            "**快慢指针**：`slow` 每次走 1 步，`fast` 每次走 2 步。\n\n"
            "当 `fast` 到达链表末尾时，`slow` 恰好走过一半的路程，正好停在中间结点。\n\n"
            "注意**偶数长度要返回第二个中间结点**：循环条件写成「`fast` 和 `fast->next` 都非空时"
            "才继续前进」，这样偶数长度下 `slow` 会多走一步，落到第二个中间结点上。\n\n"
            "时间 $O(n)$，空间 $O(1)$。"
        ),
        "starter_code": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <vector>\n\n"
                "// 本题以数组形式给出链表，请用快慢指针思路求解\n"
                "int main() {\n"
                "    int n;\n"
                "    scanf(\"%d\", &n);\n"
                "    std::vector<long long> v(n);\n"
                "    for (int i = 0; i < n; ++i) scanf(\"%lld\", &v[i]);\n\n"
                "    if (n == 0) { printf(\"\\n\"); return 0; }\n\n"
                "    // TODO: 快慢指针找中间结点\n"
                "    int mid = 0;\n"
                "    printf(\"%lld\\n\", v[mid]);\n"
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
                "    std::vector<long long> v(n);\n"
                "    for (int i = 0; i < n; ++i) scanf(\"%lld\", &v[i]);\n\n"
                "    if (n == 0) { printf(\"\\n\"); return 0; }\n\n"
                "    int slow = 0, fast = 0;\n"
                "    while (fast + 1 < n) {      // fast 还能走两步\n"
                "        slow += 1;\n"
                "        fast += 2;\n"
                "    }\n"
                "    printf(\"%lld\\n\", v[slow]);\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "time_limit": 2.0,
    }


# ============================================================ 4. 多数元素
def solve_majority(text: str) -> str:
    """Boyer-Moore 投票：候选者计数，抵消即换人。"""
    nums = numbers(text)
    n, a = nums[0], nums[1:1 + nums[0]]
    cand = a[0]
    cnt = 0
    for x in a:
        if cnt == 0:
            cand = x
            cnt = 1
        elif x == cand:
            cnt += 1
        else:
            cnt -= 1
    return f"{cand}\n"


MAJ_SPECS = [
    ("样例 1", "3\n3 2 3", 10),
    ("样例 2", "7\n2 2 1 1 1 2 2", 10),
    ("单元素", "1\n5", 10),
    ("全相同", "5\n4 4 4 4 4", 15),
    ("多数在末尾", "7\n1 2 1 3 1 4 1", 20),
    ("含负数", "9\n-1 -1 -1 -1 -1 2 2 3 3", 20),
    ("恰好过半再加一", "6\n7 7 7 7 1 2", 25),
]


def build_majority() -> dict:
    tests = build_tests(MAJ_SPECS, solve_majority)
    return {
        "id": "array-majority-element",
        "title": "多数元素（投票法）",
        "difficulty": "简单",
        "tags": ["数组", "Boyer-Moore", "贪心"],
        "source": {
            "name": "LeetCode 169 / Boyer-Moore 投票算法",
            "url": "https://leetcode.cn/problems/majority-element/",
        },
        "statement": (
            "给定一个长度为 $n$ 的数组 $a$，求其中的**多数元素**。\n\n"
            "多数元素的定义是：出现次数**严格大于** $\\lfloor n/2 \\rfloor$ 的元素。\n\n"
            "题目**保证**数组中一定存在多数元素。\n\n"
            "**进阶要求**：请设计 $O(n)$ 时间、$O(1)$ 空间的算法。"
        ),
        "input_format": "第一行一个整数 $n$（$1 \\le n \\le 2 \\times 10^5$）。\n\n第二行 $n$ 个整数 $a_i$（$|a_i| \\le 10^9$）。保证存在多数元素。",
        "output_format": "一行，输出多数元素的值。",
        "constraints": ["1 ≤ n ≤ 2×10^5", "|a_i| ≤ 10^9", "保证存在多数元素", "要求 O(n) 时间 / O(1) 空间"],
        "samples": [
            {"input": "3\n3 2 3\n", "output": "3\n",
             "explain": "3 出现 2 次，超过 ⌊3/2⌋=1，是多数元素。"},
            {"input": "7\n2 2 1 1 1 2 2\n", "output": "2\n",
             "explain": "2 出现 4 次，超过 ⌊7/2⌋=3，是多数元素。"},
        ],
        "hint": (
            "**Boyer-Moore 投票算法**：维护一个候选者 `cand` 和一个计数器 `cnt`。\n\n"
            "- 若 `cnt == 0`，把当前元素设为候选者，`cnt = 1`；\n"
            "- 若当前元素等于候选者，`cnt += 1`；\n"
            "- 否则 `cnt -= 1`（相当于「一换一抵消」）。\n\n"
            "**直觉**：多数元素出现次数超过一半，即使把它和其他所有元素两两抵消，"
            "最后剩下的仍然是它。时间 $O(n)$，空间 $O(1)$。"
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
                "    // TODO: Boyer-Moore 投票算法\n"
                "    long long cand = a[0];\n\n"
                "    printf(\"%lld\\n\", cand);\n"
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
                "    long long cand = a[0];\n"
                "    int cnt = 0;\n"
                "    for (int i = 0; i < n; ++i) {\n"
                "        if (cnt == 0) { cand = a[i]; cnt = 1; }\n"
                "        else if (a[i] == cand) ++cnt;\n"
                "        else --cnt;\n"
                "    }\n"
                "    printf(\"%lld\\n\", cand);\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "time_limit": 2.0,
    }


def main() -> None:
    builders = [
        build_remove_duplicates,
        build_move_zeroes,
        build_middle_node,
        build_majority,
    ]
    for b in builders:
        prob = b()
        path = finalize(prob, OUT / f"{prob['id']}.json")
        total = sum(t["score"] for t in prob["tests"])
        print(f"生成 {prob['id']:32s} {len(prob['tests'])} 测试点, 总分 {total:3d}  -> {path.name}")


if __name__ == "__main__":
    main()
