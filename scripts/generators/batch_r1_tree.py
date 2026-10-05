"""树与二叉树 · 批量 R1（16 道）。"""
from __future__ import annotations

import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from genkit import CPP_HEADER, finalize, problem  # noqa: E402

OUT = ROOT / "oj" / "data" / "problems" / "04-tree"
P: list = []


def add(**kw):
    P.append(problem(**kw))


class Node:
    __slots__ = ("v", "l", "r")

    def __init__(self, v):
        self.v, self.l, self.r = v, None, None


def build(vals):
    if not vals or vals[0] == "null":
        return None
    root = Node(int(vals[0]))
    q = deque([root])
    i = 1
    while q and i < len(vals):
        cur = q.popleft()
        if i < len(vals):
            if vals[i] != "null":
                cur.l = Node(int(vals[i])); q.append(cur.l)
            i += 1
        if i < len(vals):
            if vals[i] != "null":
                cur.r = Node(int(vals[i])); q.append(cur.r)
            i += 1
    return root


def parse(t):
    return build(t.strip().split())


CPP_TREE = CPP_HEADER + """
struct Node { long long v; Node *l=nullptr,*r=nullptr; };

Node* buildTree(const vector<string>&t){
    if(t.empty()||t[0]=="null")return nullptr;
    Node*root=new Node{stoll(t[0])};
    queue<Node*>q;q.push(root);size_t i=1;
    while(!q.empty()&&i<t.size()){
        Node*cur=q.front();q.pop();
        if(i<t.size()){if(t[i]!="null"){cur->l=new Node{stoll(t[i])};q.push(cur->l);}++i;}
        if(i<t.size()){if(t[i]!="null"){cur->r=new Node{stoll(t[i])};q.push(cur->r);}++i;}
    }
    return root;
}

vector<string> readTok(){
    vector<string>tok;string x;
    while(cin>>x)tok.push_back(x);
    return tok;
}
"""


def cpp_body(body: str) -> str:
    return CPP_TREE + body


# ---------------------------------------------------------------- 1
def s_preorder(t):
    root = parse(t)
    res = []
    def go(n):
        if n is None:
            return
        res.append(n.v); go(n.l); go(n.r)
    go(root)
    return ((" ".join(map(str, res)) + "\n") if res else "\n")


add(
    pid="tree-preorder", title="二叉树的前序遍历", difficulty="入门",
    tags=["树", "二叉树", "遍历", "栈"], source="LeetCode 144", url="https://leetcode.cn/problems/binary-tree-preorder-traversal/",
    statement="输出二叉树的**前序遍历**序列（根 → 左 → 右）。\n\n**进阶**：请尝试用**迭代**（显式栈）实现，而不是递归。",
    input_format="一行，二叉树的层序序列（空格分隔，`null` 表示空节点，末尾 null 省略）。节点数 $\\le 10^5$。",
    output_format="一行，前序遍历的节点值，以空格分隔。空树输出空行。",
    constraints=["节点数 ≤ 10^5", "|v| ≤ 10^9", "层序表示"],
    solver=s_preorder,
    specs=[("样例 1", "1 null 2 3", 10), ("空树", "null", 10),
           ("单节点", "1", 15), ("完整树", "1 2 3 4 5 6 7", 15),
           ("只有左链", "1 2 null 3", 20), ("含负数", "-1 2 -3", 20),
           ("锯齿", "1 2 3 null 4 null 5", 20)],
    cpp=cpp_body("""int main(){auto tk=readTok();if(tk.empty())tk.push_back("null");
Node*root=buildTree(tk);
vector<long long>res;vector<Node*>st;
if(root)st.push_back(root);
while(!st.empty()){
Node*n=st.back();st.pop_back();
res.push_back(n->v);
if(n->r)st.push_back(n->r);
if(n->l)st.push_back(n->l);}
for(size_t i=0;i<res.size();++i){if(i)printf(" ");printf("%lld",res[i]);}
printf("\\n");return 0;}
"""),
    hint="**迭代写法**：用栈，先把根压入。每次弹出节点就访问它，然后**先压右孩子、再压左孩子**——这样左孩子会先出栈，保证「根左右」的顺序。\n\n时间 $O(n)$。",
)

# ---------------------------------------------------------------- 2
def s_postorder(t):
    root = parse(t)
    res = []
    def go(n):
        if n is None:
            return
        go(n.l); go(n.r); res.append(n.v)
    go(root)
    return ((" ".join(map(str, res)) + "\n") if res else "\n")


