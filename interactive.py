#!/usr/bin/env python3
"""
魔方置换群 - 交互式分析工具
Interactive Cube Analyzer
"""

from cube import *
import sys


def print_menu():
    """打印菜单"""
    print("\n" + "="*70)
    print("🎲 魔方置换群交互式分析工具")
    print("="*70)
    print("\n可用命令：")
    print("  1. analyze <公式>     - 分析公式的置换结构")
    print("  2. commutator <A> <B> - 计算交换子 [A, B]")
    print("  3. order <公式>       - 计算公式的阶")
    print("  4. inverse <公式>     - 计算公式的逆")
    print("  5. compare <公式1> <公式2> - 比较两个公式")
    print("  6. moves              - 显示所有可用操作")
    print("  7. help               - 显示帮助信息")
    print("  8. examples           - 显示示例命令")
    print("  9. quit / exit        - 退出程序")
    print("\n提示：支持所有6个面的操作 F, R, U, L, B, D")
    print("     逆操作：F', R', U', L', B', D'")
    print("     双层：F2, R2, U2, L2, B2, D2")
    print("     交换子：[F, R] 或嵌套 [F, [R, U]]")
    print("="*70)


def cmd_analyze(alg):
    """分析公式"""
    analyze_algorithm(alg)


def cmd_commutator(a, b):
    """计算交换子"""
    alg = f"[{a}, {b}]"
    print(f"\n计算交换子: [{a}, {b}]")
    print(f"展开为: {a} {b} {' '.join(invert_sequence([a]))} {' '.join(invert_sequence([b]))}")
    analyze_algorithm(alg)


def cmd_order(alg):
    """计算公式的阶"""
    print(f"\n计算公式的阶: {alg}")
    print("-"*60)
    
    state = CubeState()
    count = 0
    max_iterations = 10000
    
    print("迭代中", end="", flush=True)
    
    while count < max_iterations:
        state = apply_algorithm(state, alg)
        count += 1
        
        if count % 100 == 0:
            print(".", end="", flush=True)
        
        if state.is_solved():
            print(f"\n\n✓ 阶 = {count}")
            print(f"  意义: 重复该公式 {count} 次后，魔方会回到初始状态")
            
            # 显示一些中间状态
            if count <= 10:
                print(f"\n  前几次迭代的效果：")
                temp_state = CubeState()
                for i in range(1, min(count + 1, 6)):
                    temp_state = apply_algorithm(temp_state, alg)
                    corner_cycles = permutation_cycles(temp_state.corners)
                    print(f"    第{i}次: 角块循环 {format_cycles(corner_cycles)}")
            
            return
    
    print(f"\n\n⚠️  超过 {max_iterations} 次迭代未找到阶")
    print(f"  该公式可能有非常大的阶，或者在当前模型下不会回到初始状态")


def cmd_inverse(alg):
    """计算逆公式"""
    print(f"\n原公式: {alg}")
    
    # 解析并求逆
    moves = parse_algorithm(alg)
    inverse_moves = invert_sequence(moves)
    inverse_alg = " ".join(inverse_moves)
    
    print(f"逆公式: {inverse_alg}")
    print("\n验证: 原公式 + 逆公式 应该得到恒等置换")
    
    combined = alg + " " + inverse_alg
    analyze_algorithm(combined)


def cmd_compare(alg1, alg2):
    """比较两个公式"""
    print(f"\n比较两个公式:")
    print(f"  公式1: {alg1}")
    print(f"  公式2: {alg2}")
    print("-"*60)
    
    # 获取两个公式的置换
    corner1, edge1 = get_algorithm_permutation(alg1)
    corner2, edge2 = get_algorithm_permutation(alg2)
    
    print("\n公式1:")
    print(f"  角块循环: {format_cycles(permutation_cycles(corner1))}")
    print(f"  棱块循环: {format_cycles(permutation_cycles(edge1))}")
    
    print("\n公式2:")
    print(f"  角块循环: {format_cycles(permutation_cycles(corner2))}")
    print(f"  棱块循环: {format_cycles(permutation_cycles(edge2))}")
    
    # 检查是否相同
    if corner1 == corner2 and edge1 == edge2:
        print("\n✓ 两个公式产生相同的置换！")
    else:
        print("\n✗ 两个公式产生不同的置换")
        
        # 显示差异
        if corner1 != corner2:
            print("  角块置换不同")
        if edge1 != edge2:
            print("  棱块置换不同")


def cmd_moves():
    """显示所有可用操作"""
    print("\n可用的所有操作：")
    print("="*60)
    
    faces = {"F": "前面", "R": "右面", "U": "上面", "L": "左面", "B": "后面", "D": "下面"}
    
    # 基本操作
    print("\n【基本操作】")
    for move_name in ["F", "R", "U", "L", "B", "D"]:
        move = MOVES[move_name]
        corner_cycles = permutation_cycles(move.corner_perm)
        edge_cycles = permutation_cycles(move.edge_perm)
        
        print(f"\n{move_name:2s} - {faces[move_name]}顺时针90度")
        print(f"     角块: {format_cycles(corner_cycles)}")
        print(f"     棱块: {format_cycles(edge_cycles)}")
    
    # 逆操作
    print("\n【逆操作】")
    for move_name in ["F'", "R'", "U'", "L'", "B'", "D'"]:
        print(f"{move_name:3s} - {move_name[0]} 的逆操作（逆时针90度）")
    
    # 双层
    print("\n【双层旋转】")
    for move_name in ["F2", "R2", "U2", "L2", "B2", "D2"]:
        print(f"{move_name:3s} - {move_name[0]} 的180度旋转")


