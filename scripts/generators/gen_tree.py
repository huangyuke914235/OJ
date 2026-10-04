"""生成「树与二叉树」分类的题目。

树的输入统一采用**层序（BFS）序列 + null 占位**的表示法，
这是 LeetCode 等平台最通用的做法，便于用户理解与手工构造。
"""
from __future__ import annotations

import sys
from collections import deque
from pathlib import Path
from typing import List, Optional

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from genkit import build_tests, finalize  # noqa: E402

OUT = ROOT / "oj" / "data" / "problems" / "04-tree"


# ---------------------------------------------------------------- 工具

def parse_level_order(text: str) -> Optional[List[Optional[int]]]:
    """把 "1 2 3 null 4" 解析为列表。空串 / "null" 表示空树。"""
    s = text.strip()
    if not s or s == "null":
        return []
    return [None if tok == "null" else int(tok) for tok in s.split()]


def build_tree(vals: List[Optional[int]]):
    """由层序列表构造二叉树（含 None 占位），返回根节点或 None。"""
    if not vals or vals[0] is None:
        return None
    root = [vals[0], None, None]
    q = deque([root])
    i = 1
    while q and i < len(vals):
        node = q.popleft()
        if i < len(vals):
            v = vals[i]; i += 1
            if v is not None:
                node[1] = [v, None, None]
                q.append(node[1])
        if i < len(vals):
            v = vals[i]; i += 1
            if v is not None:
                node[2] = [v, None, None]
                q.append(node[2])
    return root


def level_order_out(root) -> List[str]:
    """层序输出，保留 null 占位（去掉末尾多余的 null）。"""
    if root is None:
        return []
    out: List[str] = []
    q = deque([root])
    while q:
        node = q.popleft()
        if node is None:
            out.append("null")
        else:
            out.append(str(node[0]))
            q.append(node[1])
            q.append(node[2])
    while out and out[-1] == "null":
        out.pop()
    return out


# ============================================================ 1. 二叉树的最大深度
def solve_max_depth(text: str) -> str:
    vals = parse_level_order(text)
    root = build_tree(vals)

    def depth(node) -> int:
        if node is None:
            return 0
        return 1 + max(depth(node[1]), depth(node[2]))

    return f"{depth(root)}\n"


MAX_DEPTH_SPECS = [
    ("样例 1", "3 9 20 null null 15 7", 10),
    ("样例 2（空树）", "null", 10),
    ("只有一个节点", "1", 10),
    ("左斜树", "1 2 null 3 null 4 null", 15),
    ("完全二叉树", "1 2 3 4 5 6 7", 15),
    ("单边链（长度5）", "1 2 null 3 null 4 null 5 null", 20),
    ("不规则", "1 2 3 4 null null 5 6 null 7", 20),
]

# ============================================================ 2. 二叉树中序遍历
def solve_inorder(text: str) -> str:
    vals = parse_level_order(text)
    root = build_tree(vals)
    res: List[str] = []

    def dfs(node) -> None:
        if node is None:
            return
        dfs(node[1])
        res.append(str(node[0]))
        dfs(node[2])

    dfs(root)
    return (" ".join(res) + "\n") if res else "\n"


INORDER_SPECS = [
    ("样例 1", "1 null 2 3", 10),
    ("样例 2（空树）", "null", 10),
    ("单个节点", "5", 10),
    ("完全二叉树", "4 2 6 1 3 5 7", 15),
    ("左斜", "3 2 null 1 null", 15),
    ("右斜", "1 null 2 null 3 null 4", 15),
    ("不规则", "5 3 8 1 4 null 9 null null 7", 25),
]

# ============================================================ 3. 二叉搜索树验证
def solve_bst_validate(text: str) -> str:
    vals = parse_level_order(text)
    root = build_tree(vals)

    def valid(node, lo, hi) -> bool:
        if node is None:
            return True
        v = node[0]
        if lo is not None and v <= lo:
            return False
        if hi is not None and v >= hi:
            return False
        return valid(node[1], lo, v) and valid(node[2], v, hi)

    return "YES\n" if valid(root, None, None) else "NO\n"


