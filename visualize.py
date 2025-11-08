"""
魔方可视化模块
Rubik's Cube Visualization Module

提供文本和图形两种可视化方式
"""

from cube import *
import sys


# ==================== 文本可视化 ====================

def visualize_cube_text(state: CubeState, show_legend: bool = True):
    """
    文本方式可视化魔方状态
    
    显示魔方的展开图，标注每个位置的块编号
    
    Args:
        state: 魔方状态
        show_legend: 是否显示图例
    """
    
    # 定义魔方展开图布局（使用块编号）
    # 这是一个简化的表示，显示哪个块在哪个位置
    
    print("\n" + "="*60)
    print("🎲 魔方状态可视化（文本版）")
    print("="*60)
    
    # 显示角块状态
    print("\n【角块状态】")
    print("    UBL UBR")
    print("     2---3  ")
    print("    /|  /|  ")
    print("   1---0 |  ← UFR位置: 角块", state.corners[0])
    print("   | 6-|-7  ")
    print("   |/  |/   ")
    print("   5---4    ")
    print("    DFL DFR")
    
    print("\n当前角块置换:")
    for i in range(8):
        pos_name = ["UFR", "UFL", "UBL", "UBR", "DFR", "DFL", "DBL", "DBR"][i]
        block_name = ["UFR", "UFL", "UBL", "UBR", "DFR", "DFL", "DBL", "DBR"][state.corners[i]]
        ori = state.corner_ori[i]
        ori_str = f" 朝向:{ori}" if ori != 0 else ""
        
        if state.corners[i] != i or ori != 0:
            print(f"  位置 {i:1d}({pos_name}): 角块{state.corners[i]}({block_name}){ori_str} ← 变化了")
        else:
            print(f"  位置 {i:1d}({pos_name}): 角块{state.corners[i]}({block_name}){ori_str}")
    
    # 显示棱块状态
    print("\n【棱块状态】")
    print("       UB")
    print("     2")
    print("  1     3")
    print("UL  0  UR  ← UF位置: 棱块", state.edges[0])
    print("   UF")
    print("\n  5  4   7  6")
    print(" FL FR  BR BL")
    print("\n       DF")
    print("     8")
    print("  9    11")
    print("DL      DR")
    print("    10")
    print("       DB")
    
    print("\n当前棱块置换:")
    edge_names = ["UF", "UL", "UB", "UR", "FR", "FL", "BL", "BR", 
                  "DF", "DL", "DB", "DR"]
    for i in range(12):
        pos_name = edge_names[i]
        block_name = edge_names[state.edges[i]]
        ori = state.edge_ori[i]
        ori_str = f" 朝向:{ori}" if ori != 0 else ""
        
        if state.edges[i] != i or ori != 0:
            print(f"  位置{i:2d}({pos_name}): 棱块{state.edges[i]:2d}({block_name}){ori_str} ← 变化了")
        else:
            print(f"  位置{i:2d}({pos_name}): 棱块{state.edges[i]:2d}({block_name}){ori_str}")
    
    # 统计
    corner_moved = sum(1 for i in range(8) if state.corners[i] != i)
    edge_moved = sum(1 for i in range(12) if state.edges[i] != i)
    corner_ori_changed = sum(1 for x in state.corner_ori if x != 0)
    edge_ori_changed = sum(1 for x in state.edge_ori if x != 0)
    
    print("\n【统计】")
    print(f"  移动的角块: {corner_moved}/8")
    print(f"  移动的棱块: {edge_moved}/12")
    print(f"  朝向改变的角块: {corner_ori_changed}/8")
    print(f"  朝向改变的棱块: {edge_ori_changed}/12")
    
    # 验证朝向合法性
    is_valid, msg = check_orientation_valid(state)
    print(f"  朝向验证: {msg}")
    
    if state.is_solved():
        print(f"\n  ✅ 魔方完全还原（位置+朝向）！")
    
    print("="*60 + "\n")


def visualize_cube_flat(state: CubeState):
    """
    扁平展开图方式显示魔方
    
    显示魔方的六个面（展开图）
    """
    print("\n" + "="*60)
    print("🎲 魔方展开图（文本版）")
    print("="*60)
    print("""
        +-------+
        |2  2  3|  U (上)
        |  UBL  |
        |1  0  3|
        +-------+
+-------+-------+-------+-------+
|1  1  0|0  0  3|3  3  7|2  2  1|
|  UFL  |  UFR  |  UBR  |  UBL  |  中层
|5  5  4|4  4  7|7  7  6|6  6  2|
+-------+-------+-------+-------+
        |5  8  4|  D (下)
        |  DFL  |
        |6  10 7|
        +-------+

角块编号: 0-7
棱块编号: 0-11
    """)
    
    print("当前状态:")
    print(f"  角块: {state.corners}")
    print(f"  棱块: {state.edges}")
    print("="*60 + "\n")


