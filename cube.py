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

from typing import List, Tuple, Dict, Optional
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


# ========== 角块/棱块位置编号与常用子集（用于位置过滤） ==========
#
# 角块索引 0-7（位置名 → 编号）：
#   0: UFR  1: UFL  2: UBL  3: UBR  4: DFR  5: DFL  6: DBL  7: DBR
# 棱块索引 0-11：
#   0: UF  1: UL  2: UB  3: UR  4: FR  5: FL  6: BL  7: BR  8: DF  9: DL  10: DB  11: DR
#
# 以下常量可直接用于 is_three_cycle_algorithm / enumerate_commutator_three_cycles 的
# allowed_corners / allowed_edges 参数。

# 角块：按层/面
CORNER_TOP: List[int] = [0, 1, 2, 3]      # 顶层四角 UFR,UFL,UBL,UBR
CORNER_BOTTOM: List[int] = [4, 5, 6, 7]   # 底层四角 DFR,DFL,DBL,DBR
CORNER_FRONT: List[int] = [0, 1, 4, 5]    # 前层四角
CORNER_BACK: List[int] = [2, 3, 6, 7]      # 后层四角
CORNER_RIGHT: List[int] = [0, 3, 4, 7]     # 右层四角
CORNER_LEFT: List[int] = [1, 2, 5, 6]      # 左层四角

# 棱块：按层/面
EDGE_TOP: List[int] = [0, 1, 2, 3]       # 顶层四棱 UF,UL,UB,UR
EDGE_BOTTOM: List[int] = [8, 9, 10, 11]  # 底层四棱 DF,DL,DB,DR
EDGE_FRONT: List[int] = [0, 4, 5, 8]     # 前层四棱
EDGE_BACK: List[int] = [2, 6, 7, 10]     # 后层四棱
EDGE_RIGHT: List[int] = [3, 4, 7, 11]    # 右层四棱
EDGE_LEFT: List[int] = [1, 5, 6, 9]      # 左层四棱

# 所有位置（不过滤时可用 None，或显式传以下列表）
CORNER_ALL: List[int] = list(range(8))
EDGE_ALL: List[int] = list(range(12))


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


def permutation_parity(perm: List[int]) -> int:
    """
    计算置换的奇偶性
    
    返回值:
        0 表示偶置换, 1 表示奇置换
    """
    inv_count = 0
    n = len(perm)
    for i in range(n):
        for j in range(i + 1, n):
            if perm[i] > perm[j]:
                inv_count += 1
    return inv_count % 2


def get_algorithm_parity(alg_str: str) -> Tuple[int, int, int]:
    """
    计算公式对应置换的奇偶性
    
    Returns:
        (角块奇偶性, 棱块奇偶性, 总奇偶性)
    """
    corner_perm, edge_perm = get_algorithm_permutation(alg_str)
    corner_parity = permutation_parity(corner_perm)
    edge_parity = permutation_parity(edge_perm)
    total_parity = (corner_parity + edge_parity) % 2
    return corner_parity, edge_parity, total_parity


def get_algorithm_order(alg_str: str, max_power: int = 1000) -> int:
    """
    计算公式在整个魔方群中的阶（最小正整数 n 使得 公式^n = 恒等）
    
    注意:
        - 这里的恒等包括位置和朝向完全恢复
        - 如果在 max_power 次迭代内没有回到恒等, 返回 -1
    """
    moves = parse_algorithm(alg_str)
    if not moves:
        return 1
    
    state = CubeState()
    for power in range(1, max_power + 1):
        for move_name in moves:
            if move_name in MOVES:
                state = apply_move(state, MOVES[move_name])
        if state.is_solved():
            return power
    return -1


def invert_algorithm(alg_str: str) -> str:
    """返回公式的逆公式字符串"""
    moves = parse_algorithm(alg_str)
    inv_moves = invert_sequence(moves)
    return " ".join(inv_moves)


def compose_algorithms(*alg_strs: str) -> str:
    """依次复合多个公式, 返回合成后的公式字符串"""
    parts: List[str] = []
    for s in alg_strs:
        if not s:
            continue
        parts.extend(parse_algorithm(s))
    return " ".join(parts)