add(
    pid="tree-postorder", title="二叉树的后序遍历", difficulty="入门",
    tags=["树", "二叉树", "遍历"], source="LeetCode 145", url="https://leetcode.cn/problems/binary-tree-postorder-traversal/",
    statement="输出二叉树的**后序遍历**序列（左 → 右 → 根）。",
    input_format="一行，二叉树的层序序列（`null` 表示空节点）。节点数 $\\le 10^5$。",
    output_format="一行，后序遍历的节点值。空树输出空行。",
    constraints=["节点数 ≤ 10^5", "|v| ≤ 10^9"],
    solver=s_postorder,
    specs=[("样例 1", "1 null 2 3", 10), ("空树", "null", 10),
           ("单节点", "1", 15), ("完整树", "1 2 3 4 5 6 7", 15),
           ("只有左链", "1 2 null 3", 20), ("含负数", "-1 2 -3", 20),
           ("锯齿", "1 2 3 null 4 null 5", 20)],
    cpp=cpp_body("""void post(Node*n,vector<long long>&r){
if(!n)return;post(n->l,r);post(n->r,r);r.push_back(n->v);}
int main(){auto tk=readTok();if(tk.empty())tk.push_back("null");
Node*root=buildTree(tk);vector<long long>res;post(root,res);
for(size_t i=0;i<res.size();++i){if(i)printf(" ");printf("%lld",res[i]);}
printf("\\n");return 0;}
"""),
    hint="**递归最简单**：先递归左右子树，最后访问当前节点。\n\n**迭代技巧**：按「根 → 右 → 左」的顺序遍历，再把结果**整体反转**，就得到「左 → 右 → 根」。",
)

# ---------------------------------------------------------------- 3
def s_count_nodes(t):
    root = parse(t)
    def go(n):
        return 0 if n is None else 1 + go(n.l) + go(n.r)
    return f"{go(root)}\n"


add(
    pid="tree-count-nodes", title="二叉树的节点个数", difficulty="入门",
    tags=["树", "二叉树", "递归"], source="LeetCode 222", url="https://leetcode.cn/problems/count-complete-tree-nodes/",
    statement="统计二叉树中的**节点总数**。",
    input_format="一行，二叉树的层序序列（`null` 表示空节点）。节点数 $\\le 10^5$。",
    output_format="一行一个整数，表示节点个数。空树输出 0。",
    constraints=["节点数 ≤ 10^5"],
    solver=s_count_nodes,
    specs=[("样例 1", "1 2 3 4 5 6", 10), ("空树", "null", 10),
           ("单节点", "1", 15), ("完整树", "1 2 3 4 5 6 7", 15),
           ("只有左链", "1 2 null 3", 20), ("只有右链", "1 null 2 null 3", 20),
           ("不规则", "1 2 3 null 4 null null 5", 20)],
    cpp=cpp_body("""int cnt(Node*n){if(!n)return 0;return 1+cnt(n->l)+cnt(n->r);}
int main(){auto tk=readTok();if(tk.empty())tk.push_back("null");
printf("%d\\n",cnt(buildTree(tk)));return 0;}
"""),
    hint="**递归**：`count(n) = 1 + count(n->left) + count(n->right)`，空节点返回 0。\n\n时间 $O(n)$。",
)

# ---------------------------------------------------------------- 4
def s_count_leaves(t):
    root = parse(t)
    def go(n):
        if n is None:
            return 0
        if n.l is None and n.r is None:
            return 1
        return go(n.l) + go(n.r)
    return f"{go(root)}\n"


add(
    pid="tree-count-leaves", title="二叉树的叶子节点个数", difficulty="入门",
    tags=["树", "二叉树", "递归"], source="二叉树基础", url="https://leetcode.cn/problems/count-complete-tree-nodes/",
    statement="统计二叉树中**叶子节点**的个数。\n\n**叶子节点**指**左右孩子都为空**的节点。",
    input_format="一行，二叉树的层序序列（`null` 表示空节点）。节点数 $\\le 10^5$。",
    output_format="一行一个整数，表示叶子节点个数。空树输出 0。",
    constraints=["节点数 ≤ 10^5", "叶子 = 左右孩子都为空"],
    solver=s_count_leaves,
    specs=[("样例 1", "1 2 3 4 5 6", 10), ("空树", "null", 10),
           ("单节点（是叶子）", "1", 15), ("完整树", "1 2 3 4 5 6 7", 15),
           ("只有左链", "1 2 null 3", 20), ("只有右链", "1 null 2 null 3", 20),
           ("不规则", "1 2 3 null 4", 20)],
    cpp=cpp_body("""int leaves(Node*n){if(!n)return 0;
if(!n->l&&!n->r)return 1;
return leaves(n->l)+leaves(n->r);}
int main(){auto tk=readTok();if(tk.empty())tk.push_back("null");
printf("%d\\n",leaves(buildTree(tk)));return 0;}
"""),
    hint="**递归**：空节点返回 0；若左右孩子都为空（是叶子）返回 1；否则返回左右子树叶子数之和。\n\n> **易错点**：判断叶子必须**左右都为空**，只判一侧会把「单孩子节点」误算成叶子。",
)

# ---------------------------------------------------------------- 5
def s_sum_nodes(t):
    root = parse(t)
    def go(n):
        return 0 if n is None else n.v + go(n.l) + go(n.r)
    return f"{go(root)}\n"


