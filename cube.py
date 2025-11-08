"""
魔方置换群数学模型
Rubik's Cube Permutation Group Model

本模块实现了三阶魔方的置换群模型，包括：
1. 角块和棱块的置换表示
2. 基本操作（F, R, U等）的置换定义
3. 公式解析和执行
4. 交换子计算
5. 循环分解输出
"""

from typing import List, Tuple, Dict
import re


class CubeState:
    """
    魔方状态类
    
    使用置换和朝向表示魔方的完整状态：
    - corners: 8个角块的置换，索引0-7
    - edges: 12个棱块的置换，索引0-11
    - corner_ori: 8个角块的朝向，取值0,1,2
    - edge_ori: 12个棱块的朝向，取值0,1
    
    角块编号（从上前右逆时针）：
    0: UFR (上前右)
    1: UFL (上前左) 
    2: UBL (上后左)
    3: UBR (上后右)
    4: DFR (下前右)
    5: DFL (下前左)
    6: DBL (下后左)
    7: DBR (下后右)
    
    棱块编号：
    0: UF (上前)
    1: UL (上左)
    2: UB (上后)
    3: UR (上右)
    4: FR (前右)
    5: FL (前左)
    6: BL (后左)
    7: BR (后右)
    8: DF (下前)
    9: DL (下左)
    10: DB (下后)
    11: DR (下右)
    
    朝向说明：
    - 角块朝向：0=正常, 1=顺时针120°, 2=逆时针120°
    - 棱块朝向：0=正常, 1=翻转180°
    """
    
    def __init__(self, corners: List[int] = None, edges: List[int] = None,
                 corner_ori: List[int] = None, edge_ori: List[int] = None):
        """初始化魔方状态"""
        self.corners = corners if corners is not None else list(range(8))
        self.edges = edges if edges is not None else list(range(12))
        self.corner_ori = corner_ori if corner_ori is not None else [0] * 8
        self.edge_ori = edge_ori if edge_ori is not None else [0] * 12
    
    def copy(self) -> 'CubeState':
        """复制当前状态"""
        return CubeState(
            self.corners.copy(), 
            self.edges.copy(),
            self.corner_ori.copy(),
            self.edge_ori.copy()
        )
    
    def is_solved(self) -> bool:
        """检查是否已还原"""
        return (self.corners == list(range(8)) and 
                self.edges == list(range(12)) and
                self.corner_ori == [0] * 8 and
                self.edge_ori == [0] * 12)
    
    def __repr__(self) -> str:
        return f"CubeState(corners={self.corners}, edges={self.edges}, " \
               f"corner_ori={self.corner_ori}, edge_ori={self.edge_ori})"


class Move:
    """
    魔方操作类
    
    每个操作定义为角块和棱块上的置换和朝向变化
    """
    
    def __init__(self, name: str, corner_perm: List[int], edge_perm: List[int],
                 corner_ori: List[int] = None, edge_ori: List[int] = None):
        """
        初始化操作
        
        Args:
            name: 操作名称（如 "F", "R", "U"）
            corner_perm: 角块置换（长度8）
            edge_perm: 棱块置换（长度12）
            corner_ori: 角块朝向变化（长度8），默认全0
            edge_ori: 棱块朝向变化（长度12），默认全0
        """
        self.name = name
        self.corner_perm = corner_perm
        self.edge_perm = edge_perm
        self.corner_ori = corner_ori if corner_ori is not None else [0] * 8
        self.edge_ori = edge_ori if edge_ori is not None else [0] * 12
    
    def __repr__(self) -> str:
        return f"Move({self.name})"


def apply_permutation(state: List[int], perm: List[int]) -> List[int]:
    """
    应用置换到状态
    
    Args:
        state: 当前状态
        perm: 置换
    
    Returns:
        新状态
    """
    return [state[perm[i]] for i in range(len(state))]


def compose_permutation(p: List[int], q: List[int]) -> List[int]:
    """
    复合两个置换：先应用p，再应用q
    
    Args:
        p: 第一个置换
        q: 第二个置换
    
    Returns:
        复合置换
    """
    return [p[q[i]] for i in range(len(p))]