def cmd_examples():
    """显示示例命令"""
    print("\n示例命令：")
    print("="*60)
    
    examples = [
        ("analyze F R U R' U' F'", "分析一个简单公式"),
        ("commutator R U", "计算交换子 [R, U]"),
        ("order R U R' U'", "计算 Sexy Move 的阶"),
        ("inverse R U R' U R U2 R'", "计算 Sune 的逆"),
        ("compare [R, U] [U, R]", "比较两个交换子"),
        ("analyze [F, [R, U]]", "分析嵌套交换子"),
        ("analyze R U2 R' U' R U' R'", "分析 Antisune"),
    ]
    
    for i, (cmd, desc) in enumerate(examples, 1):
        print(f"\n{i}. {desc}")
        print(f"   > {cmd}")


def cmd_help():
    """显示帮助信息"""
    print("\n帮助信息：")
    print("="*60)
    
    print("\n📖 魔方记法：")
    print("  F, R, U       - 前、右、上面顺时针90度")
    print("  F', R', U'    - 逆时针90度")
    print("  F2, R2, U2    - 180度旋转")
    
    print("\n📖 交换子：")
    print("  [A, B]        - 交换子，等价于 A B A' B'")
    print("  [F, [R, U]]   - 支持嵌套")
    
    print("\n📖 置换循环：")
    print("  (0 1 2)       - 表示 0→1, 1→2, 2→0 的循环")
    print("  (0 1) (2 3)   - 两个独立的循环")
    
    print("\n📖 角块编号（0-7）：")
    print("  0:UFR  1:UFL  2:UBL  3:UBR")
    print("  4:DFR  5:DFL  6:DBL  7:DBR")
    
    print("\n📖 棱块编号（0-11）：")
    print("  0:UF   1:UL   2:UB   3:UR")
    print("  4:FR   5:FL   6:BL   7:BR")
    print("  8:DF   9:DL  10:DB  11:DR")
    
    print("\n📖 相关概念：")
    print("  阶(Order)     - 重复多少次回到初始状态")
    print("  逆(Inverse)   - 撤销该操作的公式")
    print("  三循环        - 恰好交换三个块的置换")


def interactive_mode():
    """交互式模式"""
    print_menu()
    
    while True:
        try:
            # 读取用户输入
            user_input = input("\n🎲 > ").strip()
            
            if not user_input:
                continue
            
            # 解析命令
            parts = user_input.split(None, 1)
            cmd = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""
            
            # 执行命令
            if cmd in ["quit", "exit", "q"]:
                print("\n👋 再见！")
                break
            
            elif cmd == "analyze":
                if not args:
                    print("❌ 请提供公式，例如: analyze F R U")
                else:
                    cmd_analyze(args)
            
            elif cmd == "commutator":
                parts = args.split(None, 1)
                if len(parts) < 2:
                    print("❌ 请提供两个公式，例如: commutator R U")
                else:
                    cmd_commutator(parts[0], parts[1])
            
            elif cmd == "order":
                if not args:
                    print("❌ 请提供公式，例如: order R U R' U'")
                else:
                    cmd_order(args)
            
            elif cmd == "inverse":
                if not args:
                    print("❌ 请提供公式，例如: inverse R U R' U'")
                else:
                    cmd_inverse(args)
            
            elif cmd == "compare":
                # 分割两个公式（使用更智能的方法）
                # 尝试用 " | " 分隔
                if " | " in args:
                    alg1, alg2 = args.split(" | ", 1)
                else:
                    # 否则假设中间有空格分隔
                    parts = args.split()
                    if len(parts) < 2:
                        print("❌ 请提供两个公式，例如: compare [R,U] | [U,R]")
                        continue
                    # 简单启发式：找到可能的分隔点
                    mid = len(parts) // 2
                    alg1 = " ".join(parts[:mid])
                    alg2 = " ".join(parts[mid:])
                
                cmd_compare(alg1.strip(), alg2.strip())
            
            elif cmd == "moves":
                cmd_moves()
            
            elif cmd == "examples":
                cmd_examples()
            
            elif cmd == "help":
                cmd_help()
            
            elif cmd == "menu":
                print_menu()
            
            else:
                print(f"❌ 未知命令: {cmd}")
                print("   输入 'help' 查看帮助，或 'menu' 查看菜单")
        
        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break
        
        except Exception as e:
            print(f"\n❌ 错误: {e}")
            print("   请检查输入格式，或输入 'help' 查看帮助")


def batch_mode(alg):
    """批处理模式：直接分析一个公式"""
    cmd_analyze(alg)


def main():
    """主函数"""
    if len(sys.argv) > 1:
        # 批处理模式
        alg = " ".join(sys.argv[1:])
        batch_mode(alg)
    else:
        # 交互式模式
        interactive_mode()


if __name__ == "__main__":
    main()