add(
    pid="tree-sum-nodes", title="二叉树所有节点值之和", difficulty="入门",
    tags=["树", "二叉树", "递归"], source="二叉树基础", url="https://leetcode.cn/problems/sum-of-root-to-leaf-binary-numbers/",
    statement="求二叉树中**所有节点值的总和**。",
    input_format="一行，二叉树的层序序列（`null` 表示空节点）。节点数 $\\le 10^5$，$|v| \\le 10^9$。",
    output_format="一行一个整数，表示所有节点值之和。空树输出 0。",
    constraints=["节点数 ≤ 10^5", "|v| ≤ 10^9"],
    solver=s_sum_nodes,
    specs=[("样例 1", "1 2 3", 10), ("空树", "null", 10),
           ("单节点", "5", 15), ("含负数", "-1 -2 -3", 15),
           ("完整树", "1 2 3 4 5 6 7", 20), ("大值", "1000000000 1000000000", 20),
           ("零", "0 0 0", 20)],
    cpp=cpp_body("""long long sm(Node*n){if(!n)return 0;return n->v+sm(n->l)+sm(n->r);}
int main(){auto tk=readTok();if(tk.empty())tk.push_back("null");
printf("%lld\\n",sm(buildTree(tk)));return 0;}
"""),
    hint="**递归求和**：`sum(n) = n->val + sum(左) + sum(右)`，空节点返回 0。\n\n> **注意**：节点值可达 $10^9$ 且节点数可达 $10^5$，总和可能超出 `int`，要用 `long long`。",
)

# ---------------------------------------------------------------- 6
def s_same_tree(t):
    ls = t.strip("\n").split("\n")
    a, b = parse(ls[0]), parse(ls[1])
    def same(x, y):
        if x is None and y is None:
            return True
        if x is None or y is None or x.v != y.v:
            return False
        return same(x.l, y.l) and same(x.r, y.r)
    return ("YES\n" if same(a, b) else "NO\n")


add(
    pid="tree-same", title="相同的树", difficulty="入门",
    tags=["树", "二叉树", "递归"], source="LeetCode 100", url="https://leetcode.cn/problems/same-tree/",
    statement="判断两棵二叉树在**结构和节点值**上是否完全相同。\n\n相同输出 `YES`，否则 `NO`。",
    input_format="第一行，第一棵树的层序序列。\n\n第二行，第二棵树的层序序列。\n\n`null` 表示空节点。节点数均 $\\le 10^5$。",
    output_format="一行，输出 `YES` 或 `NO`。",
    constraints=["节点数 ≤ 10^5", "|v| ≤ 10^9"],
    solver=s_same_tree,
    specs=[("样例 1（相同）", "1 2 3\n1 2 3", 10), ("样例 2（不同）", "1 2\n1 null 2", 10),
           ("都为空", "null\nnull", 15), ("一空一非空", "1\nnull", 15),
           ("值不同", "1 2 3\n1 2 4", 20), ("结构不同", "1 2 3\n1 2", 20),
           ("含负数", "-1 2\n-1 2", 20)],
    cpp=cpp_body("""bool same(Node*a,Node*b){
if(!a&&!b)return true;
if(!a||!b)return false;
if(a->v!=b->v)return false;
return same(a->l,b->l)&&same(a->r,b->r);}
int main(){string l1,l2;getline(cin,l1);getline(cin,l2);
stringstream s1(l1),s2(l2);vector<string>t1,t2;string x;
while(s1>>x)t1.push_back(x);while(s2>>x)t2.push_back(x);
if(t1.empty())t1.push_back("null");if(t2.empty())t2.push_back("null");
printf("%s\\n",same(buildTree(t1),buildTree(t2))?"YES":"NO");return 0;}
"""),
    hint="**同步递归**：\n\n1. 两个节点都为空 → 相同；\n2. 只有一个是空 → 不同；\n3. 值不同 → 不同；\n4. 否则递归比较左右子树。\n\n> **易错点**：必须先判「都为空」，再判「其中一个为空」，顺序反了会空指针。",
)

# ---------------------------------------------------------------- 7
def s_balanced(t):
    root = parse(t)
    ok = [True]
    def h(n):
        if n is None or not ok[0]:
            return 0
        lh, rh = h(n.l), h(n.r)
        if abs(lh - rh) > 1:
            ok[0] = False
        return 1 + max(lh, rh)
    h(root)
    return ("YES\n" if ok[0] else "NO\n")