def invert_permutation(p: List[int]) -> List[int]:
    """
    求置换的逆
    
    Args:
        p: 置换
    
    Returns:
        逆置换
    """
    inv = [0] * len(p)
    for i in range(len(p)):
        inv[p[i]] = i
    return inv


def permutation_cycles(perm: List[int]) -> List[Tuple[int, ...]]:
    """
    将置换分解为循环
    
    Args:
        perm: 置换
    
    Returns:
        循环列表，每个循环是一个元组
    """
    n = len(perm)
    visited = [False] * n
    cycles = []
    
    for start in range(n):
        if visited[start] or perm[start] == start:
            continue
        
        cycle = []
        current = start
        while not visited[current]:
            visited[current] = True
            cycle.append(current)
            current = perm[current]
        
        if len(cycle) > 1:
            cycles.append(tuple(cycle))
    
    return cycles


def format_cycles(cycles: List[Tuple[int, ...]]) -> str:
    """格式化循环输出"""
    if not cycles:
        return "identity (恒等置换)"
    return " ".join(f"({' '.join(map(str, cycle))})" for cycle in cycles)


# ========== 基本操作定义 ==========

# F (Front) - 前面顺时针90度
# 影响的角块：UFR(0) -> DFR(4) -> DFL(5) -> UFL(1) -> UFR(0)
# 即循环：(0 4 5 1)
# 位置0←块1, 位置1←块5, 位置4←块0, 位置5←块4
F_CORNERS = [1, 5, 2, 3, 0, 4, 6, 7]  # 位置i的块来自F_CORNERS[i]

# 影响的棱块：UF(0) -> FR(4) -> DF(8) -> FL(5) -> UF(0)
# 即循环：(0 4 8 5)
# 位置0←块5, 位置4←块0, 位置5←块8, 位置8←块4
F_EDGES = [5, 1, 2, 3, 0, 8, 6, 7, 4, 9, 10, 11]

# F操作的朝向变化
# 角块：前面的4个角块朝向会改变（UFR, UFL, DFR, DFL）
# 规则：顺时针移入前面的角块朝向+1，逆时针移入的+2 (mod 3)
F_CORNER_ORI = [1, 2, 0, 0, 2, 1, 0, 0]  # 位置i的块朝向增加F_CORNER_ORI[i]

# 棱块：前面的4个棱块朝向会翻转
F_EDGE_ORI = [1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0]  # 位置i的块朝向增加F_EDGE_ORI[i] (mod 2)

# R (Right) - 右面顺时针90度
# 影响的角块：UFR(0) -> UBR(3) -> DBR(7) -> DFR(4) -> UFR(0)
# 即循环：(0 3 7 4)
# 位置0←块4, 位置3←块0, 位置4←块7, 位置7←块3
R_CORNERS = [4, 1, 2, 0, 7, 5, 6, 3]

# 影响的棱块：UR(3) -> BR(7) -> DR(11) -> FR(4) -> UR(3)
# 即循环：(3 7 11 4)
# 位置3←块4, 位置4←块11, 位置7←块3, 位置11←块7
R_EDGES = [0, 1, 2, 4, 11, 5, 6, 3, 8, 9, 10, 7]

# R操作的朝向变化
R_CORNER_ORI = [2, 0, 0, 1, 1, 0, 0, 2]  # 右面角块朝向变化
R_EDGE_ORI = [0] * 12  # R/L操作不改变棱块朝向

# U (Up) - 上面顺时针90度
# 影响的角块：UFR(0) -> UBR(3) -> UBL(2) -> UFL(1) -> UFR(0)
# 即循环：(0 3 2 1)
# 位置0←块3, 位置1←块0, 位置2←块1, 位置3←块2
U_CORNERS = [3, 0, 1, 2, 4, 5, 6, 7]

# 影响的棱块：UF(0) -> UR(3) -> UB(2) -> UL(1) -> UF(0)
# 即循环：(0 3 2 1)
# 位置0←块3, 位置1←块0, 位置2←块1, 位置3←块2
U_EDGES = [3, 0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11]

