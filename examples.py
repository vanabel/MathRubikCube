"""
魔方置换群 - 高级示例
Advanced Examples for Rubik's Cube Permutation Group Model
"""

from cube import *


def example_commutators():
    """示例1: 交换子的性质"""
    print("\n" + "="*70)
    print("📐 示例1: 交换子的性质")
    print("="*70)
    
    # 单个交换子
    print("\n1. 简单交换子 [R, U]")
    analyze_algorithm("[R, U]")
    
    # 嵌套交换子
    print("\n2. 嵌套交换子 [F, [R, U]]")
    analyze_algorithm("[F, [R, U]]")
    
    # 双层嵌套
    print("\n3. 双层嵌套 [[F, R], [U, R]]")
    analyze_algorithm("[[F, R], [U, R]]")
    
    print("\n💡 观察: 交换子通常会产生三循环，这在魔方还原中很有用！")


def example_famous_algorithms():
    """示例2: 著名的魔方公式"""
    print("\n" + "="*70)
    print("🎯 示例2: 著名的魔方公式")
    print("="*70)
    
    algorithms = {
        "Sexy Move": "R U R' U'",
        "Sune": "R U R' U R U2 R'",
        "Antisune": "R U2 R' U' R U' R'",
        "T-Perm": "R U R' U' R' F R2 U' R' U' R U R' F'",
        "J-Perm": "R U R' F' R U R' U' R' F R2 U' R'",
    }
    
    for name, alg in algorithms.items():
        print(f"\n🔹 {name}")
        print(f"   公式: {alg}")
        corner_perm, edge_perm = get_algorithm_permutation(alg)
        corner_cycles = permutation_cycles(corner_perm)
        edge_cycles = permutation_cycles(edge_perm)
        print(f"   角块循环: {format_cycles(corner_cycles)}")
        print(f"   棱块循环: {format_cycles(edge_cycles)}")


def example_order_of_algorithms():
    """示例3: 计算公式的阶（重复多少次回到初始状态）"""
    print("\n" + "="*70)
    print("🔄 示例3: 公式的阶（Order）")
    print("="*70)
    
    test_algorithms = [
        ("R U R' U'", "Sexy Move"),
        ("R U2 R' U' R U' R'", "Antisune"),
        ("[R, U]", "交换子 [R, U]"),
    ]
    
    for alg, name in test_algorithms:
        print(f"\n🔹 {name}: {alg}")
        
        state = CubeState()
        count = 0
        max_iterations = 1000
        
        while count < max_iterations:
            state = apply_algorithm(state, alg)
            count += 1
            
            if state.is_solved():
                print(f"   ✓ 阶 = {count} (重复{count}次后回到初始状态)")
                break
        
        if count == max_iterations:
            print(f"   ⚠️  超过{max_iterations}次迭代未找到阶")


def example_permutation_composition():
    """示例4: 置换的复合"""
    print("\n" + "="*70)
    print("🔗 示例4: 置换的复合")
    print("="*70)
    
    print("\n研究: R U R' U' 与 F 的复合")
    
    # 先应用 R U R' U'
    alg1 = "R U R' U'"
    print(f"\n第一步: {alg1}")
    corner1, edge1 = get_algorithm_permutation(alg1)
    print(f"角块循环: {format_cycles(permutation_cycles(corner1))}")
    
    # 再应用 F
    alg2 = "F"
    print(f"\n第二步: {alg2}")
    corner2, edge2 = get_algorithm_permutation(alg2)
    print(f"角块循环: {format_cycles(permutation_cycles(corner2))}")
    
    # 复合结果
    alg_combined = alg1 + " " + alg2
    print(f"\n复合结果: {alg_combined}")
    corner_c, edge_c = get_algorithm_permutation(alg_combined)
    print(f"角块循环: {format_cycles(permutation_cycles(corner_c))}")
    
    # 验证复合
    corner_composed = compose_permutation(corner1, corner2)
    print(f"\n✓ 验证: 手动复合 = {corner_composed == corner_c}")


def example_inverse():
    """示例5: 逆操作"""
    print("\n" + "="*70)
    print("↩️  示例5: 逆操作")
    print("="*70)
    
    alg = "R U R' U R U2 R'"
    print(f"\n原公式: {alg}")
    
    # 获取原公式的置换
    corner_perm, edge_perm = get_algorithm_permutation(alg)
    print(f"角块循环: {format_cycles(permutation_cycles(corner_perm))}")
    
    # 计算逆
    moves = parse_algorithm(alg)
    inverse_moves = invert_sequence(moves)
    inverse_alg = " ".join(inverse_moves)
    
    print(f"\n逆公式: {inverse_alg}")
    corner_inv, edge_inv = get_algorithm_permutation(inverse_alg)
    print(f"角块循环: {format_cycles(permutation_cycles(corner_inv))}")
    
    # 验证：原公式 + 逆公式 = 恒等
    combined = alg + " " + inverse_alg
    print(f"\n验证: {alg} + 逆 = ?")
    analyze_algorithm(combined)