def animate_algorithm_text(alg_str: str, delay: float = 0.5):
    """
    动画方式展示公式执行过程（文本版）
    
    Args:
        alg_str: 公式字符串
        delay: 每步之间的延迟（秒）
    """
    import time
    
    print("\n" + "="*60)
    print(f"🎬 算法动画演示: {alg_str}")
    print("="*60)
    
    moves = parse_algorithm(alg_str)
    state = CubeState()
    
    print("\n初始状态:")
    print(f"  角块: {state.corners}")
    print(f"  棱块: {state.edges}")
    
    for i, move_name in enumerate(moves, 1):
        if move_name in MOVES:
            state = apply_move(state, MOVES[move_name])
            
            print(f"\n第 {i} 步: {move_name}")
            print(f"  角块: {state.corners}")
            print(f"  棱块: {state.edges}")
            
            # 显示循环
            corner_cycles = permutation_cycles(state.corners)
            if corner_cycles:
                print(f"  角块循环: {format_cycles(corner_cycles)}")
            
            time.sleep(delay)
    
    print("\n最终状态:")
    if state.is_solved():
        print("  ✅ 回到初始状态！")
    else:
        print("  ⚠️  未还原")
    
    print("="*60 + "\n")


# ==================== 图形可视化 ====================

def visualize_cube_matplotlib(state: CubeState, title: str = "魔方状态"):
    """
    使用 matplotlib 绘制魔方展开图
    
    Args:
        state: 魔方状态
        title: 图表标题
    """
    try:
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches
        from matplotlib.patches import FancyBboxPatch
        import matplotlib
        
        # 配置中文字体支持
        matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'STSong', 'DejaVu Sans']
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    except ImportError:
        print("❌ 需要安装 matplotlib: pip install matplotlib")
        return
    
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlim(-0.5, 12.5)
    ax.set_ylim(-0.5, 9.5)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # 定义块大小和颜色
    block_size = 1.0
    
    # 定义魔方展开图布局
    # 格式: (x, y, 标签)
    
    # 魔方展开图标准布局 - 完全紧密贴合，无间隙
    #        [U]
    # [L] [F] [R] [B]
    #        [D]
    
    # 每个面3x3格子，block_size=1.0
    # D面: y=0-2, F面: y=3-5, U面: y=6-8 (完全连续，无间隙)
    # L面: x=0-2, F面: x=3-5, R面: x=6-8, B面: x=9-11 (完全连续，无间隙)
    
    # 上面 (U) - 位于 F 面正上方（y=6开始）
    u_positions = [
        (3, 8, "2", "UBL"),
        (4, 8, "2", "UB"),
        (5, 8, "3", "UBR"),
        (3, 7, "1", "UL"),
        (4, 7, "", "U中心"),
        (5, 7, "3", "UR"),
        (3, 6, "1", "UFL"),
        (4, 6, "0", "UF"),
        (5, 6, "0", "UFR"),
    ]
    
    # 左面 (L) - 中间行最左
    l_positions = [
        (0, 5, "2", "UBL"),
        (1, 5, "1", "UL"),
        (2, 5, "1", "UFL"),
        (0, 4, "6", "BL"),
        (1, 4, "", "L中心"),
        (2, 4, "5", "FL"),
        (0, 3, "6", "DBL"),
        (1, 3, "9", "DL"),
        (2, 3, "5", "DFL"),
    ]
    
    # 前面 (F) - 中间行第二个
    f_positions = [
        (3, 5, "1", "UFL"),
        (4, 5, "0", "UF"),
        (5, 5, "0", "UFR"),
        (3, 4, "5", "FL"),
        (4, 4, "", "F中心"),
        (5, 4, "4", "FR"),
        (3, 3, "5", "DFL"),
        (4, 3, "8", "DF"),
        (5, 3, "4", "DFR"),
    ]
    
    # 右面 (R) - 中间行第三个
    r_positions = [
        (6, 5, "0", "UFR"),
        (7, 5, "3", "UR"),
        (8, 5, "3", "UBR"),
        (6, 4, "4", "FR"),
        (7, 4, "", "R中心"),
        (8, 4, "7", "BR"),
        (6, 3, "4", "DFR"),
        (7, 3, "11", "DR"),
        (8, 3, "7", "DBR"),
    ]
    
    # 后面 (B) - 中间行最右
    b_positions = [
        (9, 5, "3", "UBR"),
        (10, 5, "2", "UB"),
        (11, 5, "2", "UBL"),
        (9, 4, "7", "BR"),
        (10, 4, "", "B中心"),
        (11, 4, "6", "BL"),
        (9, 3, "7", "DBR"),
        (10, 3, "10", "DB"),
        (11, 3, "6", "DBL"),
    ]
    
    # 下面 (D) - 位于 F 面下方
    d_positions = [
        (3, 2, "5", "DFL"),
        (4, 2, "8", "DF"),
        (5, 2, "4", "DFR"),
        (3, 1, "9", "DL"),
        (4, 1, "", "D中心"),
        (5, 1, "11", "DR"),
        (3, 0, "6", "DBL"),
        (4, 0, "10", "DB"),
        (5, 0, "7", "DBR"),
    ]
    
    all_positions = [
        ("U", u_positions, "yellow"),
        ("L", l_positions, "red"),
        ("F", f_positions, "green"),
        ("R", r_positions, "orange"),
        ("B", b_positions, "blue"),
        ("D", d_positions, "white"),
    ]
    
    # 角块和棱块名称映射
    corner_names = ["UFR", "UFL", "UBL", "UBR", "DFR", "DFL", "DBL", "DBR"]
    edge_names = ["UF", "UL", "UB", "UR", "FR", "FL", "BL", "BR", 
                  "DF", "DL", "DB", "DR"]
    
    # 绘制每个面
    for face_name, positions, base_color in all_positions:
        for x, y, label, pos_name in positions:
            # 确定这个位置的实际块
            if label.isdigit():
                # 首先检查是否是角块位置
                if pos_name in corner_names:
                    pos_idx = corner_names.index(pos_name)
                    actual_block = state.corners[pos_idx]
                    is_moved = actual_block != pos_idx
                    # 显示位置编号，如果移动了则附加箭头和实际块
                    if is_moved:
                        block_label = f"{pos_idx}→{actual_block}"
                    else:
                        block_label = str(pos_idx)
                    color = "lightcoral" if is_moved else "lightgreen"
                # 然后检查是否是棱块位置
                elif pos_name in edge_names:
                    pos_idx = edge_names.index(pos_name)
                    actual_block = state.edges[pos_idx]
                    is_moved = actual_block != pos_idx
                    # 显示位置编号，如果移动了则附加箭头和实际块
                    if is_moved:
                        block_label = f"{pos_idx}→{actual_block}"
                    else:
                        block_label = str(pos_idx)
                    color = "lightsalmon" if is_moved else "lightblue"
                else:
                    # 未知位置，显示原始标签
                    color = "lightgray"
                    block_label = label
            else:
                color = base_color
                block_label = face_name
            
            # 绘制方块（使用普通矩形，确保完全贴合）
            rect = patches.Rectangle(
                (x, y), block_size, block_size,
                facecolor=color,
                edgecolor="black",
                linewidth=1.5
            )
            ax.add_patch(rect)
            
            # 添加文本
            if block_label:
                # 根据标签长度调整字体大小
                if '→' in str(block_label):
                    fontsize = 8  # 移动的块，标签较长
                elif len(str(block_label)) > 1:
                    fontsize = 9  # 两位数或特殊标签
                else:
                    fontsize = 10  # 单个字符
                
                ax.text(
                    x + block_size/2, y + block_size/2,
                    block_label,
                    ha='center', va='center',
                    fontsize=fontsize,
                    fontweight='bold'
                )
    
    # 添加标题和图例
    ax.text(6, 9.2, title, ha='center', fontsize=14, fontweight='bold')
    
    # 图例（左上角）
    legend_x = -0.3
    legend_y = 8.8
    ax.text(legend_x, legend_y, "图例:", fontsize=9, fontweight='bold')
    
    legend_items = [
        ("lightgreen", "角块未动"),
        ("lightcoral", "角块已动"),
        ("lightblue", "棱块未动"),
        ("lightsalmon", "棱块已动"),
    ]
    
    for i, (color, label) in enumerate(legend_items):
        y = legend_y - 0.35 - i * 0.35
        rect = patches.Rectangle((legend_x, y), 0.25, 0.25, facecolor=color, edgecolor='black', linewidth=1)
        ax.add_patch(rect)
        ax.text(legend_x + 0.35, y + 0.12, label, fontsize=7, va='center')
    
    # 添加说明
    ax.text(legend_x, legend_y - 1.7, "注: U/L/F/R/B/D", fontsize=6, style='italic')
    ax.text(legend_x, legend_y - 2.0, "为面中心（固定）", fontsize=6, style='italic')
    
    # 统计信息（右上角）
    corner_moved = sum(1 for i in range(8) if state.corners[i] != i)
    edge_moved = sum(1 for i in range(12) if state.edges[i] != i)
    
    stats_text = f"移动的角块: {corner_moved}/8\n移动的棱块: {edge_moved}/12"
    ax.text(12.2, 8.8, stats_text, fontsize=9, va='top', ha='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # 添加鼠标悬停交互功能
    # 存储每个块的信息
    block_info = {}
    for face_name, positions, base_color in all_positions:
        for x, y, label, pos_name in positions:
            if label.isdigit():
                if pos_name in corner_names:
                    pos_idx = corner_names.index(pos_name)
                    actual_block = state.corners[pos_idx]
                    actual_name = corner_names[actual_block]
                    info = f"位置: {pos_name} (角块{pos_idx})\n当前块: {actual_name} (角块{actual_block})"
                    if actual_block != pos_idx:
                        info += f"\n状态: 已移动"
                    else:
                        info += f"\n状态: 未移动"
                elif pos_name in edge_names:
                    pos_idx = edge_names.index(pos_name)
                    actual_block = state.edges[pos_idx]
                    actual_name = edge_names[actual_block]
                    info = f"位置: {pos_name} (棱块{pos_idx})\n当前块: {actual_name} (棱块{actual_block})"
                    if actual_block != pos_idx:
                        info += f"\n状态: 已移动"
                    else:
                        info += f"\n状态: 未移动"
                else:
                    info = f"{pos_name}"
            else:
                info = f"面中心: {face_name}"
            
            block_info[(x, y)] = info
    
    # 创建悬停标注
    annot = ax.annotate("", xy=(0,0), xytext=(15,15), textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="lightyellow", ec="black", alpha=0.95),
                        fontsize=9, visible=False, zorder=1000)
    
    def on_hover(event):
        """鼠标悬停事件处理"""
        if event.inaxes == ax:
            # 查找鼠标位置对应的块
            for (bx, by), info in block_info.items():
                if bx <= event.xdata < bx + block_size and by <= event.ydata < by + block_size:
                    annot.xy = (event.xdata, event.ydata)
                    annot.set_text(info)
                    annot.set_visible(True)
                    fig.canvas.draw_idle()
                    return
            
            # 如果不在任何块上，隐藏标注
            if annot.get_visible():
                annot.set_visible(False)
                fig.canvas.draw_idle()
    
    # 连接事件
    fig.canvas.mpl_connect('motion_notify_event', on_hover)
    
    plt.tight_layout()
    plt.show()


