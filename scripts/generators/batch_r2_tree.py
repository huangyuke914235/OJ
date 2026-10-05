"""树与二叉树 · 批量 R2（14 道）。"""
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


def serialize(root):
    if root is None:
        return "null"
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
    return " ".join(out)


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
def s_inorder_iter(t):
    root = parse(t)
    res = []
    st = []
    cur = root
    while cur or st:
        while cur:
            st.append(cur)
            cur = cur.l
        cur = st.pop()
        res.append(cur.v)
        cur = cur.r
    return ((" ".join(map(str, res)) + "\n") if res else "\n")


add(
    pid="tree-inorder-iterative", title="中序遍历（迭代实现）", difficulty="简单",
    tags=["树", "二叉树", "遍历", "栈"], source="LeetCode 94", url="https://leetcode.cn/problems/binary-tree-inorder-traversal/",
    statement="用**迭代**（显式栈）实现二叉树的**中序遍历**，输出遍历序列。\n\n中序顺序：**左 → 根 → 右**。",
    input_format="一行，二叉树的层序序列（`null` 表示空节点）。节点数 $\\le 10^5$。",
    output_format="一行，中序遍历序列；空树输出空行。",
    constraints=["节点数 ≤ 10^5", "|v| ≤ 10^9", "必须用迭代实现"],
    solver=s_inorder_iter,
    specs=[("样例 1", "1 null 2 3", 10), ("空树", "null", 10),
           ("单节点", "1", 15), ("完整树", "1 2 3 4 5 6 7", 15),
           ("只有左链", "1 2 null 3", 20), ("含负数", "-1 2 -3", 20)],
    cpp=cpp_body("""int main(){auto tk=readTok();if(tk.empty())tk.push_back("null");
Node*root=buildTree(tk);
vector<long long>res;vector<Node*>st;Node*cur=root;
while(cur||!st.empty()){
while(cur){st.push_back(cur);cur=cur->l;}
cur=st.back();st.pop_back();
res.push_back(cur->v);
cur=cur->r;}
for(size_t i=0;i<res.size();++i){if(i)printf(" ");printf("%lld",res[i]);}
printf("\\n");return 0;}
"""),
    hint="**迭代中序的经典写法**：\n\n1. 从当前节点**一路向左**，沿途全部压栈；\n2. 弹出栈顶、访问它；\n3. 转向它的**右子树**，重复。\n\n循环条件是 `cur || !st.empty()`——两个都不能少。\n\n> **易错点**：这是最考验「递归转迭代」理解的一道题，建议手推一遍。",
)

# ---------------------------------------------------------------- 2
def s_postorder_iter(t):
    root = parse(t)
    res = []
    if root:
        st = [root]
        while st:
            n = st.pop()
            res.append(n.v)
            if n.l:
                st.append(n.l)
            if n.r:
                st.append(n.r)
        res.reverse()
    return ((" ".join(map(str, res)) + "\n") if res else "\n")


add(
    pid="tree-postorder-iterative", title="后序遍历（迭代实现）", difficulty="中等",
    tags=["树", "二叉树", "遍历", "栈"], source="LeetCode 145", url="https://leetcode.cn/problems/binary-tree-postorder-traversal/",
    statement="用**迭代**实现二叉树的**后序遍历**，输出遍历序列。\n\n后序顺序：**左 → 右 → 根**。",
    input_format="一行，二叉树的层序序列（`null` 表示空节点）。节点数 $\\le 10^5$。",
    output_format="一行，后序遍历序列；空树输出空行。",
    constraints=["节点数 ≤ 10^5", "|v| ≤ 10^9", "必须用迭代实现"],
    solver=s_postorder_iter,
    specs=[("样例 1", "1 null 2 3", 10), ("空树", "null", 10),
           ("单节点", "1", 15), ("完整树", "1 2 3 4 5 6 7", 15),
           ("只有左链", "1 2 null 3", 20), ("含负数", "-1 2 -3", 20)],
    cpp=cpp_body("""int main(){auto tk=readTok();if(tk.empty())tk.push_back("null");
Node*root=buildTree(tk);
vector<long long>res;vector<Node*>st;
if(root)st.push_back(root);
while(!st.empty()){Node*n=st.back();st.pop_back();
res.push_back(n->v);
if(n->l)st.push_back(n->l);
if(n->r)st.push_back(n->r);}
reverse(res.begin(),res.end());
for(size_t i=0;i<res.size();++i){if(i)printf(" ");printf("%lld",res[i]);}
printf("\\n");return 0;}
"""),
    hint="**「反向」技巧**：\n\n按「根 → **右** → **左**」的顺序做前序遍历（只需在压栈时**先左后右**），最后把结果**整体反转**，就得到「左 → 右 → 根」。\n\n> 这是迭代实现后序最简洁的写法。**严格模拟后序**（用 `lastVisited` 标记）也可以，但代码复杂得多。",
)