BST_SPECS = [
    ("样例 1（合法 BST）", "2 1 3", 10),
    ("样例 2（非法）", "5 1 4 null null 3 6", 10),
    ("空树（视为合法）", "null", 10),
    ("单节点", "1", 10),
    ("相等值非法", "2 2 3", 15),
    ("合法多层", "8 3 10 1 6 null 14 null null 4 7 13", 20),
    ("深层非法", "10 5 15 null null 6 20", 20),
    ("只有右子树", "1 null 2 null 3", 15),
]

# ============================================================ 4. 对称二叉树
def solve_symmetric(text: str) -> str:
    vals = parse_level_order(text)
    root = build_tree(vals)
    if root is None:
        return "YES\n"

    def mirror(a, b) -> bool:
        if a is None and b is None:
            return True
        if a is None or b is None:
            return False
        return a[0] == b[0] and mirror(a[1], b[2]) and mirror(a[2], b[1])

    return "YES\n" if mirror(root[1], root[2]) else "NO\n"


SYMMETRIC_SPECS = [
    ("样例 1（对称）", "1 2 2 3 4 4 3", 10),
    ("样例 2（不对称）", "1 2 2 null 3 null 3", 10),
    ("单节点", "1", 10),
    ("空树", "null", 10),
    ("两层对称", "1 2 2", 15),
    ("值相同但结构不对称", "1 2 2 null 3 3 null", 20),
    ("三层对称", "1 2 2 3 4 4 3 5 6 7 8 8 7 6 5", 25),
]

# ============================================================ 5. 最近公共祖先（BST）
def solve_lca_bst(text: str) -> str:
    """在二叉搜索树中求两个节点的最近公共祖先。输入末行为两个查询值。"""
    lines = text.strip("\n").split("\n")
    vals = parse_level_order(lines[0])
    p, q = [int(x) for x in lines[1].split()]
    root = build_tree(vals)
    node = root
    while node is not None:
        v = node[0]
        if p < v and q < v:
            node = node[1]
        elif p > v and q > v:
            node = node[2]
        else:
            return f"{v}\n"
    return "-1\n"


LCA_SPECS = [
    ("样例 1", "6 2 8 0 4 7 9 null null 3 5\n2 8", 10),
    ("样例 2（同为祖先链）", "6 2 8 0 4 7 9 null null 3 5\n2 4", 15),
    ("根节点为答案", "6 2 8 0 4 7 9\n2 8", 10),
    ("都在右子树", "6 2 8 0 4 7 9\n7 9", 15),
    ("一个节点是另一个的父", "6 2 8 0 4 7 9\n4 5", 20),
    ("单节点树", "5\n5 5", 10),
    ("深树", "20 10 30 5 15 25 35 3 7 12 17\n3 17", 20),
]

# ============================================================ 6. 二叉树的层序遍历
def solve_level_order_traversal(text: str) -> str:
    """层序遍历并**逐层输出**，每层一行。"""
    vals = parse_level_order(text)
    root = build_tree(vals)
    if root is None:
        return "\n"
    lines: List[str] = []
    q = deque([root])
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(str(node[0]))
            if node[1]:
                q.append(node[1])
            if node[2]:
                q.append(node[2])
        lines.append(" ".join(level))
    return "\n".join(lines) + "\n"


LEVEL_ORDER_SPECS = [
    ("样例 1", "3 9 20 null null 15 7", 10),
    ("空树", "null", 10),
    ("单节点", "1", 10),
    ("完全二叉树", "1 2 3 4 5 6 7", 15),
    ("左斜", "1 2 null 3 null", 15),
    ("不规则", "1 2 3 null 4 null 5 6", 20),
    ("三层", "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15", 20),
]


def _mk(id_, title, difficulty, tags, source, statement, input_format, output_format,
        constraints, samples, hint, starter, reference, tests, tl=2.0):
    return {
        "id": id_, "title": title, "difficulty": difficulty, "tags": tags,
        "source": source, "statement": statement, "input_format": input_format,
        "output_format": output_format, "constraints": constraints,
        "samples": samples, "hint": hint,
        "starter_code": {"cpp": starter}, "tests": tests,
        "reference": {"cpp": reference}, "time_limit": tl,
    }