# U操作的朝向变化
U_CORNER_ORI = [0] * 8  # U/D操作不改变角块朝向
U_EDGE_ORI = [0] * 12  # U/D操作不改变棱块朝向

# L (Left) - 左面顺时针90度
# 影响的角块：UFL(1) -> UBL(2) -> DBL(6) -> DFL(5) -> UFL(1)
# 即循环：(1 2 6 5)
# 位置1←块2, 位置2←块6, 位置5←块1, 位置6←块5
L_CORNERS = [0, 2, 6, 3, 4, 1, 5, 7]

# 影响的棱块：UL(1) -> BL(6) -> DL(9) -> FL(5) -> UL(1)
# 即循环：(1 6 9 5)
# 位置1←块6, 位置5←块1, 位置6←块9, 位置9←块5
L_EDGES = [0, 6, 2, 3, 4, 1, 9, 7, 8, 5, 10, 11]

# L操作的朝向变化
L_CORNER_ORI = [0, 1, 2, 0, 0, 2, 1, 0]  # 左面角块朝向变化
L_EDGE_ORI = [0] * 12  # R/L操作不改变棱块朝向

# B (Back) - 后面顺时针90度
# 影响的角块：UBR(3) -> UBL(2) -> DBL(6) -> DBR(7) -> UBR(3)
# 即循环：(3 2 6 7)
# 位置2←块7, 位置3←块2, 位置6←块3, 位置7←块6... wait，让我重新算
# 循环(3 2 6 7)表示 3→2→6→7→3
# 所以：位置2←块3, 位置3←块7, 位置6←块2, 位置7←块6
# 这个是对的，但实际应该反过来：位置2←块6, 位置3←块2, 位置6←块7, 位置7←块3
B_CORNERS = [0, 1, 6, 2, 4, 5, 7, 3]

# 影响的棱块：UB(2) -> BL(6) -> DB(10) -> BR(7) -> UB(2)
# 即循环：(2 6 10 7)
# 位置2←块6, 位置6←块10, 位置7←块2, 位置10←块7
B_EDGES = [0, 1, 6, 3, 4, 5, 10, 2, 8, 9, 7, 11]

# B操作的朝向变化
B_CORNER_ORI = [0, 0, 1, 2, 0, 0, 2, 1]  # 后面角块朝向变化
B_EDGE_ORI = [0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0]  # 后面棱块朝向变化

# D (Down) - 下面顺时针90度
# 影响的角块：DFR(4) -> DFL(5) -> DBL(6) -> DBR(7) -> DFR(4)
# 即循环：(4 5 6 7)
# 位置4←块5, 位置5←块6, 位置6←块7, 位置7←块4
D_CORNERS = [0, 1, 2, 3, 5, 6, 7, 4]

# 影响的棱块：DF(8) -> DL(9) -> DB(10) -> DR(11) -> DF(8)
# 即循环：(8 9 10 11)
# 位置8←块9, 位置9←块10, 位置10←块11, 位置11←块8
D_EDGES = [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 8]

# D操作的朝向变化
D_CORNER_ORI = [0] * 8  # U/D操作不改变角块朝向
D_EDGE_ORI = [0] * 12  # U/D操作不改变棱块朝向