add(
    pid="tree-balanced", title="平衡二叉树", difficulty="简单",
    tags=["树", "二叉树", "递归"], source="LeetCode 110", url="https://leetcode.cn/problems/balanced-binary-tree/",
    statement="判断二叉树是否是**高度平衡**的。\n\n平衡的定义：**每个节点**的左右子树高度差**不超过 1**。\n\n是则输出 `YES`，否则 `NO`。",
    input_format="一行，二叉树的层序序列（`null` 表示空节点）。节点数 $\\le 10^5$。",
    output_format="一行，输出 `YES` 或 `NO`。",
    constraints=["节点数 ≤ 10^5", "高度差 ≤ 1"],
    solver=s_balanced,
    specs=[("样例 1（平衡）", "3 9 20 null null 15 7", 10),
           ("样例 2（不平衡）", "1 2 2 3 3 null null 4 4", 10),
           ("空树", "null", 15), ("单节点", "1", 15),
           ("完整树", "1 2 3 4 5 6 7", 20), ("左链", "1 2 null 3", 20),
           ("差 1 的链", "1 2 3", 20)],
    cpp=cpp_body("""int h(Node*n,bool&ok){
if(!n||!ok)return 0;
int lh=h(n->l,ok),rh=h(n->r,ok);
if(abs(lh-rh)>1)ok=false;
return 1+max(lh,rh);}
int main(){auto tk=readTok();if(tk.empty())tk.push_back("null");
bool ok=true;h(buildTree(tk),ok);
printf("%s\\n",ok?"YES":"NO");return 0;}
"""),
    hint="**一次递归同时求高度并判断**：返回当前子树的高度，途中若发现某节点左右高度差 > 1 就把全局标记置为 false。\n\n> **常见错误**：对每个节点都单独调用一次求高度函数，会退化成 $O(n^2)$。**要在同一次递归里完成**。",
)

# ---------------------------------------------------------------- 8
def s_diameter(t):
    root = parse(t)
    best = [0]
    def h(n):
        if n is None:
            return 0
        lh, rh = h(n.l), h(n.r)
        best[0] = max(best[0], lh + rh)
        return 1 + max(lh, rh)
    h(root)
    return f"{best[0]}\n"


add(
    pid="tree-diameter", title="二叉树的直径", difficulty="简单",
    tags=["树", "二叉树", "递归"], source="LeetCode 543", url="https://leetcode.cn/problems/diameter-of-binary-tree/",
    statement="二叉树的**直径**指任意两节点之间**最长路径的边数**。这条路径可能经过根，也可能不经过。\n\n求直径。",
    input_format="一行，二叉树的层序序列（`null` 表示空节点）。节点数 $\\le 10^4$。",
    output_format="一行一个整数，表示直径（边数）。空树输出 0。",
    constraints=["节点数 ≤ 10^4"],
    solver=s_diameter,
    specs=[("样例 1", "1 2 3 4 5", 10), ("空树", "null", 10),
           ("单节点", "1", 15), ("只有左链", "1 2 null 3 null 4", 15),
           ("完整树", "1 2 3 4 5 6 7", 20), ("两节点", "1 2", 20),
           ("不经过根", "1 2 3 4 null null 5 6", 20)],
    cpp=cpp_body("""int best=0;
int h(Node*n){if(!n)return 0;
int lh=h(n->l),rh=h(n->r);
best=max(best,lh+rh);
return 1+max(lh,rh);}
int main(){auto tk=readTok();if(tk.empty())tk.push_back("null");
h(buildTree(tk));printf("%d\\n",best);return 0;}
"""),
    hint="**在求高度的递归里顺便更新答案**：对每个节点，经过它的最长路径长度是 `左高 + 右高`（边数）。\n\n用全局变量记录这个值的最大值即可。时间 $O(n)$。\n\n> **易错点**：直径**不一定经过根**，所以要对每个节点都计算一次，不能只算根节点。",
)

# ---------------------------------------------------------------- 9
def s_left_leaves(t):
    root = parse(t)
    total = 0
    def go(n, is_left):
        nonlocal total
        if n is None:
            return
        if n.l is None and n.r is None and is_left:
            total += n.v
        go(n.l, True); go(n.r, False)
    go(root, False)
    return f"{total}\n"


add(
    pid="tree-sum-left-leaves", title="左叶子之和", difficulty="入门",
    tags=["树", "二叉树", "递归"], source="LeetCode 404", url="https://leetcode.cn/problems/sum-of-left-leaves/",
    statement="求二叉树中**所有左叶子节点**的值之和。\n\n**左叶子**指：它是某个节点的**左孩子**，且**本身是叶子**（左右孩子都为空）。",
    input_format="一行，二叉树的层序序列（`null` 表示空节点）。节点数 $\\le 1000$。",
    output_format="一行一个整数，表示左叶子之和。",
    constraints=["节点数 ≤ 1000", "|v| ≤ 1000"],
    solver=s_left_leaves,
    specs=[("样例 1", "3 9 20 null null 15 7", 10), ("空树", "null", 10),
           ("单节点（根不算左叶）", "1", 15), ("只有左叶", "1 2", 15),
           ("只有右叶", "1 null 2", 20), ("含负数", "-1 -2 -3", 20),
           ("完整树", "1 2 3 4 5 6 7", 20)],
    cpp=cpp_body("""long long sm(Node*n,bool isLeft){
if(!n)return 0;
if(!n->l&&!n->r)return isLeft?n->v:0;
return sm(n->l,true)+sm(n->r,false);}
int main(){auto tk=readTok();if(tk.empty())tk.push_back("null");
printf("%lld\\n",sm(buildTree(tk),false));return 0;}
"""),
    hint="**递归时多传一个「我是不是左孩子」的标志**。\n\n当节点是叶子**且**标志为真时，累加它的值。\n\n> **易错点**：根节点不算左叶子（它没有父节点），所以初始调用传 `false`。",
)