def commutator(alg_a: str, alg_b: str) -> str:
    """
    构造交换子 [A, B] = A B A⁻¹ B⁻¹ 的显式公式字符串
    
    这在研究换向子子群 [G, G] 时非常有用。
    """
    a = " ".join(parse_algorithm(alg_a))
    b = " ".join(parse_algorithm(alg_b))
    a_inv = invert_algorithm(a)
    b_inv = invert_algorithm(b)
    return " ".join([a, b, a_inv, b_inv])


def conjugate(alg_x: str, alg_a: str) -> str:
    """
    构造共轭 x A x⁻¹ 的显式公式字符串
    
    共轭用于“搬运”某个局部操作到空间中的其他位置。
    """
    x = " ".join(parse_algorithm(alg_x))
    a = " ".join(parse_algorithm(alg_a))
    x_inv = invert_algorithm(x)
    return " ".join([x, a, x_inv])


def _cycles_respect_allowed_positions(
    cycles: List[Tuple[int, ...]],
    allowed: Optional[List[int]],
) -> bool:
    """
    检查所有非平凡循环是否完全落在 allowed 给定的位置集合中
    
    如果 allowed 为 None, 认为总是满足。
    """
    if allowed is None:
        return True
    allowed_set = set(allowed)
    for cycle in cycles:
        for v in cycle:
            if v not in allowed_set:
                return False
    return True


def algorithm_position_key(alg_str: str) -> Tuple[Tuple[int, ...], Tuple[int, ...]]:
    """
    只看位置（忽略朝向）时, 把一个公式对应的群元素编码为键值
    
    返回:
        (角块置换元组, 棱块置换元组)
    """
    corner_perm, edge_perm = get_algorithm_permutation(alg_str)
    return tuple(corner_perm), tuple(edge_perm)


def is_three_cycle_algorithm(
    alg_str: str,
    part: str = "any",
    pure: bool = False,
    allowed_corners: Optional[List[int]] = None,
    allowed_edges: Optional[List[int]] = None,
) -> bool:
    """
    判定一个公式是否实现了“某类三循环”
    
    Args:
        alg_str: 公式字符串
        part:    作用部位:
                 - 'corner': 只看角块
                 - 'edge'  : 只看棱块
                 - 'both'  : 角块和棱块都要出现三循环
                 - 'any'   : 任一出现三循环即可
        pure:    是否要求是“纯三循环”:
                 - True : 该部分必须恰好只有一个3-循环且其余全固定
                 - False: 只要存在长度为3的循环即可（可以伴随其他循环）
    """
    corner_perm, edge_perm = get_algorithm_permutation(alg_str)
    corner_cycles = permutation_cycles(corner_perm)
    edge_cycles = permutation_cycles(edge_perm)

    # 如果给定了限制位置, 要求所有被移动的位置都在允许集合中
    if not _cycles_respect_allowed_positions(corner_cycles, allowed_corners):
        return False
    if not _cycles_respect_allowed_positions(edge_cycles, allowed_edges):
        return False

    def has_3(cycles):
        return any(len(c) == 3 for c in cycles)

    def is_pure_3(cycles):
        return len(cycles) == 1 and len(cycles[0]) == 3

    if part == "corner":
        ok = has_3(corner_cycles)
        pure_ok = is_pure_3(corner_cycles)
    elif part == "edge":
        ok = has_3(edge_cycles)
        pure_ok = is_pure_3(edge_cycles)
    elif part == "both":
        ok = has_3(corner_cycles) and has_3(edge_cycles)
        pure_ok = is_pure_3(corner_cycles) and is_pure_3(edge_cycles)
    else:  # 'any'
        ok = has_3(corner_cycles) or has_3(edge_cycles)
        pure_ok = is_pure_3(corner_cycles) or is_pure_3(edge_cycles)

    return pure_ok if pure else ok


