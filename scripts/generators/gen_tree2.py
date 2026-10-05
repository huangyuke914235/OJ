"""生成「树与二叉树」分类的第二批题目。

题目统一采用 LeetCode 风格的层序序列表示二叉树：
空格分隔的整数表示节点值，`null` 表示空节点，末尾多余的 `null` 省略。
"""
from __future__ import annotations

import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from genkit import build_tests, finalize  # noqa: E402

OUT = ROOT / "oj" / "data" / "problems" / "04-tree"


# ============================================================ 树工具
class Node:
    __slots__ = ("v", "l", "r")

    def __init__(self, v):
        self.v = v
        self.l = None
        self.r = None


def build(vals):
    """由层序序列构造二叉树。"""
    if not vals or vals[0] == "null":
        return None
    root = Node(int(vals[0]))
    q = deque([root])
    i = 1
    while q and i < len(vals):
        cur = q.popleft()
        if i < len(vals):
            if vals[i] != "null":
                cur.l = Node(int(vals[i]))
                q.append(cur.l)
            i += 1
        if i < len(vals):
            if vals[i] != "null":
                cur.r = Node(int(vals[i]))
                q.append(cur.r)
            i += 1
    return root


def serialize(root) -> str:
    """把二叉树序列化为层序序列，末尾 null 省略。"""
    if root is None:
        return "null"
    out = []
    q = deque([root])
    while q:
        n = q.popleft()
        if n is None:
            out.append("null")
        else:
            out.append(str(n.v))
            q.append(n.l)
            q.append(n.r)
    while out and out[-1] == "null":
        out.pop()
    return " ".join(out)


def parse_line(text: str):
    return text.strip().split()


# ============================================================ 1. 翻转二叉树
def solve_invert(text: str) -> str:
    vals = parse_line(text)

    def rec(n):
        if n is None:
            return None
        n.l, n.r = rec(n.r), rec(n.l)
        return n

    return serialize(rec(build(vals))) + "\n"


INV_SPECS = [
    ("样例 1", "4 2 7 1 3 6 9", 10),
    ("样例 2（单节点）", "1", 10),
    ("空树", "null", 10),
    ("只有左子树", "1 2 null 3", 15),
    ("只有右子树", "1 null 2 null 3", 15),
    ("完全二叉树", "1 2 3 4 5 6 7", 20),
    ("链状树", "1 2 null 3 null 4", 20),
]