def interactive_cube_gui():
    """
    交互式魔方GUI - 可以输入公式并实时查看效果
    """
    try:
        import matplotlib.pyplot as plt
        from matplotlib.widgets import TextBox, Button
        import matplotlib.patches as patches
        import matplotlib
        
        # 配置中文字体支持
        matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'STSong', 'DejaVu Sans']
        matplotlib.rcParams['axes.unicode_minus'] = False
    except ImportError:
        print("❌ 需要安装 matplotlib: pip install matplotlib")
        return
    
    # 初始状态
    current_state = CubeState()
    current_formula = ""
    formula_history = []
    
    # 创建图形
    fig = plt.figure(figsize=(12, 9))
    
    # 主绘图区域
    ax_main = plt.axes([0.1, 0.25, 0.8, 0.65])
    
    # 文本输入框
    ax_textbox = plt.axes([0.15, 0.12, 0.5, 0.05])
    textbox = TextBox(ax_textbox, '公式:', initial="")
    
    # 按钮区域
    ax_apply = plt.axes([0.68, 0.12, 0.08, 0.05])
    ax_reset = plt.axes([0.78, 0.12, 0.08, 0.05])
    ax_undo = plt.axes([0.88, 0.12, 0.08, 0.05])
    
    btn_apply = Button(ax_apply, '应用')
    btn_reset = Button(ax_reset, '重置')
    btn_undo = Button(ax_undo, '撤销')
    
    # 历史显示区域
    ax_history = plt.axes([0.1, 0.02, 0.8, 0.08])
    ax_history.axis('off')
    
    def draw_cube(state, title_text="", annot_obj=None):
        """绘制魔方状态"""
        ax_main.clear()
        ax_main.set_xlim(-0.5, 12.5)
        ax_main.set_ylim(-0.5, 9.5)
        ax_main.set_aspect('equal')
        ax_main.axis('off')
        
        # 重新创建annot（因为clear会删除它）
        if annot_obj is not None:
            # 将annot重新添加到axes
            ax_main.add_artist(annot_obj)
        
        block_size = 1.0
        
        # 使用之前定义的布局
        u_positions = [(3, 8, "2", "UBL"), (4, 8, "2", "UB"), (5, 8, "3", "UBR"),
                       (3, 7, "1", "UL"), (4, 7, "", "U中心"), (5, 7, "3", "UR"),
                       (3, 6, "1", "UFL"), (4, 6, "0", "UF"), (5, 6, "0", "UFR")]
        
        l_positions = [(0, 5, "2", "UBL"), (1, 5, "1", "UL"), (2, 5, "1", "UFL"),
                       (0, 4, "6", "BL"), (1, 4, "", "L中心"), (2, 4, "5", "FL"),
                       (0, 3, "6", "DBL"), (1, 3, "9", "DL"), (2, 3, "5", "DFL")]
        
        f_positions = [(3, 5, "1", "UFL"), (4, 5, "0", "UF"), (5, 5, "0", "UFR"),
                       (3, 4, "5", "FL"), (4, 4, "", "F中心"), (5, 4, "4", "FR"),
                       (3, 3, "5", "DFL"), (4, 3, "8", "DF"), (5, 3, "4", "DFR")]
        
        r_positions = [(6, 5, "0", "UFR"), (7, 5, "3", "UR"), (8, 5, "3", "UBR"),
                       (6, 4, "4", "FR"), (7, 4, "", "R中心"), (8, 4, "7", "BR"),
                       (6, 3, "4", "DFR"), (7, 3, "11", "DR"), (8, 3, "7", "DBR")]
        
        b_positions = [(9, 5, "3", "UBR"), (10, 5, "2", "UB"), (11, 5, "2", "UBL"),
                       (9, 4, "7", "BR"), (10, 4, "", "B中心"), (11, 4, "6", "BL"),
                       (9, 3, "7", "DBR"), (10, 3, "10", "DB"), (11, 3, "6", "DBL")]
        
        d_positions = [(3, 2, "5", "DFL"), (4, 2, "8", "DF"), (5, 2, "4", "DFR"),
                       (3, 1, "9", "DL"), (4, 1, "", "D中心"), (5, 1, "11", "DR"),
                       (3, 0, "6", "DBL"), (4, 0, "10", "DB"), (5, 0, "7", "DBR")]
        
        all_positions = [
            ("U", u_positions, "yellow"),
            ("L", l_positions, "red"),
            ("F", f_positions, "green"),
            ("R", r_positions, "orange"),
            ("B", b_positions, "blue"),
            ("D", d_positions, "white"),
        ]
        
        corner_names = ["UFR", "UFL", "UBL", "UBR", "DFR", "DFL", "DBL", "DBR"]
        edge_names = ["UF", "UL", "UB", "UR", "FR", "FL", "BL", "BR", "DF", "DL", "DB", "DR"]
        
        # 绘制每个块
        for face_name, positions, base_color in all_positions:
            for x, y, label, pos_name in positions:
                if label.isdigit():
                    if pos_name in corner_names:
                        pos_idx = corner_names.index(pos_name)
                        actual_block = state.corners[pos_idx]
                        is_moved = actual_block != pos_idx
                        if is_moved:
                            block_label = f"{pos_idx}→{actual_block}"
                        else:
                            block_label = str(pos_idx)
                        color = "lightcoral" if is_moved else "lightgreen"
                    elif pos_name in edge_names:
                        pos_idx = edge_names.index(pos_name)
                        actual_block = state.edges[pos_idx]
                        is_moved = actual_block != pos_idx
                        if is_moved:
                            block_label = f"{pos_idx}→{actual_block}"
                        else:
                            block_label = str(pos_idx)
                        color = "lightsalmon" if is_moved else "lightblue"
                    else:
                        color = "lightgray"
                        block_label = label
                else:
                    color = base_color
                    block_label = face_name
                
                rect = patches.Rectangle((x, y), block_size, block_size,
                                        facecolor=color, edgecolor="black", linewidth=1.5)
                ax_main.add_patch(rect)
                
                if block_label:
                    if '→' in str(block_label):
                        fontsize = 7
                    elif len(str(block_label)) > 1:
                        fontsize = 8
                    else:
                        fontsize = 9
                    
                    ax_main.text(x + block_size/2, y + block_size/2, block_label,
                               ha='center', va='center', fontsize=fontsize, fontweight='bold')
        
        # 标题（自适应大小）
        if title_text and len(title_text) > 50:
            fontsize = 11
        elif title_text and len(title_text) > 30:
            fontsize = 12
        else:
            fontsize = 13
        ax_main.text(6, 9.2, title_text or "交互式魔方", ha='center', fontsize=fontsize, fontweight='bold')
        
        # 图例（左上角）
        legend_x = -0.3
        legend_y = 8.8
        ax_main.text(legend_x, legend_y, "图例:", fontsize=9, fontweight='bold')
        
        legend_items = [
            ("lightgreen", "角块未动"),
            ("lightcoral", "角块已动"),
            ("lightblue", "棱块未动"),
            ("lightsalmon", "棱块已动"),
        ]
        
        for i, (color, label) in enumerate(legend_items):
            y = legend_y - 0.35 - i * 0.35
            rect = patches.Rectangle((legend_x, y), 0.25, 0.25, facecolor=color, edgecolor='black', linewidth=1)
            ax_main.add_patch(rect)
            ax_main.text(legend_x + 0.35, y + 0.12, label, fontsize=7, va='center')
        
        # 添加说明
        ax_main.text(legend_x, legend_y - 1.7, "注: U/L/F/R/B/D", fontsize=6, style='italic')
        ax_main.text(legend_x, legend_y - 2.0, "为面中心（固定）", fontsize=6, style='italic')
        
        # 统计信息（右上角）
        corner_moved = sum(1 for i in range(8) if state.corners[i] != i)
        edge_moved = sum(1 for i in range(12) if state.edges[i] != i)
        corner_ori_changed = sum(1 for x in state.corner_ori if x != 0)
        edge_ori_changed = sum(1 for x in state.edge_ori if x != 0)
        
        stats_text = f"位置: 角{corner_moved}/8 棱{edge_moved}/12\n朝向: 角{corner_ori_changed}/8 棱{edge_ori_changed}/12"
        ax_main.text(12.2, 8.8, stats_text, fontsize=9, va='top', ha='right',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        # 鼠标悬停功能 - 存储块信息
        block_info = {}
        for face_name, positions, base_color in all_positions:
            for x, y, label, pos_name in positions:
                if label.isdigit():
                    if pos_name in corner_names:
                        pos_idx = corner_names.index(pos_name)
                        actual_block = state.corners[pos_idx]
                        actual_name = corner_names[actual_block]
                        ori = state.corner_ori[pos_idx]
                        info = f"位置: {pos_name} (角块{pos_idx})\n当前块: {actual_name} (角块{actual_block})\n朝向: {ori}"
                        if actual_block != pos_idx:
                            info += f"\n状态: 已移动"
                        elif ori != 0:
                            info += f"\n状态: 朝向改变"
                        else:
                            info += f"\n状态: 未变化"
                    elif pos_name in edge_names:
                        pos_idx = edge_names.index(pos_name)
                        actual_block = state.edges[pos_idx]
                        actual_name = edge_names[actual_block]
                        ori = state.edge_ori[pos_idx]
                        info = f"位置: {pos_name} (棱块{pos_idx})\n当前块: {actual_name} (棱块{actual_block})\n朝向: {ori}"
                        if actual_block != pos_idx:
                            info += f"\n状态: 已移动"
                        elif ori != 0:
                            info += f"\n状态: 朝向改变"
                        else:
                            info += f"\n状态: 未变化"
                    else:
                        info = f"{pos_name}"
                else:
                    info = f"面中心: {face_name}"
                
                block_info[(x, y)] = info
        
        fig.canvas.draw_idle()
        
        # 返回块信息用于悬停
        return block_info
    
    def update_history():
        """更新历史显示"""
        ax_history.clear()
        ax_history.axis('off')
        if formula_history:
            history_text = "历史: " + " → ".join(formula_history[-5:])  # 显示最近5个
            ax_history.text(0.5, 0.5, history_text, ha='center', va='center',
                          fontsize=9, transform=ax_history.transAxes)
        fig.canvas.draw_idle()
    
    def apply_formula(formula):
        """应用公式"""
        nonlocal current_state, current_formula
        try:
            if formula.strip():
                current_state = apply_algorithm(current_state, formula)
                current_formula = formula
                formula_history.append(formula)
                
                # 分析公式
                corner_cycles = permutation_cycles(current_state.corners)
                edge_cycles = permutation_cycles(current_state.edges)
                
                corner_str = format_cycles(corner_cycles) if corner_cycles else 'identity'
                edge_str = format_cycles(edge_cycles) if edge_cycles else 'identity'
                title = f"应用: {formula}\n角块: {corner_str}  棱块: {edge_str}"
                block_info = draw_cube(current_state, title, annot)
                current_block_info['data'] = block_info  # 更新字典内容
                update_history()
                
                print(f"\n✓ 已应用公式: {formula}")
                print(f"  角块循环: {format_cycles(corner_cycles) if corner_cycles else 'identity'}")
                print(f"  棱块循环: {format_cycles(edge_cycles) if edge_cycles else 'identity'}")
        except Exception as e:
            print(f"❌ 错误: {e}")
    
    def on_submit(text):
        """文本框提交"""
        apply_formula(text)
        textbox.set_val("")  # 清空输入框
    
    def on_apply(event):
        """应用按钮"""
        text = textbox.text
        apply_formula(text)
        textbox.set_val("")
    
    def on_reset(event):
        """重置按钮"""
        nonlocal current_state, current_formula, formula_history
        current_state = CubeState()
        current_formula = ""
        formula_history = []
        block_info = draw_cube(current_state, "交互式魔方 - 已重置", annot)
        current_block_info['data'] = block_info
        update_history()
        print("\n✓ 已重置为初始状态")
    
    def on_undo(event):
        """撤销按钮"""
        nonlocal current_state, formula_history
        if formula_history:
            formula_history.pop()
            # 从头重新应用所有历史公式
            current_state = CubeState()
            for f in formula_history:
                current_state = apply_algorithm(current_state, f)
            
            if formula_history:
                title = f"撤销后: {formula_history[-1]}"
            else:
                title = "交互式魔方 - 已撤销"
            block_info = draw_cube(current_state, title, annot)
            current_block_info['data'] = block_info
            update_history()
            print("\n✓ 已撤销上一步")
        else:
            print("\n⚠️  没有可撤销的操作")
    
    # 存储当前的block_info（使用可变对象来保证引用更新）
    current_block_info = {'data': {}}
    
    # 创建悬停标注
    annot = ax_main.annotate("", xy=(0,0), xytext=(15,15), textcoords="offset points",
                            bbox=dict(boxstyle="round", fc="lightyellow", ec="black", alpha=0.95),
                            fontsize=9, visible=False, zorder=1000)
    
    def on_hover(event):
        """鼠标悬停事件处理"""
        if event.inaxes == ax_main and event.xdata is not None and event.ydata is not None:
            block_data = current_block_info.get('data', {})
            if not block_data:
                return
            
            # 查找鼠标位置对应的块
            found = False
            for (bx, by), info in block_data.items():
                if bx <= event.xdata < bx + 1.0 and by <= event.ydata < by + 1.0:
                    annot.xy = (event.xdata, event.ydata)
                    annot.set_text(info)
                    annot.set_visible(True)
                    annot.set_zorder(1000)  # 确保在最上层
                    fig.canvas.draw_idle()
                    found = True
                    break
            
            # 如果不在任何块上，隐藏标注
            if not found and annot.get_visible():
                annot.set_visible(False)
                fig.canvas.draw_idle()
        elif annot.get_visible():
            # 鼠标移出图形区域
            annot.set_visible(False)
            fig.canvas.draw_idle()
    
    # 连接事件
    textbox.on_submit(on_submit)
    btn_apply.on_clicked(on_apply)
    btn_reset.on_clicked(on_reset)
    btn_undo.on_clicked(on_undo)
    fig.canvas.mpl_connect('motion_notify_event', on_hover)
    
    # 初始绘制
    block_info = draw_cube(current_state, "交互式魔方 - 输入公式开始", annot)
    current_block_info['data'] = block_info
    
    # 打印使用说明
    print("\n" + "="*60)
    print("🎮 交互式魔方GUI")
    print("="*60)
    print("\n使用说明:")
    print("  1. 在文本框中输入公式（如 F, R U, [F,R], D L B 等）")
    print("  2. 按Enter或点击'应用'按钮")
    print("  3. 点击'撤销'可以撤销上一步")
    print("  4. 点击'重置'回到初始状态")
    print("  5. 鼠标移到块上查看详细信息（位置名称如UFR等）")
    print("\n支持的操作: F, R, U, L, B, D（所有6个面）")
    print("     逆操作: F', R', U', L', B', D'")
    print("     双层: F2, R2, U2, L2, B2, D2")
    print("     交换子: [F,R], [L,D], [F,[R,U]] 等")
    print("="*60 + "\n")
    
    plt.show()


def animate_algorithm_matplotlib(alg_str: str):
    """
    使用 matplotlib 动画展示公式执行
    
    Args:
        alg_str: 公式字符串
    """
    try:
        import matplotlib.pyplot as plt
        from matplotlib.animation import FuncAnimation
        import matplotlib
        
        # 配置中文字体支持
        matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'STSong', 'DejaVu Sans']
        matplotlib.rcParams['axes.unicode_minus'] = False
    except ImportError:
        print("❌ 需要安装 matplotlib: pip install matplotlib")
        return
    
    moves = parse_algorithm(alg_str)
    states = [CubeState()]
    
    # 生成每一步的状态
    current = CubeState()
    for move_name in moves:
        if move_name in MOVES:
            current = apply_move(current, MOVES[move_name])
            states.append(current.copy())
    
    # 创建动画
    fig, ax = plt.subplots(figsize=(10, 8))
    
    def update(frame):
        ax.clear()
        state = states[frame]
        
        # 这里简化显示
        ax.text(0.5, 0.9, f"步骤 {frame}/{len(states)-1}", 
                ha='center', transform=ax.transAxes, fontsize=14, fontweight='bold')
        
        if frame > 0:
            ax.text(0.5, 0.8, f"操作: {moves[frame-1]}", 
                    ha='center', transform=ax.transAxes, fontsize=12)
        
        # 显示置换
        corner_cycles = permutation_cycles(state.corners)
        edge_cycles = permutation_cycles(state.edges)
        
        ax.text(0.5, 0.6, "角块循环:", 
                ha='center', transform=ax.transAxes, fontsize=11, fontweight='bold')
        ax.text(0.5, 0.5, format_cycles(corner_cycles) if corner_cycles else "identity", 
                ha='center', transform=ax.transAxes, fontsize=10)
        
        ax.text(0.5, 0.35, "棱块循环:", 
                ha='center', transform=ax.transAxes, fontsize=11, fontweight='bold')
        ax.text(0.5, 0.25, format_cycles(edge_cycles) if edge_cycles else "identity", 
                ha='center', transform=ax.transAxes, fontsize=10)
        
        ax.axis('off')
    
    anim = FuncAnimation(fig, update, frames=len(states), interval=1000, repeat=True)
    plt.show()


