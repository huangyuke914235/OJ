"""字符串与哈希 · 批量 T1（16 道）。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from genkit import CPP_HEADER, finalize, numbers, problem  # noqa: E402

OUT = ROOT / "oj" / "data" / "problems" / "03-string-hash"
P: list = []


def add(**kw):
    P.append(problem(**kw))


def first_line(t):
    return t.split("\n")[0]


# ---------------------------------------------------------------- 1
def s_lower(t):
    return first_line(t).lower() + "\n"


add(
    pid="string-to-lower", title="转换成小写字母", difficulty="入门",
    tags=["字符串", "字符处理"], source="LeetCode 709", url="https://leetcode.cn/problems/to-lower-case/",
    statement="把给定字符串中的**所有大写字母**转成小写，其他字符不变，输出结果。",
    input_format="一行一个字符串 $s$（$0 \\le |s| \\le 10^5$），可含大小写字母、数字与空格。",
    output_format="一行，转换后的字符串。",
    constraints=["0 ≤ |s| ≤ 10^5", "可含字母、数字、空格"],
    solver=s_lower,
    specs=[("样例 1", "Hello", 10), ("样例 2", "here", 10),
           ("样例 3", "LOVELY", 15), ("含数字", "AbC123", 15),
           ("空串", "\n", 20), ("含空格", "Hello World", 20),
           ("无字母", "12345", 20)],
    cpp=CPP_HEADER + """int main(){string s;getline(cin,s);
for(char&c:s)if(c>='A'&&c<='Z')c=c-'A'+'a';
printf("%s\\n",s.c_str());return 0;}
""",
    hint="**逐字符判断**：若字符在 `'A'..'Z'` 范围内，就加上 `'a' - 'A'`（即 32）。\n\n时间 $O(n)$。\n\n> **易错点**：输入可能含空格，要用 `getline` 而不是 `cin >>`。",
)

# ---------------------------------------------------------------- 2
def s_rev_letters(t):
    s = first_line(t)
    ls = list(s)
    i, j = 0, len(ls) - 1
    while i < j:
        while i < j and not ls[i].isalpha():
            i += 1
        while i < j and not ls[j].isalpha():
            j -= 1
        ls[i], ls[j] = ls[j], ls[i]
        i += 1
        j -= 1
    return "".join(ls) + "\n"


add(
    pid="string-reverse-only-letters", title="仅仅反转字母", difficulty="简单",
    tags=["字符串", "双指针"], source="LeetCode 917", url="https://leetcode.cn/problems/reverse-only-letters/",
    statement="给定字符串 $s$，**只反转其中的字母**，所有非字母字符保持**原来的位置**。",
    input_format="一行一个字符串（长度 $1 \\le |s| \\le 100$），可含字母与 ASCII 可见字符。",
    output_format="一行，处理后的字符串。",
    constraints=["1 ≤ |s| ≤ 100", "字母保持大小写"],
    solver=s_rev_letters,
    specs=[("样例 1", "ab-cd", 10), ("样例 2", "a-bC-dEf-ghIj", 10),
           ("样例 3", "Test1ng-Leet=code-Q!", 15), ("全字母", "abc", 15),
           ("全非字母", "1-2=3", 20), ("单字母", "a", 20),
           ("单非字母", "1", 20)],
    cpp=CPP_HEADER + """int main(){string s;getline(cin,s);
int i=0,j=(int)s.size()-1;
while(i<j){
while(i<j&&!isalpha((unsigned char)s[i]))++i;
while(i<j&&!isalpha((unsigned char)s[j]))--j;
swap(s[i],s[j]);++i;--j;}
printf("%s\\n",s.c_str());return 0;}
""",
    hint="**相向双指针 + 跳过非字母**：左指针找字母、右指针找字母，找到就交换。\n\n> **易错点**：内层 while 也要带 `i < j` 边界，否则可能越界。",
)

# ---------------------------------------------------------------- 3
def s_detect_capital(t):
    w = first_line(t)
    ok = (w == w.upper() or w == w.lower()
          or (w[0].isupper() and w[1:] == w[1:].lower()))
    return ("YES\n" if ok else "NO\n")


add(
    pid="string-detect-capital", title="检测大写字母", difficulty="入门",
    tags=["字符串", "模拟"], source="LeetCode 520", url="https://leetcode.cn/problems/detect-capital/",
    statement="判断一个单词的大写用法是否**正确**。正确的情况只有三种：\n\n1. 全部字母都是大写（如 `USA`）；\n2. 全部字母都是小写（如 `leetcode`）；\n3. 只有**首字母**大写（如 `Google`）。\n\n正确输出 `YES`，否则 `NO`。",
    input_format="一行一个单词 $w$（$1 \\le |w| \\le 100$），仅含大小写英文字母。",
    output_format="一行，输出 `YES` 或 `NO`。",
    constraints=["1 ≤ |w| ≤ 100", "仅含英文字母"],
    solver=s_detect_capital,
    specs=[("样例 1（正确）", "USA", 10), ("样例 2（错误）", "FlaG", 10),
           ("全小写", "leetcode", 15), ("首字母大写", "Google", 15),
           ("单字母大写", "A", 20), ("单字母小写", "a", 20),
           ("中间大写", "gooGle", 20)],
    cpp=CPP_HEADER + """bool allUpper(const string&s){for(char c:s)if(!isupper((unsigned char)c))return false;return true;}
