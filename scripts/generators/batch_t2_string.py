"""字符串与哈希 · 批量 T2（14 道）。"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from genkit import CPP_HEADER, finalize, problem  # noqa: E402

OUT = ROOT / "oj" / "data" / "problems" / "03-string-hash"
P: list = []


def add(**kw):
    P.append(problem(**kw))


def L(t):
    return t.strip("\n").split("\n")


def fl(t):
    return t.split("\n")[0]


# ---------------------------------------------------------------- 1
def s_remove_vowels(t):
    s = fl(t)
    return "".join(c for c in s if c.lower() not in "aeiou") + "\n"


add(
    pid="string-remove-vowels", title="删除字符串中的元音字母", difficulty="入门",
    tags=["字符串", "字符处理"], source="字符串基础", url="https://leetcode.cn/problems/reverse-vowels-of-a-string/",
    statement="给定一个字符串，**删除其中所有元音字母**（`a`、`e`、`i`、`o`、`u`，不分大小写），输出结果。",
    input_format="一行一个字符串 $s$（$0 \\le |s| \\le 10^5$），可含字母、数字与空格。",
    output_format="一行，删除元音后的字符串。",
    constraints=["0 ≤ |s| ≤ 10^5", "元音不分大小写"],
    solver=s_remove_vowels,
    specs=[("样例 1", "leetcode", 10), ("样例 2", "aeiou", 10),
           ("空串", "\n", 15), ("无元音", "xyz", 15),
           ("含大写", "AEIOUabc", 20), ("含空格", "hello world", 20)],
    cpp=CPP_HEADER + """int main(){string s;getline(cin,s);
string r;
for(char c:s){
char l=tolower((unsigned char)c);
if(l=='a'||l=='e'||l=='i'||l=='o'||l=='u')continue;
r+=c;}
printf("%s\\n",r.c_str());return 0;}
""",
    hint="**逐字符过滤**：把字符转成小写后判断是否为元音，不是就保留。\n\n> **易错点**：输入可能含空格，要用 `getline`；元音判断**不分大小写**。",
)

# ---------------------------------------------------------------- 2
def s_first_twice(t):
    s = fl(t)
    seen = set()
    for c in s:
        if c in seen:
            return f"{c}\n"
        seen.add(c)
    return "\n"


add(
    pid="string-first-char-twice", title="第一个出现两次的字母", difficulty="入门",
    tags=["字符串", "哈希表"], source="LeetCode 2351", url="https://leetcode.cn/problems/first-letter-to-appear-twice/",
    statement="给定一个小写字母字符串，找出**第一个出现两次**的字母并输出。\n\n**保证**至少有一个字母出现两次。",
    input_format="一行一个字符串 $s$（$2 \\le |s| \\le 100$），仅含小写字母。",
    output_format="一行，第一个出现两次的字母。",
    constraints=["2 ≤ |s| ≤ 100", "仅小写字母", "保证存在答案"],
    solver=s_first_twice,
    specs=[("样例 1", "abccbaacz", 10), ("样例 2", "abcdd", 10),
           ("相邻重复", "aabb", 15), ("首尾相同", "abca", 15),
           ("两字符", "aa", 20), ("多次出现", "abcabc", 20)],
    cpp=CPP_HEADER + """int main(){string s;cin>>s;bool seen[26]={false};
for(char c:s){
int i=c-'a';
if(seen[i]){printf("%c\\n",c);return 0;}
seen[i]=true;}
printf("\\n");return 0;}
""",
    hint="**边扫描边记录**：用一个布尔数组记录「已经出现过」的字母，遇到重复立即返回。\n\n时间 $O(n)$。",
)

# ---------------------------------------------------------------- 3
def s_defang_ip(t):
    s = fl(t)
    return s.replace(".", "[.]") + "\n"


add(
    pid="string-defang-ip", title="IP 地址无效化", difficulty="入门",
    tags=["字符串", "替换"], source="LeetCode 1108", url="https://leetcode.cn/problems/defanging-an-ip-address/",
    statement="把 IP 地址中的每个 `.` 替换成 `[.]`，输出结果。",
    input_format="一行一个字符串，为合法的 IPv4 地址（如 `192.168.1.1`）。",
    output_format="一行，替换后的字符串。",
    constraints=["字符串为合法 IPv4 地址"],
    solver=s_defang_ip,
    specs=[("样例 1", "1.1.1.1", 10), ("样例 2", "255.100.50.0", 10),
           ("三个点", "0.0.0.0", 15), ("普通地址", "192.168.1.1", 15),
           ("含大数字", "111.222.333.444", 20), ("全零", "0.0.0.1", 20)],
    cpp=CPP_HEADER + """int main(){string s;cin>>s;string r;
for(char c:s){if(c=='.')r+="[.]";else r+=c;}
printf("%s\\n",r.c_str());return 0;}
""",
    hint="**逐字符替换**：遇到 `.` 就输出 `[.]`，否则原样输出。\n\n时间 $O(n)$。",
)

# ---------------------------------------------------------------- 4
def s_max_power(t):
    s = fl(t)
    best = cur = 1
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            cur += 1
            best = max(best, cur)
        else:
            cur = 1
    return f"{best}\n"


add(
    pid="string-max-power", title="连续字符", difficulty="入门",
    tags=["字符串", "遍历"], source="LeetCode 1446", url="https://leetcode.cn/problems/consecutive-characters/",
    statement="求字符串中**只含一种字符的最长连续子串**的长度。",
    input_format="一行一个字符串 $s$（$1 \\le |s| \\le 10^5$），仅含小写字母。",
    output_format="一行一个整数。",
    constraints=["1 ≤ |s| ≤ 10^5", "仅小写字母"],
    solver=s_max_power,
    specs=[("样例 1", "leetcode", 10), ("样例 2", "abbcccddddeeeeedcba", 10),
           ("单字符", "a", 15), ("全相同", "aaaa", 15),
           ("两段", "aabbbbaa", 20), ("最长在末尾", "abcccccc", 20)],
    cpp=CPP_HEADER + """int main(){string s;cin>>s;int best=1,cur=1;
for(size_t i=1;i<s.size();++i){
if(s[i]==s[i-1]){++cur;best=max(best,cur);}else cur=1;}
printf("%d\\n",best);return 0;}
""",
    hint="**一次遍历**：维护当前连续长度 `cur` 和最大值 `best`。\n\n遇到相同字符 `cur++`，否则重置为 1。时间 $O(n)$。",
)

# ---------------------------------------------------------------- 5
def s_balanced_split(t):
    s = fl(t)
    bal = cnt = 0
    for c in s:
        bal += 1 if c == "L" else -1
        if bal == 0:
            cnt += 1
    return f"{cnt}\n"


add(
    pid="string-balanced-split", title="分割平衡字符串", difficulty="简单",
    tags=["字符串", "贪心", "计数"], source="LeetCode 1221", url="https://leetcode.cn/problems/split-a-string-in-balanced-strings/",
    statement="**平衡字符串**指其中 `L` 和 `R` 的数量相等。\n\n给定一个平衡字符串，把它**尽可能多地**分割成若干个平衡子串，求最多能分成几段。",
    input_format="一行一个字符串 $s$（$2 \\le |s| \\le 1000$，长度为偶数），仅含 `L` 和 `R`，且整体平衡。",
    output_format="一行一个整数。",
    constraints=["2 ≤ |s| ≤ 1000", "仅含 L 和 R", "整体平衡"],
    solver=s_balanced_split,
    specs=[("样例 1", "RLRRLLRLRL", 10), ("样例 2", "RLLLLRRRLR", 10),
           ("两段", "LR", 15), ("四段", "LRLRLRLR", 15),
           ("两大段", "LLRRLLRR", 20), ("嵌套", "RLRLRLRL", 20)],
    cpp=CPP_HEADER + """int main(){string s;cin>>s;int bal=0,cnt=0;
for(char c:s){bal+=(c=='L')?1:-1;if(bal==0)++cnt;}
printf("%d\\n",cnt);return 0;}
""",
    hint="**贪心计数**：遍历时 `L` 加一、`R` 减一，**每当计数归零就切一刀**。\n\n> **为什么贪心最优**：每凑成一个平衡前缀就立刻切分，不会影响后面——因为后面本身也是平衡的。\n\n时间 $O(n)$。",
)

# ---------------------------------------------------------------- 6
def s_pangram(t):
    s = fl(t)
    letters = {c.lower() for c in s if c.isalpha()}
    return ("YES\n" if len(letters) == 26 else "NO\n")


add(
    pid="string-check-pangram", title="判断全字母句", difficulty="入门",
    tags=["字符串", "哈希集合"], source="LeetCode 1832", url="https://leetcode.cn/problems/check-if-the-sentence-is-pangram/",
    statement="**全字母句**指包含了英文字母表中**所有 26 个字母**的句子（不区分大小写）。\n\n是全字母句输出 `YES`，否则 `NO`。",
    input_format="一行一个字符串 $s$（$1 \\le |s| \\le 1000$），仅含小写英文字母。",
    output_format="一行，输出 `YES` 或 `NO`。",
    constraints=["1 ≤ |s| ≤ 1000", "仅小写字母"],
    solver=s_pangram,
    specs=[("样例 1（是）", "thequickbrownfoxjumpsoverthelazydog", 10),
           ("样例 2（不是）", "leetcode", 10), ("单字符", "a", 15),
           ("26 个字母", "abcdefghijklmnopqrstuvwxyz", 15),
           ("缺一个", "abcdefghijklmnopqrstuvwxy", 20),
           ("重复但不全", "aaaaaaaaaaaaaaaaaaaaaaaaaa", 20)],
    cpp=CPP_HEADER + """int main(){string s;cin>>s;bool seen[26]={false};int c=0;
for(char ch:s){int i=ch-'a';if(!seen[i]){seen[i]=true;++c;}}
printf("%s\\n",c==26?"YES":"NO");return 0;}
""",
    hint="**用集合去重**：统计出现了多少种不同字母，等于 26 就是全字母句。\n\n时间 $O(n)$。",
)

# ---------------------------------------------------------------- 7
def s_goal_parser(t):
    s = fl(t)
    return s.replace("()", "o").replace("(al)", "al") + "\n"


add(
    pid="string-goal-parser", title="设计 Goal 解析器", difficulty="入门",
    tags=["字符串", "替换"], source="LeetCode 1678", url="https://leetcode.cn/problems/goal-parser-interpretation/",
    statement="把命令字符串按以下规则解析：\n\n- `G` → `G`；\n- `()` → `o`；\n- `(al)` → `al`。",
    input_format="一行一个字符串 $s$（$1 \\le |s| \\le 100$），仅含 `G`、`()`、`(al)` 三种片段。",
    output_format="一行，解析后的字符串。",
    constraints=["1 ≤ |s| ≤ 100", "仅含三种片段"],
    solver=s_goal_parser,
    specs=[("样例 1", "G()(al)", 10), ("样例 2", "G()()()()(al)", 10),
           ("只有 G", "GGGG", 15), ("只有 ()", "()()()", 15),
           ("只有 (al)", "(al)(al)", 20), ("混合", "G(al)G()G", 20)],
    cpp=CPP_HEADER + """int main(){string s;cin>>s;string r;
for(size_t i=0;i<s.size();){
if(s[i]=='G'){r+='G';++i;}
else if(s[i]=='('&&i+1<s.size()&&s[i+1]==')'){r+='o';i+=2;}
else{r+="al";i+=4;}}
printf("%s\\n",r.c_str());return 0;}
""",
    hint="**从左到右识别三种片段**：\n\n- `G`：长度 1；\n- `()`：长度 2；\n- `(al)`：长度 4。\n\n时间 $O(n)$。",
)

# ---------------------------------------------------------------- 8
def s_truncate(t):
    ls = L(t)
    s = ls[0].strip()
    k = int(ls[1])
    words = s.split()
    return " ".join(words[:k]) + "\n"


add(
    pid="string-truncate-sentence", title="截断句子", difficulty="入门",
    tags=["字符串", "模拟"], source="LeetCode 1816", url="https://leetcode.cn/problems/truncate-sentence/",
    statement="给定一个由空格分隔的单词组成的句子和整数 $k$，输出**前 $k$ 个单词**（用单个空格连接）。",
    input_format="第一行一个句子（单词数 $1 \\le n \\le 500$，单词仅含小写字母，单词间用单个空格分隔）。\n\n第二行一个整数 $k$（$1 \\le k \\le n$）。",
    output_format="一行，前 $k$ 个单词。",
    constraints=["单词数 ≤ 500", "仅小写字母", "单词间单个空格"],
    solver=s_truncate,
    specs=[("样例 1", "Hello how are you Contestant\n4", 10),
           ("样例 2", "What is the solution to this problem\n4", 10),
           ("k = 1", "a b c\n1", 15), ("k = n", "a b c\n3", 15),
           ("单单词", "hello\n1", 20), ("长句", "one two three four five\n2", 20)],
    cpp=CPP_HEADER + """int main(){string line;getline(cin,line);int k;scanf("%d",&k);
stringstream ss(line);string w;bool first=true;int c=0;
while(ss>>w&&c<k){if(!first)printf(" ");printf("%s",w.c_str());first=false;++c;}
printf("\\n");return 0;}
""",
    hint="**切分后取前 $k$ 个**：用 `stringstream` 或 `split` 切分单词，输出前 $k$ 个并用单空格连接。\n\n时间 $O(n)$。",
)

# ---------------------------------------------------------------- 9
def s_capitalize_title(t):
    ls = L(t)
    title = ls[0].strip()
    out = []
    for w in title.split():
        if len(w) <= 2:                     # 长度 ≤ 2 的单词全部小写
            out.append(w.lower())
        else:
            out.append(w[0].upper() + w[1:].lower())
    return " ".join(out) + "\n"


add(
    pid="string-capitalize-title", title="将标题首字母大写", difficulty="简单",
    tags=["字符串", "模拟"], source="LeetCode 2129", url="https://leetcode.cn/problems/capitalize-the-title/",
    statement="把标题中每个单词改成「**首字母大写、其余字母小写**」。\n\n**特例**：长度为 1 或 2 的单词**全部转成小写**。\n\n单词间用单个空格分隔。",
    input_format="第一行一个标题字符串（长度 $1 \\le |s| \\le 100$），由空格分隔的字母单词组成。",
    output_format="一行，处理后的标题。",
    constraints=["1 ≤ |s| ≤ 100", "仅含字母与空格"],
    solver=s_capitalize_title,
    specs=[("样例 1", "capiTalIze tHe titLe", 10),
           ("样例 2", "First leTTeR of EACH Word", 10),
           ("全短词", "a bc def", 15), ("全大写", "HELLO WORLD", 15),
           ("单词", "a", 20), ("长标题", "tHe QUICK brown FOX", 20)],
    cpp=CPP_HEADER + """int main(){string line;getline(cin,line);
stringstream ss(line);string w;bool first=true;
while(ss>>w){
if(w.size()<=2)for(char&c:w)c=tolower((unsigned char)c);
else{w[0]=toupper((unsigned char)w[0]);
for(size_t i=1;i<w.size();++i)w[i]=tolower((unsigned char)w[i]);}
if(!first)printf(" ");printf("%s",w.c_str());first=false;}
printf("\\n");return 0;}
""",
    hint="**逐单词处理**：长度 $\\le 2$ 的单词全小写，否则首字母大写、其余小写。\n\n> **易错点**：`toupper` / `tolower` 的返回值是 `int`，赋给 `char` 前建议显式转换。",
)

# ---------------------------------------------------------------- 10
def s_reverse_prefix(t):
    ls = L(t)
    s = ls[0].strip()
    ch = ls[1].strip()
    idx = s.find(ch)
    if idx == -1:
        return s + "\n"
    return s[:idx + 1][::-1] + s[idx + 1:] + "\n"


add(
    pid="string-reverse-prefix", title="反转单词前缀", difficulty="入门",
    tags=["字符串", "双指针"], source="LeetCode 2000", url="https://leetcode.cn/problems/reverse-prefix-of-word/",
    statement="给定字符串 $s$ 和一个字符 $ch$，找出 $ch$ 在 $s$ 中**第一次出现**的位置，"
              "把从开头到该位置（含）的**前缀反转**，其余部分保持不变。\n\n若 $ch$ 不存在，返回原字符串。",
    input_format="第一行一个字符串 $s$（$1 \\le |s| \\le 250$），仅含小写字母。\n\n第二行一个字符 $ch$（小写字母）。",
    output_format="一行，处理后的字符串。",
    constraints=["1 ≤ |s| ≤ 250", "仅小写字母"],
    solver=s_reverse_prefix,
    specs=[("样例 1", "abcdefd\nd", 10),
           ("样例 2", "xyxzxe\nz", 10),
           ("字符不存在", "abcd\n z", 15),
           ("字符在开头", "abcd\n a", 15), ("字符在末尾", "abcd\n d", 20),
           ("单字符", "a\n a", 20)],
    cpp=CPP_HEADER + """int main(){string s,ch;cin>>s>>ch;
size_t p=s.find(ch[0]);
if(p==string::npos){printf("%s\\n",s.c_str());return 0;}
reverse(s.begin(),s.begin()+p+1);
printf("%s\\n",s.c_str());return 0;}
""",
    hint="**找到位置后反转前缀**：用 `find` 定位，再用 `reverse` 反转 $[0, p]$ 区间。\n\n时间 $O(n)$。",
)

# ---------------------------------------------------------------- 11
def s_count_matches(t):
    ls = L(t)
    n = int(ls[0])
    items = ls[1].split()
    rule_key, rule_val = ls[2].strip().split(":")
    idx = {"type": 0, "color": 1, "name": 2}[rule_key]
    cnt = 0
    for it in items:
        parts = it.split(":")
        if parts[idx] == rule_val:
            cnt += 1
    return f"{cnt}\n"


add(
    pid="string-count-matches", title="统计匹配的规则项", difficulty="简单",
    tags=["字符串", "哈希表", "计数"], source="LeetCode 1773", url="https://leetcode.cn/problems/count-items-matching-a-rule/",
    statement="给定若干物品，每个物品用 `type:color:name` 描述。\n\n再给定一条规则 `ruleKey:ruleValue`，统计满足该规则的物品个数。\n\n`ruleKey` 只会是 `type`、`color`、`name` 之一。",
    input_format="第一行一个整数 $n$（$1 \\le n \\le 10^4$）。\n\n第二行 $n$ 个物品描述，以空格分隔，每个形如 `type:color:name`（三段均为小写字母）。\n\n第三行一个规则 `ruleKey:ruleValue`。",
    output_format="一行一个整数。",
    constraints=["1 ≤ n ≤ 10^4", "三段均为小写字母", "ruleKey ∈ {type, color, name}"],
    solver=s_count_matches,
    specs=[("样例 1", "3\nphone:blue:pixel phone:red:mi phone:blue:note\ntype:phone", 10),
           ("匹配 color", "2\nphone:blue:pixel phone:red:mi\ncolor:red", 10),
           ("匹配 name", "2\nphone:blue:pixel phone:red:mi\nname:mi", 15),
           ("无匹配", "1\nphone:blue:pixel\ntype:book", 15),
           ("单物品", "1\na:b:c\ntype:a", 20),
           ("全部匹配", "3\nx:y:z x:y:z x:y:z\ntype:x", 20)],
    cpp=CPP_HEADER + """int main(){int n;scanf("%d",&n);
vector<string>items(n);
for(int i=0;i<n;++i)cin>>items[i];
string rule;cin>>rule;
size_t pos=rule.find(':');
string key=rule.substr(0,pos),val=rule.substr(pos+1);
int idx=(key=="type")?0:(key=="color"?1:2);
int cnt=0;
for(auto&it:items){
size_t p1=it.find(':'),p2=it.find(':',p1+1);
string segs[3]={it.substr(0,p1),it.substr(p1+1,p2-p1-1),it.substr(p2+1)};
if(segs[idx]==val)++cnt;}
printf("%d\\n",cnt);return 0;}
""",
    hint="**按规则字段拆分比较**：把每个物品按 `:` 拆成三段，根据 `ruleKey` 决定比较哪一段。\n\n时间 $O(n)$。",
)

# ---------------------------------------------------------------- 12
def s_shuffle_string(t):
    ls = L(t)
    s = ls[0].strip()
    idx = list(map(int, ls[1].split()))
    res = [""] * len(s)
    for i, p in enumerate(idx):
        res[p] = s[i]
    return "".join(res) + "\n"


add(
    pid="string-shuffle", title="重新排列字符串", difficulty="入门",
    tags=["字符串", "数组", "模拟"], source="LeetCode 1528", url="https://leetcode.cn/problems/shuffle-string/",
    statement="给定字符串 $s$ 和一个下标数组 $indices$，把 $s[i]$ 放到新字符串的 `indices[i]` 位置。\n\n输出重排后的字符串。",
    input_format="第一行一个字符串 $s$（$1 \\le |s| \\le 100$），仅含小写字母。\n\n第二行 $|s|$ 个整数，为 $0 \\sim |s|-1$ 的一个排列。",
    output_format="一行，重排后的字符串。",
    constraints=["1 ≤ |s| ≤ 100", "indices 是 0..n−1 的排列"],
    solver=s_shuffle_string,
    specs=[("样例 1", "codeleet\n4 5 6 7 0 2 1 3", 10),
           ("样例 2", "abc\n0 1 2", 10), ("逆序", "abc\n2 1 0", 15),
           ("单字符", "a\n0", 15), ("交换两字符", "ab\n1 0", 20),
           ("部分移动", "abcd\n1 0 3 2", 20)],
    cpp=CPP_HEADER + """int main(){string s;cin>>s;int n=s.size();
vector<int>idx(n);
for(int i=0;i<n;++i)scanf("%d",&idx[i]);
string r(n,' ');
for(int i=0;i<n;++i)r[idx[i]]=s[i];
printf("%s\\n",r.c_str());return 0;}
""",
    hint="**直接按映射放置**：新建结果字符串，把 `s[i]` 放到 `r[indices[i]]`。\n\n时间 $O(n)$。",
)

# ---------------------------------------------------------------- 13
def s_count_asterisks(t):
    s = fl(t)
    bars = [i for i, c in enumerate(s) if c == "|"]
    if len(bars) < 2:
        return "0\n"
    return f"{s.count('*', bars[0], bars[1])}\n"


add(
    pid="string-count-asterisks", title="统计星号", difficulty="入门",
    tags=["字符串", "遍历"], source="LeetCode 2315", url="https://leetcode.cn/problems/count-asterisks/",
    statement="给定一个字符串，统计**位于前两个 `|` 之间**的 `*` 的个数。\n\n若字符串中不足 2 个 `|`，输出 $0$。",
    input_format="一行一个字符串 $s$（$1 \\le |s| \\le 1000$），仅含 `*`、`|` 和小写字母。",
    output_format="一行一个整数。",
    constraints=["1 ≤ |s| ≤ 1000", "不足 2 个 | 时输出 0"],
    solver=s_count_asterisks,
    specs=[("样例 1", "l|*e*et|c**o|*de|", 10),
           ("样例 2", "iamprogrammer", 10),
           ("样例 3", "yo|uar|e**|b|e***au|tifu|l", 15),
           ("两竖线相邻", "a||b*c", 15),
           ("星号在外", "a*|b|c*", 20),
           ("全在中间", "|***|", 20)],
    cpp=CPP_HEADER + """int main(){string s;cin>>s;
vector<int>bars;
for(int i=0;i<(int)s.size();++i)if(s[i]=='|')bars.push_back(i);
if(bars.size()<2){printf("0\\n");return 0;}
int c=0;
for(int i=bars[0]+1;i<bars[1];++i)if(s[i]=='*')++c;
printf("%d\\n",c);return 0;}
""",
    hint="**定位前两个 `|`**：找出前两个竖线的下标，统计它们之间的 `*` 个数。\n\n> **注意**：样例 2 没有竖线，但题面说「保证至少 2 个」——为稳妥起见，代码里仍做了兜底返回 0。",
)

# ---------------------------------------------------------------- 14
def s_reverse_vowels(t):
    s = fl(t)
    vowels = "aeiouAEIOU"
    arr = list(s)
    i, j = 0, len(arr) - 1
    while i < j:
        while i < j and arr[i] not in vowels:
            i += 1
        while i < j and arr[j] not in vowels:
            j -= 1
        arr[i], arr[j] = arr[j], arr[i]
        i += 1
        j -= 1
    return "".join(arr) + "\n"


add(
    pid="string-reverse-vowels", title="反转字符串中的元音字母", difficulty="简单",
    tags=["字符串", "双指针"], source="LeetCode 345", url="https://leetcode.cn/problems/reverse-vowels-of-a-string/",
    statement="给定一个字符串，**只反转其中的元音字母**（`a`、`e`、`i`、`o`、`u`，不分大小写），其余字符位置不变。",
    input_format="一行一个字符串 $s$（$1 \\le |s| \\le 3\\times10^5$），可含字母、数字与符号。",
    output_format="一行，处理后的字符串。",
    constraints=["1 ≤ |s| ≤ 3×10^5", "元音不分大小写"],
    solver=s_reverse_vowels,
    specs=[("样例 1", "hello", 10), ("样例 2", "leetcode", 10),
           ("无元音", "xyz", 15), ("全元音", "aeiou", 15),
           ("含大写", "aA", 20), ("含数字", "a1e2i", 20)],
    cpp=CPP_HEADER + """bool isV(char c){char l=tolower((unsigned char)c);
return l=='a'||l=='e'||l=='i'||l=='o'||l=='u';}
int main(){string s;getline(cin,s);
int i=0,j=(int)s.size()-1;
while(i<j){
while(i<j&&!isV(s[i]))++i;
while(i<j&&!isV(s[j]))--j;
swap(s[i],s[j]);++i;--j;}
printf("%s\\n",s.c_str());return 0;}
""",
    hint="**相向双指针**：左右指针都只停在元音上，交换后同时向中间移动。\n\n> **易错点**：内层 while 也要带 `i < j` 边界，否则可能越界或死循环。",
)


def main() -> None:
    for p in P:
        finalize(p, OUT / f"{p['id']}.json")
        total = sum(t["score"] for t in p["tests"])
        print(f"生成 {p['id']:36s} {len(p['tests'])} 测试点, 总分 {total:3d}")


if __name__ == "__main__":
    main()