# ---------------------------------------------------------------- 10
def s_merge_trees(t):
    ls = t.strip("\n").split("\n")
    a, b = parse(ls[0]), parse(ls[1])
    def merge(x, y):
        if x is None:
            return y
        if y is None:
            return x
        x.v += y.v
        x.l = merge(x.l, y.l)
        x.r = merge(x.r, y.r)
        return x
    root = merge(a, b)
    out = []
    if root is None:
        return "null\n"
    q = deque([root])
    while q:
        n = q.popleft()
        if n is None:
            out.append("null")
        else:
            out.append(str(n.v)); q.append(n.l); q.append(n.r)
    while out and out[-1] == "null":
        out.pop()
    return " ".join(out) + "\n"


add(
    pid="tree-merge", title="合并二叉树", difficulty="简单",
    tags=["树", "二叉树", "递归"], source="LeetCode 617", url="https://leetcode.cn/problems/merge-two-binary-trees/",
    statement="把两棵二叉树合并为一棵：**对应位置**的节点值相加。\n\n规则：若两个节点都存在，值为两者之和；若只有一个存在，则**直接沿用**它。\n\n输出合并后树的层序序列（末尾 `null` 省略）。",
    input_format="第一行，第一棵树的层序序列。\n\n第二行，第二棵树的层序序列。\n\n`null` 表示空节点。",
    output_format="一行，合并后树的层序序列。若结果为空树输出 `null`。",
    constraints=["节点数 ≤ 2000", "|v| ≤ 10^4"],
    solver=s_merge_trees,
    specs=[("样例 1", "1 3 2 5\n2 1 3 null 4 null 7", 10),
           ("样例 2", "1\n1 2", 10), ("两棵都空", "null\nnull", 15),
           ("一棵为空", "1 2\nnull", 15), ("深度不同", "1 2 3\n1", 20),
           ("含负数", "-1 2\n1 -2", 20), ("右树更深", "1\n1 2 null 3", 20)],
    cpp=cpp_body("""Node* merge(Node*a,Node*b){
if(!a)return b;
if(!b)return a;
a->v+=b->v;
a->l=merge(a->l,b->l);
a->r=merge(a->r,b->r);
return a;}
int main(){string l1,l2;getline(cin,l1);getline(cin,l2);
stringstream s1(l1),s2(l2);vector<string>t1,t2;string x;
while(s1>>x)t1.push_back(x);while(s2>>x)t2.push_back(x);
if(t1.empty())t1.push_back("null");if(t2.empty())t2.push_back("null");
Node*root=merge(buildTree(t1),buildTree(t2));
if(!root){printf("null\\n");return 0;}
vector<string>out;queue<Node*>q;q.push(root);
while(!q.empty()){Node*n=q.front();q.pop();
if(!n){out.push_back("null");continue;}
out.push_back(to_string(n->v));q.push(n->l);q.push(n->r);}
while(!out.empty()&&out.back()=="null")out.pop_back();
for(size_t i=0;i<out.size();++i){if(i)printf(" ");printf("%s",out[i].c_str());}
printf("\\n");return 0;}
"""),
    hint="**同步递归**：\n\n- 若 `a` 为空，直接返回 `b`（整棵子树沿用）；\n- 若 `b` 为空，直接返回 `a`；\n- 否则 `a->val += b->val`，再递归合并左右子树。\n\n时间 $O(\\min(n, m))$。",
)

# ---------------------------------------------------------------- 11
def s_right_view(t):
    root = parse(t)
    if root is None:
        return "\n"
    res = []
    q = deque([root])
    while q:
        sz = len(q)
        for i in range(sz):
            n = q.popleft()
            if i == sz - 1:
                res.append(n.v)
            if n.l:
                q.append(n.l)
            if n.r:
                q.append(n.r)
    return " ".join(map(str, res)) + "\n"