# 创建操作字典
MOVES: Dict[str, Move] = {
    # 基本操作（包含朝向）
    "F": Move("F", F_CORNERS, F_EDGES, F_CORNER_ORI, F_EDGE_ORI),
    "R": Move("R", R_CORNERS, R_EDGES, R_CORNER_ORI, R_EDGE_ORI),
    "U": Move("U", U_CORNERS, U_EDGES, U_CORNER_ORI, U_EDGE_ORI),
    "L": Move("L", L_CORNERS, L_EDGES, L_CORNER_ORI, L_EDGE_ORI),
    "B": Move("B", B_CORNERS, B_EDGES, B_CORNER_ORI, B_EDGE_ORI),
    "D": Move("D", D_CORNERS, D_EDGES, D_CORNER_ORI, D_EDGE_ORI),
    
    # 逆操作（朝向需要特殊处理：按逆置换应用负朝向）
    "F'": Move("F'", invert_permutation(F_CORNERS), invert_permutation(F_EDGES),
               [F_CORNER_ORI[invert_permutation(F_CORNERS)[i]] for i in range(8)],
               [F_EDGE_ORI[invert_permutation(F_EDGES)[i]] for i in range(12)]),
    "R'": Move("R'", invert_permutation(R_CORNERS), invert_permutation(R_EDGES),
               [R_CORNER_ORI[invert_permutation(R_CORNERS)[i]] for i in range(8)],
               [R_EDGE_ORI[invert_permutation(R_EDGES)[i]] for i in range(12)]),
    "U'": Move("U'", invert_permutation(U_CORNERS), invert_permutation(U_EDGES),
               [0] * 8, [0] * 12),
    "L'": Move("L'", invert_permutation(L_CORNERS), invert_permutation(L_EDGES),
               [L_CORNER_ORI[invert_permutation(L_CORNERS)[i]] for i in range(8)],
               [0] * 12),
    "B'": Move("B'", invert_permutation(B_CORNERS), invert_permutation(B_EDGES),
               [B_CORNER_ORI[invert_permutation(B_CORNERS)[i]] for i in range(8)],
               [B_EDGE_ORI[invert_permutation(B_EDGES)[i]] for i in range(12)]),
    "D'": Move("D'", invert_permutation(D_CORNERS), invert_permutation(D_EDGES),
               [0] * 8, [0] * 12),
}

# 添加双层旋转 (180度) - 朝向变化是两次单层的累积
MOVES["F2"] = Move("F2", 
                   compose_permutation(F_CORNERS, F_CORNERS),
                   compose_permutation(F_EDGES, F_EDGES),
                   [(2 * x) % 3 for x in F_CORNER_ORI],  # 两次朝向变化
                   [(2 * x) % 2 for x in F_EDGE_ORI])
MOVES["R2"] = Move("R2",
                   compose_permutation(R_CORNERS, R_CORNERS),
                   compose_permutation(R_EDGES, R_EDGES),
                   [(2 * x) % 3 for x in R_CORNER_ORI],
                   [(2 * x) % 2 for x in R_EDGE_ORI])
MOVES["U2"] = Move("U2",
                   compose_permutation(U_CORNERS, U_CORNERS),
                   compose_permutation(U_EDGES, U_EDGES),
                   [0] * 8, [0] * 12)  # U不改变朝向
MOVES["L2"] = Move("L2",
                   compose_permutation(L_CORNERS, L_CORNERS),
                   compose_permutation(L_EDGES, L_EDGES),
                   [(2 * x) % 3 for x in L_CORNER_ORI],
                   [0] * 12)
MOVES["B2"] = Move("B2",
                   compose_permutation(B_CORNERS, B_CORNERS),
                   compose_permutation(B_EDGES, B_EDGES),
                   [(2 * x) % 3 for x in B_CORNER_ORI],
                   [(2 * x) % 2 for x in B_EDGE_ORI])
MOVES["D2"] = Move("D2",
                   compose_permutation(D_CORNERS, D_CORNERS),
                   compose_permutation(D_EDGES, D_EDGES),
                   [0] * 8, [0] * 12)  # D不改变朝向


def apply_move(state: CubeState, move: Move) -> CubeState:
    """
    应用一个操作到魔方状态（包括位置和朝向）
    
    Args:
        state: 当前魔方状态
        move: 要应用的操作
    
    Returns:
        新的魔方状态
    """
    new_state = state.copy()
    
    # 应用位置置换
    new_state.corners = apply_permutation(state.corners, move.corner_perm)
    new_state.edges = apply_permutation(state.edges, move.edge_perm)
    
    # 应用朝向变化
    # 角块朝向：(原朝向 + 操作引起的朝向变化) mod 3
    new_corner_ori = [0] * 8
    for i in range(8):
        # 位置i现在放着的块原来在哪里？
        original_pos = move.corner_perm[i]
        # 该块原来的朝向
        original_ori = state.corner_ori[original_pos]
        # 操作引起的朝向变化（逆操作时取负）
        ori_change = move.corner_ori[i]
        if "'" in move.name:
            ori_change = -ori_change
        # 新朝向
        new_corner_ori[i] = (original_ori + ori_change) % 3
    new_state.corner_ori = new_corner_ori
    
    # 棱块朝向：(原朝向 + 操作引起的朝向变化) mod 2
    new_edge_ori = [0] * 12
    for i in range(12):
        original_pos = move.edge_perm[i]
        original_ori = state.edge_ori[original_pos]
        ori_change = move.edge_ori[i]
        if "'" in move.name:
            ori_change = -ori_change
        new_edge_ori[i] = (original_ori + ori_change) % 2
    new_state.edge_ori = new_edge_ori
    
    return new_state