def build_invert() -> dict:
    tests = build_tests(INV_SPECS, solve_invert)
    return {
        "id": "tree-invert",
        "title": "翻转二叉树",
        "difficulty": "入门",
        "tags": ["树", "二叉树", "递归"],
        "source": {
            "name": "LeetCode 226 / 递归入门",
            "url": "https://leetcode.cn/problems/invert-binary-tree/",
        },
        "statement": (
            "给定一棵二叉树的层序序列，请把它**翻转**（左右镜像），并输出翻转后的层序序列。\n\n"
            "翻转的定义：交换每个节点的左右子树。\n\n"
            "输出时，**末尾多余的 `null` 需要省略**；若树为空，输出 `null`。"
        ),
        "input_format": (
            "一行，表示二叉树的层序序列，用空格分隔。整数表示节点值，`null` 表示空节点。\n\n"
            "$0 \\le$ 节点数 $\\le 10^5$，节点值 $|v| \\le 10^9$。若树为空，该行为 `null`。"
        ),
        "output_format": "一行，输出翻转后二叉树的层序序列（末尾多余的 `null` 省略）。空树输出 `null`。",
        "constraints": ["0 ≤ 节点数 ≤ 10^5", "|v| ≤ 10^9", "层序表示，null 表示空节点"],
        "samples": [
            {"input": "4 2 7 1 3 6 9\n", "output": "4 7 2 9 6 3 1\n",
             "explain": "根 4 的左右子树互换，递归地每一层都互换，得到镜像树。"},
            {"input": "1\n", "output": "1\n",
             "explain": "只有一个节点，翻转后不变。"},
        ],
        "hint": (
            "**递归**：对每个节点，先递归翻转它的左右子树，然后交换 `left` 和 `right` 指针。\n\n"
            "```\n"
            "TreeNode* invert(TreeNode* root) {\n"
            "    if (!root) return nullptr;\n"
            "    swap(root->left, root->right);   // 交换左右\n"
            "    invert(root->left);              // 递归处理\n"
            "    invert(root->right);\n"
            "    return root;\n"
            "}\n"
            "```\n\n"
            "交换与递归的**先后顺序无所谓**，因为两棵子树的处理互不影响。\n\n"
            "> **易错点**：输出层序序列时，要删掉末尾多余的 `null`，"
            "否则会多出大量无意义的占位符。"
        ),
        "starter_code": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <vector>\n"
                "#include <string>\n"
                "#include <queue>\n"
                "#include <iostream>\n\n"
                "struct Node {\n"
                "    long long v;\n"
                "    Node *l = nullptr, *r = nullptr;\n"
                "};\n\n"
                "// TODO: 翻转二叉树，然后按层序输出（末尾 null 省略）\n\n"
                "int main() {\n"
                "    std::vector<std::string> tok;\n"
                "    std::string t;\n"
                "    while (std::cin >> t) tok.push_back(t);\n"
                "    // TODO\n"
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
                "#include <queue>\n"
                "#include <iostream>\n\n"
                "struct Node {\n"
                "    long long v;\n"
                "    Node *l = nullptr, *r = nullptr;\n"
                "};\n\n"
                "Node* buildTree(const std::vector<std::string> &t) {\n"
                "    if (t.empty() || t[0] == \"null\") return nullptr;\n"
                "    Node *root = new Node{std::stoll(t[0])};\n"
                "    std::queue<Node*> q;\n"
                "    q.push(root);\n"
                "    size_t i = 1;\n"
                "    while (!q.empty() && i < t.size()) {\n"
                "        Node *cur = q.front(); q.pop();\n"
                "        if (i < t.size()) {\n"
                "            if (t[i] != \"null\") { cur->l = new Node{std::stoll(t[i])}; q.push(cur->l); }\n"
                "            ++i;\n"
                "        }\n"
                "        if (i < t.size()) {\n"
                "            if (t[i] != \"null\") { cur->r = new Node{std::stoll(t[i])}; q.push(cur->r); }\n"
                "            ++i;\n"
                "        }\n"
                "    }\n"
                "    return root;\n"
                "}\n\n"
                "Node* invert(Node *n) {\n"
                "    if (!n) return nullptr;\n"
                "    std::swap(n->l, n->r);\n"
                "    invert(n->l);\n"
                "    invert(n->r);\n"
                "    return n;\n"
                "}\n\n"
                "int main() {\n"
                "    std::vector<std::string> tok;\n"
                "    std::string t;\n"
                "    while (std::cin >> t) tok.push_back(t);\n"
                "    if (tok.empty()) tok.push_back(\"null\");\n\n"
                "    Node *root = invert(buildTree(tok));\n\n"
                "    if (!root) { printf(\"null\\n\"); return 0; }   // 空树单独处理\n\n"
                "    // 层序输出，末尾 null 省略\n"
                "    std::vector<std::string> out;\n"
                "    std::queue<Node*> q;\n"
                "    q.push(root);\n"
                "    while (!q.empty()) {\n"
                "        Node *n = q.front(); q.pop();\n"
                "        if (!n) { out.push_back(\"null\"); continue; }\n"
                "        out.push_back(std::to_string(n->v));\n"
                "        q.push(n->l);\n"
                "        q.push(n->r);\n"
                "    }\n"
                "    while (!out.empty() && out.back() == \"null\") out.pop_back();\n"
                "    for (size_t i = 0; i < out.size(); ++i) {\n"
                "        if (i) printf(\" \");\n"
                "        printf(\"%s\", out[i].c_str());\n"
                "    }\n"
                "    printf(\"\\n\");\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "time_limit": 2.0,
    }


# ============================================================ 2. 二叉树的最小深度
def solve_min_depth(text: str) -> str:
    """最小深度：叶子才终止，单侧为空时不能取 min(0, x)。"""
    root = build(parse_line(text))
    if root is None:
        return "0\n"

    def rec(n):
        if n is None:
            return 0
        if n.l is None and n.r is None:
            return 1
        if n.l is None:
            return 1 + rec(n.r)
        if n.r is None:
            return 1 + rec(n.l)
        return 1 + min(rec(n.l), rec(n.r))

    return f"{rec(root)}\n"


MD_SPECS = [
    ("样例 1", "3 9 20 null null 15 7", 10),
    ("样例 2（链状）", "1 2 null 3 null 4", 10),
    ("空树", "null", 10),
    ("单节点", "5", 15),
    ("只有右子树", "1 null 2 null 3", 15),
    ("完全平衡", "1 2 3 4 5 6 7", 20),
    ("左深右浅", "1 2 3 4 null null null", 20),
]