# ==================== 轨迹可视化 ====================

def visualize_block_trajectory(alg_str: str, block_type: str = "corner", block_id: int = 0):
    """
    可视化一个块在公式执行过程中的运动轨迹
    
    Args:
        alg_str: 公式字符串
        block_type: "corner" 或 "edge"
        block_id: 块的编号
    """
    print("\n" + "="*60)
    print(f"📍 块运动轨迹: {block_type.upper()} {block_id}")
    print(f"公式: {alg_str}")
    print("="*60)
    
    moves = parse_algorithm(alg_str)
    state = CubeState()
    
    trajectory = [block_id]
    current_pos = block_id
    
    print(f"\n初始位置: {current_pos}")
    
    for i, move_name in enumerate(moves, 1):
        if move_name in MOVES:
            move = MOVES[move_name]
            
            if block_type == "corner":
                perm = move.corner_perm
            else:
                perm = move.edge_perm
            
            # 找到当前位置的块会移动到哪里
            new_pos = None
            for j, val in enumerate(perm):
                if val == current_pos:
                    new_pos = j
                    break
            
            if new_pos != current_pos:
                print(f"第 {i:2d} 步 {move_name:3s}: {current_pos:2d} → {new_pos:2d}")
                current_pos = new_pos
                trajectory.append(current_pos)
            else:
                print(f"第 {i:2d} 步 {move_name:3s}: {current_pos:2d} (不动)")
    
    print(f"\n最终位置: {current_pos}")
    print(f"\n完整轨迹: {' → '.join(map(str, trajectory))}")
    print(f"总移动次数: {len([t for i, t in enumerate(trajectory[1:], 1) if t != trajectory[i-1]])}")
    
    if current_pos == block_id:
        print(f"✅ 块回到了初始位置！")
    
    print("="*60 + "\n")