def parse_algorithm(alg_str: str) -> List[str]:
    """
    解析公式字符串为操作序列
    
    支持格式：
    - 基本操作：F, R, U
    - 逆操作：F', R', U'
    - 双层：F2, R2, U2
    - 交换子：[F, R] 表示 F R F' R'
    - 嵌套：[F, [R, U]]
    
    Args:
        alg_str: 公式字符串
    
    Returns:
        操作序列
    """
    # 递归处理交换子
    def expand_commutator(s: str) -> str:
        """展开交换子 [A, B] = A B A' B'"""
        pattern = r'\[([^\[\]]+),([^\[\]]+)\]'
        
        while '[' in s:
            # 从最内层开始展开
            match = re.search(pattern, s)
            if not match:
                break
            
            a = match.group(1).strip()
            b = match.group(2).strip()
            
            # 展开交换子
            a_inv = invert_sequence(a.split())
            b_inv = invert_sequence(b.split())
            
            expanded = f"{a} {b} {' '.join(a_inv)} {' '.join(b_inv)}"
            
            # 替换原字符串中的交换子
            s = s[:match.start()] + expanded + s[match.end():]
        
        return s
    
    # 展开所有交换子
    expanded = expand_commutator(alg_str)
    
    # 分割为单独的操作
    moves = expanded.split()
    
    return [m for m in moves if m]


def invert_sequence(moves: List[str]) -> List[str]:
    """
    反转操作序列
    
    Args:
        moves: 操作序列
    
    Returns:
        反转后的序列
    """
    def invert_single_move(move: str) -> str:
        if move.endswith("'"):
            return move[:-1]
        elif move.endswith("2"):
            return move  # 180度旋转的逆是自己
        else:
            return move + "'"
    
    return [invert_single_move(m) for m in reversed(moves)]


def apply_algorithm(state: CubeState, alg_str: str) -> CubeState:
    """
    应用一个公式到魔方状态
    
    Args:
        state: 初始状态
        alg_str: 公式字符串
    
    Returns:
        最终状态
    """
    moves = parse_algorithm(alg_str)
    current_state = state.copy()
    
    for move_name in moves:
        if move_name in MOVES:
            current_state = apply_move(current_state, MOVES[move_name])
        else:
            print(f"警告: 未知操作 '{move_name}'")
    
    return current_state


def get_algorithm_permutation(alg_str: str) -> Tuple[List[int], List[int]]:
    """
    获取公式对应的总置换
    
    Args:
        alg_str: 公式字符串
    
    Returns:
        (角块置换, 棱块置换)
    """
    initial_state = CubeState()
    final_state = apply_algorithm(initial_state, alg_str)
    return final_state.corners, final_state.edges


def check_orientation_valid(state: CubeState) -> Tuple[bool, str]:
    """
    检查朝向是否合法
    
    魔方的朝向必须满足：
    - 角块朝向总和 ≡ 0 (mod 3)
    - 棱块朝向总和 ≡ 0 (mod 2)
    
    Returns:
        (is_valid, message)
    """
    corner_ori_sum = sum(state.corner_ori) % 3
    edge_ori_sum = sum(state.edge_ori) % 2
    
    if corner_ori_sum != 0:
        return False, f"角块朝向总和 = {sum(state.corner_ori)} ≡ {corner_ori_sum} (mod 3)，应该≡0"
    
    if edge_ori_sum != 0:
        return False, f"棱块朝向总和 = {sum(state.edge_ori)} ≡ {edge_ori_sum} (mod 2)，应该≡0"
    
    return True, "朝向合法 ✓"


