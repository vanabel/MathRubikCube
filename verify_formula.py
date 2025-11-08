#!/usr/bin/env python3
"""
公式验证工具
帮助对比模型和真实魔方的效果
"""

from cube import *


def verify_formula_step_by_step(alg_str):
    """逐步验证公式"""
    print("\n" + "="*70)
    print(f"📋 逐步验证公式: {alg_str}")
    print("="*70)
    
    moves = parse_algorithm(alg_str)
    print(f"\n展开为: {' '.join(moves)}")
    print(f"共 {len(moves)} 步")
    
    print("\n" + "="*70)
    print("请在真实魔方上同步执行，并对比每一步：")
    print("="*70)
    
    state = CubeState()
    corner_names = ['UFR', 'UFL', 'UBL', 'UBR', 'DFR', 'DFL', 'DBL', 'DBR']
    edge_names = ['UF', 'UL', 'UB', 'UR', 'FR', 'FL', 'BL', 'BR', 'DF', 'DL', 'DB', 'DR']
    
    for step, move_name in enumerate(moves, 1):
        print(f"\n{'─'*70}")
        print(f"第 {step} 步: {move_name}")
        print(f"{'─'*70}")
        
        # 在真实魔方上的操作说明
        move_desc = {
            'F': '前面顺时针转90度', 'F\'': '前面逆时针转90度',
            'R': '右面顺时针转90度', 'R\'': '右面逆时针转90度',
            'U': '上面顺时针转90度', 'U\'': '上面逆时针转90度',
            'L': '左面顺时针转90度', 'L\'': '左面逆时针转90度',
            'B': '后面顺时针转90度', 'B\'': '后面逆时针转90度',
            'D': '下面顺时针转90度', 'D\'': '下面逆时针转90度',
        }
        
        print(f"真实魔方操作: {move_desc.get(move_name, move_name)}")
        
        # 应用操作
        old_state = state.copy()
        state = apply_move(state, MOVES[move_name])
        
        # 显示变化
        print("\n模型预测的变化:")
        
        # 角块变化
        corner_changes = []
        for i in range(8):
            if old_state.corners[i] != state.corners[i] or old_state.corner_ori[i] != state.corner_ori[i]:
                corner_changes.append(i)
        
        if corner_changes:
            print(f"  角块变化（{len(corner_changes)}个）:")
            for i in corner_changes:
                print(f"    位置{i}({corner_names[i]}): {old_state.corners[i]}→{state.corners[i]}, 朝向{old_state.corner_ori[i]}→{state.corner_ori[i]}")
        
        # 棱块变化
        edge_changes = []
        for i in range(12):
            if old_state.edges[i] != state.edges[i] or old_state.edge_ori[i] != state.edge_ori[i]:
                edge_changes.append(i)
        
        if edge_changes:
            print(f"  棱块变化（{len(edge_changes)}个）:")
            for i in edge_changes:
                print(f"    位置{i:2d}({edge_names[i]}): {old_state.edges[i]}→{state.edges[i]}, 朝向{old_state.edge_ori[i]}→{state.edge_ori[i]}")
        
        input(f"\n按Enter继续下一步...")
    
    print("\n" + "="*70)
    print("✅ 公式执行完成")
    print("="*70)
    
    print("\n最终状态：")
    corner_cycles = permutation_cycles(state.corners)
    edge_cycles = permutation_cycles(state.edges)
    
    print(f"角块循环: {format_cycles(corner_cycles)}")
    print(f"棱块循环: {format_cycles(edge_cycles)}")
    print(f"角块朝向: {state.corner_ori}")
    print(f"棱块朝向: {state.edge_ori}")
    
    print("\n在真实魔方上验证：")
    print("  1. 检查哪些块的位置改变了？")
    print("  2. 检查哪些块的朝向（颜色方向）改变了？")
    print("  3. 与模型预测对比")


def check_common_oll_formulas():
    """检查常见OLL公式"""
    print("\n" + "="*70)
    print("📚 常见OLL公式对比")
    print("="*70)
    
    oll_formulas = {
        "OLL 45": "F R U R' U' F'",
        "Sune (OLL 27)": "R U R' U R U2 R'",
        "Antisune (OLL 26)": "R U2 R' U' R U' R'",
        "OLL 21": "R U R' U R U' R' U R U2 R'",
        "OLL 22": "R U2 R2 U' R2 U' R2 U2 R",
    }
    
    print("\n验证这些公式是否满足守恒定律:")
    
    for name, alg in oll_formulas.items():
        state = apply_algorithm(CubeState(), alg)
        is_valid, msg = check_orientation_valid(state)
        
        corner_ori_sum = sum(state.corner_ori)
        edge_ori_sum = sum(state.edge_ori)
        
        status = "✓" if is_valid else "✗"
        print(f"\n  {status} {name:20s}")
        print(f"      公式: {alg}")
        print(f"      角块朝向和: {corner_ori_sum} (mod 3 = {corner_ori_sum % 3})")
        print(f"      棱块朝向和: {edge_ori_sum} (mod 2 = {edge_ori_sum % 2})")
        print(f"      {msg}")


def suggest_verification_method():
    """建议验证方法"""
    print("\n" + "="*70)
    print("🔍 如何验证模型的正确性")
    print("="*70)
    
    print("""\n方法1: 在真实魔方上测试
  1. 准备一个还原的魔方
  2. 用贴纸标记以下块：
     - UBL(2) 上后左角
     - UBR(3) 上后右角  
     - DFR(4) 下前右角
     - DBR(7) 下后右角
  3. 执行 F R U R' U' F'
  4. 检查这4个角块是否：
     - UBL↔DBR 交换了？
     - UBR↔DFR 交换了？

方法2: 使用在线魔方模拟器
  1. 访问: https://ruwix.com/online-puzzle-simulators/3x3x3-rubiks-cube-solver/
  2. 输入公式: F R U R' U' F'
  3. 观察哪些块移动了
  4. 与我的模型对比

方法3: 查阅标准资料
  1. 查看 algdb.net 的OLL公式
  2. 查看 speedcubedb.com
  3. 对比循环结构
""")


def main():
    """主函数"""
    import sys
    
    if len(sys.argv) > 1:
        alg = " ".join(sys.argv[1:])
        verify_formula_step_by_step(alg)
    else:
        check_common_oll_formulas()
        suggest_verification_method()


if __name__ == "__main__":
    main()