bool allLower(const string&s){for(char c:s)if(!islower((unsigned char)c))return false;return true;}
int main(){string w;cin>>w;
bool ok=allUpper(w)||allLower(w)||(isupper((unsigned char)w[0])&&allLower(w.substr(1)));
printf("%s\\n",ok?"YES":"NO");return 0;}
""",
    hint="**三种情况分别判断**：\n\n1. 全大写；2. 全小写；3. 首字母大写且其余全小写。\n\n时间 $O(n)$。",
)

# ---------------------------------------------------------------- 4
def s_count_segments(t):
    s = first_line(t)
    return f"{len(s.split())}\n"


add(
    pid="string-count-segments", title="字符串中的单词数", difficulty="入门",
    tags=["字符串", "模拟"], source="LeetCode 434", url="https://leetcode.cn/problems/number-of-segments-in-a-string/",
    statement="统计字符串中**单词的个数**。单词指**连续的、不含空格**的字符序列。\n\n注意字符串**可能有前导/连续空格**，这些都不计入单词。",
    input_format="一行一个字符串（$0 \\le |s| \\le 10^5$），可含空格与 ASCII 可见字符。",
    output_format="一行一个整数，表示单词数。",
    constraints=["0 ≤ |s| ≤ 10^5", "空格分隔，可能有连续空格"],
    solver=s_count_segments,
    specs=[("样例 1", "Hello, my name is John", 10), ("样例 2", "Hello", 10),
           ("空串", "\n", 15), ("全空格", "     ", 15),
           ("前导空格", "   a b", 20), ("多个连续空格", "a   b    c", 20),
           ("单个空格", " ", 20)],
    cpp=CPP_HEADER + """int main(){string s;getline(cin,s);
stringstream ss(s);string w;int c=0;
while(ss>>w)++c;
printf("%d\\n",c);return 0;}
""",
    hint="**按空白切分**：用 `stringstream >> word` 自动跳过所有连续空格。\n\n> **易错点**：不要用「空格数 + 1」这种算法——前导空格和连续空格都会算错。",
)

# ---------------------------------------------------------------- 5
def s_roman_to_int(t):
    s = first_line(t)
    val = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    res = 0
    for i, c in enumerate(s):
        if i + 1 < len(s) and val[c] < val[s[i + 1]]:
            res -= val[c]
        else:
            res += val[c]
    return f"{res}\n"


add(
    pid="string-roman-to-int", title="罗马数字转整数", difficulty="简单",
    tags=["字符串", "哈希表", "模拟"], source="LeetCode 13", url="https://leetcode.cn/problems/roman-integer/",
    statement="把给定的罗马数字转换为整数。\n\n罗马数字规则：\n\n- `I=1, V=5, X=10, L=50, C=100, D=500, M=1000`；\n- 通常从左到右**从大到小**排列并相加；\n- 特殊规则：若**小值在大值左边**，则表示**相减**（如 `IV=4`、`IX=9`、`XL=40`）。\n\n输入保证是合法的罗马数字（范围 $1 \\sim 3999$）。",
    input_format="一行一个罗马数字字符串（$1 \\le |s| \\le 15$），仅含 `IVXLCDM`。",
    output_format="一行一个整数。",
    constraints=["1 ≤ 结果 ≤ 3999", "仅含 IVXLCDM"],
    solver=s_roman_to_int,
    specs=[("样例 1", "III", 10), ("样例 2", "LVIII", 10), ("样例 3", "MCMXCIV", 15),
           ("最小", "I", 15), ("最大", "MMMCMXCIX", 20), ("减法规则", "IV", 20),
           ("纯减法组合", "CMXCIX", 20)],
    cpp=CPP_HEADER + """int main(){string s;cin>>s;
unordered_map<char,int>v={{'I',1},{'V',5},{'X',10},{'L',50},{'C',100},{'D',500},{'M',1000}};
int r=0;
for(int i=0;i<(int)s.size();++i){
if(i+1<(int)s.size()&&v[s[i]]<v[s[i+1]])r-=v[s[i]];else r+=v[s[i]];}
printf("%d\\n",r);return 0;}
""",
    hint="**从左往右扫描**：若当前字符的值**小于**右边字符的值，说明构成减法组合，**减去**它；否则**加上**它。\n\n时间 $O(n)$。\n\n> **直觉**：`IV` 中 `I < V`，所以 `-1 + 5 = 4`。",
)

# ---------------------------------------------------------------- 6
def s_int_to_roman(t):
    n = int(t.strip())
    vals = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
            (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
    res = []
    for v, sym in vals:
        while n >= v:
            res.append(sym)
            n -= v
    return "".join(res) + "\n"


add(
    pid="string-int-to-roman", title="整数转罗马数字", difficulty="中等",
    tags=["字符串", "贪心", "模拟"], source="LeetCode 12", url="https://leetcode.cn/problems/integer-to-roman/",
    statement="把 $1 \\sim 3999$ 的整数转换为罗马数字。\n\n需要用到 13 个「值-符号」对，包括 6 个减法组合：`CM(900) CD(400) XC(90) XL(40) IX(9) IV(4)`。",
    input_format="一行一个整数 $n$（$1 \\le n \\le 3999$）。",
    output_format="一行，罗马数字表示。",
    constraints=["1 ≤ n ≤ 3999"],
    solver=s_int_to_roman,
    specs=[("样例 1", "3", 10), ("样例 2", "58", 10), ("样例 3", "1994", 15),
           ("最小", "1", 15), ("最大", "3999", 20), ("整千", "2000", 20),
           ("含减法组合", "944", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);
vector<pair<int,string>>v={{1000,"M"},{900,"CM"},{500,"D"},{400,"CD"},{100,"C"},{90,"XC"},
{50,"L"},{40,"XL"},{10,"X"},{9,"IX"},{5,"V"},{4,"IV"},{1,"I"}};
string r;
for(auto&pr:v)while(n>=pr.first){r+=pr.second;n-=pr.first;}
printf("%s\\n",r.c_str());return 0;}
""",
    hint="**贪心 + 13 个值表**：把值从大到小排列，每次能减就减，并追加对应符号。\n\n> **关键**：必须把 6 个减法组合（900、400、90、40、9、4）也放进表里，否则 `4` 会输出 `IIII` 而不是 `IV`。",
)

