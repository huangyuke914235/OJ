"""生成「字符串与哈希」分类的第二批题目。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from genkit import build_tests, finalize  # noqa: E402

OUT = ROOT / "oj" / "data" / "problems" / "03-string-hash"


def _lines(text: str):
    return text.strip("\n").split("\n")


# ============================================================ 1. 字母异位词分组
def solve_group_anagrams(text: str) -> str:
    """按字符排序签名分组；组内字典序，组间按首词字典序。"""
    ls = _lines(text)
    n = int(ls[0])
    words = [ls[i].strip() for i in range(1, n + 1)]
    groups = {}
    for w in words:
        key = "".join(sorted(w))
        groups.setdefault(key, []).append(w)
    res = []
    for v in groups.values():
        v.sort()
        res.append(v)
    res.sort(key=lambda v: v[0])          # 组间按首词字典序
    out = [" ".join(v) for v in res]
    return ("\n".join(out) + "\n") if out else "\n"


GA_SPECS = [
    ("样例 1", "6\neat\ntea\ntan\nate\nnat\nbat", 10),
    ("样例 2（无同组）", "3\nabc\ndef\nghi", 10),
    ("单字符串", "1\na", 10),
    ("全部同组", "4\nab\nba\nab\nba", 15),
    ("含重复词", "5\nabc\nabc\ncba\nxyz\nzyx", 15),
    ("长度不同", "4\na\nab\nabc\nabcd", 20),
    ("多组混杂", "8\nlisten\nsilent\nenlist\ngoogle\ngogole\ncat\nact\ntac", 20),
]


def build_group_anagrams() -> dict:
    tests = build_tests(GA_SPECS, solve_group_anagrams)
    return {
        "id": "string-group-anagrams",
        "title": "字母异位词分组",
        "difficulty": "中等",
        "tags": ["字符串", "哈希表", "排序"],
        "source": {
            "name": "LeetCode 49 / 哈希分组",
            "url": "https://leetcode.cn/problems/group-anagrams/",
        },
        "statement": (
            "给定 $n$ 个小写字母字符串，请把**字母异位词**分到同一组。\n\n"
            "字母异位词指字母种类和数量完全相同、但排列顺序不同的字符串"
            "（例如 `eat`、`tea`、`ate` 互为异位词）。\n\n"
            "**输出要求**（为保证判题唯一性）：\n"
            "1. 每组内部按**字典序**升序排列，同一行内用空格分隔；\n"
            "2. 各组之间按**组内第一个单词的字典序**升序排列，每组占一行。"
        ),
        "input_format": "第一行一个整数 $n$（$1 \\le n \\le 10^4$）。\n\n接下来 $n$ 行，每行一个小写字母字符串（长度 $1 \\le |s| \\le 100$）。",
        "output_format": "若干行，每行一组异位词（组内字典序升序，空格分隔）。组间按首个单词字典序升序。",
        "constraints": ["1 ≤ n ≤ 10^4", "1 ≤ |s| ≤ 100", "仅含小写字母"],
        "samples": [
            {"input": "6\neat\ntea\ntan\nate\nnat\nbat\n",
             "output": "ate eat tea\nbat\nnat tan\n",
             "explain": "`ate eat tea` 互为异位词；`nat tan` 互为异位词；`bat` 单独一组。"
                        "各组按首词字典序排列：ate < bat < nat。"},
            {"input": "3\nabc\ndef\nghi\n", "output": "abc\ndef\nghi\n",
             "explain": "三个词互不为异位词，各自成组。"},
        ],
        "hint": (
            "**关键是把「异位词」映射成同一个键**，这样才能用哈希表分组。\n\n"
            "两种常用键：\n"
            "1. **排序后**的字符串——异位词排序后必然相同，$O(L\\log L)$ 构造；\n"
            "2. **字符计数**编码，如 `a2b1c0...`，$O(L)$ 构造。\n\n"
            "本题字符串很短，用排序法即可。\n\n"
            "> **易错点**：哈希表遍历顺序不确定，必须**显式排序**才能得到确定的输出，"
            "否则同一份输入可能产生不同的行序，导致判题不稳定。"
        ),
        "starter_code": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <vector>\n"
                "#include <string>\n"
                "#include <map>\n"
                "#include <algorithm>\n"
                "#include <iostream>\n\n"
                "int main() {\n"
                "    int n;\n"
                "    scanf(\"%d\", &n);\n"
                "    std::map<std::string, std::vector<std::string>> groups;\n"
                "    for (int i = 0; i < n; ++i) {\n"
                "        std::string w;\n"
                "        std::cin >> w;\n"
                "        // TODO: 计算 key 并分组\n"
                "    }\n"
                "    // TODO: 按规则输出\n"
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
                "#include <map>\n"
                "#include <algorithm>\n"
                "#include <iostream>\n\n"
                "int main() {\n"
                "    int n;\n"
                "    scanf(\"%d\", &n);\n"
                "    std::map<std::string, std::vector<std::string>> groups;\n"
                "    for (int i = 0; i < n; ++i) {\n"
                "        std::string w;\n"
                "        std::cin >> w;\n"
                "        std::string key = w;\n"
                "        std::sort(key.begin(), key.end());   // 排序后的串作为 key\n"
                "        groups[key].push_back(w);\n"
                "    }\n"
                "    std::vector<std::vector<std::string>> res;\n"
                "    for (auto &kv : groups) {                // 先收集各组\n"
                "        auto v = kv.second;\n"
                "        std::sort(v.begin(), v.end());       // 组内字典序\n"
                "        res.push_back(v);\n"
                "    }\n"
                "    std::sort(res.begin(), res.end(),        // 组间按首词字典序\n"
                "              [](const std::vector<std::string> &a,\n"
                "                 const std::vector<std::string> &b) { return a[0] < b[0]; });\n"
                "    for (auto &v : res) {\n"
                "        for (size_t i = 0; i < v.size(); ++i) {\n"
                "            if (i) printf(\" \");\n"
                "            printf(\"%s\", v[i].c_str());\n"
                "        }\n"
                "        printf(\"\\n\");\n"
                "    }\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "time_limit": 2.0,
    }


# ============================================================ 2. 第一个只出现一次的字符
def solve_first_unique(text: str) -> str:
    """两趟扫描：先计数，再找第一个计数为 1 的位置。"""
    ls = _lines(text)
    s = ls[0] if ls else ""
    cnt = {}
    for c in s:
        cnt[c] = cnt.get(c, 0) + 1
    for i, c in enumerate(s):
        if cnt[c] == 1:
            return f"{i}\n"
    return "-1\n"


FU_SPECS = [
    ("样例 1", "leetcode", 10),
    ("样例 2（无唯一）", "aabb", 10),
    ("单字符", "z", 10),
    ("唯一在末尾", "aabbc", 15),
    ("唯一在开头", "abcabc", 15),
    ("全部唯一", "abcdef", 20),
    ("长重复", "aabbccddeef", 20),
]


def build_first_unique() -> dict:
    tests = build_tests(FU_SPECS, solve_first_unique)
    return {
        "id": "string-first-unique-char",
        "title": "第一个只出现一次的字符",
        "difficulty": "入门",
        "tags": ["字符串", "哈希表", "计数"],
        "source": {
            "name": "LeetCode 387 / 剑指 Offer 50",
            "url": "https://leetcode.cn/problems/first-unique-character-in-a-string/",
        },
        "statement": (
            "给定一个小写字母字符串 $s$，找到它的**第一个不重复字符**，返回其**下标**（从 $0$ 开始）。\n\n"
            "如果不存在不重复的字符，返回 $-1$。"
        ),
        "input_format": "一行一个字符串 $s$（$1 \\le |s| \\le 10^5$），仅含小写英文字母。",
        "output_format": "一行，输出第一个不重复字符的下标；若不存在则输出 $-1$。",
        "constraints": ["1 ≤ |s| ≤ 10^5", "仅含小写字母"],
        "samples": [
            {"input": "leetcode\n", "output": "0\n",
             "explain": "`l` 只出现一次，且是第一个这样的字符，下标为 0。"},
            {"input": "aabb\n", "output": "-1\n",
             "explain": "每个字符都出现了两次，没有不重复的字符。"},
        ],
        "hint": (
            "**两趟扫描**：\n\n"
            "1. 第一趟用计数数组（或哈希表）统计每个字符出现的次数；\n"
            "2. 第二趟从左到右找**第一个**计数为 $1$ 的字符，返回其下标。\n\n"
            "因为只有 26 个小写字母，用 `int cnt[26]` 比哈希表更快，常数极小。\n\n"
            "> **易错点**：不能只统计一次就返回——必须先统计完整，"
            "否则后面的字符还没被计入，会误判成「只出现一次」。"
        ),
        "starter_code": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <cstring>\n\n"
                "char s[100005];\n"
                "int cnt[26];\n\n"
                "int main() {\n"
                "    if (!fgets(s, sizeof(s), stdin)) { printf(\"-1\\n\"); return 0; }\n"
                "    int len = (int)strlen(s);\n"
                "    while (len > 0 && (s[len - 1] == '\\n' || s[len - 1] == '\\r')) s[--len] = 0;\n\n"
                "    // TODO: 第一趟统计次数，第二趟找第一个次数为 1 的下标\n"
                "    int ans = -1;\n\n"
                "    printf(\"%d\\n\", ans);\n"
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
                "int cnt[26];\n\n"
                "int main() {\n"
                "    if (!fgets(s, sizeof(s), stdin)) { printf(\"-1\\n\"); return 0; }\n"
                "    int len = (int)strlen(s);\n"
                "    while (len > 0 && (s[len - 1] == '\\n' || s[len - 1] == '\\r')) s[--len] = 0;\n\n"
                "    memset(cnt, 0, sizeof(cnt));\n"
                "    for (int i = 0; i < len; ++i) ++cnt[s[i] - 'a'];   // 第一趟\n\n"
                "    int ans = -1;\n"
                "    for (int i = 0; i < len; ++i) {                    // 第二趟\n"
                "        if (cnt[s[i] - 'a'] == 1) { ans = i; break; }\n"
                "    }\n"
                "    printf(\"%d\\n\", ans);\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "time_limit": 2.0,
    }


# ============================================================ 3. 最长公共前缀
def solve_lcp(text: str) -> str:
    """以第一个串为基准，逐字符与其他串比较，遇到不匹配就截断。"""
    ls = text.split("\n")                 # 不 strip，保留空行
    n = int(ls[0])
    words = [ls[i].strip() if i < len(ls) else "" for i in range(1, n + 1)]
    if not words:
        return "\n"
    base = words[0]
    k = len(base)
    for w in words[1:]:
        j = 0
        while j < k and j < len(w) and w[j] == base[j]:
            j += 1
        k = j
        if k == 0:
            break
    return (base[:k] + "\n") if k > 0 else "\n"


LCP_SPECS = [
    ("样例 1", "3\nflower\nflow\nflight", 10),
    ("样例 2（无公共前缀）", "3\ndog\nracecar\ncar", 10),
    ("单字符串", "1\nabc", 10),
    ("完全相同", "3\nabc\nabc\nabc", 15),
    ("某串是前缀", "3\nab\nabc\nabcd", 15),
    ("首串为空", "3\n\nabc\ndef", 20),
    ("全部空串", "2\n\n\n", 20),
]


def build_lcp() -> dict:
    tests = build_tests(LCP_SPECS, solve_lcp)
    return {
        "id": "string-longest-common-prefix",
        "title": "最长公共前缀",
        "difficulty": "入门",
        "tags": ["字符串", "模拟"],
        "source": {
            "name": "LeetCode 14 / 字符串模拟",
            "url": "https://leetcode.cn/problems/longest-common-prefix/",
        },
        "statement": (
            "给定 $n$ 个小写字母字符串，求它们的**最长公共前缀**。\n\n"
            "如果不存在公共前缀，输出空行。"
        ),
        "input_format": "第一行一个整数 $n$（$1 \\le n \\le 10^4$）。\n\n接下来 $n$ 行，每行一个字符串（可为空串，长度 $0 \\le |s| \\le 200$）。",
        "output_format": "一行，输出最长公共前缀。若不存在则输出一个空行。",
        "constraints": ["1 ≤ n ≤ 10^4", "0 ≤ |s| ≤ 200", "仅含小写字母"],
        "samples": [
            {"input": "3\nflower\nflow\nflight\n", "output": "fl\n",
             "explain": "三个串的公共前缀是 `fl`。"},
            {"input": "3\ndog\nracecar\ncar\n", "output": "\n",
             "explain": "第一个字符就不同，不存在公共前缀。"},
        ],
        "hint": (
            "**纵向扫描**：以第一个字符串为基准，记当前公共前缀长度为 $k$（初始为第一个串的长度）。\n\n"
            "依次与其他每个字符串比较：从前往后逐字符匹配，一旦不匹配或到达某个串末尾就停止，"
            "把 $k$ 更新为匹配长度。若某轮 $k$ 变成 $0$，可以提前结束。\n\n"
            "时间 $O(n \\cdot L)$（$L$ 为最短串长度），空间 $O(1)$。\n\n"
            "> **易错点**：必须同时判断「是否超出当前串长度」，否则会越界访问。"
        ),
        "starter_code": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <vector>\n"
                "#include <string>\n"
                "#include <iostream>\n\n"
                "int main() {\n"
                "    int n;\n"
                "    scanf(\"%d\", &n);\n"
                "    std::vector<std::string> w(n);\n"
                "    std::getline(std::cin, w[0]);      // 吃掉第一行剩余\n"
                "    for (int i = 0; i < n; ++i) std::getline(std::cin, w[i]);\n\n"
                "    // TODO: 纵向扫描求最长公共前缀\n"
                "    std::string ans;\n\n"
                "    printf(\"%s\\n\", ans.c_str());\n"
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
                "    int n;\n"
                "    scanf(\"%d\", &n);\n"
                "    std::vector<std::string> w(n);\n"
                "    std::getline(std::cin, w[0]);\n"
                "    for (int i = 0; i < n; ++i) std::getline(std::cin, w[i]);\n\n"
                "    int k = (int)w[0].size();\n"
                "    for (int i = 1; i < n && k > 0; ++i) {\n"
                "        int j = 0;\n"
                "        while (j < k && j < (int)w[i].size() && w[i][j] == w[0][j]) ++j;\n"
                "        k = j;\n"
                "    }\n"
                "    printf(\"%s\\n\", w[0].substr(0, k).c_str());\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "time_limit": 2.0,
    }


# ============================================================ 4. 实现 strStr
def solve_strstr(text: str) -> str:
    """KMP 前缀函数匹配。"""
    ls = _lines(text)
    hay = ls[0] if len(ls) > 0 else ""
    nee = ls[1] if len(ls) > 1 else ""
    if nee == "":
        return "0\n"
    # 构造 pi
    m = len(nee)
    pi = [0] * m
    j = 0
    for i in range(1, m):
        while j > 0 and nee[i] != nee[j]:
            j = pi[j - 1]
        if nee[i] == nee[j]:
            j += 1
        pi[i] = j
    # 匹配
    j = 0
    for i in range(len(hay)):
        while j > 0 and hay[i] != nee[j]:
            j = pi[j - 1]
        if hay[i] == nee[j]:
            j += 1
        if j == m:
            return f"{i - m + 1}\n"
    return "-1\n"


SS_SPECS = [
    ("样例 1", "sadbutsad\nsad", 10),
    ("样例 2（未找到）", "leetcode\nleeto", 10),
    ("空模式串", "abc\n", 10),
    ("模式等于主串", "abc\nabc", 15),
    ("模式在末尾", "ababab\nbab", 15),
    ("重复模式", "aaaaa\naa", 20),
    ("单字符", "a\na", 20),
]


def build_strstr() -> dict:
    tests = build_tests(SS_SPECS, solve_strstr)
    return {
        "id": "string-implement-strstr",
        "title": "实现 strStr（子串匹配）",
        "difficulty": "中等",
        "tags": ["字符串", "KMP", "子串匹配"],
        "source": {
            "name": "LeetCode 28 / KMP 算法",
            "url": "https://leetcode.cn/problems/find-the-index-of-the-first-occurrence-in-a-string/",
        },
        "statement": (
            "给定两个字符串 $haystack$ 和 $needle$，请找出 $needle$ 在 $haystack$ 中"
            "**第一次出现的位置**（下标从 $0$ 开始）。\n\n"
            "若 $needle$ 不是 $haystack$ 的子串，返回 $-1$。\n\n"
            "**特殊情况**：若 $needle$ 是空串，按惯例返回 $0$。\n\n"
            "**进阶要求**：请使用 $O(n+m)$ 的 **KMP 算法**，而非 $O(nm)$ 的暴力匹配。"
        ),
        "input_format": "第一行一个字符串 $haystack$。\n\n第二行一个字符串 $needle$（可能为空行）。\n\n两串长度均不超过 $10^5$，仅含小写英文字母。",
        "output_format": "一行，输出第一次出现的下标；不存在则输出 $-1$。",
        "constraints": ["0 ≤ |haystack|, |needle| ≤ 10^5", "仅含小写字母", "建议 O(n+m) 算法"],
        "samples": [
            {"input": "sadbutsad\nsad\n", "output": "0\n",
             "explain": "`sad` 在开头就出现了，下标为 0。"},
            {"input": "leetcode\nleeto\n", "output": "-1\n",
             "explain": "`leeto` 不是 `leetcode` 的子串。"},
        ],
        "hint": (
            "**KMP 算法**分两步：\n\n"
            "**第一步：求模式串的 `pi`（前缀函数）数组。** `pi[i]` 表示 "
            "`needle[0..i]` 的最长**相等真前后缀**的长度。递推方式："
            "`j = pi[i-1]`，若 `needle[i] != needle[j]` 就不断令 `j = pi[j-1]` 回退，"
            "匹配上则 `j++`，最后 `pi[i] = j`。\n\n"
            "**第二步：用 `pi` 做匹配。** 主串指针 `i` 一直前进不回头；"
            "失配时模式串指针 `j` 回退到 `pi[j-1]` 而不是回到 $0$，这就是省时间的关键。\n\n"
            "当 `j == m` 时匹配成功，起始位置为 `i - m + 1`。\n\n"
            "> **易错点**：`needle` 为空串时要直接返回 $0$，否则会越界访问。"
        ),
        "starter_code": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <vector>\n"
                "#include <string>\n"
                "#include <iostream>\n\n"
                "int main() {\n"
                "    std::string hay, nee;\n"
                "    std::getline(std::cin, hay);\n"
                "    std::getline(std::cin, nee);\n\n"
                "    if (nee.empty()) { printf(\"0\\n\"); return 0; }\n\n"
                "    int n = hay.size(), m = nee.size();\n"
                "    std::vector<int> pi(m, 0);\n"
                "    // TODO: 1) 构造 pi 数组  2) KMP 匹配\n\n"
                "    printf(\"-1\\n\");\n"
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
                "    std::string hay, nee;\n"
                "    std::getline(std::cin, hay);\n"
                "    std::getline(std::cin, nee);\n\n"
                "    if (nee.empty()) { printf(\"0\\n\"); return 0; }\n\n"
                "    int n = (int)hay.size(), m = (int)nee.size();\n\n"
                "    // 1) 前缀函数\n"
                "    std::vector<int> pi(m, 0);\n"
                "    for (int i = 1; i < m; ++i) {\n"
                "        int j = pi[i - 1];\n"
                "        while (j > 0 && nee[i] != nee[j]) j = pi[j - 1];\n"
                "        if (nee[i] == nee[j]) ++j;\n"
                "        pi[i] = j;\n"
                "    }\n\n"
                "    // 2) 匹配\n"
                "    int j = 0, ans = -1;\n"
                "    for (int i = 0; i < n; ++i) {\n"
                "        while (j > 0 && hay[i] != nee[j]) j = pi[j - 1];\n"
                "        if (hay[i] == nee[j]) ++j;\n"
                "        if (j == m) { ans = i - m + 1; break; }\n"
                "    }\n"
                "    printf(\"%d\\n\", ans);\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "time_limit": 2.0,
    }


def main() -> None:
    builders = [
        build_group_anagrams,
        build_first_unique,
        build_lcp,
        build_strstr,
    ]
    for b in builders:
        prob = b()
        path = finalize(prob, OUT / f"{prob['id']}.json")
        total = sum(t["score"] for t in prob["tests"])
        print(f"生成 {prob['id']:34s} {len(prob['tests'])} 测试点, 总分 {total:3d}  -> {path.name}")


if __name__ == "__main__":
    main()