# 所有树题共享的输入格式说明
_TREE_INPUT = (
    "一行，表示二叉树的**层序序列**（广度优先），用空格分隔的整数表示节点值，"
    "`null` 表示该位置没有节点。\n\n"
    "序列末尾多余的 `null` 会被省略。若整棵树为空，该行为 `null`。\n\n"
    "$0 \\le$ 节点数 $\\le 10^5$，节点值 $|v| \\le 10^9$。"
)
_TREE_CONSTRAINTS = ["0 ≤ 节点数 ≤ 10^5", "|节点值| ≤ 10^9", "输入为层序序列，null 表空"]


def build_max_depth() -> dict:
    tests = build_tests(MAX_DEPTH_SPECS, solve_max_depth)
    return _mk(
        "tree-max-depth", "二叉树的最大深度", "入门", ["树", "二叉树", "递归", "DFS"],
        {"name": "LeetCode 104", "url": "https://leetcode.cn/problems/maximum-depth-of-binary-tree/"},
        "给定一棵二叉树，求它的**最大深度**。\n\n"
        "最大深度指从根节点到最远叶子节点的**节点数**。空树的深度为 $0$，只有根节点时为 $1$。",
        _TREE_INPUT, "一行一个整数，表示树的最大深度。", _TREE_CONSTRAINTS,
        [
            {"input": "3 9 20 null null 15 7\n", "output": "3\n",
             "explain": "最长路径是 3→20→15（或 3→20→7），共 3 个节点。"},
            {"input": "null\n", "output": "0\n", "explain": "空树深度为 0。"},
        ],
        "递归定义：$f(node) = 1 + \\max(f(左), f(右))$，空节点返回 $0$。\n\n"
        "也可以层序遍历，每处理完一层深度加一。时间 $O(n)$。",
        "#include <cstdio>\n#include <algorithm>\n\n"
        "struct Node {\n    int val;\n    Node *left, *right;\n    Node(int v) : val(v), left(nullptr), right(nullptr) {}\n};\n\n"
        "int depth(Node* root) {\n    // TODO: 递归求最大深度\n    return 0;\n}\n\n"
        "// 本题主要考察算法，建树代码较长，可参考题目解析\n"
        "int main() {\n    // TODO: 读入层序序列建树并输出 depth(root)\n    return 0;\n}\n",
        "#include <cstdio>\n#include <string>\n#include <vector>\n#include <queue>\n#include <sstream>\n#include <iostream>\n#include <algorithm>\n\n"
        "struct Node {\n    int val;\n    Node *left, *right;\n    Node(int v) : val(v), left(nullptr), right(nullptr) {}\n};\n\n"
        "int depth(Node* node) {\n    if (!node) return 0;\n    return 1 + std::max(depth(node->left), depth(node->right));\n}\n\n"
        "int main() {\n"
        "    std::string line;\n"
        "    std::getline(std::cin, line);\n"
        "    std::istringstream iss(line);\n"
        "    std::vector<std::string> tok;\n"
        "    std::string t;\n"
        "    while (iss >> t) tok.push_back(t);\n"
        "    if (tok.empty() || tok[0] == \"null\") { printf(\"0\\n\"); return 0; }\n\n"
        "    std::vector<Node*> nodes(tok.size(), nullptr);\n"
        "    nodes[0] = new Node(std::stoi(tok[0]));\n"
        "    std::queue<int> q;\n    q.push(0);\n"
        "    size_t i = 1;\n"
        "    while (!q.empty() && i < tok.size()) {\n"
        "        int idx = q.front(); q.pop();\n"
        "        if (i < tok.size()) {\n"
        "            if (tok[i] != \"null\") {\n"
        "                nodes[i] = new Node(std::stoi(tok[i]));\n"
        "                nodes[idx]->left = nodes[i];\n                q.push((int)i);\n"
        "            }\n            ++i;\n        }\n"
        "        if (i < tok.size()) {\n"
        "            if (tok[i] != \"null\") {\n"
        "                nodes[i] = new Node(std::stoi(tok[i]));\n"
        "                nodes[idx]->right = nodes[i];\n                q.push((int)i);\n"
        "            }\n            ++i;\n        }\n"
        "    }\n"
        "    printf(\"%d\\n\", depth(nodes[0]));\n    return 0;\n}\n",
        tests,
    )