def build_min_depth() -> dict:
    tests = build_tests(MD_SPECS, solve_min_depth)
    return {
        "id": "tree-min-depth",
        "title": "二叉树的最小深度",
        "difficulty": "简单",
        "tags": ["树", "二叉树", "递归", "BFS"],
        "source": {
            "name": "LeetCode 111 / 递归边界",
            "url": "https://leetcode.cn/problems/minimum-depth-of-binary-tree/",
        },
        "statement": (
            "给定一棵二叉树的层序序列，求它的**最小深度**。\n\n"
            "**最小深度**的定义：从根节点到**最近的叶子节点**的节点数量。\n\n"
            "**叶子节点**指**没有左右孩子**的节点。\n\n"
            "若树为空，最小深度为 $0$。"
        ),
        "input_format": (
            "一行，表示二叉树的层序序列，用空格分隔。整数表示节点值，`null` 表示空节点。\n\n"
            "$0 \\le$ 节点数 $\\le 10^5$。若树为空，该行为 `null`。"
        ),
        "output_format": "一行一个整数，表示最小深度。空树输出 `0`。",
        "constraints": ["0 ≤ 节点数 ≤ 10^5", "层序表示", "叶子 = 左右孩子都为空"],
        "samples": [
            {"input": "3 9 20 null null 15 7\n", "output": "2\n",
             "explain": "根 3 的左孩子 9 就是叶子，路径 3→9 长度为 2，这是最短的。"},
            {"input": "1 2 null 3 null 4\n", "output": "4\n",
             "explain": "每个节点都只有一个孩子，形成一条链，唯一的叶子是 4，深度为 4。"},
        ],
        "hint": (
            "**递归**，但要注意一个**极易踩的坑**：\n\n"
            "不能简单写成 `1 + min(depth(left), depth(right))`。"
            "因为当某一侧为空时，它的深度返回 $0$，"
            "`min(0, 真实深度)` 会错误地取到 $0$。\n\n"
            "正确做法是分类讨论：\n"
            "- 左右都空 → 是叶子，返回 $1$；\n"
            "- 只有左 → 返回 `1 + depth(left)`（**不能取 min**）；\n"
            "- 只有右 → 返回 `1 + depth(right)`；\n"
            "- 左右都有 → 返回 `1 + min(depth(left), depth(right))`。\n\n"
            "> 对比：求**最大深度**时直接取 `max` 就没这个问题，因为 $0$ 不会影响最大值。"
        ),
        "starter_code": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <vector>\n"
                "#include <string>\n"
                "#include <queue>\n"
                "#include <iostream>\n\n"
                "struct Node {\n"
                "    long long v;\n"
                "    Node *l = nullptr, *r = nullptr;\n"
                "};\n\n"
                "// TODO: 求最小深度（注意单侧为空的情况）\n\n"
                "int main() {\n"
                "    std::vector<std::string> tok;\n"
                "    std::string t;\n"
                "    while (std::cin >> t) tok.push_back(t);\n"
                "    // TODO\n"
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
                "#include <queue>\n"
                "#include <algorithm>\n"
                "#include <iostream>\n\n"
                "struct Node {\n"
                "    long long v;\n"
                "    Node *l = nullptr, *r = nullptr;\n"
                "};\n\n"
                "Node* buildTree(const std::vector<std::string> &t) {\n"
                "    if (t.empty() || t[0] == \"null\") return nullptr;\n"
                "    Node *root = new Node{std::stoll(t[0])};\n"
                "    std::queue<Node*> q;\n"
                "    q.push(root);\n"
                "    size_t i = 1;\n"
                "    while (!q.empty() && i < t.size()) {\n"
                "        Node *cur = q.front(); q.pop();\n"
                "        if (i < t.size()) {\n"
                "            if (t[i] != \"null\") { cur->l = new Node{std::stoll(t[i])}; q.push(cur->l); }\n"
                "            ++i;\n"
                "        }\n"
                "        if (i < t.size()) {\n"
                "            if (t[i] != \"null\") { cur->r = new Node{std::stoll(t[i])}; q.push(cur->r); }\n"
                "            ++i;\n"
                "        }\n"
                "    }\n"
                "    return root;\n"
                "}\n\n"
                "int minDepth(Node *n) {\n"
                "    if (!n) return 0;\n"
                "    if (!n->l && !n->r) return 1;          // 叶子\n"
                "    if (!n->l) return 1 + minDepth(n->r);  // 不能取 min\n"
                "    if (!n->r) return 1 + minDepth(n->l);\n"
                "    return 1 + std::min(minDepth(n->l), minDepth(n->r));\n"
                "}\n\n"
                "int main() {\n"
                "    std::vector<std::string> tok;\n"
                "    std::string t;\n"
                "    while (std::cin >> t) tok.push_back(t);\n"
                "    if (tok.empty()) tok.push_back(\"null\");\n"
                "    printf(\"%d\\n\", minDepth(buildTree(tok)));\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "time_limit": 2.0,
    }


