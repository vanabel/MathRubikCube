#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
魔方置换群数学模型 - Streamlit Web应用

使用方法：
    streamlit run web_app.py
"""

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from cube import *
from visualize import visualize_cube_matplotlib
import io

# 页面配置
st.set_page_config(
    page_title="魔方置换群模型",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 标题
st.title("🎲 魔方置换群数学模型")
st.markdown("*交互式魔方公式分析与可视化*")

# 侧边栏 - 使用说明
with st.sidebar:
    st.header("📖 使用说明")
    st.markdown("""
    ### 支持的操作
    - **基本操作**: F, R, U, L, B, D
    - **逆操作**: F', R', U', L', B', D'
    - **双层**: F2, R2, U2, L2, B2, D2
    - **交换子**: [F,R], [L,D], [F,[R,U]]
    
    ### 颜色方案
    - U(上): 🟨 黄色
    - D(下): ⚪ 白色
    - F(前): 🟩 绿色
    - B(后): 🟦 蓝色
    - L(左): 🟥 红色
    - R(右): 🟧 橙色
    
    ### 示例公式
    """)
    
    example_formulas = {
        "Sexy Move": "R U R' U'",
        "OLL 45": "F R U R' U' F'",
        "Sune": "R U R' U R U2 R'",
        "T-Perm": "R U R' U' R' F R2 U' R' U' R U R' F'",
        "[F,R]": "[F, R]",
        "[F,[R,U]]": "[F, [R, U]]",
    }
    
    for name, formula in example_formulas.items():
        if st.button(name, key=f"ex_{name}"):
            st.session_state.formula = formula

    st.markdown("---")
    st.markdown("""
    ### 📚 资源
    - [编码参考](docs/ENCODING_REFERENCE.md)
    - [GitHub仓库](#)
    """)

# 初始化session state
if 'formula' not in st.session_state:
    st.session_state.formula = ""
if 'history' not in st.session_state:
    st.session_state.history = []

# 主界面
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🎮 公式输入")
    
    # 公式输入框
    formula = st.text_input(
        "输入魔方公式",
        value=st.session_state.formula,
        placeholder="例如: F R U R' U' F'",
        help="支持基本操作、交换子等"
    )
    
    # 按钮行
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    with btn_col1:
        apply_btn = st.button("🚀 应用公式", type="primary")
    with btn_col2:
        reset_btn = st.button("🔄 重置")
    with btn_col3:
        if st.session_state.history:
            undo_btn = st.button("↩️ 撤销")
        else:
            undo_btn = False

# 处理按钮
if apply_btn and formula.strip():
    st.session_state.history.append(formula)
    st.session_state.formula = formula

if reset_btn:
    st.session_state.history = []
    st.session_state.formula = ""
    st.rerun()

if undo_btn and st.session_state.history:
    st.session_state.history.pop()
    st.rerun()

# 计算当前状态
current_state = CubeState()
if st.session_state.history:
    for f in st.session_state.history:
        try:
            current_state = apply_algorithm(current_state, f)
        except Exception as e:
            st.error(f"❌ 公式错误: {e}")

# 显示可视化
with col1:
    st.header("📊 魔方状态可视化")
    
    try:
        # 使用matplotlib绘制
        fig, ax = plt.subplots(figsize=(12, 7))
        ax.set_xlim(-2.5, 14.5)
        ax.set_ylim(-0.5, 10.0)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # 绘制魔方（简化版，复用visualize.py的逻辑）
        # 这里为了简化，直接调用已有函数并保存为图片
        import matplotlib
        matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'STSong', 'DejaVu Sans']
        matplotlib.rcParams['axes.unicode_minus'] = False
        
        # 创建一个临时图形用于显示
        from visualize import visualize_cube_matplotlib
        
        # 保存到内存
        buf = io.BytesIO()
        
        # 使用visualize函数但不显示
        import matplotlib.pyplot as plt
        plt.ioff()  # 关闭交互模式
        visualize_cube_matplotlib(current_state, 
                                 title=f"当前状态" + (f": {st.session_state.history[-1]}" if st.session_state.history else ""))
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        plt.close()
        
        st.image(buf, use_container_width=True)
        
    except Exception as e:
        st.error(f"❌ 可视化错误: {e}")
        st.code(str(e))

# 右侧 - 分析结果
with col2:
    st.header("📈 置换分析")
    
    if st.session_state.history:
        # 角块分析
        st.subheader("🔺 角块")
        corner_cycles = permutation_cycles(current_state.corners)
        corner_str = format_cycles(corner_cycles) if corner_cycles else 'identity'
        st.code(corner_str, language=None)
        
        corner_moved = sum(1 for i in range(8) if current_state.corners[i] != i)
        corner_ori_changed = sum(1 for x in current_state.corner_ori if x != 0)
        st.metric("移动的角块", f"{corner_moved}/8")
        st.metric("朝向改变", f"{corner_ori_changed}/8")
        
        # 棱块分析
        st.subheader("🔹 棱块")
        edge_cycles = permutation_cycles(current_state.edges)
        edge_str = format_cycles(edge_cycles) if edge_cycles else 'identity'
        st.code(edge_str, language=None)
        
        edge_moved = sum(1 for i in range(12) if current_state.edges[i] != i)
        edge_ori_changed = sum(1 for x in current_state.edge_ori if x != 0)
        st.metric("移动的棱块", f"{edge_moved}/12")
        st.metric("朝向改变", f"{edge_ori_changed}/12")
        
        # 朝向验证
        is_valid, msg = check_orientation_valid(current_state)
        if is_valid:
            st.success(f"✅ {msg}")
        else:
            st.error(f"❌ {msg}")
        
        # 是否还原
        if current_state.is_solved():
            st.success("🎉 魔方已还原！")
    else:
        st.info("👆 输入公式开始分析")

# 历史记录
if st.session_state.history:
    st.header("📜 操作历史")
    st.write(" → ".join(st.session_state.history[-10:]))  # 显示最近10个

# 页脚
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>🎲 魔方置换群数学模型 | 基于Python实现 | 支持位置与朝向分析</p>
    <p><a href='docs/ENCODING_REFERENCE.md'>编码参考</a> | 
       <a href='docs/QUICKSTART.md'>快速开始</a> | 
       <a href='#'>GitHub</a></p>
</div>
""", unsafe_allow_html=True)