# ---------------------------------------------------------------- 3
def s_zigzag(t):
    root = parse(t)
    if root is None:
        return "\n"
    res = []
    q = deque([root])
    left_to_right = True
    while q:
        sz = len(q)
        level = []
        for _ in range(sz):
            n = q.popleft()
            level.append(n.v)
            if n.l:
                q.append(n.l)
            if n.r:
                q.append(n.r)
        if not left_to_right:
            level.reverse()
        res.append(" ".join(map(str, level)))
        left_to_right = not left_to_right
    return "\n".join(res) + "\n"


add(
    pid="tree-zigzag-level-order", title="二叉树的锯齿形层序遍历", difficulty="中等",
    tags=["树", "二叉树", "BFS", "层序"], source="LeetCode 103", url="https://leetcode.cn/problems/binary-tree-zigzag-level-order-traversal/",
    statement="对二叉树做**锯齿形**层序遍历：\n\n- 第 1 层**从左到右**；\n- 第 2 层**从右到左**；\n- 第 3 层从左到右……依此类推。\n\n每层占一行。",
    input_format="一行，二叉树的层序序列（`null` 表示空节点）。节点数 $\\le 10^5$。",
    output_format="若干行，每行一层（按锯齿方向）。空树输出空行。",
    constraints=["节点数 ≤ 10^5", "|v| ≤ 10^9", "每层一行"],
    solver=s_zigzag,
    specs=[("样例 1", "3 9 20 null null 15 7", 10), ("空树", "null", 10),
           ("单节点", "1", 15), ("完整树", "1 2 3 4 5 6 7", 15),
           ("只有左链", "1 2 null 3", 20), ("含负数", "-1 2 3", 20)],
    cpp=cpp_body("""int main(){auto tk=readTok();if(tk.empty())tk.push_back("null");
Node*root=buildTree(tk);
if(!root){printf("\\n");return 0;}
queue<Node*>q;q.push(root);bool l2r=true;
while(!q.empty()){int sz=q.size();vector<long long>lv;
for(int i=0;i<sz;++i){Node*n=q.front();q.pop();lv.push_back(n->v);
if(n->l)q.push(n->l);if(n->r)q.push(n->r);}
if(!l2r)reverse(lv.begin(),lv.end());
for(size_t i=0;i<lv.size();++i){if(i)printf(" ");printf("%lld",lv[i]);}
printf("\\n");l2r=!l2r;}
return 0;}
"""),
    hint="**层序遍历 + 隔层反转**：先用普通 BFS 按层收集，再对**奇数层**（第 2、4、… 层）把该层结果**反转**。\n\n> **更优写法**：用**双端队列**，奇数层从队尾取、偶数层从队首取，一次遍历完成。\n\n时间 $O(n)$。",
)

# ---------------------------------------------------------------- 4
def s_leaf_similar(t):
    ls = t.strip("\n").split("\n")
    def leaves(root):
        out = []
        def go(n):
            if n is None:
                return
            if n.l is None and n.r is None:
                out.append(n.v)
            go(n.l); go(n.r)
        go(root)
        return out
    a = leaves(parse(ls[0]))
    b = leaves(parse(ls[1]))
    return ("YES\n" if a == b else "NO\n")