def example_three_cycles():
    """示例6: 寻找三循环"""
    print("\n" + "="*70)
    print("🔺 示例6: 寻找三循环（三角置换）")
    print("="*70)
    
    print("\n三循环在魔方还原中非常重要，因为任何偶置换都可以分解为三循环的乘积。")
    
    test_algs = [
        "[R, U]",
        "[F, [R, U]]",
        "[R U R', F]",
        "R U R' U' R' F R F'",
    ]
    
    for alg in test_algs:
        corner_perm, edge_perm = get_algorithm_permutation(alg)
        corner_cycles = permutation_cycles(corner_perm)
        edge_cycles = permutation_cycles(edge_perm)
        
        has_3cycle = any(len(c) == 3 for c in corner_cycles) or \
                     any(len(c) == 3 for c in edge_cycles)
        
        if has_3cycle:
            print(f"\n✓ {alg}")
            print(f"  角块: {format_cycles(corner_cycles)}")
            print(f"  棱块: {format_cycles(edge_cycles)}")


def example_custom_commutators():
    """示例7: 自定义交换子探索"""
    print("\n" + "="*70)
    print("🔬 示例7: 自定义交换子探索")
    print("="*70)
    
    print("\n探索不同的交换子组合，寻找有趣的置换模式：")
    
    base_moves = ["F", "R", "U"]
    
    print("\n所有简单交换子 [X, Y]：")
    for i, x in enumerate(base_moves):
        for y in base_moves[i+1:]:
            alg = f"[{x}, {y}]"
            corner_perm, _ = get_algorithm_permutation(alg)
            corner_cycles = permutation_cycles(corner_perm)
            
            print(f"\n  {alg}")
            print(f"    角块: {format_cycles(corner_cycles)}")
            
            # 统计循环长度
            cycle_lengths = sorted([len(c) for c in corner_cycles])
            if cycle_lengths:
                print(f"    循环长度: {cycle_lengths}")


def example_visualization_prep():
    """示例8: 为可视化准备数据"""
    print("\n" + "="*70)
    print("📊 示例8: 为可视化准备数据")
    print("="*70)
    
    alg = "[F, [R, U]]"
    print(f"\n公式: {alg}")
    
    # 获取置换
    corner_perm, edge_perm = get_algorithm_permutation(alg)
    
    print("\n角块移动映射：")
    for i in range(8):
        if corner_perm[i] != i:
            print(f"  角块 {i} → {corner_perm[i]}")
    
    print("\n棱块移动映射：")
    for i in range(12):
        if edge_perm[i] != i:
            print(f"  棱块 {i} → {edge_perm[i]}")
    
    # 追踪一个特定块的轨迹
    print("\n\n追踪角块0的轨迹：")
    state = CubeState()
    moves = parse_algorithm(alg)
    
    trajectory = [0]  # 初始位置
    current_pos = 0
    
    for move_name in moves:
        if move_name in MOVES:
            move = MOVES[move_name]
            # 找到当前位置的块会移动到哪里
            for i, val in enumerate(move.corner_perm):
                if val == current_pos:
                    current_pos = i
                    trajectory.append(current_pos)
                    break
    
    print(f"  轨迹: {' → '.join(map(str, trajectory))}")


def main():
    """主函数：运行所有示例"""
    print("\n" + "="*70)
    print("🎲 魔方置换群 - 高级示例集")
    print("="*70)
    
    examples = [
        ("交换子的性质", example_commutators),
        ("著名的魔方公式", example_famous_algorithms),
        ("公式的阶", example_order_of_algorithms),
        ("置换的复合", example_permutation_composition),
        ("逆操作", example_inverse),
        ("寻找三循环", example_three_cycles),
        ("自定义交换子探索", example_custom_commutators),
        ("为可视化准备数据", example_visualization_prep),
    ]
    
    print("\n可用示例：")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    
    print("\n" + "="*70)
    
    # 运行所有示例
    for name, func in examples:
        try:
            func()
        except Exception as e:
            print(f"\n❌ 示例 '{name}' 运行出错: {e}")
    
    print("\n" + "="*70)
    print("✅ 所有示例运行完成！")
    print("="*70)


if __name__ == "__main__":
    main()