def build_inorder() -> dict:
    tests = build_tests(INORDER_SPECS, solve_inorder)
    return _mk(
        "tree-inorder", "二叉树的中序遍历", "入门", ["树", "二叉树", "遍历", "递归", "栈"],
        {"name": "LeetCode 94", "url": "https://leetcode.cn/problems/binary-tree-inorder-traversal/"},
        "给定一棵二叉树，输出它的**中序遍历**结果。\n\n"
        "中序遍历的顺序为：**左子树 → 根节点 → 右子树**，递归地进行。\n\n"
        "若树为空，输出空行。",
        _TREE_INPUT, "一行，按中序遍历顺序输出节点值，以空格分隔。空树输出空行。",
        _TREE_CONSTRAINTS,
        [
            {"input": "1 null 2 3\n", "output": "1 3 2\n",
             "explain": "根为 1，右子节点为 2；2 的左子节点为 3。中序访问顺序：1 → 3 → 2。"},
            {"input": "null\n", "output": "\n", "explain": "空树输出空行。"},
        ],
        "递归写法最直观：先递归左子树，再访问根，最后递归右子树。\n\n"
        "进阶：用**显式栈**模拟递归过程，实现 $O(1)$ 额外空间的迭代版本"
        "（Morris 遍历可进一步做到 $O(1)$ 空间）。",
        "#include <cstdio>\n#include <vector>\n\n"
        "struct Node {\n    int val;\n    Node *left, *right;\n    Node(int v) : val(v), left(nullptr), right(nullptr) {}\n};\n\n"
        "void inorder(Node* node, std::vector<int>& out) {\n    // TODO: 递归中序遍历\n}\n\n"
        "int main() {\n    // TODO: 建树 + 输出\n    return 0;\n}\n",
        "#include <cstdio>\n#include <string>\n#include <vector>\n#include <queue>\n#include <sstream>\n#include <iostream>\n\n"
        "struct Node {\n    int val;\n    Node *left, *right;\n    Node(int v) : val(v), left(nullptr), right(nullptr) {}\n};\n\n"
        "void inorder(Node* node, std::vector<int>& out) {\n"
        "    if (!node) return;\n"
        "    inorder(node->left, out);\n    out.push_back(node->val);\n"
        "    inorder(node->right, out);\n}\n\n"
        "int main() {\n"
        "    std::string line;\n"
        "    std::getline(std::cin, line);\n"
        "    std::istringstream iss(line);\n"
        "    std::vector<std::string> tok;\n"
        "    std::string t;\n"
        "    while (iss >> t) tok.push_back(t);\n"
        "    if (tok.empty() || tok[0] == \"null\") { printf(\"\\n\"); return 0; }\n\n"
        "    std::vector<Node*> nodes(tok.size(), nullptr);\n"
        "    nodes[0] = new Node(std::stoi(tok[0]));\n"
        "    std::queue<int> q;\n    q.push(0);\n"
        "    size_t i = 1;\n"
        "    while (!q.empty() && i < tok.size()) {\n"
        "        int idx = q.front(); q.pop();\n"
        "        if (i < tok.size()) {\n"
        "            if (tok[i] != \"null\") {\n"
        "                nodes[i] = new Node(std::stoi(tok[i]));\n"
        "                nodes[idx]->left = nodes[i];\n                q.push((int)i);\n"
        "            }\n            ++i;\n        }\n"
        "        if (i < tok.size()) {\n"
        "            if (tok[i] != \"null\") {\n"
        "                nodes[i] = new Node(std::stoi(tok[i]));\n"
        "                nodes[idx]->right = nodes[i];\n                q.push((int)i);\n"
        "            }\n            ++i;\n        }\n"
        "    }\n"
        "    std::vector<int> out;\n    inorder(nodes[0], out);\n"
        "    for (size_t k = 0; k < out.size(); ++k) {\n"
        "        if (k) printf(\" \");\n        printf(\"%d\", out[k]);\n"
        "    }\n    printf(\"\\n\");\n    return 0;\n}\n",
        tests,
    )


