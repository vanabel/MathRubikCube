#!/usr/bin/env python3
"""
朝向可视化演示
Orientation Visualization Demo
"""

from cube import *
from visualize import *


def demo_orientation_basics():
    """演示朝向的基本概念"""
    print("\n" + "="*70)
    print("📐 朝向基本概念")
    print("="*70)
    
    print("\n角块朝向（3种）：")
    print("  0 = 正常方向")
    print("  1 = 顺时针旋转120° (标记为 ↻)")
    print("  2 = 逆时针旋转120° (标记为 ↺)")
    
    print("\n棱块朝向（2种）：")
    print("  0 = 正常方向")
    print("  1 = 翻转180° (标记为 ⟲)")
    
    print("\n颜色编码：")
    print("  🟢 绿色/蓝色 - 位置和朝向都正常")
    print("  🟡 黄色/青色 - 只有朝向变了")
    print("  🔴 浅红/橙色 - 只有位置变了")
    print("  🔴 深红色 - 位置和朝向都变了")


def demo_oll_vs_pll():
    """演示OLL vs PLL的区别"""
    print("\n" + "="*70)
    print("🎯 OLL vs PLL：朝向 vs 位置")
    print("="*70)
    
    print("\n【OLL公式示例：F R U R' U' F'】")
    print("-"*70)
    analyze_algorithm("F R U R' U' F'")
    
    print("\n观察要点：")
    print("  ✓ 角块朝向改变了4个 - 这是OLL的主要作用！")
    print("  ✓ 棱块朝向没有改变")
    print("  • 位置也有变化（副作用）")
    
    print("\n在GUI中查看：")
    print("  • 黄色块 = 只有朝向变了")
    print("  • 深红块 = 位置和朝向都变了")
    print("  • 块上的↻或↺符号显示旋转方向")


def demo_position_only():
    """演示只改变位置的公式"""
    print("\n" + "="*70)
    print("🔄 只改变位置的公式")
    print("="*70)
    
    print("\n【U操作：只改变位置，不改变朝向】")
    print("-"*70)
    analyze_algorithm("U")
    
    print("\n观察要点：")
    print("  ✓ 角块朝向全部为0 - 没有朝向变化")
    print("  ✓ 棱块朝向全部为0 - 没有朝向变化")
    print("  ✓ 只有位置改变")
    
    print("\n结论：U和D操作不改变任何块的朝向！")


def demo_orientation_only():
    """寻找只改变朝向的公式"""
    print("\n" + "="*70)
    print("🔬 寻找只改变朝向的公式")
    print("="*70)
    
    print("\n理论上可能存在位置不变但朝向改变的公式...")
    print("（这种公式比较罕见）")
    
    # 测试一些可能的候选
    candidates = [
        "[F2, R2]",
        "[F F, R R]",
        "[[F, F], [R, R]]",
    ]
    
    found = False
    for alg in candidates:
        state = apply_algorithm(CubeState(), alg)
        
        pos_unchanged = (state.corners == list(range(8)) and 
                        state.edges == list(range(12)))
        ori_changed = (state.corner_ori != [0] * 8 or 
                      state.edge_ori != [0] * 12)
        
        if pos_unchanged and ori_changed:
            print(f"\n✓ 找到了！{alg}")
            print(f"  位置：未变")
            print(f"  朝向：已变")
            print(f"  角块朝向: {state.corner_ori}")
            print(f"  棱块朝向: {state.edge_ori}")
            found = True
    
    if not found:
        print("\n未找到纯朝向变化的公式（在测试的候选中）")


def demo_visual_comparison():
    """可视化对比"""
    print("\n" + "="*70)
    print("🎨 可视化对比")
    print("="*70)
    
    print("\n对比以下三个公式的可视化效果：")
    print("\n1. F（改变位置+朝向）")
    print("2. U（只改变位置）")
    print("3. F R U R' U' F'（OLL，改变位置+朝向）")
    
    print("\n在GUI中依次输入这些公式，观察：")
    print("  • 黄色块出现 = 有角块朝向改变")
    print("  • 青色块出现 = 有棱块朝向改变")
    print("  • ↻↺⟲符号 = 朝向变化的方向")
    
    print("\n运行GUI查看：")
    print("  python visualize.py -i")


def demo_orientation_conservation():
    """演示朝向守恒定律"""
    print("\n" + "="*70)
    print("⚖️  朝向守恒定律")
    print("="*70)
    
    print("\n魔方的朝向必须满足守恒定律：")
    print("  • 角块朝向总和 ≡ 0 (mod 3)")
    print("  • 棱块朝向总和 ≡ 0 (mod 2)")
    
    print("\n测试几个公式：")
    
    test_algs = ["F", "F R U", "[F, R]", "F R U R' U' F'"]
    
    for alg in test_algs:
        state = apply_algorithm(CubeState(), alg)
        corner_sum = sum(state.corner_ori)
        edge_sum = sum(state.edge_ori)
        
        is_valid, msg = check_orientation_valid(state)
        
        print(f"\n  {alg:20s}")
        print(f"    角块朝向和: {corner_sum:2d} ≡ {corner_sum % 3} (mod 3)")
        print(f"    棱块朝向和: {edge_sum:2d} ≡ {edge_sum % 2} (mod 2)")
        print(f"    验证: {msg}")
    
    print("\n结论：所有合法的魔方操作都自动满足守恒定律！")


def main():
    """主演示函数"""
    print("\n" + "="*70)
    print("🎲 朝向功能完整演示")
    print("="*70)
    
    demos = [
        ("朝向基本概念", demo_orientation_basics),
        ("OLL vs PLL", demo_oll_vs_pll),
        ("只改变位置", demo_position_only),
        ("寻找只改变朝向", demo_orientation_only),
        ("可视化对比", demo_visual_comparison),
        ("朝向守恒定律", demo_orientation_conservation),
    ]
    
    for name, func in demos:
        func()
    
    print("\n" + "="*70)
    print("✅ 朝向演示完成！")
    print("="*70)
    
    print("\n下一步：")
    print("  1. 运行交互式GUI查看朝向可视化：")
    print("     python visualize.py -i")
    print("\n  2. 在GUI中尝试：")
    print("     • 输入：F")
    print("     • 查看黄色块（朝向改变）和↻符号")
    print("     • 输入：F R U R' U' F'")
    print("     • 观察OLL如何改变朝向")
    print("\n  3. 鼠标移到块上查看详细朝向值")
    print("="*70)


if __name__ == "__main__":
    main()