add(
    pid="tree-right-side-view", title="二叉树的右视图", difficulty="中等",
    tags=["树", "二叉树", "BFS", "层序"], source="LeetCode 199", url="https://leetcode.cn/problems/binary-tree-right-side-view/",
    statement="站在二叉树的**右侧**看它，输出**从顶到底**能看到的节点值。\n\n等价于：输出**每一层最右边**的那个节点值。",
    input_format="一行，二叉树的层序序列（`null` 表示空节点）。节点数 $\\le 100$。",
    output_format="一行，右视图的节点值（自上而下）。空树输出空行。",
    constraints=["节点数 ≤ 100"],
    solver=s_right_view,
    specs=[("样例 1", "1 2 3 null 5 null 4", 10), ("样例 2", "1 null 3", 10),
           ("空树", "null", 15), ("单节点", "1", 15),
           ("只有左链", "1 2 null 3", 20), ("完整树", "1 2 3 4 5 6 7", 20),
           ("含负数", "-1 2 3", 20)],
    cpp=cpp_body("""int main(){auto tk=readTok();if(tk.empty())tk.push_back("null");
Node*root=buildTree(tk);
if(!root){printf("\\n");return 0;}
vector<long long>res;queue<Node*>q;q.push(root);
while(!q.empty()){int sz=q.size();
for(int i=0;i<sz;++i){Node*n=q.front();q.pop();
if(i==sz-1)res.push_back(n->v);
if(n->l)q.push(n->l);
if(n->r)q.push(n->r);}}
for(size_t i=0;i<res.size();++i){if(i)printf(" ");printf("%lld",res[i]);}
printf("\\n");return 0;}
"""),
    hint="**层序遍历（BFS）**：按层处理，**每层的最后一个节点**就是该层从右侧能看到的那一个。\n\n> **关键技巧**：进入每层循环前先固定 `sz = q.size()`，循环 `sz` 次刚好处理完一整层。\n\n时间 $O(n)$。",
)

# ---------------------------------------------------------------- 12
def s_bst_search(t):
    ls = t.strip("\n").split("\n")
    root = parse(ls[0])
    target = int(ls[1])
    cur = root
    while cur:
        if cur.v == target:
            return "YES\n"
        cur = cur.l if target < cur.v else cur.r
    return "NO\n"


add(
    pid="tree-bst-search", title="二叉搜索树中的搜索", difficulty="入门",
    tags=["树", "二叉搜索树", "查找"], source="LeetCode 700", url="https://leetcode.cn/problems/search-in-a-binary-search-tree/",
    statement="在二叉搜索树（BST）中查找值为 $target$ 的节点。\n\n找到输出 `YES`，否则 `NO`。\n\n**要求**：利用 BST 的大小性质，时间复杂度 $O(h)$（$h$ 为树高）。",
    input_format="第一行，BST 的层序序列（`null` 表示空节点）。\n\n第二行一个整数 $target$。",
    output_format="一行，输出 `YES` 或 `NO`。",
    constraints=["节点数 ≤ 5000", "|v|, |target| ≤ 10^9", "输入保证是合法 BST"],
    solver=s_bst_search,
    specs=[("样例 1（找到）", "4 2 7 1 3\n2", 10), ("样例 2（未找到）", "4 2 7 1 3\n5", 10),
           ("空树", "null\n1", 15), ("根命中", "5 3 8\n5", 15),
           ("最小值", "5 3 8 1\n1", 20), ("最大值", "5 3 8 9\n9", 20),
           ("左链", "5 4 null 3\n3", 20)],
    cpp=cpp_body("""int main(){string line;getline(cin,line);
stringstream ss(line);vector<string>tk;string x;
while(ss>>x)tk.push_back(x);
if(tk.empty())tk.push_back("null");
long long target;scanf("%lld",&target);
Node*cur=buildTree(tk);bool found=false;
while(cur){if(cur->v==target){found=true;break;}
cur=(target<cur->v)?cur->l:cur->r;}
printf("%s\\n",found?"YES":"NO");return 0;}
"""),
    hint="**利用 BST 性质**：从根出发，`target` 比当前值小就往左走，大就往右走，相等就找到。\n\n不需要遍历整棵树，时间 $O(h)$。",
)

# ---------------------------------------------------------------- 13
def s_bst_range_sum(t):
    ls = t.strip("\n").split("\n")
    root = parse(ls[0])
    lo, hi = map(int, ls[1].split())
    total = 0
    def go(n):
        nonlocal total
        if n is None:
            return
        if lo <= n.v <= hi:
            total += n.v
        if n.v > lo:
            go(n.l)
        if n.v < hi:
            go(n.r)
    go(root)
    return f"{total}\n"