add(
    pid="tree-leaf-similar", title="叶子相似的树", difficulty="简单",
    tags=["树", "二叉树", "DFS"], source="LeetCode 872", url="https://leetcode.cn/problems/leaf-similar-trees/",
    statement="若两棵二叉树的**叶子节点值序列**（从左到右）完全相同，则称它们**叶子相似**。\n\n相似输出 `YES`，否则 `NO`。",
    input_format="第一行，第一棵树的层序序列。\n\n第二行，第二棵树的层序序列。\n\n`null` 表示空节点。",
    output_format="一行，输出 `YES` 或 `NO`。",
    constraints=["节点数 ≤ 200", "|v| ≤ 200"],
    solver=s_leaf_similar,
    specs=[("样例 1（相似）", "3 5 1 6 2 9 8 null null 7 4\n3 5 1 6 7 4 2 null null null null null null 9 8", 10),
           ("样例 2（不相似）", "1 2 3\n1 3 2", 10),
           ("两棵都空", "null\nnull", 15), ("单节点相同", "1\n1", 15),
           ("单节点不同", "1\n2", 20), ("叶子顺序不同", "1 2 3\n1 3 2", 20)],
    cpp=cpp_body("""void leaves(Node*n,vector<long long>&r){
if(!n)return;
if(!n->l&&!n->r){r.push_back(n->v);return;}
leaves(n->l,r);leaves(n->r,r);}
int main(){string l1,l2;getline(cin,l1);getline(cin,l2);
stringstream s1(l1),s2(l2);vector<string>t1,t2;string x;
while(s1>>x)t1.push_back(x);while(s2>>x)t2.push_back(x);
if(t1.empty())t1.push_back("null");if(t2.empty())t2.push_back("null");
vector<long long>a,b;
leaves(buildTree(t1),a);leaves(buildTree(t2),b);
printf("%s\\n",a==b?"YES":"NO");return 0;}
"""),
    hint="**各自收集叶子序列再比较**：DFS 到叶子（左右都空）时记录值。\n\n> **易错点**：必须按**从左到右**的顺序收集，所以要先递归左子树再递归右子树。",
)

# ---------------------------------------------------------------- 5
def s_search_value(t):
    ls = t.strip("\n").split("\n")
    root = parse(ls[0])
    target = int(ls[1])
    found = False
    if root:
        st = [root]
        while st:
            n = st.pop()
            if n.v == target:
                found = True
                break
            if n.l:
                st.append(n.l)
            if n.r:
                st.append(n.r)
    return ("YES\n" if found else "NO\n")


add(
    pid="tree-search-value", title="在二叉树中查找值", difficulty="入门",
    tags=["树", "二叉树", "DFS"], source="二叉树基础", url="https://leetcode.cn/problems/search-in-a-binary-search-tree/",
    statement="在二叉树中查找是否存在值为 $target$ 的节点。\n\n存在输出 `YES`，否则 `NO`。",
    input_format="第一行，二叉树的层序序列（`null` 表示空节点）。\n\n第二行一个整数 $target$。",
    output_format="一行，输出 `YES` 或 `NO`。",
    constraints=["节点数 ≤ 10^5", "|v|, |target| ≤ 10^9"],
    solver=s_search_value,
    specs=[("样例 1（找到）", "1 2 3\n2", 10), ("样例 2（未找到）", "1 2 3\n4", 10),
           ("空树", "null\n1", 15), ("根命中", "5 3 8\n5", 15),
           ("叶子命中", "1 2 null 3\n3", 20), ("含负数", "-1 2 -3\n-3", 20)],
    cpp=cpp_body("""int main(){string line;getline(cin,line);
stringstream ss(line);vector<string>tk;string x;
while(ss>>x)tk.push_back(x);
if(tk.empty())tk.push_back("null");
long long target;scanf("%lld",&target);
Node*root=buildTree(tk);bool found=false;
vector<Node*>st;if(root)st.push_back(root);
while(!st.empty()){Node*n=st.back();st.pop_back();
if(n->v==target){found=true;break;}
if(n->l)st.push_back(n->l);
if(n->r)st.push_back(n->r);}
printf("%s\\n",found?"YES":"NO");return 0;}
"""),
    hint="**遍历整棵树**（普通二叉树没有大小关系可利用，必须全遍历）。\n\n> **对比 BST**：BST 上查找可以按大小关系只走一条路径，$O(h)$。",
)

# ---------------------------------------------------------------- 6
def s_tree_max(t):
    root = parse(t)
    if root is None:
        return "\n"
    best = None
    st = [root]
    while st:
        n = st.pop()
        best = n.v if best is None else max(best, n.v)
        if n.l:
            st.append(n.l)
        if n.r:
            st.append(n.r)
    return f"{best}\n"


