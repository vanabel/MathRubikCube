#!/usr/bin/env python3
"""
cube 模块使用示例（对应 docs/USAGE_REFERENCE.md）

在项目根目录执行：python examples/usage_demo.py
"""
import sys
from pathlib import Path

# 保证可导入项目根目录的 cube
_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from cube import (
    CubeState,
    MOVES,
    apply_move,
    apply_algorithm,
    parse_algorithm,
    get_algorithm_permutation,
    permutation_cycles,
    format_cycles,
    get_algorithm_parity,
    get_algorithm_order,
    invert_algorithm,
    commutator,
    conjugate,
    is_three_cycle_algorithm,
    enumerate_commutator_three_cycles,
    CORNER_TOP,
    EDGE_TOP,
    check_orientation_valid,
    analyze_algorithm,
)


def main():
    print("=== 1. 状态与单步 ===")
    s = CubeState()
    assert s.is_solved()
    s = apply_move(s, MOVES["F"])
    assert not s.is_solved()
    s = apply_algorithm(CubeState(), "F F F F")
    assert s.is_solved()
    print("  CubeState / apply_move / apply_algorithm 正常\n")

    print("=== 2. 公式与置换 ===")
    moves = parse_algorithm("[R, U]")
    assert len(moves) == 4
    cp, ep = get_algorithm_permutation("R U R' U'")
    print("  R U R' U' 角块循环:", format_cycles(permutation_cycles(cp)))
    print("  R U R' U' 棱块循环:", format_cycles(permutation_cycles(ep)), "\n")

    print("=== 3. 群论 ===")
    print("  奇偶性:", get_algorithm_parity("R U R' U'"))
    print("  阶 F:", get_algorithm_order("F"), "| R U R' U':", get_algorithm_order("R U R' U'"))
    inv = invert_algorithm("F R")
    s = apply_algorithm(CubeState(), "F R " + inv)
    assert s.is_solved()
    print("  交换子 [R,U]:", commutator("R", "U"))
    print("  共轭 F(R U R' U')F':", conjugate("F", "R U R' U'"), "\n")

    print("=== 4. 三循环与位置过滤 ===")
    assert is_three_cycle_algorithm("R U R' U'", part="any") is True
    results = enumerate_commutator_three_cycles(
        allowed_corners=CORNER_TOP,
        allowed_edges=EDGE_TOP,
    )
    print("  顶层角+顶层棱三循环交换子个数:", len(results))
    for r in results[:2]:
        print("   ", r["alg"], "阶:", r["order"], "角:", r["corner_cycles"], "棱:", r["edge_cycles"])
    print()

    print("=== 5. 朝向与综合分析 ===")
    s = apply_algorithm(CubeState(), "F R U R' U' F'")
    ok, msg = check_orientation_valid(s)
    print("  朝向合法:", ok, msg)
    print("  --- analyze_algorithm 输出 ---")
    analyze_algorithm("F R U R' U' F'")
    print("  --- 示例结束 ---")


if __name__ == "__main__":
    main()
