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
    
    使用置换表示魔方的状态：
    - corners: 8个角块的置换，索引0-7
    - edges: 12个棱块的置换，索引0-11
    
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
    """
    
    def __init__(self, corners: List[int] = None, edges: List[int] = None):
        """初始化魔方状态"""
        self.corners = corners if corners is not None else list(range(8))
        self.edges = edges if edges is not None else list(range(12))
    
    def copy(self) -> 'CubeState':
        """复制当前状态"""
        return CubeState(self.corners.copy(), self.edges.copy())
    
    def is_solved(self) -> bool:
        """检查是否已还原"""
        return (self.corners == list(range(8)) and 
                self.edges == list(range(12)))
    
    def __repr__(self) -> str:
        return f"CubeState(corners={self.corners}, edges={self.edges})"


class Move:
    """
    魔方操作类
    
    每个操作定义为角块和棱块上的置换
    """
    
    def __init__(self, name: str, corner_perm: List[int], edge_perm: List[int]):
        """
        初始化操作
        
        Args:
            name: 操作名称（如 "F", "R", "U"）
            corner_perm: 角块置换（长度8）
            edge_perm: 棱块置换（长度12）
        """
        self.name = name
        self.corner_perm = corner_perm
        self.edge_perm = edge_perm
    
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
F_CORNERS = [4, 0, 2, 3, 5, 1, 6, 7]  # 位置i的块来自F_CORNERS[i]

# 影响的棱块：UF(0) -> FR(4) -> DF(8) -> FL(5) -> UF(0)
# 即循环：(0 4 8 5)
F_EDGES = [4, 1, 2, 3, 8, 0, 6, 7, 5, 9, 10, 11]

# R (Right) - 右面顺时针90度
# 影响的角块：UFR(0) -> UBR(3) -> DBR(7) -> DFR(4) -> UFR(0)
# 即循环：(0 3 7 4)
R_CORNERS = [3, 1, 2, 7, 0, 5, 6, 4]

# 影响的棱块：UR(3) -> BR(7) -> DR(11) -> FR(4) -> UR(3)
# 即循环：(3 7 11 4)
R_EDGES = [0, 1, 2, 7, 3, 5, 6, 11, 8, 9, 10, 4]

# U (Up) - 上面顺时针90度
# 影响的角块：UFR(0) -> UBR(3) -> UBL(2) -> UFL(1) -> UFR(0)
# 即循环：(0 3 2 1)
U_CORNERS = [3, 0, 1, 2, 4, 5, 6, 7]

# 影响的棱块：UF(0) -> UR(3) -> UB(2) -> UL(1) -> UF(0)
# 即循环：(0 3 2 1)
U_EDGES = [3, 0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11]

# 创建操作字典
MOVES: Dict[str, Move] = {
    "F": Move("F", F_CORNERS, F_EDGES),
    "R": Move("R", R_CORNERS, R_EDGES),
    "U": Move("U", U_CORNERS, U_EDGES),
    "F'": Move("F'", invert_permutation(F_CORNERS), invert_permutation(F_EDGES)),
    "R'": Move("R'", invert_permutation(R_CORNERS), invert_permutation(R_EDGES)),
    "U'": Move("U'", invert_permutation(U_CORNERS), invert_permutation(U_EDGES)),
}

# 添加F2, R2, U2 (180度旋转)
MOVES["F2"] = Move("F2", 
                   compose_permutation(F_CORNERS, F_CORNERS),
                   compose_permutation(F_EDGES, F_EDGES))
MOVES["R2"] = Move("R2",
                   compose_permutation(R_CORNERS, R_CORNERS),
                   compose_permutation(R_EDGES, R_EDGES))
MOVES["U2"] = Move("U2",
                   compose_permutation(U_CORNERS, U_CORNERS),
                   compose_permutation(U_EDGES, U_EDGES))


def apply_move(state: CubeState, move: Move) -> CubeState:
    """
    应用一个操作到魔方状态
    
    Args:
        state: 当前魔方状态
        move: 要应用的操作
    
    Returns:
        新的魔方状态
    """
    new_state = state.copy()
    new_state.corners = apply_permutation(state.corners, move.corner_perm)
    new_state.edges = apply_permutation(state.edges, move.edge_perm)
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
    
    print(f"\n【角块置换】")
    print(f"置换: {corner_perm}")
    print(f"循环分解: {format_cycles(corner_cycles)}")
    if corner_cycles:
        print(f"移动的角块数: {sum(len(c) for c in corner_cycles)}")
    
    print(f"\n【棱块置换】")
    print(f"置换: {edge_perm}")
    print(f"循环分解: {format_cycles(edge_cycles)}")
    if edge_cycles:
        print(f"移动的棱块数: {sum(len(c) for c in edge_cycles)}")
    
    # 检查是否为恒等置换
    if not corner_cycles and not edge_cycles:
        print(f"\n✓ 这是恒等置换，魔方回到初始状态！")
    
    print(f"{'='*60}\n")


if __name__ == "__main__":
    print("🚀 魔方置换群数学模型 - 演示程序")
    print("="*60)
    
    # 测试基本操作
    print("\n1️⃣ 测试基本操作")
    print("-"*60)
    
    for move_name in ["F", "R", "U"]:
        move = MOVES[move_name]
        corner_cycles = permutation_cycles(move.corner_perm)
        edge_cycles = permutation_cycles(move.edge_perm)
        
        print(f"\n操作 {move_name}:")
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