# ==================== 主程序 ====================

def main():
    """主函数"""
    print("\n" + "="*70)
    print("🎨 魔方可视化工具")
    print("="*70)
    
    # 检查是否启动交互式GUI
    if len(sys.argv) > 1 and sys.argv[1] in ['-i', '--interactive', 'interactive', 'gui']:
        print("\n启动交互式GUI...")
        interactive_cube_gui()
        return
    
    if len(sys.argv) > 1:
        alg = " ".join(sys.argv[1:])
    else:
        alg = "[F, [R, U]]"
    
    print(f"\n演示公式: {alg}")
    print("\n💡 提示: 使用 'python visualize.py -i' 启动交互式GUI")
    
    # 1. 初始状态
    print("\n" + "━"*70)
    print("1️⃣ 初始状态")
    print("━"*70)
    initial_state = CubeState()
    visualize_cube_text(initial_state)
    
    # 2. 应用公式后的状态
    print("\n" + "━"*70)
    print(f"2️⃣ 应用公式后: {alg}")
    print("━"*70)
    final_state = apply_algorithm(initial_state, alg)
    visualize_cube_text(final_state)
    
    # 3. 循环分解
    print("\n" + "━"*70)
    print("3️⃣ 循环分解")
    print("━"*70)
    analyze_algorithm(alg)
    
    # 4. 块轨迹
    print("\n" + "━"*70)
    print("4️⃣ 块运动轨迹")
    print("━"*70)
    visualize_block_trajectory(alg, "corner", 0)
    
    # 5. 图形可视化（可选）
    print("\n" + "━"*70)
    print("5️⃣ 图形可视化")
    print("━"*70)
    
    try:
        import matplotlib
        print("✓ 检测到 matplotlib，显示图形...")
        visualize_cube_matplotlib(final_state, f"应用公式后: {alg}")
    except ImportError:
        print("ℹ️  未安装 matplotlib")
        print("   安装方法: pip install matplotlib")
        print("   安装后可以看到彩色的图形化展示")
    
    print("\n✅ 可视化完成！\n")


if __name__ == "__main__":
    main()