# ============================================================ 3. 路径总和
def solve_path_sum(text: str) -> str:
    """是否存在根到叶子的路径，节点值之和等于目标。"""
    parts = text.strip().split("\n")
    vals = parts[0].strip().split()
    target = int(parts[1].strip())
    root = build(vals)

    def rec(n, rest):
        if n is None:
            return False
        rest -= n.v
        if n.l is None and n.r is None:
            return rest == 0
        return rec(n.l, rest) or rec(n.r, rest)

    return ("YES\n" if rec(root, target) else "NO\n")


PS_SPECS = [
    ("样例 1（存在）", "5 4 8 11 null 13 4 7 2 null null null 1\n22", 10),
    ("样例 2（不存在）", "1 2 3\n5", 10),
    ("空树", "null\n0", 10),
    ("单节点命中", "5\n5", 15),
    ("单节点未命中", "5\n3", 15),
    ("含负数", "1 -2 -3\n-1", 20),
    ("只有左链", "1 2 null 3\n6", 20),
]


def build_path_sum() -> dict:
    tests = build_tests(PS_SPECS, solve_path_sum)
    return {
        "id": "tree-path-sum",
        "title": "路径总和",
        "difficulty": "简单",
        "tags": ["树", "二叉树", "递归", "DFS"],
        "source": {
            "name": "LeetCode 112 / 递归回溯",
            "url": "https://leetcode.cn/problems/path-sum/",
        },
        "statement": (
            "给定一棵二叉树和一个目标和 $target$，判断树中是否存在**从根节点到叶子节点**的路径，"
            "使得路径上所有节点值之和等于 $target$。\n\n"
            "**叶子节点**指**没有左右孩子**的节点。路径必须**终止于叶子**，"
            "不能在中途某个节点就停下。\n\n"
            "若存在这样的路径输出 `YES`，否则输出 `NO`。"
        ),
        "input_format": (
            "第一行，二叉树的层序序列，空格分隔，`null` 表示空节点。\n\n"
            "第二行，一个整数 $target$（$-10^9 \\le target \\le 10^9$）。\n\n"
            "$0 \\le$ 节点数 $\\le 10^5$。"
        ),
        "output_format": "一行，输出 `YES` 或 `NO`。",
        "constraints": ["0 ≤ 节点数 ≤ 10^5", "|target| ≤ 10^9", "路径必须终止于叶子"],
        "samples": [
            {"input": "5 4 8 11 null 13 4 7 2 null null null 1\n22\n", "output": "YES\n",
             "explain": "路径 5 → 4 → 11 → 2 的和是 22，且 2 是叶子，满足条件。"},
            {"input": "1 2 3\n5\n", "output": "NO\n",
             "explain": "所有根到叶子的路径和为 1+2=3 或 1+3=4，都不等于 5。"},
        ],
        "hint": (
            "**递归（自顶向下）**：把「剩余需要的和」作为参数往下传。\n\n"
            "到达节点 $u$ 时，剩余和变为 `rest - u->val`。若 $u$ 是**叶子**"
            "（左右都空），判断剩余和是否为 $0$；否则递归左右子树，只要有一侧成立即可。\n\n"
            "```\n"
            "bool dfs(Node* n, long long rest) {\n"
            "    if (!n) return false;\n"
            "    rest -= n->v;\n"
            "    if (!n->l && !n->r) return rest == 0;   // 必须到叶子\n"
            "    return dfs(n->l, rest) || dfs(n->r, rest);\n"
            "}\n"
            "```\n\n"
            "> **易错点**：不能在 `rest == 0` 时立即返回 true——必须确认当前节点是叶子。"
            "否则形如「1 → 2，target=1」会误判成 YES。"
        ),
        "starter_code": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <vector>\n"
                "#include <string>\n"
                "#include <queue>\n"
                "#include <iostream>\n\n"
                "struct Node {\n"
                "    long long v;\n"
                "    Node *l = nullptr, *r = nullptr;\n"
                "};\n\n"
                "// TODO: 判断是否存在根到叶子的路径和为 target\n\n"
                "int main() {\n"
                "    std::string line;\n"
                "    std::getline(std::cin, line);\n"
                "    long long target;\n"
                "    scanf(\"%lld\", &target);\n"
                "    // TODO\n"
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
                "#include <queue>\n"
                "#include <sstream>\n"
                "#include <iostream>\n\n"
                "struct Node {\n"
                "    long long v;\n"
                "    Node *l = nullptr, *r = nullptr;\n"
                "};\n\n"
                "Node* buildTree(const std::vector<std::string> &t) {\n"
                "    if (t.empty() || t[0] == \"null\") return nullptr;\n"
                "    Node *root = new Node{std::stoll(t[0])};\n"
                "    std::queue<Node*> q;\n"
                "    q.push(root);\n"
                "    size_t i = 1;\n"
                "    while (!q.empty() && i < t.size()) {\n"
                "        Node *cur = q.front(); q.pop();\n"
                "        if (i < t.size()) {\n"
                "            if (t[i] != \"null\") { cur->l = new Node{std::stoll(t[i])}; q.push(cur->l); }\n"
                "            ++i;\n"
                "        }\n"
                "        if (i < t.size()) {\n"
                "            if (t[i] != \"null\") { cur->r = new Node{std::stoll(t[i])}; q.push(cur->r); }\n"
                "            ++i;\n"
                "        }\n"
                "    }\n"
                "    return root;\n"
                "}\n\n"
                "bool dfs(Node *n, long long rest) {\n"
                "    if (!n) return false;\n"
                "    rest -= n->v;\n"
                "    if (!n->l && !n->r) return rest == 0;   // 必须是叶子\n"
                "    return dfs(n->l, rest) || dfs(n->r, rest);\n"
                "}\n\n"
                "int main() {\n"
                "    std::string line;\n"
                "    std::getline(std::cin, line);\n"
                "    long long target;\n"
                "    scanf(\"%lld\", &target);\n\n"
                "    std::istringstream iss(line);\n"
                "    std::vector<std::string> tok;\n"
                "    std::string t;\n"
                "    while (iss >> t) tok.push_back(t);\n"
                "    if (tok.empty()) tok.push_back(\"null\");\n\n"
                "    printf(\"%s\\n\", dfs(buildTree(tok), target) ? \"YES\" : \"NO\");\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "time_limit": 2.0,
    }


