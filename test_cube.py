"""
魔方置换群 - 单元测试
Unit Tests for Rubik's Cube Permutation Group Model
"""

from cube import *


def test_basic_moves():
    """测试基本操作"""
    print("\n测试基本操作...")
    
    state = CubeState()
    
    # 测试F操作
    state_f = apply_move(state, MOVES["F"])
    assert state_f.corners != state.corners, "F操作应该改变状态"
    
    # 测试F4 = identity
    state_f4 = state.copy()
    for _ in range(4):
        state_f4 = apply_move(state_f4, MOVES["F"])
    assert state_f4.is_solved(), "F^4 应该回到初始状态"
    
    print("  ✓ 基本操作测试通过")


def test_inverse():
    """测试逆操作"""
    print("\n测试逆操作...")
    
    for move_name in ["F", "R", "U"]:
        state = CubeState()
        
        # 应用操作
        state = apply_move(state, MOVES[move_name])
        # 应用逆操作
        state = apply_move(state, MOVES[move_name + "'"])
        
        assert state.is_solved(), f"{move_name} {move_name}' 应该回到初始状态"
    
    print("  ✓ 逆操作测试通过")


def test_permutation_composition():
    """测试置换复合"""
    print("\n测试置换复合...")
    
    p = [1, 2, 0, 3]  # (0 1 2)
    q = [0, 2, 1, 3]  # (1 2)
    
    # p * q
    pq = compose_permutation(p, q)
    
    # 手动验证
    state = [0, 1, 2, 3]
    state = apply_permutation(state, p)
    state = apply_permutation(state, q)
    
    assert apply_permutation([0, 1, 2, 3], pq) == state, "置换复合应该正确"
    
    print("  ✓ 置换复合测试通过")


def test_permutation_inverse():
    """测试置换求逆"""
    print("\n测试置换求逆...")
    
    p = [1, 2, 3, 0, 4, 5, 6, 7]  # (0 1 2 3)
    p_inv = invert_permutation(p)
    
    # p * p_inv = identity
    identity = compose_permutation(p, p_inv)
    assert identity == list(range(8)), "p * p^-1 应该是恒等置换"
    
    print("  ✓ 置换求逆测试通过")


def test_cycles():
    """测试循环分解"""
    print("\n测试循环分解...")
    
    # 测试单个循环
    p1 = [1, 2, 0, 3, 4]  # (0 1 2)
    cycles1 = permutation_cycles(p1)
    assert cycles1 == [(0, 1, 2)], "应该识别三循环"
    
    # 测试多个循环
    p2 = [1, 0, 3, 2, 4]  # (0 1)(2 3)
    cycles2 = permutation_cycles(p2)
    assert len(cycles2) == 2, "应该识别两个二循环"
    
    # 测试恒等置换
    p3 = [0, 1, 2, 3]
    cycles3 = permutation_cycles(p3)
    assert cycles3 == [], "恒等置换没有循环"
    
    print("  ✓ 循环分解测试通过")


def test_algorithm_parsing():
    """测试公式解析"""
    print("\n测试公式解析...")
    
    # 测试简单公式
    moves1 = parse_algorithm("F R U")
    assert moves1 == ["F", "R", "U"], "简单公式应该正确解析"
    
    # 测试逆操作
    moves2 = parse_algorithm("F' R' U'")
    assert moves2 == ["F'", "R'", "U'"], "逆操作应该正确解析"
    
    # 测试双层
    moves3 = parse_algorithm("F2 R2")
    assert moves3 == ["F2", "R2"], "双层操作应该正确解析"
    
    print("  ✓ 公式解析测试通过")


def test_commutator():
    """测试交换子"""
    print("\n测试交换子...")
    
    # [R, U] = R U R' U'
    alg1 = "[R, U]"
    moves1 = parse_algorithm(alg1)
    assert moves1 == ["R", "U", "R'", "U'"], "交换子应该正确展开"
    
    # 验证交换子性质：[A, B] 应该是偶置换
    corner_perm, _ = get_algorithm_permutation(alg1)
    cycles = permutation_cycles(corner_perm)
    
    # 计算置换的符号（奇偶性）
    total_moves = sum(len(c) - 1 for c in cycles)
    assert total_moves % 2 == 0, "交换子应该是偶置换"
    
    print("  ✓ 交换子测试通过")


def test_nested_commutator():
    """测试嵌套交换子"""
    print("\n测试嵌套交换子...")
    
    alg = "[F, [R, U]]"
    moves = parse_algorithm(alg)
    
    # 应该展开为 F [R,U] F' [R,U]'
    # = F R U R' U' F' U R U' R'
    expected = ["F", "R", "U", "R'", "U'", "F'", "U", "R", "U'", "R'"]
    assert moves == expected, f"嵌套交换子展开错误: {moves}"
    
    print("  ✓ 嵌套交换子测试通过")


def test_algorithm_order():
    """测试公式的阶"""
    print("\n测试公式的阶...")
    
    # Sexy Move 的阶应该是 6
    alg = "R U R' U'"
    state = CubeState()
    
    for i in range(1, 10):
        state = apply_algorithm(state, alg)
        if state.is_solved():
            assert i == 6, f"Sexy Move 的阶应该是 6，但得到 {i}"
            break
    
    print("  ✓ 公式阶测试通过")


def test_inverse_algorithm():
    """测试公式求逆"""
    print("\n测试公式求逆...")
    
    alg = "R U R' U R U2 R'"
    moves = parse_algorithm(alg)
    inverse_moves = invert_sequence(moves)
    
    # 验证：原公式 + 逆 = identity
    combined_alg = alg + " " + " ".join(inverse_moves)
    corner, edge = get_algorithm_permutation(combined_alg)
    
    assert corner == list(range(8)), "角块应该回到初始状态"
    assert edge == list(range(12)), "棱块应该回到初始状态"
    
    print("  ✓ 公式求逆测试通过")


def test_three_cycles():
    """测试三循环"""
    print("\n测试三循环...")
    
    # [F, [R, U]] 应该产生角块三循环
    alg = "[F, [R, U]]"
    corner_perm, _ = get_algorithm_permutation(alg)
    cycles = permutation_cycles(corner_perm)
    
    # 应该有一个长度为3的循环
    has_3cycle = any(len(c) == 3 for c in cycles)
    assert has_3cycle, "应该产生三循环"
    
    print("  ✓ 三循环测试通过")


def run_all_tests():
    """运行所有测试"""
    print("="*60)
    print("🧪 运行单元测试")
    print("="*60)
    
    tests = [
        test_basic_moves,
        test_inverse,
        test_permutation_composition,
        test_permutation_inverse,
        test_cycles,
        test_algorithm_parsing,
        test_commutator,
        test_nested_commutator,
        test_algorithm_order,
        test_inverse_algorithm,
        test_three_cycles,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ {test.__name__} 失败: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ {test.__name__} 错误: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("="*60)
    
    if failed == 0:
        print("✅ 所有测试通过！")
    else:
        print(f"❌ 有 {failed} 个测试失败")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)

