"""
测试所有6个面的操作
"""

from cube import *

def test_all_basic_moves():
    """测试所有基本操作"""
    print("\n" + "="*60)
    print("🧪 测试所有6个面的操作")
    print("="*60)
    
    all_moves = ["F", "R", "U", "L", "B", "D"]
    faces = {"F": "前", "R": "右", "U": "上", "L": "左", "B": "后", "D": "下"}
    
    for move_name in all_moves:
        print(f"\n测试 {move_name} ({faces[move_name]}面)...")
        
        # 测试1: 四次旋转回到初始状态
        state = CubeState()
        for _ in range(4):
            state = apply_move(state, MOVES[move_name])
        
        assert state.is_solved(), f"{move_name}^4 应该回到初始状态"
        print(f"  ✓ {move_name}^4 = identity")
        
        # 测试2: 操作 + 逆操作 = 恒等
        state = CubeState()
        state = apply_move(state, MOVES[move_name])
        state = apply_move(state, MOVES[move_name + "'"])
        
        assert state.is_solved(), f"{move_name} · {move_name}' 应该回到初始状态"
        print(f"  ✓ {move_name} · {move_name}' = identity")
        
        # 测试3: 双层 = 两次单层
        state1 = CubeState()
        state1 = apply_move(state1, MOVES[move_name])
        state1 = apply_move(state1, MOVES[move_name])
        
        state2 = CubeState()
        state2 = apply_move(state2, MOVES[move_name + "2"])
        
        assert state1.corners == state2.corners, f"{move_name}2 角块应该等于两次{move_name}"
        assert state1.edges == state2.edges, f"{move_name}2 棱块应该等于两次{move_name}"
        print(f"  ✓ {move_name}2 = {move_name} · {move_name}")
        
        # 显示循环结构
        move = MOVES[move_name]
        corner_cycles = permutation_cycles(move.corner_perm)
        edge_cycles = permutation_cycles(move.edge_perm)
        print(f"  角块循环: {format_cycles(corner_cycles)}")
        print(f"  棱块循环: {format_cycles(edge_cycles)}")
    
    print("\n" + "="*60)
    print("✅ 所有6个面的操作测试通过！")
    print("="*60)


def test_famous_algorithms_with_all_moves():
    """测试使用所有操作的著名公式"""
    print("\n" + "="*60)
    print("🎯 测试著名魔方公式（使用全部操作）")
    print("="*60)
    
    algorithms = {
        "超级翻转": "M' U' M' U' M' U M' U M' U' M' U' M' U M' U",  # 需要中层
        "T-Perm完整": "R U R' U' R' F R2 U' R' U' R U R' F'",
        "Y-Perm": "F R U' R' U' R U R' F' R U R' U' R' F R F'",
        "简单六面": "F R U L B D",
        "交换子[L,D]": "[L, D]",
        "嵌套[B,[L,D]]": "[B, [L, D]]",
    }
    
    for name, alg in algorithms.items():
        try:
            print(f"\n🔹 {name}")
            print(f"   公式: {alg}")
            
            corner_perm, edge_perm = get_algorithm_permutation(alg)
            corner_cycles = permutation_cycles(corner_perm)
            edge_cycles = permutation_cycles(edge_perm)
            
            print(f"   角块循环: {format_cycles(corner_cycles)}")
            print(f"   棱块循环: {format_cycles(edge_cycles)}")
        except Exception as e:
            print(f"   ⚠️  跳过: {e}")


def test_all_commutators():
    """测试所有简单交换子"""
    print("\n" + "="*60)
    print("🔬 测试所有简单交换子 [X, Y]")
    print("="*60)
    
    base_moves = ["F", "R", "U", "L", "B", "D"]
    three_cycles = []
    
    for i, x in enumerate(base_moves):
        for y in base_moves[i+1:]:
            alg = f"[{x}, {y}]"
            corner_perm, edge_perm = get_algorithm_permutation(alg)
            corner_cycles = permutation_cycles(corner_perm)
            edge_cycles = permutation_cycles(edge_perm)
            
            # 检查是否有三循环
            has_3cycle = any(len(c) == 3 for c in corner_cycles) or \
                         any(len(c) == 3 for c in edge_cycles)
            
            if has_3cycle:
                three_cycles.append((alg, corner_cycles, edge_cycles))
    
    print(f"\n找到 {len(three_cycles)} 个产生三循环的交换子：\n")
    for alg, c_cycles, e_cycles in three_cycles:
        print(f"  {alg:10s} 角块: {format_cycles(c_cycles):30s} 棱块: {format_cycles(e_cycles)}")


def main():
    """主测试函数"""
    test_all_basic_moves()
    test_famous_algorithms_with_all_moves()
    test_all_commutators()
    
    print("\n" + "="*60)
    print("✅ 所有测试完成！")
    print("="*60)


if __name__ == "__main__":
    main()