def enumerate_commutator_three_cycles(
    base_moves: List[str] = None,
    nested: bool = False,
    part: str = "any",
    pure: bool = False,
    allowed_corners: Optional[List[int]] = None,
    allowed_edges: Optional[List[int]] = None,
) -> List[Dict[str, object]]:
    """
    系统枚举由交换子产生的三循环
    
    Args:
        base_moves: 参与构造的基本操作集合, 默认使用 ["F", "R", "U", "L", "B", "D"]
        nested    : 是否枚举嵌套交换子 [A, [B, C]]
        part      : 三循环作用部位, 见 is_three_cycle_algorithm
        pure      : 是否要求纯三循环
    
    Returns:
        一个字典列表, 每个元素包含:
        {
            "alg": 公式字符串,
            "corner_cycles": 角块循环,
            "edge_cycles":   棱块循环,
            "order":         元素阶,
            "parity":        (角块奇偶, 棱块奇偶, 总奇偶)
        }
    """
    if base_moves is None:
        base_moves = ["F", "R", "U", "L", "B", "D"]

    results: Dict[Tuple[Tuple[int, ...], Tuple[int, ...]], Dict[str, object]] = {}

    # 简单交换子 [A, B]
    for i, a in enumerate(base_moves):
        for b in base_moves[i + 1 :]:
            alg = f"[{a}, {b}]"
            if not is_three_cycle_algorithm(
                alg,
                part=part,
                pure=pure,
                allowed_corners=allowed_corners,
                allowed_edges=allowed_edges,
            ):
                continue
            key = algorithm_position_key(alg)
            if key in results:
                continue
            corner_perm, edge_perm = get_algorithm_permutation(alg)
            corner_cycles = permutation_cycles(corner_perm)
            edge_cycles = permutation_cycles(edge_perm)
            order = get_algorithm_order(alg, max_power=200)
            parity = get_algorithm_parity(alg)
            results[key] = {
                "alg": alg,
                "corner_cycles": corner_cycles,
                "edge_cycles": edge_cycles,
                "order": order,
                "parity": parity,
            }

    # 嵌套交换子 [A, [B, C]]
    if nested:
        n = len(base_moves)
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    a = base_moves[i]
                    b = base_moves[j]
                    c = base_moves[k]
                    inner = f"[{b}, {c}]"
                    alg = f"[{a}, {inner}]"
                    if not is_three_cycle_algorithm(
                        alg,
                        part=part,
                        pure=pure,
                        allowed_corners=allowed_corners,
                        allowed_edges=allowed_edges,
                    ):
                        continue
                    key = algorithm_position_key(alg)
                    if key in results:
                        continue
                    corner_perm, edge_perm = get_algorithm_permutation(alg)
                    corner_cycles = permutation_cycles(corner_perm)
                    edge_cycles = permutation_cycles(edge_perm)
                    order = get_algorithm_order(alg, max_power=500)
                    parity = get_algorithm_parity(alg)
                    results[key] = {
                        "alg": alg,
                        "corner_cycles": corner_cycles,
                        "edge_cycles": edge_cycles,
                        "order": order,
                        "parity": parity,
                    }

    return list(results.values())


def sample_commutators(
    generators: List[str] = None,
    max_word_length: int = 2,
) -> List[str]:
    """
    在有限深度内, 采样由生成元构成的交换子集合
    
    步骤:
        1. 用 generators 及其逆元生成长度 ≤ max_word_length 的所有单词
        2. 对所有 (w1, w2) 计算交换子 [w1, w2]
        3. 仅按“位置置换”去重, 返回代表性公式列表
    """
    if generators is None:
        generators = ["F", "R", "U", "L", "B", "D"]

    # 字母表: 生成元及其逆
    alphabet: List[str] = []
    for g in generators:
        if g not in alphabet:
            alphabet.append(g)
        g_inv = invert_algorithm(g)
        if g_inv not in alphabet:
            alphabet.append(g_inv)

    # 生成长度 ≤ max_word_length 的所有单词
    words: List[str] = []
    current = [""]
    for _ in range(max_word_length):
        next_level: List[str] = []
        for w in current:
            for a in alphabet:
                new = (w + " " + a).strip()
                if new not in words:
                    words.append(new)
                next_level.append(new)
        current = next_level

    # 计算所有交换子, 并按位置置换去重
    commutators: Dict[Tuple[Tuple[int, ...], Tuple[int, ...]], str] = {}
    for w1 in words:
        for w2 in words:
            alg = commutator(w1, w2)
            key = algorithm_position_key(alg)
            if key not in commutators:
                commutators[key] = alg

    return list(commutators.values())


