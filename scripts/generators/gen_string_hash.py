"""生成「字符串与哈希」分类的题目。"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from genkit import build_tests, finalize, numbers  # noqa: E402

OUT = ROOT / "oj" / "data" / "problems" / "03-string-hash"


# ============================================================ 1. 字符串反转单词
def solve_reverse_words(text: str) -> str:
    s = text.strip("\n")
    words = s.split()
    return (" ".join(reversed(words)) + "\n") if words else "\n"


REVERSE_WORDS_SPECS = [
    ("样例 1", "the sky is blue", 10),
    ("样例 2（多空格）", "  hello   world  ", 10),
    ("单个单词", "abc", 10),
    ("全空格", "     ", 15),
    ("单字符单词", "a b c d", 15),
    ("含标点", "Hello, World!", 15),
    ("大量单词", " ".join(f"w{i}" for i in range(20)), 25),
]

# ============================================================ 2. 最长无重复子串
def solve_longest_unique(text: str) -> str:
    s = text.strip("\n")
    last = {}
    best = 0
    start = 0
    for i, ch in enumerate(s):
        if ch in last and last[ch] >= start:
            start = last[ch] + 1
        last[ch] = i
        best = max(best, i - start + 1)
    return f"{best}\n"


LONGEST_UNIQUE_SPECS = [
    ("样例 1", "abcabcbb", 10),
    ("样例 2（全相同）", "bbbbb", 10),
    ("样例 3", "pwwkew", 15),
    ("空串", "\n", 10),
    ("单字符", "a", 10),
    ("全部不同", "abcdefg", 15),
    ("数字与字母", "a1b2c3a4b5", 15),
    ("对称结构", "abba", 15),
]

# ============================================================ 3. 有效的字母异位词
def solve_anagram(text: str) -> str:
    ls = text.strip("\n").split("\n")
    a = ls[0] if ls else ""
    b = ls[1] if len(ls) > 1 else ""
    return "YES\n" if Counter(a) == Counter(b) else "NO\n"


ANAGRAM_SPECS = [
    ("样例 1（是异位词）", "anagram\nnagaram", 10),
    ("样例 2（不是）", "rat\ncar", 10),
    ("长度不同", "abc\nab", 10),
    ("同一单词", "abc\nabc", 15),
    ("含空格", "a b c\na bc ", 15),
    ("全相同字母", "aaa\naaa", 15),
    ("大小写敏感", "Abc\nabc", 15),
    ("长字符串", "".join(sorted("qwertyuiop" * 3)) + "\n" + "qwertyuiop" * 3, 10),
]

# ============================================================ 4. 字符串哈希：子串出现次数
def solve_substr_count(text: str) -> str:
    """统计模式串在文本中作为**不重叠**子串出现的次数（KMP 思想）。"""
    ls = text.strip("\n").split("\n")
    hay = ls[0] if ls else ""
    pat = ls[1] if len(ls) > 1 else ""
    if not pat:
        return "0\n"
    cnt = 0
    i = 0
    while i + len(pat) <= len(hay):
        if hay[i:i + len(pat)] == pat:
            cnt += 1
            i += len(pat)
        else:
            i += 1
    return f"{cnt}\n"


SUBSTR_COUNT_SPECS = [
    ("样例 1", "aaaa\naa", 10),
    ("样例 2", "abcabcabc\nabc", 15),
    ("无匹配", "abcdef\nxyz", 10),
    ("模式比文本长", "ab\nabcd", 10),
    ("完全匹配", "abc\nabc", 15),
    ("单字符模式", "ababab\na", 15),
    ("重叠不计数", "aaa\naa", 10),
    ("长文本", "ab" * 20 + "\nab", 15),
]

# ============================================================ 5. 回文串判断
def solve_palindrome(text: str) -> str:
    """忽略非字母数字字符与大小写，判断是否回文。"""
    s = text.strip("\n")
    filtered = [c.lower() for c in s if c.isalnum()]
    return "YES\n" if filtered == filtered[::-1] else "NO\n"


PALINDROME_SPECS = [
    ("样例 1（经典）", "A man, a plan, a canal: Panama", 10),
    ("样例 2（不是）", "race a car", 10),
    ("空串", "\n", 10),
    ("纯数字回文", "12321", 15),
    ("纯数字非回文", "12345", 15),
    ("单一字符", "a", 10),
    ("含大量符号", "!!!a!!!", 15),
    ("大小写混合", "AbBa", 15),
    ("空格也算忽略", "  ", 10),
]


def _problem_reverse_words() -> dict:
    tests = build_tests(REVERSE_WORDS_SPECS, solve_reverse_words)
    return {
        "id": "string-reverse-words",
        "title": "反转字符串中的单词",
        "difficulty": "入门",
        "tags": ["字符串", "模拟"],
        "source": {"name": "LeetCode 151", "url": "https://leetcode.cn/problems/reverse-words-in-a-string/"},
        "statement": (
            "给定一个字符串 $s$，请你**反转其中单词的顺序**，单词之间用一个空格分隔。\n\n"
            "注意：输入中可能包含**前导空格、尾随空格或单词间的多余空格**，"
            "输出时需要把这些多余空格处理掉，单词之间只保留**单个空格**。"
        ),
        "input_format": "一行字符串 $s$（$0 \\le |s| \\le 10^5$），仅包含可见 ASCII 字符与空格。",
        "output_format": "一行，输出反转单词顺序后的字符串。若 $s$ 不含任何单词，输出一个空行。",
        "constraints": ["0 ≤ |s| ≤ 10^5", "仅含可见 ASCII 与空格"],
        "samples": [
            {"input": "the sky is blue\n", "output": "blue is sky the\n",
             "explain": "单词顺序由「the sky is blue」反转为「blue is sky the」。"},
            {"input": "  hello   world  \n", "output": "world hello\n",
             "explain": "先按单词切分（忽略多余空格），再反转顺序，最后单空格拼接。"},
        ],
        "hint": (
            "按空白字符切分出所有单词（`s.split()` 会自动忽略连续空白），"
            "然后逆序用一个空格连接即可。\n\n"
            "若要求原地 $O(1)$ 额外空间，可先将整个字符串翻转，再逐个翻转每个单词。"
        ),
        "starter_code": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <string>\n"
                "#include <vector>\n"
                "#include <sstream>\n\n"
                "int main() {\n"
                "    std::string line;\n"
                "    std::getline(std::cin, line);\n"
                "    std::istringstream iss(line);\n"
                "    std::vector<std::string> words;\n"
                "    std::string w;\n"
                "    while (iss >> w) words.push_back(w);\n\n"
                "    // TODO: 逆序输出单词，用单个空格分隔\n\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "tests": tests,
        "reference": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <string>\n"
                "#include <vector>\n"
                "#include <sstream>\n"
                "#include <iostream>\n\n"
                "int main() {\n"
                "    std::string line;\n"
                "    std::getline(std::cin, line);\n"
                "    std::istringstream iss(line);\n"
                "    std::vector<std::string> words;\n"
                "    std::string w;\n"
                "    while (iss >> w) words.push_back(w);\n\n"
                "    for (int i = (int)words.size() - 1; i >= 0; --i) {\n"
                "        if (i != (int)words.size() - 1) printf(\" \");\n"
                "        printf(\"%s\", words[i].c_str());\n"
                "    }\n"
                "    printf(\"\\n\");\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "time_limit": 2.0,
    }


def _problem_longest_unique() -> dict:
    tests = build_tests(LONGEST_UNIQUE_SPECS, solve_longest_unique)
    return {
        "id": "string-longest-unique-substr",
        "title": "最长无重复字符子串",
        "difficulty": "中等",
        "tags": ["字符串", "滑动窗口", "哈希表"],
        "source": {"name": "LeetCode 3", "url": "https://leetcode.cn/problems/longest-substring-without-repeating-characters/"},
        "statement": (
            "给定一个字符串 $s$，请找出其中**不含重复字符**的**最长子串**的长度。\n\n"
            "子串指原字符串中连续的一段字符。"
        ),
        "input_format": "一行字符串 $s$（$0 \\le |s| \\le 10^5$），由可见 ASCII 字符组成。",
        "output_format": "一行一个整数，表示最长无重复字符子串的长度。",
        "constraints": ["0 ≤ |s| ≤ 10^5", "字符为可见 ASCII"],
        "samples": [
            {"input": "abcabcbb\n", "output": "3\n", "explain": "最长无重复子串是 `abc`，长度为 3。"},
            {"input": "bbbbb\n", "output": "1\n", "explain": "所有字符相同，最长只能是单个 `b`。"},
            {"input": "pwwkew\n", "output": "3\n", "explain": "最长的是 `wke`（注意 `pwke` 不是子串，因为不连续）。"},
        ],
        "hint": (
            "**滑动窗口**：用左右指针 `l, r` 维护一个不含重复字符的窗口，"
            "并用哈希表记录每个字符**最后一次出现的位置**。\n\n"
            "右指针右移时，若当前字符上次出现的位置 $\\ge l$，就把 $l$ 移到该位置 $+1$；"
            "窗口大小 $r - l + 1$ 的最大值即为答案。时间 $O(n)$。"
        ),
        "starter_code": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <string>\n"
                "#include <algorithm>\n\n"
                "int main() {\n"
                "    std::string s;\n"
                "    if (!std::getline(std::cin, s)) { printf(\"0\\n\"); return 0; }\n"
                "    int last[256];\n"
                "    std::fill(last, last + 256, -1);\n"
                "    int best = 0, l = 0;\n"
                "    // TODO: 滑动窗口\n\n"
                "    printf(\"%d\\n\", best);\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "tests": tests,
        "reference": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <string>\n"
                "#include <iostream>\n"
                "#include <algorithm>\n\n"
                "int main() {\n"
                "    std::string s;\n"
                "    if (!std::getline(std::cin, s)) { printf(\"0\\n\"); return 0; }\n"
                "    int last[256];\n"
                "    std::fill(last, last + 256, -1);\n"
                "    int best = 0, l = 0;\n"
                "    for (int r = 0; r < (int)s.size(); ++r) {\n"
                "        unsigned char c = (unsigned char)s[r];\n"
                "        if (last[c] >= l) l = last[c] + 1;\n"
                "        last[c] = r;\n"
                "        best = std::max(best, r - l + 1);\n"
                "    }\n"
                "    printf(\"%d\\n\", best);\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "time_limit": 2.0,
    }


def _problem_anagram() -> dict:
    tests = build_tests(ANAGRAM_SPECS, solve_anagram)
    return {
        "id": "string-valid-anagram",
        "title": "有效的字母异位词",
        "difficulty": "入门",
        "tags": ["字符串", "哈希表", "计数"],
        "source": {"name": "LeetCode 242", "url": "https://leetcode.cn/problems/valid-anagram/"},
        "statement": (
            "给定两个字符串 $s$ 和 $t$，判断 $t$ 是否是 $s$ 的**字母异位词**。\n\n"
            "字母异位词指：两个字符串包含的**字符种类与每种字符的个数完全相同**，"
            "只是排列顺序可能不同。区分大小写与空格。"
        ),
        "input_format": "第一行字符串 $s$。\n\n第二行字符串 $t$。\n\n（$0 \\le |s|, |t| \\le 10^5$）",
        "output_format": "一行，若 $t$ 是 $s$ 的字母异位词输出 `YES`，否则输出 `NO`。",
        "constraints": ["0 ≤ |s|, |t| ≤ 10^5", "区分大小写"],
        "samples": [
            {"input": "anagram\nnagaram\n", "output": "YES\n",
             "explain": "两个字符串都由 3 个 `a`、1 个 `n`、1 个 `g`、1 个 `r`、1 个 `m` 组成。"},
            {"input": "rat\ncar\n", "output": "NO\n",
             "explain": "`rat` 含 `t`，`car` 不含，字符构成不同。"},
        ],
        "hint": (
            "用一个长度 256 的计数数组统计 $s$ 中每个字符出现次数，"
            "再遍历 $t$ 逐个减掉；若出现负数或最后计数器不全为 0，则不是异位词。\n\n"
            "也可以用哈希表（`std::unordered_map`）实现，思路相同。时间 $O(n)$。"
        ),
        "starter_code": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <string>\n"
                "#include <iostream>\n\n"
                "int main() {\n"
                "    std::string s, t;\n"
                "    std::getline(std::cin, s);\n"
                "    std::getline(std::cin, t);\n"
                "    if (s.size() != t.size()) { printf(\"NO\\n\"); return 0; }\n\n"
                "    int cnt[256] = {0};\n"
                "    // TODO: 用计数数组判断\n\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "tests": tests,
        "reference": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <string>\n"
                "#include <iostream>\n\n"
                "int main() {\n"
                "    std::string s, t;\n"
                "    std::getline(std::cin, s);\n"
                "    std::getline(std::cin, t);\n"
                "    if (s.size() != t.size()) { printf(\"NO\\n\"); return 0; }\n\n"
                "    int cnt[256] = {0};\n"
                "    for (unsigned char c : s) cnt[c]++;\n"
                "    for (unsigned char c : t) cnt[c]--;\n"
                "    bool ok = true;\n"
                "    for (int i = 0; i < 256; ++i) if (cnt[i] != 0) { ok = false; break; }\n"
                "    printf(\"%s\\n\", ok ? \"YES\" : \"NO\");\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "time_limit": 2.0,
    }


def _problem_substr_count() -> dict:
    tests = build_tests(SUBSTR_COUNT_SPECS, solve_substr_count)
    return {
        "id": "string-substr-count",
        "title": "子串出现次数（不重叠）",
        "difficulty": "简单",
        "tags": ["字符串", "哈希", "KMP"],
        "source": {"name": "字符串匹配经典题 / KMP 应用", "url": "https://oi-wiki.org/string/kmp/"},
        "statement": (
            "给定一个文本串 $T$ 和一个模式串 $P$，请统计 $P$ 作为 $T$ 的**不重叠子串**出现的次数。\n\n"
            "所谓不重叠，指每次匹配成功后从匹配段的**下一个字符**继续尝试，"
            "已用掉的字符不能再次参与匹配。\n\n"
            "例如 $T$ = `aaaa`，$P$ = `aa`，第 1、2 个字符匹配成功后从第 4 个字符继续，"
            "因此答案是 **2** 而不是 3。"
        ),
        "input_format": "第一行文本串 $T$。\n\n第二行模式串 $P$。\n\n（$0 \\le |T|, |P| \\le 10^5$）",
        "output_format": "一行一个整数，表示出现次数。",
        "constraints": ["0 ≤ |T|, |P| ≤ 10^5", "仅含可见 ASCII"],
        "samples": [
            {"input": "aaaa\naa\n", "output": "2\n", "explain": "匹配位置为 1 和 3，互不重叠，共 2 次。"},
            {"input": "abcabcabc\nabc\n", "output": "3\n", "explain": "从位置 1、4、7 各匹配一次，共 3 次。"},
        ],
        "hint": (
            "朴素做法：从每个位置尝试匹配，匹配成功则跳过整个模式串长度。"
            "最坏复杂度 $O(|T| \\cdot |P|)$。\n\n"
            "更优做法是 **KMP 算法**：先用 $O(|P|)$ 预处理出 `nxt` 数组，"
            "再线性扫描 $T$，整体 $O(|T| + |P|)$。本题数据规模下朴素做法也能通过。"
        ),
        "starter_code": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <string>\n"
                "#include <iostream>\n\n"
                "int main() {\n"
                "    std::string t, p;\n"
                "    std::getline(std::cin, t);\n"
                "    std::getline(std::cin, p);\n"
                "    if (p.empty() || p.size() > t.size()) { printf(\"0\\n\"); return 0; }\n\n"
                "    int cnt = 0;\n"
                "    // TODO: 统计不重叠出现次数\n\n"
                "    printf(\"%d\\n\", cnt);\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "tests": tests,
        "reference": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <string>\n"
                "#include <iostream>\n\n"
                "int main() {\n"
                "    std::string t, p;\n"
                "    std::getline(std::cin, t);\n"
                "    std::getline(std::cin, p);\n"
                "    if (p.empty() || p.size() > t.size()) { printf(\"0\\n\"); return 0; }\n\n"
                "    int cnt = 0;\n"
                "    size_t i = 0;\n"
                "    while (i + p.size() <= t.size()) {\n"
                "        if (t.compare(i, p.size(), p) == 0) { ++cnt; i += p.size(); }\n"
                "        else ++i;\n"
                "    }\n"
                "    printf(\"%d\\n\", cnt);\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "time_limit": 2.0,
    }


def _problem_palindrome() -> dict:
    tests = build_tests(PALINDROME_SPECS, solve_palindrome)
    return {
        "id": "string-palindrome",
        "title": "验证回文串",
        "difficulty": "入门",
        "tags": ["字符串", "双指针"],
        "source": {"name": "LeetCode 125", "url": "https://leetcode.cn/problems/valid-palindrome/"},
        "statement": (
            "给定一个字符串 $s$，判断它是否**回文**。\n\n"
            "判定规则：**只考虑字母和数字字符**，忽略其他所有字符（空格、标点等），"
            "并且**忽略字母的大小写**。\n\n"
            "空字符串视为回文。"
        ),
        "input_format": "一行字符串 $s$（$0 \\le |s| \\le 10^5$），由可见 ASCII 字符组成（可能含空格）。",
        "output_format": "一行，若 $s$ 是回文串输出 `YES`，否则输出 `NO`。",
        "constraints": ["0 ≤ |s| ≤ 10^5", "忽略非字母数字字符", "忽略大小写"],
        "samples": [
            {"input": "A man, a plan, a canal: Panama\n", "output": "YES\n",
             "explain": "去掉非字母数字并统一小写后得到 `amanaplanacanalpanama`，是回文。"},
            {"input": "race a car\n", "output": "NO\n",
             "explain": "处理后为 `raceacar`，不是回文。"},
        ],
        "hint": (
            "**双指针**：左指针从头、右指针从尾相向移动，"
            "遇到非字母数字字符就跳过；比较两个指针处的字符（统一转小写）是否相等。\n\n"
            "也可以用 `isalnum()` / `tolower()` 辅助判断，时间 $O(n)$，空间 $O(1)$。"
        ),
        "starter_code": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <string>\n"
                "#include <cctype>\n"
                "#include <iostream>\n\n"
                "int main() {\n"
                "    std::string s;\n"
                "    std::getline(std::cin, s);\n\n"
                "    int i = 0, j = (int)s.size() - 1;\n"
                "    bool ok = true;\n"
                "    // TODO: 双指针验证回文\n\n"
                "    printf(\"%s\\n\", ok ? \"YES\" : \"NO\");\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "tests": tests,
        "reference": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <string>\n"
                "#include <cctype>\n"
                "#include <iostream>\n\n"
                "int main() {\n"
                "    std::string s;\n"
                "    std::getline(std::cin, s);\n\n"
                "    int i = 0, j = (int)s.size() - 1;\n"
                "    bool ok = true;\n"
                "    while (i < j) {\n"
                "        while (i < j && !std::isalnum((unsigned char)s[i])) ++i;\n"
                "        while (i < j && !std::isalnum((unsigned char)s[j])) --j;\n"
                "        if (std::tolower((unsigned char)s[i]) != std::tolower((unsigned char)s[j])) {\n"
                "            ok = false; break;\n"
                "        }\n"
                "        ++i; --j;\n"
                "    }\n"
                "    printf(\"%s\\n\", ok ? \"YES\" : \"NO\");\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "time_limit": 2.0,
    }


def main() -> None:
    builders = [
        _problem_reverse_words,
        _problem_longest_unique,
        _problem_anagram,
        _problem_substr_count,
        _problem_palindrome,
    ]
    for b in builders:
        prob = b()
        path = finalize(prob, OUT / f"{prob['id']}.json")
        total = sum(t["score"] for t in prob["tests"])
        print(f"生成 {prob['id']:36s} {len(prob['tests'])} 测试点, 总分 {total}  -> {path.name}")


if __name__ == "__main__":
    main()