# ---------------------------------------------------------------- 7
def s_add_strings(t):
    ls = t.strip("\n").split("\n")
    a, b = ls[0].strip(), ls[1].strip()
    i, j = len(a) - 1, len(b) - 1
    carry = 0
    res = []
    while i >= 0 or j >= 0 or carry:
        s = carry
        if i >= 0:
            s += int(a[i]); i -= 1
        if j >= 0:
            s += int(b[j]); j -= 1
        res.append(str(s % 10))
        carry = s // 10
    return "".join(reversed(res)) + "\n"


add(
    pid="string-add-strings", title="字符串相加", difficulty="简单",
    tags=["字符串", "模拟", "大数"], source="LeetCode 415", url="https://leetcode.cn/problems/add-strings/",
    statement="给定两个**非负整数字符串**，返回它们的和（同样以字符串表示）。\n\n**不能**把字符串直接转成整数（数字可能非常大）。",
    input_format="第一行一个数字字符串 $a$。\n\n第二行一个数字字符串 $b$。\n\n长度均不超过 $10^4$，无前导零（除非为 \"0\"）。",
    output_format="一行，两数之和的字符串表示。",
    constraints=["|a|, |b| ≤ 10^4", "无前导零", "不允许转成整数"],
    solver=s_add_strings,
    specs=[("样例 1", "11\n123", 10), ("样例 2", "456\n77", 10),
           ("零加零", "0\n0", 15), ("含进位链", "999\n1", 15),
           ("长度不等", "1\n9999", 20), ("大数", "9999999999\n1", 20),
           ("无进位", "123\n456", 20)],
    cpp=CPP_HEADER + """int main(){string a,b;cin>>a>>b;
int i=a.size()-1,j=b.size()-1,carry=0;string r;
while(i>=0||j>=0||carry){int s=carry;
if(i>=0)s+=a[i--]-'0';
if(j>=0)s+=b[j--]-'0';
r+=(char)('0'+s%10);carry=s/10;}
reverse(r.begin(),r.end());
printf("%s\\n",r.c_str());return 0;}
""",
    hint="**模拟竖式加法**：从**最低位**开始逐位相加，维护进位 `carry`。\n\n每轮的和是「进位 + 两个对应位（若存在）」，当前位为 `s % 10`，新进位为 `s / 10`。\n\n最后把结果**反转**输出。时间 $O(n)$。",
)

