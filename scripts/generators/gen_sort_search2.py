"""生成「排序与查找」分类的第二批题目。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from genkit import build_tests, finalize, numbers  # noqa: E402

OUT = ROOT / "oj" / "data" / "problems" / "07-sort-search"


def _lines(text: str):
    return text.strip("\n").split("\n")


# ============================================================ 1. 搜索旋转排序数组
def solve_rotated(text: str) -> str:
    """二分：先判断哪一半有序，再决定收缩方向。"""
    ls = _lines(text)
    first = numbers(ls[0])
    n = first[0]
    a = first[1:1 + n]
    target = int(ls[1].strip())

    lo, hi = 0, n - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == target:
            return f"{mid}\n"
        if a[lo] <= a[mid]:                  # 左半有序
            if a[lo] <= target < a[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:                                 # 右半有序
            if a[mid] < target <= a[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return "-1\n"


ROT_SPECS = [
    ("样例 1", "7 4 5 6 7 0 1 2\n0", 10),
    ("样例 2（未找到）", "7 4 5 6 7 0 1 2\n3", 10),
    ("未旋转", "5 1 2 3 4 5\n3", 10),
    ("单元素命中", "1 1\n1", 15),
    ("单元素未命中", "1 1\n0", 15),
    ("旋转在末尾", "5 5 1 2 3 4\n4", 20),
    ("两元素", "2 3 1\n1", 20),
]


def build_rotated() -> dict:
    tests = build_tests(ROT_SPECS, solve_rotated)
    return {
        "id": "search-rotated-array",
        "title": "搜索旋转排序数组",
        "difficulty": "中等",
        "tags": ["二分查找", "数组"],
        "source": {
            "name": "LeetCode 33 / 二分变体",
            "url": "https://leetcode.cn/problems/search-in-rotated-sorted-array/",
        },
        "statement": (
            "给定一个**严格递增**的数组，它经过了**一次旋转**"
            "（即把前面若干元素整体移到末尾，例如 `[0,1,2,4,5,6,7]` 旋转后可能是 `[4,5,6,7,0,1,2]`）。\n\n"
            "再给定一个目标值 $target$，请在数组中查找它，返回其**下标**；若不存在则返回 $-1$。\n\n"
            "**要求：时间复杂度 $O(\\log n)$**，不能直接线性扫描。\n\n"
            "数组中**没有重复元素**。"
        ),
        "input_format": (
            "第一行一个整数 $n$ 后跟 $n$ 个整数（$1 \\le n \\le 10^5$），为旋转后的数组，"
            "保证由严格递增数组旋转一次得到。\n\n"
            "第二行一个整数 $target$（$|target| \\le 10^9$）。"
        ),
        "output_format": "一行，输出 $target$ 的下标；若不存在则输出 $-1$。",
        "constraints": ["1 ≤ n ≤ 10^5", "元素严格递增后旋转一次", "无重复元素", "要求 O(log n)"],
        "samples": [
            {"input": "7\n4 5 6 7 0 1 2\n0\n", "output": "4\n",
             "explain": "0 在下标 4 处。"},
            {"input": "7\n4 5 6 7 0 1 2\n3\n", "output": "-1\n",
             "explain": "数组中不存在 3。"},
        ],
        "hint": (
            "**二分的核心观察**：把旋转数组从中间切开，**至少有一半是完全有序的**。\n\n"
            "每轮取 `mid`，比较 `a[lo]` 与 `a[mid]`：\n\n"
            "- 若 `a[lo] <= a[mid]`：说明**左半段有序**。再看 $target$ 是否落在 "
            "`[a[lo], a[mid])` 区间内——在就收缩到左半，否则去右半；\n"
            "- 否则**右半段有序**。看 $target$ 是否落在 `(a[mid], a[hi]]` 内——"
            "在就去右半，否则去左半。\n\n"
            "每次都能排除一半，因此是 $O(\\log n)$。\n\n"
            "> **易错点**：判断区间时边界开闭要一致。上面用的是"
            "「左闭右开」`[a[lo], a[mid])` 和「左开右闭」`(a[mid], a[hi]]`，"
            "因为 `a[mid] == target` 已经在前面单独判断过了。"
        ),
        "starter_code": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <vector>\n\n"
                "int main() {\n"
                "    int n;\n"
                "    scanf(\"%d\", &n);\n"
                "    std::vector<long long> a(n);\n"
                "    for (int i = 0; i < n; ++i) scanf(\"%lld\", &a[i]);\n"
                "    long long target;\n"
                "    scanf(\"%lld\", &target);\n\n"
                "    int lo = 0, hi = n - 1, ans = -1;\n"
                "    // TODO: 二分查找（先判断哪一半有序）\n\n"
                "    printf(\"%d\\n\", ans);\n"
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
                "    for (int i = 0; i < n; ++i) scanf(\"%lld\", &a[i]);\n"
                "    long long target;\n"
                "    scanf(\"%lld\", &target);\n\n"
                "    int lo = 0, hi = n - 1, ans = -1;\n"
                "    while (lo <= hi) {\n"
                "        int mid = lo + (hi - lo) / 2;\n"
                "        if (a[mid] == target) { ans = mid; break; }\n"
                "        if (a[lo] <= a[mid]) {                 // 左半有序\n"
                "            if (a[lo] <= target && target < a[mid]) hi = mid - 1;\n"
                "            else                                    lo = mid + 1;\n"
                "        } else {                               // 右半有序\n"
                "            if (a[mid] < target && target <= a[hi]) lo = mid + 1;\n"
                "            else                                    hi = mid - 1;\n"
                "        }\n"
                "    }\n"
                "    printf(\"%d\\n\", ans);\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "time_limit": 2.0,
    }


# ============================================================ 2. 颜色分类
def solve_color_sort(text: str) -> str:
    """三路划分（荷兰国旗）：[0,low) 是 0，(low,i) 是 1，(high,n) 是 2。"""
    nums = numbers(text)
    n, a = nums[0], nums[1:1 + nums[0]]
    low, i, high = 0, 0, n - 1
    while i <= high:
        if a[i] == 0:
            a[low], a[i] = a[i], a[low]
            low += 1
            i += 1
        elif a[i] == 1:
            i += 1
        else:
            a[i], a[high] = a[high], a[i]
            high -= 1
    return " ".join(map(str, a)) + "\n"


CS_SPECS = [
    ("样例 1", "6\n2 0 2 1 1 0", 10),
    ("样例 2（全 0）", "3\n0 0 0", 10),
    ("全 1", "3\n1 1 1", 10),
    ("全 2", "3\n2 2 2", 15),
    ("已有序", "6\n0 0 1 1 2 2", 15),
    ("逆序", "6\n2 2 1 1 0 0", 20),
    ("单元素", "1\n1", 20),
]


def build_color_sort() -> dict:
    tests = build_tests(CS_SPECS, solve_color_sort)
    return {
        "id": "sort-color-sort",
        "title": "颜色分类（三路划分）",
        "difficulty": "中等",
        "tags": ["数组", "双指针", "三路划分", "荷兰国旗"],
        "source": {
            "name": "LeetCode 75 / 荷兰国旗问题",
            "url": "https://leetcode.cn/problems/sort-colors/",
        },
        "statement": (
            "给定一个只包含 $0$、$1$、$2$ 的数组，请将它**原地排序**，"
            "使得所有 $0$ 在前、$1$ 居中、$2$ 在后。\n\n"
            "**要求**：\n"
            "- 不能使用库函数排序；\n"
            "- 只能遍历**一趟**；\n"
            "- 空间复杂度 $O(1)$。"
        ),
        "input_format": "第一行一个整数 $n$（$1 \\le n \\le 10^5$）。\n\n第二行 $n$ 个整数，每个为 $0$、$1$ 或 $2$。",
        "output_format": "一行 $n$ 个整数，为排序后的数组，以空格分隔。",
        "constraints": ["1 ≤ n ≤ 10^5", "元素仅为 0/1/2", "要求一趟遍历", "要求 O(1) 空间"],
        "samples": [
            {"input": "6\n2 0 2 1 1 0\n", "output": "0 0 1 1 2 2\n",
             "explain": "所有 0 移到前面，1 居中，2 移到最后。"},
            {"input": "6\n2 2 1 1 0 0\n", "output": "0 0 1 1 2 2\n",
             "explain": "完全逆序的输入也能在一趟内整理好。"},
        ],
        "hint": (
            "**荷兰国旗问题（三路划分）**：用三个指针把数组分成四段：\n\n"
            "```\n"
            "[0, low)  → 全是 0\n"
            "[low, i)  → 全是 1\n"
            "[i, high] → 待处理\n"
            "(high, n) → 全是 2\n"
            "```\n\n"
            "每轮看 `a[i]`：\n"
            "- 是 $0$：与 `a[low]` 交换，`low++`、`i++`；\n"
            "- 是 $1$：`i++`（已经在正确区域）；\n"
            "- 是 $2$：与 `a[high]` 交换，`high--`（**`i` 不动**！）。\n\n"
            "循环条件是 `i <= high`。时间 $O(n)$，空间 $O(1)$。\n\n"
            "> **最关键的易错点**：处理 $2$ 时**不能 `i++`**。"
            "因为从 `high` 换过来的元素还**没有被检查过**，"
            "必须留在原地等下一轮处理，否则会漏掉它。"
        ),
        "starter_code": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <vector>\n\n"
                "int main() {\n"
                "    int n;\n"
                "    scanf(\"%d\", &n);\n"
                "    std::vector<int> a(n);\n"
                "    for (int i = 0; i < n; ++i) scanf(\"%d\", &a[i]);\n\n"
                "    int low = 0, i = 0, high = n - 1;\n"
                "    // TODO: 三路划分\n\n"
                "    for (int j = 0; j < n; ++j) {\n"
                "        if (j) printf(\" \");\n"
                "        printf(\"%d\", a[j]);\n"
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
                "#include <vector>\n#include <algorithm>\n\n"
                "int main() {\n"
                "    int n;\n"
                "    scanf(\"%d\", &n);\n"
                "    std::vector<int> a(n);\n"
                "    for (int i = 0; i < n; ++i) scanf(\"%d\", &a[i]);\n\n"
                "    int low = 0, i = 0, high = n - 1;\n"
                "    while (i <= high) {\n"
                "        if (a[i] == 0) {\n"
                "            std::swap(a[low], a[i]);\n"
                "            ++low; ++i;\n"
                "        } else if (a[i] == 1) {\n"
                "            ++i;\n"
                "        } else {\n"
                "            std::swap(a[i], a[high]);\n"
                "            --high;                       // i 不动！换来的元素尚未检查\n"
                "        }\n"
                "    }\n\n"
                "    for (int j = 0; j < n; ++j) {\n"
                "        if (j) printf(\" \");\n"
                "        printf(\"%d\", a[j]);\n"
                "    }\n"
                "    printf(\"\\n\");\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "time_limit": 2.0,
    }


# ============================================================ 3. 二分答案求平方根
def solve_sqrt(text: str) -> str:
    """二分答案：找最大的 x 使 x*x <= n。"""
    n = int(text.strip())
    if n < 2:
        return f"{n}\n"
    lo, hi = 1, n
    while lo < hi:
        mid = (lo + hi + 1) // 2       # 上取整，避免死循环
        if mid * mid <= n:
            lo = mid
        else:
            hi = mid - 1
    return f"{lo}\n"


SQ_SPECS = [
    ("样例 1", "4", 10),
    ("样例 2", "8", 10),
    ("零", "0", 10),
    ("一", "1", 15),
    ("完全平方数", "144", 15),
    ("大数", "1000000000", 20),
    ("质数", "2147483647", 20),
]


def build_sqrt() -> dict:
    tests = build_tests(SQ_SPECS, solve_sqrt)
    return {
        "id": "search-sqrt",
        "title": "x 的平方根（二分答案）",
        "difficulty": "简单",
        "tags": ["二分查找", "二分答案", "数学"],
        "source": {
            "name": "LeetCode 69 / 二分答案入门",
            "url": "https://leetcode.cn/problems/sqrtx/",
        },
        "statement": (
            "给定一个非负整数 $n$，求它的**算术平方根的整数部分**，"
            "即最大的整数 $x$ 满足 $x^2 \\le n$。\n\n"
            "**禁止**使用任何库函数（如 `sqrt`、`pow`）。\n\n"
            "**要求：时间复杂度 $O(\\log n)$**。"
        ),
        "input_format": "一行一个整数 $n$（$0 \\le n \\le 2^{31}-1$）。",
        "output_format": "一行一个整数，表示 $\\lfloor\\sqrt{n}\\rfloor$。",
        "constraints": ["0 ≤ n ≤ 2^31−1", "禁止使用 sqrt/pow", "要求 O(log n)"],
        "samples": [
            {"input": "4\n", "output": "2\n",
             "explain": "2² = 4 ≤ 4，而 3² = 9 > 4，所以答案是 2。"},
            {"input": "8\n", "output": "2\n",
             "explain": "2² = 4 ≤ 8，3² = 9 > 8，所以答案是 2。"},
        ],
        "hint": (
            "这是**二分答案**的入门题：答案 $x$ 具有**单调性**——"
            "「$x^2 \\le n$ 是否成立」随着 $x$ 增大从 true 变为 false。\n\n"
            "在 $[0, n]$ 上二分，每次取 `mid`，判断 `mid*mid <= n`：\n"
            "- 成立 → `mid` 可行，尝试更大：`lo = mid`；\n"
            "- 不成立 → `hi = mid - 1`。\n\n"
            "**注意中点要上取整**（`(lo + hi + 1) / 2`），"
            "否则当 `lo` 与 `hi` 相邻时会陷入死循环。\n\n"
            "> **溢出提醒**：$n$ 可达 $2^{31}-1$，`mid*mid` 会超过 `int` 范围，"
            "**必须用 `long long`** 做乘法，否则会得到负数导致判断出错。"
        ),
        "starter_code": {
            "cpp": (
                "#include <cstdio>\n\n"
                "int main() {\n"
                "    long long n;\n"
                "    scanf(\"%lld\", &n);\n\n"
                "    // TODO: 二分答案，注意用 long long 计算 mid*mid\n"
                "    long long ans = 0;\n\n"
                "    printf(\"%lld\\n\", ans);\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "tests": tests,
        "reference": {
            "cpp": (
                "#include <cstdio>\n\n"
                "int main() {\n"
                "    long long n;\n"
                "    scanf(\"%lld\", &n);\n\n"
                "    if (n < 2) { printf(\"%lld\\n\", n); return 0; }\n\n"
                "    long long lo = 1, hi = n;\n"
                "    while (lo < hi) {\n"
                "        long long mid = lo + (hi - lo + 1) / 2;   // 上取整\n"
                "        if (mid * mid <= n) lo = mid;\n"
                "        else                hi = mid - 1;\n"
                "    }\n"
                "    printf(\"%lld\\n\", lo);\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "time_limit": 2.0,
    }


def main() -> None:
    builders = [build_rotated, build_color_sort, build_sqrt]
    for b in builders:
        prob = b()
        path = finalize(prob, OUT / f"{prob['id']}.json")
        total = sum(t["score"] for t in prob["tests"])
        print(f"生成 {prob['id']:26s} {len(prob['tests'])} 测试点, 总分 {total:3d}  -> {path.name}")


if __name__ == "__main__":
    main()
