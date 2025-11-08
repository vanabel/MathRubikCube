#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证真实魔方结果
"""

from cube import *

def get_block_colors(block_id, position_id, orientation):
    """
    获取角块在特定位置和朝向下，各个面上显示的颜色
    
    block_id: 原始块编号 (0-7)
    position_id: 当前位置编号 (0-7)
    orientation: 朝向值 (0, 1, 2)
    """
    # 定义每个块的原始颜色（按U/D, F/B, L/R顺序）
    corner_colors = {
        0: ("Yellow", "Green", "Orange"),   # UFR: U, F, R
        1: ("Yellow", "Green", "Red"),      # UFL: U, F, L
        2: ("Yellow", "Blue", "Red"),       # UBL: U, B, L
        3: ("Yellow", "Blue", "Orange"),    # UBR: U, B, R
        4: ("White", "Green", "Orange"),    # DFR: D, F, R
        5: ("White", "Green", "Red"),       # DFL: D, F, L
        6: ("White", "Blue", "Red"),        # DBL: D, B, L
        7: ("White", "Blue", "Orange"),     # DBR: D, B, R
    }
    
    # 定义每个位置的面顺序（哪个面对应UD/FB/LR）
    position_faces = {
        0: ("U", "F", "R"),   # UFR
        1: ("U", "F", "L"),   # UFL
        2: ("U", "B", "L"),   # UBL
        3: ("U", "B", "R"),   # UBR
        4: ("D", "F", "R"),   # DFR
        5: ("D", "F", "L"),   # DFL
        6: ("D", "B", "L"),   # DBL
        7: ("D", "B", "R"),   # DBR
    }
    
    block_cols = corner_colors[block_id]
    pos_faces = position_faces[position_id]
    
    # 应用朝向旋转
    # 对于角块，朝向旋转是沿着UD轴的
    rotated_colors = list(block_cols)
    if orientation == 1:  # 顺时针120度
        rotated_colors = [block_cols[0], block_cols[2], block_cols[1]]
    elif orientation == 2:  # 逆时针120度
        rotated_colors = [block_cols[0], block_cols[1], block_cols[2]]
        rotated_colors = [block_cols[0], block_cols[2], block_cols[1]]
        rotated_colors = [rotated_colors[0], rotated_colors[2], rotated_colors[1]]
    
    result = {}
    for i, face in enumerate(pos_faces):
        result[face] = rotated_colors[i]
    
    return result


def analyze_real_cube():
    """分析真实魔方的状态"""
    print("="*70)
    print("🔍 分析真实魔方 vs 模型预测")
    print("="*70)
    
    # 执行公式
    state = CubeState()
    state = apply_algorithm(state, "F R U R' U' F'")
    
    print("\n【模型预测】")
    print("\n角块置换:", state.corners)
    print("角块朝向:", state.corner_ori)
    print("\n棱块置换:", state.edges)
    print("棱块朝向:", state.edge_ori)
    
    print("\n【模型预测 - 角块详细】")
    corner_names = ["UFR", "UFL", "UBL", "UBR", "DFR", "DFL", "DBL", "DBR"]
    
    for pos in range(8):
        block = state.corners[pos]
        ori = state.corner_ori[pos]
        colors = get_block_colors(block, pos, ori)
        
        pos_name = corner_names[pos]
        block_name = corner_names[block]
        
        print(f"\n位置{pos} ({pos_name}):")
        print(f"  块编号: {block} ({block_name})")
        print(f"  朝向: {ori}")
        print(f"  颜色: {colors}")
    
    print("\n" + "="*70)
    print("【真实魔方观察】")
    print("="*70)
    
    real_corners = {
        0: {"U": "Red", "F": "Green", "R": "Yellow"},
        1: {"U": "Yellow", "F": "Orange", "L": "Green"},
        2: {"U": "Yellow", "B": "Orange", "L": "Blue"},
        3: {"U": "Red", "B": "Blue", "R": "Yellow"},
    }
    
    print("\n角块位置（用户观察）:")
    for pos, colors in real_corners.items():
        print(f"位置{pos}: {colors}")
    
    print("\n" + "="*70)
    print("【对比分析】")
    print("="*70)
    
    # 根据观察到的颜色，推断是哪个块
    def find_block_by_colors(observed_colors):
        """根据观察到的颜色找到对应的块"""
        # 提取观察到的颜色集合
        color_set = set(observed_colors.values())
        
        corner_color_sets = {
            0: {"Yellow", "Green", "Orange"},
            1: {"Yellow", "Green", "Red"},
            2: {"Yellow", "Blue", "Red"},
            3: {"Yellow", "Blue", "Orange"},
            4: {"White", "Green", "Orange"},
            5: {"White", "Green", "Red"},
            6: {"White", "Blue", "Red"},
            7: {"White", "Blue", "Orange"},
        }
        
        for block_id, block_colors in corner_color_sets.items():
            if color_set == block_colors:
                return block_id
        return None
    
    print("\n从颜色推断真实状态:")
    for pos, observed in real_corners.items():
        block_id = find_block_by_colors(observed)
        if block_id is not None:
            corner_names = ["UFR", "UFL", "UBL", "UBR", "DFR", "DFL", "DBL", "DBR"]
            print(f"\n位置{pos}:")
            print(f"  观察到的颜色: {observed}")
            print(f"  推断的块: {block_id} ({corner_names[block_id]})")
            
            # 对比模型预测
            model_block = state.corners[pos]
            model_ori = state.corner_ori[pos]
            print(f"  模型预测: 块{model_block} ({corner_names[model_block]}), 朝向{model_ori}")
            
            if block_id == model_block:
                print(f"  ✓ 块匹配！")
            else:
                print(f"  ✗ 块不匹配！模型错误？")


if __name__ == "__main__":
    analyze_real_cube()