# ---------------------------------------------------------------- 8
def s_add_binary(t):
    ls = t.strip("\n").split("\n")
    a, b = ls[0].strip(), ls[1].strip()
    i, j = len(a) - 1, len(b) - 1
    carry = 0
    res = []
    while i >= 0 or j >= 0 or carry:
        s = carry
        if i >= 0:
            s += int(a[i]); i -= 1
        if j >= 0:
            s += int(b[j]); j -= 1
        res.append(str(s % 2))
        carry = s // 2
    return "".join(reversed(res)) + "\n"


add(
    pid="string-add-binary", title="二进制求和", difficulty="简单",
    tags=["字符串", "位运算", "模拟"], source="LeetCode 67", url="https://leetcode.cn/problems/add-binary/",
    statement="给定两个**二进制字符串**，返回它们的和（二进制字符串）。",
    input_format="第一行一个二进制字符串 $a$。\n\n第二行一个二进制字符串 $b$。\n\n长度均不超过 $10^4$，无前导零（除非为 \"0\"）。",
    output_format="一行，两数之和的二进制表示（无前导零）。",
    constraints=["|a|, |b| ≤ 10^4", "无前导零", "仅含 0 和 1"],
    solver=s_add_binary,
    specs=[("样例 1", "11\n1", 10), ("样例 2", "1010\n1011", 10),
           ("零加零", "0\n0", 15), ("全 1 进位", "1111\n1", 15),
           ("长度不等", "1\n1111", 20), ("长串", "1111111111\n1", 20),
           ("无进位", "100\n10", 20)],
    cpp=CPP_HEADER + """int main(){string a,b;cin>>a>>b;
int i=a.size()-1,j=b.size()-1,carry=0;string r;
while(i>=0||j>=0||carry){int s=carry;
if(i>=0)s+=a[i--]-'0';
if(j>=0)s+=b[j--]-'0';
r+=(char)('0'+s%2);carry=s/2;}
reverse(r.begin(),r.end());
printf("%s\\n",r.c_str());return 0;}
""",
    hint="**与十进制字符串相加完全同构**，只是进制从 10 变成 2：当前位 `s % 2`，进位 `s / 2`。\n\n> 也可以先把二进制转成十进制整数再相加（本题数据范围内 `long long` 够用），但大数场景必须用字符串模拟。",
)

# ---------------------------------------------------------------- 9
def s_compress(t):
    ls = t.strip("\n").split("\n")
    chars = ls[0].split()
    res = []
    i = 0
    while i < len(chars):
        j = i
        while j < len(chars) and chars[j] == chars[i]:
            j += 1
        res.append(chars[i])
        if j - i > 1:
            res.extend(list(str(j - i)))
        i = j
    return " ".join(res) + "\n"


add(
    pid="string-compress-chars", title="压缩字符串", difficulty="中等",
    tags=["字符串", "双指针", "原地"], source="LeetCode 443", url="https://leetcode.cn/problems/string-compression/",
    statement="用「字符 + 连续出现次数」的方式压缩字符数组：\n\n- 只出现 1 次的字符后面**不写数字**；\n- 次数为多位数时，**逐位拆开**写入。\n\n例如 `['a','a','b','b','c','c','c']` 压缩为 `['a','2','b','2','c','3']`。\n\n请输出压缩后的序列。",
    input_format="第一行若干个以空格分隔的字符（$1 \\le n \\le 2000$），每个为单个小写字母。",
    output_format="一行，压缩后的字符序列，以空格分隔。",
    constraints=["1 ≤ n ≤ 2000", "仅小写字母", "次数为多位数时逐位拆开"],
    solver=s_compress,
    specs=[("样例 1", "a a b b c c c", 10), ("全不同", "a b c", 10),
           ("全相同", "a a a a", 15), ("单个", "a", 15),
           ("次数为两位数", " ".join(["a"] * 12), 20),
           ("两段", "a a a b b", 20),
           ("次数为三位数", " ".join(["x"] * 100), 20)],
    cpp=CPP_HEADER + """int main(){vector<char>a;char buf[8];
while(scanf("%s",buf)==1)a.push_back(buf[0]);
vector<char>r;
int i=0,n=a.size();
while(i<n){int j=i;while(j<n&&a[j]==a[i])++j;
r.push_back(a[i]);
if(j-i>1){string num=to_string(j-i);for(char c:num)r.push_back(c);}
i=j;}
for(size_t k=0;k<r.size();++k){if(k)printf(" ");printf("%c",r[k]);}
printf("\\n");return 0;}
""",
    hint="**读写双指针 + 计数**：用 `i` 指向当前字符组的开头，`j` 向后找组尾。\n\n输出该字符；若组长度 > 1，把长度的**十进制各位**依次追加。\n\n> **易错点**：长度 10 以上要**逐位拆开**（`12` 写成 `'1'` 和 `'2'` 两个字符），不能当成一个整体。",
)