add(
    pid="tree-max-value", title="二叉树的最大值", difficulty="入门",
    tags=["树", "二叉树", "遍历"], source="二叉树基础", url="https://leetcode.cn/problems/maximum-depth-of-binary-tree/",
    statement="求二叉树中所有节点值的**最大值**。空树输出空行。",
    input_format="一行，二叉树的层序序列（`null` 表示空节点）。节点数 $\\le 10^5$，$|v| \\le 10^9$。",
    output_format="一行一个整数；空树输出空行。",
    constraints=["节点数 ≤ 10^5", "|v| ≤ 10^9"],
    solver=s_tree_max,
    specs=[("样例 1", "1 2 3", 10), ("空树", "null", 10),
           ("单节点", "5", 15), ("含负数", "-1 -2 -3", 15),
           ("完整树", "1 2 3 4 5 6 7", 20), ("大值", "1 1000000000", 20)],
    cpp=cpp_body("""int main(){auto tk=readTok();if(tk.empty())tk.push_back("null");
Node*root=buildTree(tk);
if(!root){printf("\\n");return 0;}
long long best=LLONG_MIN;vector<Node*>st;st.push_back(root);
while(!st.empty()){Node*n=st.back();st.pop_back();
best=max(best,n->v);
if(n->l)st.push_back(n->l);
if(n->r)st.push_back(n->r);}
printf("%lld\\n",best);return 0;}
"""),
    hint="**遍历取最大**：任选一种遍历方式（DFS/BFS），维护全局最大值。\n\n> **易错点**：初值不能用 0——数组可能**全为负数**，应取 $-\\infty$（或第一个节点的值）。",
)

# ---------------------------------------------------------------- 7
def s_tree_min(t):
    root = parse(t)
    if root is None:
        return "\n"
    best = None
    st = [root]
    while st:
        n = st.pop()
        best = n.v if best is None else min(best, n.v)
        if n.l:
            st.append(n.l)
        if n.r:
            st.append(n.r)
    return f"{best}\n"


add(
    pid="tree-min-value", title="二叉树的最小值", difficulty="入门",
    tags=["树", "二叉树", "遍历"], source="二叉树基础", url="https://leetcode.cn/problems/minimum-depth-of-binary-tree/",
    statement="求二叉树中所有节点值的**最小值**。空树输出空行。",
    input_format="一行，二叉树的层序序列（`null` 表示空节点）。节点数 $\\le 10^5$，$|v| \\le 10^9$。",
    output_format="一行一个整数；空树输出空行。",
    constraints=["节点数 ≤ 10^5", "|v| ≤ 10^9"],
    solver=s_tree_min,
    specs=[("样例 1", "1 2 3", 10), ("空树", "null", 10),
           ("单节点", "5", 15), ("含负数", "-1 -2 -3", 15),
           ("完整树", "1 2 3 4 5 6 7", 20), ("含零", "0 1 2", 20)],
    cpp=cpp_body("""int main(){auto tk=readTok();if(tk.empty())tk.push_back("null");
Node*root=buildTree(tk);
if(!root){printf("\\n");return 0;}
long long best=LLONG_MAX;vector<Node*>st;st.push_back(root);
while(!st.empty()){Node*n=st.back();st.pop_back();
best=min(best,n->v);
if(n->l)st.push_back(n->l);
if(n->r)st.push_back(n->r);}
printf("%lld\\n",best);return 0;}
"""),
    hint="**遍历取最小**：初值取 $+\\infty$。\n\n> **对比 BST**：BST 的最小值就是**最左节点**，可以一路向左 $O(h)$ 找到，不必遍历全树。",
)

# ---------------------------------------------------------------- 8
def s_count_even(t):
    root = parse(t)
    cnt = 0
    if root:
        st = [root]
        while st:
            n = st.pop()
            if n.v % 2 == 0:
                cnt += 1
            if n.l:
                st.append(n.l)
            if n.r:
                st.append(n.r)
    return f"{cnt}\n"


