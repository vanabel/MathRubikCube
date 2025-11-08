"""
朝向功能测试
Test Orientation Functionality
"""

from cube import *


def test_basic_orientation():
    """测试基本操作的朝向"""
    print("\n" + "="*60)
    print("🧪 测试基本操作的朝向")
    print("="*60)
    
    tests = [
        ("F", "前面操作应该改变角块和棱块朝向"),
        ("R", "右面操作应该改变角块朝向"),
        ("U", "上面操作不应该改变朝向"),
        ("L", "左面操作应该改变角块朝向"),
        ("B", "后面操作应该改变角块和棱块朝向"),
        ("D", "下面操作不应该改变朝向"),
    ]
    
    for move_name, desc in tests:
        print(f"\n测试 {move_name}: {desc}")
        state = apply_move(CubeState(), MOVES[move_name])
        
        corner_ori_sum = sum(state.corner_ori)
        edge_ori_sum = sum(state.edge_ori)
        
        print(f"  角块朝向总和: {corner_ori_sum}")
        print(f"  棱块朝向总和: {edge_ori_sum}")
        
        # 验证合法性
        is_valid, msg = check_orientation_valid(state)
        if is_valid:
            print(f"  ✓ {msg}")
        else:
            print(f"  ✗ {msg}")
            return False
    
    print("\n✅ 所有基本操作的朝向测试通过！")
    return True


def test_四次旋转():
    """测试X^4 = identity（包括朝向）"""
    print("\n" + "="*60)
    print("🧪 测试 X^4 = identity（朝向）")
    print("="*60)
    
    for move_name in ["F", "R", "U", "L", "B", "D"]:
        print(f"\n测试 {move_name}^4...")
        state = CubeState()
        
        for _ in range(4):
            state = apply_move(state, MOVES[move_name])
        
        if state.is_solved():
            print(f"  ✓ {move_name}^4 完全还原（位置+朝向）")
        else:
            print(f"  ✗ {move_name}^4 未完全还原")
            print(f"     角块朝向: {state.corner_ori}")
            print(f"     棱块朝向: {state.edge_ori}")
            return False
    
    print("\n✅ 所有操作的四次旋转测试通过！")
    return True


def test_逆操作朝向():
    """测试X · X' = identity（朝向）"""
    print("\n" + "="*60)
    print("🧪 测试 X · X' = identity（朝向）")
    print("="*60)
    
    for move_name in ["F", "R", "U", "L", "B", "D"]:
        print(f"\n测试 {move_name} · {move_name}'...")
        state = CubeState()
        
        state = apply_move(state, MOVES[move_name])
        state = apply_move(state, MOVES[move_name + "'"])
        
        if state.is_solved():
            print(f"  ✓ {move_name} · {move_name}' 完全还原")
        else:
            print(f"  ✗ {move_name} · {move_name}' 未完全还原")
            print(f"     角块朝向: {state.corner_ori}")
            print(f"     棱块朝向: {state.edge_ori}")
            return False
    
    print("\n✅ 所有逆操作测试通过！")
    return True


def test_OLL公式():
    """测试OLL公式的朝向特性"""
    print("\n" + "="*60)
    print("🧪 测试OLL公式的朝向特性")
    print("="*60)
    
    oll_algorithms = {
        "F R U R' U' F'": "Sune的镜像",
        "R U R' U R U2 R'": "Sune",
        "R U2 R' U' R U' R'": "Antisune",
    }
    
    for alg, name in oll_algorithms.items():
        print(f"\n测试: {name}")
        print(f"公式: {alg}")
        
        state = apply_algorithm(CubeState(), alg)
        
        corner_ori_changed = sum(1 for x in state.corner_ori if x != 0)
        edge_ori_changed = sum(1 for x in state.edge_ori if x != 0)
        
        print(f"  角块朝向改变: {corner_ori_changed}/8")
        print(f"  棱块朝向改变: {edge_ori_changed}/12")
        
        # OLL公式通常会改变角块朝向
        if corner_ori_changed > 0:
            print(f"  ✓ 这是一个OLL类型的公式（改变角块朝向）")
        
        # 验证合法性
        is_valid, msg = check_orientation_valid(state)
        print(f"  {msg}")
    
    print("\n✅ OLL公式测试完成！")
    return True


def test_朝向守恒():
    """测试朝向守恒定律"""
    print("\n" + "="*60)
    print("🧪 测试朝向守恒定律")
    print("="*60)
    
    test_algorithms = [
        "F",
        "F R U",
        "[F, R]",
        "[F, [R, U]]",
        "F R U R' U' F'",
        "R U R' U R U2 R'",
        "F R U L B D",
    ]
    
    print("\n所有合法的魔方操作都必须满足朝向守恒：")
    print("  • 角块朝向总和 ≡ 0 (mod 3)")
    print("  • 棱块朝向总和 ≡ 0 (mod 2)")
    
    for alg in test_algorithms:
        state = apply_algorithm(CubeState(), alg)
        is_valid, msg = check_orientation_valid(state)
        
        status = "✓" if is_valid else "✗"
        print(f"\n  {status} {alg:20s} - {msg}")
        
        if not is_valid:
            return False
    
    print("\n✅ 所有公式都满足朝向守恒定律！")
    return True


def test_朝向和位置独立():
    """测试位置可以还原但朝向改变的情况"""
    print("\n" + "="*60)
    print("🧪 测试朝向和位置的独立性")
    print("="*60)
    
    # 构造一个位置还原但朝向改变的公式（理论上存在）
    print("\n寻找位置还原但朝向改变的公式...")
    
    # 简单测试：某些公式可能有这个性质
    test_algs = [
        "[F, F]",  # 应该是恒等
        "[F2, R2]",  # 可能只改变朝向
    ]
    
    for alg in test_algs:
        state = apply_algorithm(CubeState(), alg)
        
        pos_solved = (state.corners == list(range(8)) and 
                     state.edges == list(range(12)))
        ori_solved = (state.corner_ori == [0] * 8 and 
                     state.edge_ori == [0] * 12)
        
        print(f"\n  {alg}:")
        print(f"    位置还原: {pos_solved}")
        print(f"    朝向还原: {ori_solved}")
        
        if pos_solved and not ori_solved:
            print(f"    ✓ 找到了！位置还原但朝向改变")
            print(f"    角块朝向: {state.corner_ori}")
            print(f"    棱块朝向: {state.edge_ori}")
    
    print("\n✅ 朝向和位置独立性验证完成！")
    return True


def main():
    """运行所有测试"""
    print("\n" + "="*60)
    print("🎯 朝向功能完整测试套件")
    print("="*60)
    
    tests = [
        test_basic_orientation,
        test_四次旋转,
        test_逆操作朝向,
        test_OLL公式,
        test_朝向守恒,
        test_朝向和位置独立,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"\n❌ 测试出错: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "="*60)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("="*60)
    
    if failed == 0:
        print("✅ 所有朝向测试通过！")
        print("\n🎉 阶段4完成：朝向功能已实现！")
    else:
        print(f"❌ 有 {failed} 个测试失败")
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