def build_bst_validate() -> dict:
    tests = build_tests(BST_SPECS, solve_bst_validate)
    return _mk(
        "tree-validate-bst", "验证二叉搜索树", "中等", ["树", "二叉搜索树", "递归", "中序遍历"],
        {"name": "LeetCode 98", "url": "https://leetcode.cn/problems/validate-binary-search-tree/"},
        "给定一棵二叉树，判断它是否是**二叉搜索树（BST）**。\n\n"
        "BST 的定义：对于任意节点，其**左子树中所有节点值严格小于它**，"
        "**右子树中所有节点值严格大于它**。\n\n"
        "空树视为合法的 BST。",
        _TREE_INPUT, "一行，若为合法的 BST 输出 `YES`，否则输出 `NO`。", _TREE_CONSTRAINTS,
        [
            {"input": "2 1 3\n", "output": "YES\n", "explain": "左子 1 < 2，右子 3 > 2，合法。"},
            {"input": "5 1 4 null null 3 6\n", "output": "NO\n",
             "explain": "节点 4 位于 5 的右子树中，但 3 < 5，违反了右子树全部大于根的要求。"},
        ],
        "**常见错误**：只比较父子两层的值是不够的，必须保证**整棵子树**都在合法区间内。\n\n"
        "正确做法是递归时传递开区间 $(lo, hi)$：对节点值 $v$，要求 $lo < v < hi$；"
        "递归左子树时上界收紧为 $v$，递归右子树时下界收紧为 $v$。\n\n"
        "等价做法：中序遍历必须是**严格递增**序列。",
        "#include <cstdio>\n#include <vector>\n\n"
        "struct Node {\n    int val;\n    Node *left, *right;\n    Node(int v) : val(v), left(nullptr), right(nullptr) {}\n};\n\n"
        "bool valid(Node* node, long long lo, long long hi) {\n    // TODO: 区间约束递归\n    return true;\n}\n\n"
        "int main() {\n    // TODO\n    return 0;\n}\n",
        "#include <cstdio>\n#include <string>\n#include <vector>\n#include <queue>\n#include <sstream>\n#include <iostream>\n\n"
        "struct Node {\n    int val;\n    Node *left, *right;\n    Node(int v) : val(v), left(nullptr), right(nullptr) {}\n};\n\n"
        "bool valid(Node* node, long long lo, long long hi) {\n"
        "    if (!node) return true;\n"
        "    long long v = node->val;\n"
        "    if (v <= lo || v >= hi) return false;\n"
        "    return valid(node->left, lo, v) && valid(node->right, v, hi);\n}\n\n"
        "int main() {\n"
        "    std::string line;\n"
        "    std::getline(std::cin, line);\n"
        "    std::istringstream iss(line);\n"
        "    std::vector<std::string> tok;\n"
        "    std::string t;\n"
        "    while (iss >> t) tok.push_back(t);\n"
        "    if (tok.empty() || tok[0] == \"null\") { printf(\"YES\\n\"); return 0; }\n\n"
        "    std::vector<Node*> nodes(tok.size(), nullptr);\n"
        "    nodes[0] = new Node(std::stoi(tok[0]));\n"
        "    std::queue<int> q;\n    q.push(0);\n"
        "    size_t i = 1;\n"
        "    while (!q.empty() && i < tok.size()) {\n"
        "        int idx = q.front(); q.pop();\n"
        "        if (i < tok.size()) {\n"
        "            if (tok[i] != \"null\") {\n"
        "                nodes[i] = new Node(std::stoi(tok[i]));\n"
        "                nodes[idx]->left = nodes[i];\n                q.push((int)i);\n"
        "            }\n            ++i;\n        }\n"
        "        if (i < tok.size()) {\n"
        "            if (tok[i] != \"null\") {\n"
        "                nodes[i] = new Node(std::stoi(tok[i]));\n"
        "                nodes[idx]->right = nodes[i];\n                q.push((int)i);\n"
        "            }\n            ++i;\n        }\n"
        "    }\n"
        "    printf(\"%s\\n\", valid(nodes[0], -2147483649LL, 2147483648LL) ? \"YES\" : \"NO\");\n"
        "    return 0;\n}\n",
        tests,
    )