add(
    pid="tree-count-even", title="统计二叉树中偶数值节点", difficulty="入门",
    tags=["树", "二叉树", "遍历"], source="二叉树基础", url="https://leetcode.cn/problems/count-complete-tree-nodes/",
    statement="统计二叉树中**值为偶数**的节点个数。",
    input_format="一行，二叉树的层序序列（`null` 表示空节点）。节点数 $\\le 10^5$，$|v| \\le 10^9$。",
    output_format="一行一个整数。",
    constraints=["节点数 ≤ 10^5", "|v| ≤ 10^9", "0 视为偶数"],
    solver=s_count_even,
    specs=[("样例 1", "1 2 3 4", 10), ("空树", "null", 10),
           ("全偶", "2 4 6", 15), ("全奇", "1 3 5", 15),
           ("含 0", "0 1 2", 20), ("含负数", "-2 -1 0", 20)],
    cpp=cpp_body("""int main(){auto tk=readTok();if(tk.empty())tk.push_back("null");
Node*root=buildTree(tk);int cnt=0;
vector<Node*>st;if(root)st.push_back(root);
while(!st.empty()){Node*n=st.back();st.pop_back();
if(n->v%2==0)++cnt;
if(n->l)st.push_back(n->l);
if(n->r)st.push_back(n->r);}
printf("%d\\n",cnt);return 0;}
"""),
    hint="**遍历计数**：判断 `v % 2 == 0` 即可。\n\n> **注意**：$0$ 和负偶数（如 $-2$）都满足 `% 2 == 0`，视为偶数。",
)

# ---------------------------------------------------------------- 9
def s_bst_min(t):
    root = parse(t)
    if root is None:
        return "\n"
    cur = root
    while cur.l:
        cur = cur.l
    return f"{cur.v}\n"


add(
    pid="tree-bst-min", title="BST 中的最小值", difficulty="入门",
    tags=["树", "二叉搜索树", "查找"], source="BST 性质", url="https://leetcode.cn/problems/minimum-absolute-difference-in-bst/",
    statement="给定一棵**二叉搜索树**，求其中的**最小值**。\n\n**要求**：利用 BST 性质，$O(h)$ 完成（$h$ 为树高），不必遍历全树。",
    input_format="一行，BST 的层序序列（`null` 表示空节点）。节点数 $\\le 10^5$。",
    output_format="一行一个整数；空树输出空行。",
    constraints=["节点数 ≤ 10^5", "保证是合法 BST", "要求 O(h)"],
    solver=s_bst_min,
    specs=[("样例 1", "5 3 8 1", 10), ("空树", "null", 10),
           ("单节点", "7", 15), ("左链", "5 4 null 3", 15),
           ("含负数", "0 -1 1", 20), ("完整 BST", "8 4 12 2 6 10 14", 20)],
    cpp=cpp_body("""int main(){auto tk=readTok();if(tk.empty())tk.push_back("null");
Node*root=buildTree(tk);
if(!root){printf("\\n");return 0;}
Node*cur=root;
while(cur->l)cur=cur->l;
printf("%lld\\n",cur->v);return 0;}
"""),
    hint="**BST 的最小值在最左端**：从根出发**一路向左**，走到底就是最小值。\n\n时间 $O(h)$。\n\n> **对比普通二叉树**：必须遍历全树，$O(n)$。",
)

# ---------------------------------------------------------------- 10
def s_bst_max(t):
    root = parse(t)
    if root is None:
        return "\n"
    cur = root
    while cur.r:
        cur = cur.r
    return f"{cur.v}\n"


add(
    pid="tree-bst-max", title="BST 中的最大值", difficulty="入门",
    tags=["树", "二叉搜索树", "查找"], source="BST 性质", url="https://leetcode.cn/problems/minimum-absolute-difference-in-bst/",
    statement="给定一棵**二叉搜索树**，求其中的**最大值**。\n\n**要求**：利用 BST 性质，$O(h)$ 完成。",
    input_format="一行，BST 的层序序列（`null` 表示空节点）。节点数 $\\le 10^5$。",
    output_format="一行一个整数；空树输出空行。",
    constraints=["节点数 ≤ 10^5", "保证是合法 BST", "要求 O(h)"],
    solver=s_bst_max,
    specs=[("样例 1", "5 3 8 1", 10), ("空树", "null", 10),
           ("单节点", "7", 15), ("右链", "5 null 8 null null null 9", 15),
           ("含负数", "0 -1 1", 20), ("完整 BST", "8 4 12 2 6 10 14", 20)],
    cpp=cpp_body("""int main(){auto tk=readTok();if(tk.empty())tk.push_back("null");
Node*root=buildTree(tk);
if(!root){printf("\\n");return 0;}
Node*cur=root;
while(cur->r)cur=cur->r;
printf("%lld\\n",cur->v);return 0;}
"""),
    hint="**BST 的最大值在最右端**：从根出发**一路向右**，走到底就是最大值。\n\n时间 $O(h)$。",
)