add(
    pid="tree-bst-range-sum", title="二叉搜索树的范围和", difficulty="简单",
    tags=["树", "二叉搜索树", "递归", "剪枝"], source="LeetCode 938", url="https://leetcode.cn/problems/range-sum-of-bst/",
    statement="给定 BST 和区间 $[lo, hi]$，求树中所有**值落在区间内**的节点之和。\n\n**要求**：利用 BST 性质剪枝，不必遍历所有节点。",
    input_format="第一行，BST 的层序序列（`null` 表示空节点）。\n\n第二行两个整数 $lo, hi$（$lo \\le hi$）。",
    output_format="一行一个整数，表示区间和。",
    constraints=["节点数 ≤ 2×10^4", "1 ≤ lo ≤ hi ≤ 10^9", "输入保证是合法 BST"],
    solver=s_bst_range_sum,
    specs=[("样例 1", "10 5 15 3 7 null 18\n7 15", 10),
           ("样例 2", "10 5 15 3 7 13 18 1 null 6\n6 10", 10),
           ("全在区间内", "5 3 8\n1 10", 15), ("全不在区间", "5 3 8\n100 200", 15),
           ("单节点命中", "5\n5 5", 20), ("单节点未命中", "5\n1 4", 20),
           ("边界值", "10 5 15\n5 10", 20)],
    cpp=cpp_body("""long long sum(Node*n,long long lo,long long hi){
if(!n)return 0;
long long r=0;
if(n->v>=lo&&n->v<=hi)r+=n->v;
if(n->v>lo)r+=sum(n->l,lo,hi);
if(n->v<hi)r+=sum(n->r,lo,hi);
return r;}
int main(){string line;getline(cin,line);
stringstream ss(line);vector<string>tk;string x;
while(ss>>x)tk.push_back(x);
if(tk.empty())tk.push_back("null");
long long lo,hi;scanf("%lld %lld",&lo,&hi);
printf("%lld\\n",sum(buildTree(tk),lo,hi));return 0;}
"""),
    hint="**带剪枝的递归**：\n\n- 当前值在区间内 → 累加；\n- **仅当 `n->val > lo` 时才递归左子树**（左子树都更小，若当前值已不大于 lo，左边不可能有满足的）；\n- **仅当 `n->val < hi` 时才递归右子树**。\n\n这样能跳过大量不相关节点。",
)

# ---------------------------------------------------------------- 14
def s_paths(t):
    root = parse(t)
    res = []
    def go(n, path):
        if n is None:
            return
        path = path + [str(n.v)]
        if n.l is None and n.r is None:
            res.append("->".join(path))
            return
        go(n.l, path); go(n.r, path)
    go(root, [])
    return ("\n".join(res) + "\n") if res else "\n"


add(
    pid="tree-root-to-leaf-paths", title="所有根到叶子的路径", difficulty="简单",
    tags=["树", "二叉树", "DFS", "回溯"], source="LeetCode 257", url="https://leetcode.cn/problems/binary-tree-paths/",
    statement="输出二叉树中**所有从根到叶子的路径**。\n\n格式：节点值之间用 `->` 连接，每条路径占一行，按**先左后右**的遍历顺序输出。\n\n**叶子**指左右孩子都为空的节点。",
    input_format="一行，二叉树的层序序列（`null` 表示空节点）。节点数 $\\le 100$。",
    output_format="每行一条路径。空树输出空行。",
    constraints=["节点数 ≤ 100", "|v| ≤ 1000", "先左后右顺序"],
    solver=s_paths,
    specs=[("样例 1", "1 2 3 null 5", 10), ("空树", "null", 10),
           ("单节点", "1", 15), ("只有左链", "1 2 null 3", 15),
           ("完整树", "1 2 3", 20), ("含负数", "-1 2 -3", 20),
           ("两叶", "1 2 3", 20)],
    cpp=cpp_body("""void dfs(Node*n,string path,vector<string>&res){
if(!n)return;
path+=(path.empty()?"":"->")+to_string(n->v);
if(!n->l&&!n->r){res.push_back(path);return;}
dfs(n->l,path,res);dfs(n->r,path,res);}
int main(){auto tk=readTok();if(tk.empty())tk.push_back("null");
vector<string>res;dfs(buildTree(tk),"",res);
for(auto&s:res)printf("%s\\n",s.c_str());
if(res.empty())printf("\\n");
return 0;}
"""),
    hint="**DFS + 路径字符串**：递归时把「已走过的路径」作为参数往下传（传值，天然实现回溯）。\n\n到达**叶子**时把整条路径加入结果。\n\n> **易错点**：判断叶子要用「左右都为空」，并且只在叶子处收集路径，中途节点不算。",
)

# ---------------------------------------------------------------- 15
def s_bst_insert(t):
    ls = t.strip("\n").split("\n")
    root = parse(ls[0])
    val = int(ls[1])
    def ins(n):
        if n is None:
            return Node(val)
        if val < n.v:
            n.l = ins(n.l)
        elif val > n.v:
            n.r = ins(n.r)
        return n
    root = ins(root)
    if root is None:
        return "null\n"
    out = []
    q = deque([root])
    while q:
        n = q.popleft()
        if n is None:
            out.append("null")
        else:
            out.append(str(n.v)); q.append(n.l); q.append(n.r)
    while out and out[-1] == "null":
        out.pop()
    return " ".join(out) + "\n"