def build_symmetric() -> dict:
    tests = build_tests(SYMMETRIC_SPECS, solve_symmetric)
    return _mk(
        "tree-symmetric", "对称二叉树", "简单", ["树", "二叉树", "递归", "镜像"],
        {"name": "LeetCode 101", "url": "https://leetcode.cn/problems/symmetric-tree/"},
        "给定一棵二叉树，判断它是否**轴对称（镜像对称）**。\n\n"
        "即把树沿根节点竖直中线折叠，左右两侧能够完全重合。\n\n"
        "空树与单节点树都视为对称。",
        _TREE_INPUT, "一行，若树是镜像对称的输出 `YES`，否则输出 `NO`。", _TREE_CONSTRAINTS,
        [
            {"input": "1 2 2 3 4 4 3\n", "output": "YES\n",
             "explain": "左子树 [`2,3,4`] 与右子树 [`2,4,3`] 互为镜像。"},
            {"input": "1 2 2 null 3 null 3\n", "output": "NO\n",
             "explain": "左子树的右孩子是 3，右子树的左孩子也应为 3，但这里右子树的左孩子为空。"},
        ],
        "把「对称」转化为「两棵树互为镜像」：\n\n"
        "$mirror(a, b)$ 成立当且仅当：\n"
        "1. 两者都为空，或\n"
        "2. 值相等，且 $mirror(a.左, b.右)$ 与 $mirror(a.右, b.左)$ 都成立。\n\n"
        "初始调用 $mirror(root.左, root.右)$。时间 $O(n)$。",
        "#include <cstdio>\n\n"
        "struct Node {\n    int val;\n    Node *left, *right;\n    Node(int v) : val(v), left(nullptr), right(nullptr) {}\n};\n\n"
        "bool mirror(Node* a, Node* b) {\n    // TODO: 判断两棵子树是否互为镜像\n    return true;\n}\n\n"
        "int main() {\n    // TODO\n    return 0;\n}\n",
        "#include <cstdio>\n#include <string>\n#include <vector>\n#include <queue>\n#include <sstream>\n#include <iostream>\n\n"
        "struct Node {\n    int val;\n    Node *left, *right;\n    Node(int v) : val(v), left(nullptr), right(nullptr) {}\n};\n\n"
        "bool mirror(Node* a, Node* b) {\n"
        "    if (!a && !b) return true;\n"
        "    if (!a || !b) return false;\n"
        "    return a->val == b->val && mirror(a->left, b->right) && mirror(a->right, b->left);\n}\n\n"
        "int main() {\n"
        "    std::string line;\n"
        "    std::getline(std::cin, line);\n"
        "    std::istringstream iss(line);\n"
        "    std::vector<std::string> tok;\n"
        "    std::string t;\n"
        "    while (iss >> t) tok.push_back(t);\n"
        "    if (tok.empty() || tok[0] == \"null\") { printf(\"YES\\n\"); return 0; }\n\n"
        "    std::vector<Node*> nodes(tok.size(), nullptr);\n"
        "    nodes[0] = new Node(std::stoi(tok[0]));\n"
        "    std::queue<int> q;\n    q.push(0);\n"
        "    size_t i = 1;\n"
        "    while (!q.empty() && i < tok.size()) {\n"
        "        int idx = q.front(); q.pop();\n"
        "        if (i < tok.size()) {\n"
        "            if (tok[i] != \"null\") {\n"
        "                nodes[i] = new Node(std::stoi(tok[i]));\n"
        "                nodes[idx]->left = nodes[i];\n                q.push((int)i);\n"
        "            }\n            ++i;\n        }\n"
        "        if (i < tok.size()) {\n"
        "            if (tok[i] != \"null\") {\n"
        "                nodes[i] = new Node(std::stoi(tok[i]));\n"
        "                nodes[idx]->right = nodes[i];\n                q.push((int)i);\n"
        "            }\n            ++i;\n        }\n"
        "    }\n"
        "    printf(\"%s\\n\", mirror(nodes[0]->left, nodes[0]->right) ? \"YES\" : \"NO\");\n"
        "    return 0;\n}\n",
        tests,
    )