# ---------------------------------------------------------------- 11
def s_height_edges(t):
    root = parse(t)
    if root is None:
        return "0\n"
    def h(n):
        if n is None:
            return -1          # 空节点高度为 -1，叶子高度为 0
        return 1 + max(h(n.l), h(n.r))
    return f"{h(root)}\n"


add(
    pid="tree-height-edges", title="二叉树的高度（按边数）", difficulty="入门",
    tags=["树", "二叉树", "递归"], source="树的高度", url="https://leetcode.cn/problems/maximum-depth-of-binary-tree/",
    statement="求二叉树的高度，定义为**根到最远叶子的边数**。\n\n> 注意与「最大深度」的区别：最大深度按**节点数**计，高度按**边数**计，两者相差 1。\n\n空树高度为 $0$。",
    input_format="一行，二叉树的层序序列（`null` 表示空节点）。节点数 $\\le 10^5$。",
    output_format="一行一个整数。",
    constraints=["节点数 ≤ 10^5", "高度按边数计", "空树高度为 0"],
    solver=s_height_edges,
    specs=[("样例 1", "1 2 3", 10), ("空树", "null", 10),
           ("单节点", "1", 15), ("链状", "1 2 null 3 null 4", 15),
           ("完整树", "1 2 3 4 5 6 7", 20), ("两节点", "1 2", 20)],
    cpp=cpp_body("""int h(Node*n){if(!n)return -1;return 1+max(h(n->l),h(n->r));}
int main(){auto tk=readTok();if(tk.empty())tk.push_back("null");
Node*root=buildTree(tk);
if(!root){printf("0\\n");return 0;}     // 空树高度为 0
printf("%d\\n",h(root));return 0;}
"""),
    hint="**递归求高度**：空节点返回 $-1$，叶子返回 $0$，其余返回 `1 + max(左高, 右高)`。\n\n> **关键点**：空节点返回 $-1$（而不是 0）才能让**叶子高度为 0**。若想求「最大深度」（节点数），空节点返回 0 即可。",
)

# ---------------------------------------------------------------- 12
def s_sum_depths(t):
    root = parse(t)
    if root is None:
        return "0\n"
    total = 0
    q = deque([(root, 0)])
    while q:
        n, d = q.popleft()
        total += d
        if n.l:
            q.append((n.l, d + 1))
        if n.r:
            q.append((n.r, d + 1))
    return f"{total}\n"


add(
    pid="tree-sum-depths", title="所有节点的深度之和", difficulty="简单",
    tags=["树", "二叉树", "BFS"], source="树的性质", url="https://leetcode.cn/problems/sum-of-root-to-leaf-binary-numbers/",
    statement="根节点深度为 $0$，其余节点的深度等于父节点深度加 1。\n\n求二叉树中**所有节点的深度之和**。空树输出 $0$。",
    input_format="一行，二叉树的层序序列（`null` 表示空节点）。节点数 $\\le 10^5$。",
    output_format="一行一个整数。",
    constraints=["节点数 ≤ 10^5", "根深度为 0"],
    solver=s_sum_depths,
    specs=[("样例 1", "1 2 3", 10), ("空树", "null", 10),
           ("单节点", "1", 15), ("完整树", "1 2 3 4 5 6 7", 15),
           ("链状", "1 2 null 3", 20), ("两节点", "1 2", 20)],
    cpp=cpp_body("""int main(){auto tk=readTok();if(tk.empty())tk.push_back("null");
Node*root=buildTree(tk);
if(!root){printf("0\\n");return 0;}
long long total=0;queue<pair<Node*,int>>q;q.push({root,0});
while(!q.empty()){auto pr=q.front();q.pop();
total+=pr.second;
if(pr.first->l)q.push({pr.first->l,pr.second+1});
if(pr.first->r)q.push({pr.first->r,pr.second+1});}
printf("%lld\\n",total);return 0;}
"""),
    hint="**BFS 带层号**：队列中同时存节点和它的深度，出队时累加。\n\n时间 $O(n)$。\n\n> **另解**：也可以用 DFS 传深度参数。",
)

# ---------------------------------------------------------------- 13
def s_count_greater(t):
    ls = t.strip("\n").split("\n")
    root = parse(ls[0])
    x = int(ls[1])
    cnt = 0
    if root:
        st = [root]
        while st:
            n = st.pop()
            if n.v > x:
                cnt += 1
            if n.l:
                st.append(n.l)
            if n.r:
                st.append(n.r)
    return f"{cnt}\n"