# ============================================================ 4. BST 第 k 小
def solve_bst_kth(text: str) -> str:
    """中序遍历取第 k 个。"""
    parts = text.strip().split("\n")
    root = build(parts[0].strip().split())
    k = int(parts[1].strip())

    seq = []

    def inorder(n):
        if n is None or len(seq) >= k:
            return
        inorder(n.l)
        seq.append(n.v)
        inorder(n.r)

    inorder(root)
    return f"{seq[k - 1]}\n"


BK_SPECS = [
    ("样例 1", "3 1 4 null 2\n1", 10),
    ("样例 2", "5 3 6 2 4 null null 1\n3", 10),
    ("单节点", "7\n1", 10),
    ("取最大", "2 1 3\n3", 15),
    ("取最小", "2 1 3\n1", 15),
    ("左链", "5 4 null 3 null 2 null 1\n2", 20),
    ("完整树", "8 4 12 2 6 10 14\n5", 20),
]


def build_bst_kth() -> dict:
    tests = build_tests(BK_SPECS, solve_bst_kth)
    return {
        "id": "tree-bst-kth-smallest",
        "title": "二叉搜索树中第 k 小的元素",
        "difficulty": "中等",
        "tags": ["树", "二叉搜索树", "中序遍历"],
        "source": {
            "name": "LeetCode 230 / BST 中序遍历",
            "url": "https://leetcode.cn/problems/kth-smallest-element-in-a-bst/",
        },
        "statement": (
            "给定一棵**二叉搜索树**（BST）和一个整数 $k$，求树中**第 $k$ 小**的元素值。\n\n"
            "保证 $1 \\le k \\le$ 节点总数。"
        ),
        "input_format": (
            "第一行，二叉搜索树的层序序列，空格分隔，`null` 表示空节点。\n\n"
            "第二行，一个整数 $k$。\n\n"
            "$1 \\le$ 节点数 $\\le 10^5$，$1 \\le k \\le$ 节点数。"
        ),
        "output_format": "一行，输出第 $k$ 小的元素值。",
        "constraints": ["1 ≤ 节点数 ≤ 10^5", "1 ≤ k ≤ 节点数", "输入保证是合法的 BST"],
        "samples": [
            {"input": "3 1 4 null 2\n1\n", "output": "1\n",
             "explain": "中序遍历得到 `1 2 3 4`，第 1 小是 1。"},
            {"input": "5 3 6 2 4 null null 1\n3\n", "output": "3\n",
             "explain": "中序遍历得到 `1 2 3 4 5 6`，第 3 小是 3。"},
        ],
        "hint": (
            "**利用 BST 的核心性质：中序遍历得到严格递增序列。**\n\n"
            "所以「第 $k$ 小」就是中序遍历序列的第 $k$ 个元素。\n\n"
            "实现时用计数器，中序遍历到第 $k$ 个就可以**提前返回**，不必遍历完整棵树。\n\n"
            "```\n"
            "void inorder(Node* n) {\n"
            "    if (!n || cnt >= k) return;\n"
            "    inorder(n->l);\n"
            "    if (++cnt == k) { ans = n->v; return; }\n"
            "    inorder(n->r);\n"
            "}\n"
            "```\n\n"
            "时间 $O(h + k)$（$h$ 为树高），最坏 $O(n)$。\n\n"
            "> **进阶**：若树经常被修改，可以在每个节点维护「子树节点数」，"
            "这样能像二分一样 $O(h)$ 直接定位，无需遍历。"
        ),
        "starter_code": {
            "cpp": (
                "#include <cstdio>\n"
                "#include <vector>\n"
                "#include <string>\n"
                "#include <queue>\n"
                "#include <iostream>\n\n"
                "struct Node {\n"
                "    long long v;\n"
                "    Node *l = nullptr, *r = nullptr;\n"
                "};\n\n"
                "// TODO: 中序遍历找第 k 小\n\n"
                "int main() {\n"
                "    std::string line;\n"
                "    std::getline(std::cin, line);\n"
                "    int k;\n"
                "    scanf(\"%d\", &k);\n"
                "    // TODO\n"
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
                "#include <queue>\n"
                "#include <sstream>\n"
                "#include <iostream>\n\n"
                "struct Node {\n"
                "    long long v;\n"
                "    Node *l = nullptr, *r = nullptr;\n"
                "};\n\n"
                "Node* buildTree(const std::vector<std::string> &t) {\n"
                "    if (t.empty() || t[0] == \"null\") return nullptr;\n"
                "    Node *root = new Node{std::stoll(t[0])};\n"
                "    std::queue<Node*> q;\n"
                "    q.push(root);\n"
                "    size_t i = 1;\n"
                "    while (!q.empty() && i < t.size()) {\n"
                "        Node *cur = q.front(); q.pop();\n"
                "        if (i < t.size()) {\n"
                "            if (t[i] != \"null\") { cur->l = new Node{std::stoll(t[i])}; q.push(cur->l); }\n"
                "            ++i;\n"
                "        }\n"
                "        if (i < t.size()) {\n"
                "            if (t[i] != \"null\") { cur->r = new Node{std::stoll(t[i])}; q.push(cur->r); }\n"
                "            ++i;\n"
                "        }\n"
                "    }\n"
                "    return root;\n"
                "}\n\n"
                "int k, cnt = 0;\n"
                "long long ans = 0;\n\n"
                "void inorder(Node *n) {\n"
                "    if (!n || cnt >= k) return;\n"
                "    inorder(n->l);\n"
                "    if (++cnt == k) { ans = n->v; return; }\n"
                "    inorder(n->r);\n"
                "}\n\n"
                "int main() {\n"
                "    std::string line;\n"
                "    std::getline(std::cin, line);\n"
                "    scanf(\"%d\", &k);\n\n"
                "    std::istringstream iss(line);\n"
                "    std::vector<std::string> tok;\n"
                "    std::string t;\n"
                "    while (iss >> t) tok.push_back(t);\n\n"
                "    inorder(buildTree(tok));\n"
                "    printf(\"%lld\\n\", ans);\n"
                "    return 0;\n"
                "}\n"
            )
        },
        "time_limit": 2.0,
    }


def main() -> None:
    builders = [build_invert, build_min_depth, build_path_sum, build_bst_kth]
    for b in builders:
        prob = b()
        path = finalize(prob, OUT / f"{prob['id']}.json")
        total = sum(t["score"] for t in prob["tests"])
        print(f"生成 {prob['id']:30s} {len(prob['tests'])} 测试点, 总分 {total:3d}  -> {path.name}")


if __name__ == "__main__":
    main()