def build_lca_bst() -> dict:
    tests = build_tests(LCA_SPECS, solve_lca_bst)
    return _mk(
        "tree-lca-bst", "二叉搜索树的最近公共祖先", "简单",
        ["树", "二叉搜索树", "LCA", "迭代"],
        {"name": "LeetCode 235", "url": "https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-search-tree/"},
        "给定一棵**二叉搜索树（BST）**和两个节点值 $p, q$，"
        "求它们的**最近公共祖先（LCA）**。\n\n"
        "最近公共祖先指：同时是 $p$ 和 $q$ 祖先的**深度最大**的那个节点"
        "（一个节点也可以是它自己的祖先）。\n\n"
        "数据保证 $p$ 与 $q$ 都存在于树中，且 $p \\ne q$。",
        _TREE_INPUT + "\n\n**额外一行**：两个整数 $p, q$，表示查询的两个节点值。",
        "一行一个整数，表示最近公共祖先的节点值。",
        _TREE_CONSTRAINTS + ["保证 p, q 均在树中且 p ≠ q"],
        [
            {"input": "6 2 8 0 4 7 9 null null 3 5\n2 8\n", "output": "6\n",
             "explain": "2 在左子树、8 在右子树，分居根节点两侧，故 LCA 为根 6。"},
            {"input": "6 2 8 0 4 7 9 null null 3 5\n2 4\n", "output": "2\n",
             "explain": "4 在 2 的右子树中，2 是 4 的祖先，故 LCA 为 2。"},
        ],
        "利用 BST 的**有序性**，无需递归整棵树：从根出发，\n\n"
        "- 若 $p, q$ **都小于**当前节点值 → 向左走；\n"
        "- 若 $p, q$ **都大于**当前节点值 → 向右走；\n"
        "- 否则（分居两侧，或其中之一等于当前节点）→ 当前节点即为 LCA。\n\n"
        "时间 $O(h)$，其中 $h$ 为树高；额外空间 $O(1)$。",
        "#include <cstdio>\n#include <vector>\n#include <string>\n#include <queue>\n#include <sstream>\n#include <iostream>\n\n"
        "struct Node {\n    int val;\n    Node *left, *right;\n    Node(int v) : val(v), left(nullptr), right(nullptr) {}\n};\n\n"
        "int lca(Node* root, int p, int q) {\n    // TODO: 利用 BST 性质向下走\n    return -1;\n}\n\n"
        "int main() {\n    // TODO: 建树 + 读 p,q + 输出 lca\n    return 0;\n}\n",
        "#include <cstdio>\n#include <vector>\n#include <string>\n#include <queue>\n#include <sstream>\n#include <iostream>\n\n"
        "struct Node {\n    int val;\n    Node *left, *right;\n    Node(int v) : val(v), left(nullptr), right(nullptr) {}\n};\n\n"
        "int lca(Node* root, int p, int q) {\n"
        "    Node* node = root;\n"
        "    while (node) {\n"
        "        if (p < node->val && q < node->val) node = node->left;\n"
        "        else if (p > node->val && q > node->val) node = node->right;\n"
        "        else return node->val;\n"
        "    }\n"
        "    return -1;\n}\n\n"
        "int main() {\n"
        "    std::string line, qline;\n"
        "    std::getline(std::cin, line);\n"
        "    std::getline(std::cin, qline);\n"
        "    std::istringstream iss(line);\n"
        "    std::vector<std::string> tok;\n"
        "    std::string t;\n"
        "    while (iss >> t) tok.push_back(t);\n"
        "    std::istringstream qs(qline);\n"
        "    int p, q; qs >> p >> q;\n\n"
        "    std::vector<Node*> nodes(tok.size(), nullptr);\n"
        "    nodes[0] = new Node(std::stoi(tok[0]));\n"
        "    std::queue<int> dq;\n    dq.push(0);\n"
        "    size_t i = 1;\n"
        "    while (!dq.empty() && i < tok.size()) {\n"
        "        int idx = dq.front(); dq.pop();\n"
        "        if (i < tok.size()) {\n"
        "            if (tok[i] != \"null\") {\n"
        "                nodes[i] = new Node(std::stoi(tok[i]));\n"
        "                nodes[idx]->left = nodes[i];\n                dq.push((int)i);\n"
        "            }\n            ++i;\n        }\n"
        "        if (i < tok.size()) {\n"
        "            if (tok[i] != \"null\") {\n"
        "                nodes[i] = new Node(std::stoi(tok[i]));\n"
        "                nodes[idx]->right = nodes[i];\n                dq.push((int)i);\n"
        "            }\n            ++i;\n        }\n"
        "    }\n"
        "    printf(\"%d\\n\", lca(nodes[0], p, q));\n    return 0;\n}\n",
        tests,
    )