add(
    pid="tree-count-greater", title="统计大于给定值的节点数", difficulty="入门",
    tags=["树", "二叉树", "遍历"], source="二叉树基础", url="https://leetcode.cn/problems/count-complete-tree-nodes/",
    statement="统计二叉树中**值严格大于 $x$** 的节点个数。",
    input_format="第一行，二叉树的层序序列（`null` 表示空节点）。\n\n第二行一个整数 $x$。",
    output_format="一行一个整数。",
    constraints=["节点数 ≤ 10^5", "|v|, |x| ≤ 10^9"],
    solver=s_count_greater,
    specs=[("样例 1", "1 2 3\n1", 10), ("全部大于", "5 6 7\n1", 10),
           ("全部不大于", "1 2 3\n10", 15), ("空树", "null\n0", 15),
           ("含负数", "-1 -2 0\n-2", 20), ("严格大于", "5 5 5\n5", 20)],
    cpp=cpp_body("""int main(){string line;getline(cin,line);
stringstream ss(line);vector<string>tk;string t;
while(ss>>t)tk.push_back(t);
if(tk.empty())tk.push_back("null");
long long x;scanf("%lld",&x);
Node*root=buildTree(tk);int cnt=0;
vector<Node*>st;if(root)st.push_back(root);
while(!st.empty()){Node*n=st.back();st.pop_back();
if(n->v>x)++cnt;
if(n->l)st.push_back(n->l);
if(n->r)st.push_back(n->r);}
printf("%d\\n",cnt);return 0;}
"""),
    hint="**遍历计数**：判断 `v > x`（**严格大于**）。\n\n> **注意**：等于 $x$ 的**不计数**。",
)

# ---------------------------------------------------------------- 14
def s_level_max(t):
    root = parse(t)
    if root is None:
        return "\n"
    res = []
    q = deque([root])
    while q:
        sz = len(q)
        best = None
        for _ in range(sz):
            n = q.popleft()
            best = n.v if best is None else max(best, n.v)
            if n.l:
                q.append(n.l)
            if n.r:
                q.append(n.r)
        res.append(str(best))
    return " ".join(res) + "\n"


add(
    pid="tree-level-max", title="二叉树每一层的最大值", difficulty="中等",
    tags=["树", "二叉树", "BFS", "层序"], source="LeetCode 515", url="https://leetcode.cn/problems/find-largest-value-in-each-tree-row/",
    statement="输出二叉树**每一层节点值的最大值**，从根所在层开始，以空格分隔。\n\n空树输出空行。",
    input_format="一行，二叉树的层序序列（`null` 表示空节点）。节点数 $\\le 10^4$，$|v| \\le 10^9$。",
    output_format="一行，各层最大值，以空格分隔；空树输出空行。",
    constraints=["节点数 ≤ 10^4", "|v| ≤ 10^9"],
    solver=s_level_max,
    specs=[("样例 1", "1 3 2 5 3 null 9", 10), ("空树", "null", 10),
           ("单节点", "5", 15), ("完整树", "1 2 3 4 5 6 7", 15),
           ("含负数", "-1 -2 -3", 20), ("只有左链", "1 2 null 3", 20)],
    cpp=cpp_body("""int main(){auto tk=readTok();if(tk.empty())tk.push_back("null");
Node*root=buildTree(tk);
if(!root){printf("\\n");return 0;}
queue<Node*>q;q.push(root);bool first=true;
while(!q.empty()){int sz=q.size();long long best=LLONG_MIN;
for(int i=0;i<sz;++i){Node*n=q.front();q.pop();
best=max(best,n->v);
if(n->l)q.push(n->l);if(n->r)q.push(n->r);}
if(!first)printf(" ");printf("%lld",best);first=false;}
printf("\\n");return 0;}
"""),
    hint="**层序遍历 + 逐层取最大**：每层先固定 `sz = q.size()`，处理这一层时维护该层最大值。\n\n> **易错点**：每层的最大值初值要用 $-\\infty$（或该层第一个节点的值），不能用 0——节点值可能是负数。\n\n时间 $O(n)$。",
)


def main() -> None:
    for p in P:
        finalize(p, OUT / f"{p['id']}.json")
        total = sum(t["score"] for t in p["tests"])
        print(f"生成 {p['id']:34s} {len(p['tests'])} 测试点, 总分 {total:3d}")


if __name__ == "__main__":
    main()