def classify_conjugacy_classes(
    algs: List[str],
    conjugators: List[str] = None,
) -> List[Dict[str, object]]:
    """
    在给定有限集合 algs 中, 按共轭关系划分共轭类并统计
    
    Args:
        algs: 有限个公式字符串, 视为一个有限子集
        conjugators: 用于共轭的元素集合, 默认使用基本操作 ["F", "R", "U", "L", "B", "D"]
    
    Returns:
        每个共轭类一个字典:
        {
            "representative": 代表公式,
            "size":           在样本集中的类大小,
            "corner_cycles":  代表元的角块循环,
            "edge_cycles":    代表元的棱块循环,
            "order":          代表元阶,
            "parity": {
                "corner": 角块奇偶,
                "edge":   棱块奇偶,
                "total":  总奇偶,
            },
        }
    """
    if conjugators is None:
        conjugators = ["F", "R", "U", "L", "B", "D"]

    # 构造共轭器集合: 包含逆元
    conj_elems: List[str] = []
    for g in conjugators:
        if g not in conj_elems:
            conj_elems.append(g)
        g_inv = invert_algorithm(g)
        if g_inv not in conj_elems:
            conj_elems.append(g_inv)

    # 把样本元素按“位置置换”编码
    key_to_alg: Dict[Tuple[Tuple[int, ...], Tuple[int, ...]], str] = {}
    for alg in algs:
        key = algorithm_position_key(alg)
        if key not in key_to_alg:
            key_to_alg[key] = alg

    unclassified = set(key_to_alg.keys())
    classes: List[Dict[str, object]] = []

    while unclassified:
        rep_key = unclassified.pop()
        rep_alg = key_to_alg[rep_key]

        # BFS 找到该共轭类在样本中的所有元素
        class_keys = {rep_key}
        queue = [rep_key]

        while queue:
            key = queue.pop()
            alg = key_to_alg[key]
            for c in conj_elems:
                conj_alg = conjugate(c, alg)
                conj_key = algorithm_position_key(conj_alg)
                if conj_key in unclassified and conj_key not in class_keys:
                    class_keys.add(conj_key)
                    unclassified.remove(conj_key)
                    queue.append(conj_key)

        # 用代表元计算一些群论不变量
        rep_corner, rep_edge = get_algorithm_permutation(rep_alg)
        corner_cycles = permutation_cycles(rep_corner)
        edge_cycles = permutation_cycles(rep_edge)
        corner_parity, edge_parity, total_parity = get_algorithm_parity(rep_alg)
        order = get_algorithm_order(rep_alg, max_power=500)

        classes.append(
            {
                "representative": rep_alg,
                "size": len(class_keys),
                "corner_cycles": corner_cycles,
                "edge_cycles": edge_cycles,
                "order": order,
                "parity": {
                    "corner": corner_parity,
                    "edge": edge_parity,
                    "total": total_parity,
                },
            }
        )

    return classes


def commutator_conjugacy_statistics(
    generators: List[str] = None,
    max_word_length: int = 1,
) -> List[Dict[str, object]]:
    """
    综合工具: 
        1. 在给定生成元及深度下采样所有交换子
        2. 按共轭关系划分共轭类
        3. 返回每个共轭类的代表元及基本统计信息
    
    这对于直观地“观察”换向子子群 [G, G] 在有限采样下的结构很有用。
    """
    comms = sample_commutators(generators=generators, max_word_length=max_word_length)
    return classify_conjugacy_classes(comms, conjugators=generators)


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
    
    # 奇偶性分析
    corner_parity, edge_parity, total_parity = get_algorithm_parity(alg_str)
    parity_str = lambda p: "偶置换" if p == 0 else "奇置换"
    print(f"\n【奇偶性分析】")
    print(f"角块置换: {parity_str(corner_parity)}")
    print(f"棱块置换: {parity_str(edge_parity)}")
    print(f"整体置换: {parity_str(total_parity)}")
    
    # 群元素的阶
    order = get_algorithm_order(alg_str, max_power=500)
    print(f"\n【元素阶】")
    if order == -1:
        print(f"在 500 次复合内未回到恒等，阶 > 500（或非常大）")
    else:
        print(f"公式的阶 = {order}")
    
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