def analyze_algorithm(alg_str: str) -> None:
    """
    分析并打印公式的置换结构
    
    Args:
        alg_str: 公式字符串
    """
    print(f"\n{'='*60}")
    print(f"分析公式: {alg_str}")
    print(f"{'='*60}")
    
    # 解析公式
    moves = parse_algorithm(alg_str)
    print(f"\n展开后的操作序列: {' '.join(moves)}")
    print(f"操作步数: {len(moves)}")
    
    # 获取置换
    corner_perm, edge_perm = get_algorithm_permutation(alg_str)
    
    # 计算循环分解
    corner_cycles = permutation_cycles(corner_perm)
    edge_cycles = permutation_cycles(edge_perm)
    
    # 获取完整状态（包括朝向）
    final_state = apply_algorithm(CubeState(), alg_str)
    
    print(f"\n【角块置换】")
    print(f"置换: {corner_perm}")
    print(f"循环分解: {format_cycles(corner_cycles)}")
    if corner_cycles:
        print(f"移动的角块数: {sum(len(c) for c in corner_cycles)}")
    
    # 显示朝向
    print(f"朝向: {final_state.corner_ori}")
    corner_ori_changed = sum(1 for x in final_state.corner_ori if x != 0)
    if corner_ori_changed > 0:
        print(f"朝向改变的角块数: {corner_ori_changed}")
    
    print(f"\n【棱块置换】")
    print(f"置换: {edge_perm}")
    print(f"循环分解: {format_cycles(edge_cycles)}")
    if edge_cycles:
        print(f"移动的棱块数: {sum(len(c) for c in edge_cycles)}")
    
    # 显示朝向
    print(f"朝向: {final_state.edge_ori}")
    edge_ori_changed = sum(1 for x in final_state.edge_ori if x != 0)
    if edge_ori_changed > 0:
        print(f"朝向改变的棱块数: {edge_ori_changed}")
    
    # 检查朝向合法性
    is_valid, msg = check_orientation_valid(final_state)
    print(f"\n【朝向验证】{msg}")
    
    # 检查是否完全还原
    if final_state.is_solved():
        print(f"\n✓ 这是恒等操作，魔方完全回到初始状态（位置+朝向）！")
    elif not corner_cycles and not edge_cycles:
        print(f"\n⚠️  位置回到初始状态，但朝向改变了！")
    
    print(f"{'='*60}\n")


if __name__ == "__main__":
    print("🚀 魔方置换群数学模型 - 演示程序")
    print("="*60)
    
    # 测试基本操作
    print("\n1️⃣ 测试所有基本操作")
    print("-"*60)
    
    for move_name in ["F", "R", "U", "L", "B", "D"]:
        move = MOVES[move_name]
        corner_cycles = permutation_cycles(move.corner_perm)
        edge_cycles = permutation_cycles(move.edge_perm)
        
        faces = {"F": "前", "R": "右", "U": "上", "L": "左", "B": "后", "D": "下"}
        print(f"\n操作 {move_name} ({faces[move_name]}面):")
        print(f"  角块循环: {format_cycles(corner_cycles)}")
        print(f"  棱块循环: {format_cycles(edge_cycles)}")
    
    # 测试简单公式
    print("\n\n2️⃣ 测试简单公式")
    print("-"*60)
    analyze_algorithm("F R U R' U' F'")
    
    # 测试交换子
    print("\n3️⃣ 测试交换子 [R, U]")
    print("-"*60)
    analyze_algorithm("[R, U]")
    
    # 测试嵌套交换子
    print("\n4️⃣ 测试嵌套交换子 [F, [R, U]]")
    print("-"*60)
    analyze_algorithm("[F, [R, U]]")
    
    # 测试操作复合
    print("\n5️⃣ 测试操作复合 F F F F (应该回到初始状态)")
    print("-"*60)
    analyze_algorithm("F F F F")
    
    print("\n✅ 演示完成！")