add(
    pid="tree-bst-insert", title="二叉搜索树中的插入操作", difficulty="简单",
    tags=["树", "二叉搜索树", "递归"], source="LeetCode 701", url="https://leetcode.cn/problems/insert-into-a-binary-search-tree/",
    statement="向 BST 中插入一个值（保证该值**原本不存在**），返回插入后的树的层序序列。\n\n插入位置不唯一，本题要求按「**标准 BST 插入**」：从根往下按大小关系走，走到空位置就挂上去。",
    input_format="第一行，BST 的层序序列（`null` 表示空树）。\n\n第二行一个整数 $val$。",
    output_format="一行，插入后 BST 的层序序列（末尾 `null` 省略）。",
    constraints=["节点数 ≤ 5000", "|v| ≤ 10^8", "插入值不重复"],
    solver=s_bst_insert,
    specs=[("样例 1", "4 2 7 1 3\n5", 10), ("样例 2", "40 20 60 10 30 50 70\n25", 10),
           ("空树插入", "null\n5", 15), ("插到最左", "5 3 8\n1", 15),
           ("插到最右", "5 3 8\n9", 20), ("单节点树", "5\n3", 20),
           ("插到中间", "10 5 15\n7", 20)],
    cpp=cpp_body("""Node* ins(Node*n,long long v){
if(!n)return new Node{v};
if(v<n->v)n->l=ins(n->l,v);
else if(v>n->v)n->r=ins(n->r,v);
return n;}
int main(){string line;getline(cin,line);
stringstream ss(line);vector<string>tk;string x;
while(ss>>x)tk.push_back(x);
if(tk.empty())tk.push_back("null");
long long v;scanf("%lld",&v);
Node*root=ins(buildTree(tk),v);
vector<string>out;queue<Node*>q;q.push(root);
while(!q.empty()){Node*n=q.front();q.pop();
if(!n){out.push_back("null");continue;}
out.push_back(to_string(n->v));q.push(n->l);q.push(n->r);}
while(!out.empty()&&out.back()=="null")out.pop_back();
for(size_t i=0;i<out.size();++i){if(i)printf(" ");printf("%s",out[i].c_str());}
printf("\\n");return 0;}
"""),
    hint="**递归插入**：\n\n- 若当前节点为空 → 新建节点返回；\n- 若 `val < 当前值` → 递归插入左子树；\n- 若 `val > 当前值` → 递归插入右子树。\n\n时间 $O(h)$。",
)

# ---------------------------------------------------------------- 16
def s_level_avg(t):
    root = parse(t)
    if root is None:
        return "\n"
    res = []
    q = deque([root])
    while q:
        sz = len(q)
        s = 0
        for _ in range(sz):
            n = q.popleft()
            s += n.v
            if n.l:
                q.append(n.l)
            if n.r:
                q.append(n.r)
        res.append(f"{s / sz:.5f}")
    return " ".join(res) + "\n"


add(
    pid="tree-level-average", title="二叉树的层平均值", difficulty="简单",
    tags=["树", "二叉树", "BFS", "层序"], source="LeetCode 637", url="https://leetcode.cn/problems/average-of-levels-in-binary-tree/",
    statement="输出二叉树**每一层节点值的平均值**，从根所在层开始，每层保留 **5 位小数**，以空格分隔。",
    input_format="一行，二叉树的层序序列（`null` 表示空节点）。节点数 $\\le 10^4$。",
    output_format="一行，各层平均值（保留 5 位小数）。空树输出空行。",
    constraints=["节点数 ≤ 10^4", "|v| ≤ 2^31−1"],
    solver=s_level_avg,
    specs=[("样例 1", "3 9 20 null null 15 7", 10), ("空树", "null", 10),
           ("单节点", "5", 15), ("完整树", "1 2 3 4 5 6 7", 15),
           ("含负数", "-1 -2 -3", 20), ("只有左链", "1 2 null 3", 20),
           ("两层", "1 2 3", 20)],
    cpp=cpp_body("""int main(){auto tk=readTok();if(tk.empty())tk.push_back("null");
Node*root=buildTree(tk);
if(!root){printf("\\n");return 0;}
queue<Node*>q;q.push(root);bool first=true;
while(!q.empty()){int sz=q.size();long long s=0;
for(int i=0;i<sz;++i){Node*n=q.front();q.pop();s+=n->v;
if(n->l)q.push(n->l);if(n->r)q.push(n->r);}
if(!first)printf(" ");printf("%.5f",(double)s/sz);first=false;}
printf("\\n");return 0;}
"""),
    hint="**层序遍历 + 逐层求和**：每层先固定 `sz = q.size()`，处理这一层的 `sz` 个节点并累加，最后求平均。\n\n> **易错点**：求平均时用 `long long` 存和，最后再转 `double` 相除，避免精度损失。",
)


def main() -> None:
    for p in P:
        finalize(p, OUT / f"{p['id']}.json")
        total = sum(t["score"] for t in p["tests"])
        print(f"生成 {p['id']:34s} {len(p['tests'])} 测试点, 总分 {total:3d}")


if __name__ == "__main__":
    main()