def build_level_order_traversal() -> dict:
    tests = build_tests(LEVEL_ORDER_SPECS, solve_level_order_traversal)
    return _mk(
        "tree-level-order", "二叉树的层序遍历", "简单",
        ["树", "二叉树", "BFS", "队列"],
        {"name": "LeetCode 102", "url": "https://leetcode.cn/problems/binary-tree-level-order-traversal/"},
        "给定一棵二叉树，请**逐层**输出它的节点值：每一层占一行，"
        "同一层内从左到右以空格分隔。\n\n"
        "这就是**广度优先搜索（BFS）**的顺序。若树为空，输出空行。",
        _TREE_INPUT,
        "若干行，第 $k$ 行为第 $k$ 层（从根所在层算起）的节点值，以空格分隔。",
        _TREE_CONSTRAINTS,
        [
            {"input": "3 9 20 null null 15 7\n", "output": "3\n9 20\n15 7\n",
             "explain": "根层为 3；第二层为 9 20；第三层为 15 7。"},
            {"input": "null\n", "output": "\n", "explain": "空树输出空行。"},
        ],
        "用**队列**实现 BFS。关键在于「分层」：每次进入循环时先记录当前队列长度 `sz`，"
        "只处理这 `sz` 个节点，它们恰好是同一层；"
        "处理时把子节点入队，供下一轮使用。\n\n时间 $O(n)$，空间 $O(w)$（$w$ 为最大层宽）。",
        "#include <cstdio>\n#include <vector>\n#include <queue>\n\n"
        "struct Node {\n    int val;\n    Node *left, *right;\n    Node(int v) : val(v), left(nullptr), right(nullptr) {}\n};\n\n"
        "int main() {\n    // TODO: BFS 逐层输出\n    return 0;\n}\n",
        "#include <cstdio>\n#include <string>\n#include <vector>\n#include <queue>\n#include <sstream>\n#include <iostream>\n\n"
        "struct Node {\n    int val;\n    Node *left, *right;\n    Node(int v) : val(v), left(nullptr), right(nullptr) {}\n};\n\n"
        "int main() {\n"
        "    std::string line;\n"
        "    std::getline(std::cin, line);\n"
        "    std::istringstream iss(line);\n"
        "    std::vector<std::string> tok;\n"
        "    std::string t;\n"
        "    while (iss >> t) tok.push_back(t);\n"
        "    if (tok.empty() || tok[0] == \"null\") { printf(\"\\n\"); return 0; }\n\n"
        "    std::vector<Node*> nodes(tok.size(), nullptr);\n"
        "    nodes[0] = new Node(std::stoi(tok[0]));\n"
        "    std::queue<int> q;\n    q.push(0);\n"
        "    size_t i = 1;\n"
        "    while (!q.empty() && i < tok.size()) {\n"
        "        int idx = q.front(); q.pop();\n"
        "        if (i < tok.size()) {\n"
        "            if (tok[i] != \"null\") {\n"
        "                nodes[i] = new Node(std::stoi(tok[i]));\n"
        "                nodes[idx]->left = nodes[i];\n                q.push((int)i);\n"
        "            }\n            ++i;\n        }\n"
        "        if (i < tok.size()) {\n"
        "            if (tok[i] != \"null\") {\n"
        "                nodes[i] = new Node(std::stoi(tok[i]));\n"
        "                nodes[idx]->right = nodes[i];\n                q.push((int)i);\n"
        "            }\n            ++i;\n        }\n"
        "    }\n"
        "    std::queue<Node*> bfs;\n    bfs.push(nodes[0]);\n"
        "    while (!bfs.empty()) {\n"
        "        int sz = (int)bfs.size();\n"
        "        for (int k = 0; k < sz; ++k) {\n"
        "            Node* cur = bfs.front(); bfs.pop();\n"
        "            if (k) printf(\" \");\n            printf(\"%d\", cur->val);\n"
        "            if (cur->left) bfs.push(cur->left);\n"
        "            if (cur->right) bfs.push(cur->right);\n"
        "        }\n        printf(\"\\n\");\n    }\n"
        "    return 0;\n}\n",
        tests,
    )


def main() -> None:
    builders = [
        build_max_depth, build_inorder, build_bst_validate,
        build_symmetric, build_lca_bst, build_level_order_traversal,
    ]
    for b in builders:
        prob = b()
        path = finalize(prob, OUT / f"{prob['id']}.json")
        total = sum(t["score"] for t in prob["tests"])
        print(f"生成 {prob['id']:32s} {len(prob['tests'])} 测试点, 总分 {total}  -> {path.name}")


if __name__ == "__main__":
    main()