# ---------------------------------------------------------------- 10
def s_license_key(t):
    ls = t.strip("\n").split("\n")
    s = ls[0].strip()
    k = int(ls[1])
    s2 = "".join(c for c in s if c != "-").upper()
    res = []
    first = len(s2) % k
    if first:
        res.append(s2[:first])
    for i in range(first, len(s2), k):
        res.append(s2[i:i + k])
    return "-".join(res) + "\n"


add(
    pid="string-license-key", title="密钥格式化", difficulty="简单",
    tags=["字符串", "模拟"], source="LeetCode 482", url="https://leetcode.cn/problems/license-key-formatting/",
    statement="给定密钥字符串 $s$（含字母、数字和 `-`）与整数 $k$，重新格式化：\n\n1. 去掉所有 `-`，并把字母转为**大写**；\n2. 从**左到右**按每 $k$ 个字符分组，组间用 `-` 连接；\n3. 若第一组不足 $k$ 个，则**第一组较短**，其余每组恰好 $k$ 个。",
    input_format="第一行一个字符串 $s$（$1 \\le |s| \\le 10^5$），含字母、数字、`-`。\n\n第二行一个整数 $k$（$1 \\le k \\le 10^4$）。",
    output_format="一行，格式化后的密钥。",
    constraints=["1 ≤ |s| ≤ 10^5", "1 ≤ k ≤ 10^4", "字母转大写"],
    solver=s_license_key,
    specs=[("样例 1", "5F3Z-2e-9-w\n4", 10), ("样例 2", "2-5g-3-J\n2", 10),
           ("无连字符", "abc\n2", 15), ("k 整除长度", "abcd\n2", 15),
           ("含多个连字符", "a-b-c-d\n2", 20), ("k 大于长度", "ab\n5", 20),
           ("单个字符", "a\n1", 20)],
    cpp=CPP_HEADER + """int main(){string s;int k;cin>>s>>k;
string t;
for(char c:s)if(c!='-')t+=toupper((unsigned char)c);
int n=t.size();int first=n%k;if(first==0)first=k;
string r=t.substr(0,first);
for(int i=first;i<n;i+=k)r+="-"+t.substr(i,k);
printf("%s\\n",r.c_str());return 0;}
""",
    hint="**先清洗再分组**：去掉所有 `-` 并转大写后，令 `first = n % k`（若为 0 则取 $k$）。\n\n先输出前 `first` 个字符，之后每 $k$ 个加一个 `-`。\n\n> **易错点**：第一组的长度是 `n % k`，**不足 $k$ 的是第一组而不是最后一组**。",
)

# ---------------------------------------------------------------- 11
def s_count_binary(t):
    s = first_line(t)
    groups = []
    i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        groups.append(j - i)
        i = j
    res = sum(min(groups[i], groups[i + 1]) for i in range(len(groups) - 1))
    return f"{res}\n"


add(
    pid="string-count-binary-substrings", title="计数二进制子串", difficulty="简单",
    tags=["字符串", "分组", "双指针"], source="LeetCode 696", url="https://leetcode.cn/problems/count-binary-substrings/",
    statement="给定一个只含 `0` 和 `1` 的字符串，统计**满足「连续 0 与连续 1 的个数相同」的子串数量**（子串中所有 0 必须连续、所有 1 也必须连续）。\n\n例如 `00110011` 有 6 个这样的子串：`0011`、`01`、`1100`、`10`、`0011`、`01`。",
    input_format="一行一个字符串 $s$（$1 \\le |s| \\le 10^5$），仅含 `0` 和 `1`。",
    output_format="一行一个整数，表示符合条件的子串数量。",
    constraints=["1 ≤ |s| ≤ 10^5", "仅含 0 和 1"],
    solver=s_count_binary,
    specs=[("样例 1", "00110011", 10), ("样例 2", "10101", 10),
           ("单字符", "0", 15), ("全相同", "0000", 15),
           ("两字符相等", "01", 20), ("交替", "010101", 20),
           ("不等长", "000111", 20)],
    cpp=CPP_HEADER + """int main(){string s;cin>>s;
vector<int>g;int i=0,n=s.size();
while(i<n){int j=i;while(j<n&&s[j]==s[i])++j;g.push_back(j-i);i=j;}
long long r=0;
for(size_t k=0;k+1<g.size();++k)r+=min(g[k],g[k+1]);
printf("%lld\\n",r);return 0;}
""",
    hint="**先分组，再取相邻组最小值之和**：把字符串按连续相同字符切分成若干组，记录每组的长度。\n\n对**每两个相邻组**，它们能组成的合法子串数量是 `min(len[i], len[i+1])`——把所有这些加起来即可。\n\n时间 $O(n)$。",
)

# ---------------------------------------------------------------- 12
def s_repeated_substring(t):
    s = first_line(t)
    n = len(s)
    ok = False
    for L in range(1, n // 2 + 1):
        if n % L == 0 and s[:L] * (n // L) == s:
            ok = True
            break
    return ("YES\n" if ok else "NO\n")


add(
    pid="string-repeated-substring", title="重复的子字符串", difficulty="简单",
    tags=["字符串", "KMP", "枚举"], source="LeetCode 459", url="https://leetcode.cn/problems/repeated-substring-pattern/",
    statement="判断一个非空字符串**能否由它的某个子串重复多次构成**。\n\n例如 `abab` 可以由 `ab` 重复两次构成；`aba` 不行。\n\n是则输出 `YES`，否则 `NO`。",
    input_format="一行一个字符串 $s$（$1 \\le |s| \\le 10^4$），仅含小写英文字母。",
    output_format="一行，输出 `YES` 或 `NO`。",
    constraints=["1 ≤ |s| ≤ 10^4", "仅小写字母"],
    solver=s_repeated_substring,
    specs=[("样例 1（可以）", "abab", 10), ("样例 2（不行）", "aba", 10),
           ("样例 3", "abcabcabcabc", 15), ("单字符", "a", 15),
           ("两字符相同", "aa", 20), ("两字符不同", "ab", 20),
           ("周期为 3", "abcabc", 20)],
    cpp=CPP_HEADER + """int main(){string s;cin>>s;int n=s.size();bool ok=false;
for(int L=1;L<=n/2;++L){if(n%L)continue;
bool good=true;
for(int i=L;i<n&&good;++i)if(s[i]!=s[i-L])good=false;
if(good){ok=true;break;}}
printf("%s\\n",ok?"YES":"NO");return 0;}
""",
    hint="**枚举周期长度**：只需枚举 $L$ 从 $1$ 到 $n/2$，且 $L$ 必须**整除** $n$。\n\n对每个候选 $L$，检查是否所有 `s[i] == s[i-L]`。\n\n时间 $O(n \\cdot \\text{约数个数})$，最坏 $O(n\\sqrt{n})$。\n\n> **更优解法**：用 **KMP 求前缀函数** `pi[n-1]`，若 `n % (n - pi[n-1]) == 0` 则说明存在周期，做到 $O(n)$。",
)

# ---------------------------------------------------------------- 13
def s_isomorphic(t):
    ls = t.strip("\n").split("\n")
    a, b = ls[0].strip(), ls[1].strip()
    if len(a) != len(b):
        return "NO\n"
    m1, m2 = {}, {}
    for x, y in zip(a, b):
        if m1.setdefault(x, y) != y or m2.setdefault(y, x) != x:
            return "NO\n"
    return "YES\n"


add(
    pid="string-isomorphic", title="同构字符串", difficulty="简单",
    tags=["字符串", "哈希表"], source="LeetCode 205", url="https://leetcode.cn/problems/isomorphic-strings/",
    statement="两个字符串**同构**指：$s$ 中每个字符都能被**唯一地**替换成 $t$ 中的对应字符，且不同字符不能映射到同一字符。\n\n字符的**顺序必须保持一致**。\n\n同构输出 `YES`，否则 `NO`。",
    input_format="第一行一个字符串 $s$。\n\n第二行一个字符串 $t$。\n\n长度均不超过 $5\\times10^4$，仅含小写字母。",
    output_format="一行，输出 `YES` 或 `NO`。",
    constraints=["|s|, |t| ≤ 5×10^4", "仅小写字母"],
    solver=s_isomorphic,
    specs=[("样例 1（同构）", "egg\nadd", 10), ("样例 2（不同构）", "foo\nbar", 10),
           ("样例 3（同构）", "paper\ntitle", 15), ("长度不等", "ab\nabc", 15),
           ("单字符", "a\nb", 20), ("全相同", "aaa\nbbb", 20),
           ("多对一", "ab\naa", 20)],
    cpp=CPP_HEADER + """int main(){string s,t;cin>>s>>t;
if(s.size()!=t.size()){printf("NO\\n");return 0;}
int m1[256],m2[256];memset(m1,-1,sizeof(m1));memset(m2,-1,sizeof(m2));
for(size_t i=0;i<s.size();++i){
int x=s[i],y=t[i];
if(m1[x]==-1)m1[x]=y;else if(m1[x]!=y){printf("NO\\n");return 0;}
if(m2[y]==-1)m2[y]=x;else if(m2[y]!=x){printf("NO\\n");return 0;}}
printf("YES\\n");return 0;}
""",
    hint="**双向映射**：维护两个哈希表 `s→t` 和 `t→s`。\n\n遍历时若发现「已有映射但不一致」就判 `NO`。\n\n> **易错点**：**必须双向检查**！只检查 `s→t` 会漏掉 `ab → aa` 这种情况（两个不同字符映射到同一个）。",
)

# ---------------------------------------------------------------- 14
def s_word_pattern(t):
    ls = t.strip("\n").split("\n")
    pattern = ls[0].strip()
    words = ls[1].split()
    if len(pattern) != len(words):
        return "NO\n"
    m1, m2 = {}, {}
    for c, w in zip(pattern, words):
        if m1.setdefault(c, w) != w or m2.setdefault(w, c) != c:
            return "NO\n"
    return "YES\n"


add(
    pid="string-word-pattern", title="单词规律", difficulty="简单",
    tags=["字符串", "哈希表"], source="LeetCode 290", url="https://leetcode.cn/problems/word-pattern/",
    statement="给定一个**模式串** $pattern$（由小写字母组成）和一个由空格分隔的单词串，判断它们是否**遵循同一规律**——即存在**双射**，使得每个模式字母唯一对应一个单词，每个单词也唯一对应一个模式字母。\n\n符合输出 `YES`，否则 `NO`。",
    input_format="第一行一个模式串 $pattern$（$1 \\le |pattern| \\le 300$），仅小写字母。\n\n第二行一个由空格分隔的单词串（单词数不超过 $300$，单词仅含小写字母）。",
    output_format="一行，输出 `YES` 或 `NO`。",
    constraints=["1 ≤ |pattern| ≤ 300", "单词数 ≤ 300", "仅小写字母"],
    solver=s_word_pattern,
    specs=[("样例 1（符合）", "abba\ndog cat cat dog", 10),
           ("样例 2（不符合）", "abba\ndog cat cat fish", 10),
           ("样例 3（不符合）", "aaaa\ndog cat cat dog", 15),
           ("数量不等", "ab\ndog", 15), ("单字母单词", "a\ndog", 20),
           ("全同", "aaa\ndog dog dog", 20), ("多对一", "ab\ndog dog", 20)],
    cpp=CPP_HEADER + """int main(){string pat,line;cin>>pat;
getline(cin,line);          // 吃掉 pattern 所在行的剩余部分
getline(cin,line);          // 读取单词行
stringstream ss(line);vector<string>w;string x;
while(ss>>x)w.push_back(x);
if(pat.size()!=w.size()){printf("NO\\n");return 0;}
unordered_map<char,string>m1;unordered_map<string,char>m2;
for(size_t i=0;i<pat.size();++i){
char c=pat[i];
if(m1.count(c)&&m1[c]!=w[i]){printf("NO\\n");return 0;}
if(m2.count(w[i])&&m2[w[i]]!=c){printf("NO\\n");return 0;}
m1[c]=w[i];m2[w[i]]=c;}
printf("YES\\n");return 0;}
""",
    hint="**与「同构字符串」完全同构**，只是把「字符↔字符」换成「字符↔单词」。\n\n> **易错点**：必须**双向映射**；另外要先检查**单词个数与模式长度是否相等**。",
)

# ---------------------------------------------------------------- 15
def s_buddy(t):
    ls = t.strip("\n").split("\n")
    a, b = ls[0].strip(), ls[1].strip()
    if a == b:
        from collections import Counter
        return ("YES\n" if max(Counter(a).values()) > 1 else "NO\n")
    if len(a) != len(b):
        return "NO\n"
    diff = [(x, y) for x, y in zip(a, b) if x != y]
    if len(diff) != 2:
        return "NO\n"
    return ("YES\n" if diff[0] == diff[1][::-1] else "NO\n")


add(
    pid="string-buddy-strings", title="亲密字符串", difficulty="简单",
    tags=["字符串", "哈希表"], source="LeetCode 859", url="https://leetcode.cn/problems/buddy-strings/",
    statement="判断能否**恰好交换** $s$ 中的**两个字符**，使得结果等于 $goal$。\n\n可以交换任意两个位置（包括内容相同的位置）。\n\n能则输出 `YES`，否则 `NO`。\n\n> 注意：若 $s == goal$，则必须存在**至少一个重复字符**，否则交换后必然不相等。",
    input_format="第一行一个字符串 $s$。\n\n第二行一个字符串 $goal$。\n\n长度均不超过 $2\\times10^4$，仅含小写字母。",
    output_format="一行，输出 `YES` 或 `NO`。",
    constraints=["|s|, |goal| ≤ 2×10^4", "仅小写字母"],
    solver=s_buddy,
    specs=[("样例 1（可以）", "ab\nba", 10), ("样例 2（不行）", "ab\nab", 10),
           ("样例 3", "aa\naa", 15), ("长度不等", "ab\nabc", 15),
           ("三处不同", "abc\ncba", 20), ("完全一致且有重复", "aab\n aab".strip(), 20),
           ("完全一致且无重复", "abc\nabc", 20)],
    cpp=CPP_HEADER + """int main(){string s,g;cin>>s>>g;
if(s==g){int c[26]={0};for(char x:s)++c[x-'a'];
for(int i=0;i<26;++i)if(c[i]>1){printf("YES\\n");return 0;}
printf("NO\\n");return 0;}
if(s.size()!=g.size()){printf("NO\\n");return 0;}
vector<int>d;
for(size_t i=0;i<s.size();++i)if(s[i]!=g[i])d.push_back(i);
if(d.size()!=2){printf("NO\\n");return 0;}
printf("%s\\n",(s[d[0]]==g[d[1]]&&s[d[1]]==g[d[0]])?"YES":"NO");return 0;}
""",
    hint="**分两种情况**：\n\n**情况一：`s == goal`** —— 必须存在**重复字符**（交换两个相同的字符，结果不变），否则不可能。\n\n**情况二：`s != goal`** —— 找出所有不同的位置，**必须恰好 2 处**，且交换后能对应上（即 `s[i]==goal[j]` 且 `s[j]==goal[i]`）。\n\n> **最易漏的点**：`s == goal` 时的「重复字符」判断——很多解法只处理了不同位置的情况。",
)

# ---------------------------------------------------------------- 16
def s_first_palindrome(t):
    words = first_line(t).split()
    for w in words:
        if w == w[::-1]:
            return f"{w}\n"
    return "\n"


add(
    pid="string-first-palindrome", title="数组中的第一个回文串", difficulty="入门",
    tags=["字符串", "双指针"], source="LeetCode 2108", url="https://leetcode.cn/problems/find-first-palindromic-string-in-the-array/",
    statement="给定一组单词，找出其中**第一个回文单词**并输出。\n\n若不存在回文单词，输出空行。",
    input_format="一行若干个以空格分隔的单词（$1 \\le$ 单词数 $\\le 100$），每个仅含小写字母，长度不超过 $100$。",
    output_format="一行，第一个回文单词；不存在则输出空行。",
    constraints=["单词数 ≤ 100", "仅小写字母", "单词长度 ≤ 100"],
    solver=s_first_palindrome,
    specs=[("样例 1", "abc car ada racecar cool", 10),
           ("样例 2（无回文）", "notapalindrome racecar", 10),
           ("样例 3（无回文）", "def ghi", 15),
           ("第一个就是", "aba xyz", 15), ("单字符", "a", 20),
           ("单个非回文", "ab", 20), ("多个回文", "aa bb cc", 20)],
    cpp=CPP_HEADER + """int main(){string w;
while(cin>>w){string r=w;reverse(r.begin(),r.end());
if(r==w){printf("%s\\n",w.c_str());return 0;}}
printf("\\n");return 0;}
""",
    hint="**逐个判断**：按顺序检查每个单词是否回文（`w == reverse(w)`），**第一个**满足的就是答案。\n\n时间 $O(总字符数)$。",
)


def main() -> None:
    for p in P:
        finalize(p, OUT / f"{p['id']}.json")
        total = sum(t["score"] for t in p["tests"])
        print(f"生成 {p['id']:36s} {len(p['tests'])} 测试点, 总分 {total:3d}")


if __name__ == "__main__":
    main()
