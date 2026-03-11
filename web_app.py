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
    initial_sidebar_state="collapsed"
)

# 自定义CSS - 紧凑布局
st.markdown("""
<style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    h1 {
        padding-top: 0rem;
        margin-top: 0rem;
        margin-bottom: 0.5rem;
    }
    h2 {
        margin-top: 0.5rem;
        margin-bottom: 0.3rem;
    }
    h3 {
        margin-top: 0.3rem;
        margin-bottom: 0.2rem;
    }
    .stMetric {
        padding: 0.2rem 0;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

# 标题 - 紧凑版
st.markdown("# 🎲 魔方置换群模型")
st.caption("交互式公式分析与可视化")

# 侧边栏 - 精简版
with st.sidebar:
    st.markdown("### 📖 说明")
    
    with st.expander("操作语法", expanded=False):
        st.markdown("""
        **基本**: F R U L B D  
        **逆**: F' R' U' L' B' D'  
        **双**: F2 R2 U2 L2 B2 D2  
        **交换子**: [F,R] [L,D]
        """)
    
    with st.expander("颜色方案", expanded=False):
        st.markdown("""
        U🟨 D⚪ F🟩 B🟦 L🟥 R🟧
        """)
    
    st.markdown("### 💡 示例")
    
    example_formulas = {
        "顶层十字": "F [R,U] F'",
        "做鱼 (L版)": "L U L' U L U2 L'",
        "做鱼 (R版)": "R' U' R U' R' U2 R",
        "角块互换": "R U2 R' U' R U2 L' U R' U' L",
        "棱块三大换": "F2 U L R' F2 R L' U F2",
        "Sexy Move": "R U R' U'",
        "OLL 45": "F R U R' U' F'",
        "Sune": "R U R' U R U2 R'",
        "T-Perm": "R U R' U' R' F R2 U' R' U' R U R' F'",
        "[F,R]": "[F, R]",
        "[F,[R,U]]": "[F, [R, U]]",
    }
    
    cols = st.columns(2)
    for idx, (name, formula) in enumerate(example_formulas.items()):
        col = cols[idx % 2]
        with col:
            if st.button(name, key=f"ex_{name}", use_container_width=True):
                # 点击示例按钮：从还原状态开始，只执行这一条公式
                st.session_state.history = [formula]
                st.session_state.formula = formula
                st.rerun()
    
    with st.expander("📚 资源", expanded=False):
        st.markdown("[编码参考](docs/ENCODING_REFERENCE.md) | [文档](docs/)")

# 初始化session state
if 'formula' not in st.session_state:
    st.session_state.formula = ""
if 'history' not in st.session_state:
    st.session_state.history = []

# 公式输入区 - 紧凑布局
input_col1, input_col2 = st.columns([3, 1])

with input_col1:
    formula = st.text_input(
        "🎮 公式",
        value=st.session_state.formula,
        placeholder="F R U R' U' F'",
        label_visibility="collapsed"
    )

with input_col2:
    btn_cols = st.columns(3)
    with btn_cols[0]:
        apply_btn = st.button("▶️", help="应用", use_container_width=True, type="primary")
    with btn_cols[1]:
        reset_btn = st.button("🔄", help="重置", use_container_width=True)
    with btn_cols[2]:
        undo_btn = st.button("↩️", help="撤销", use_container_width=True) if st.session_state.history else None

# 处理按钮
if apply_btn and formula.strip():
    # 避免重复记录同一公式（例如刚点过示例按钮，又点▶️）
    if not st.session_state.history or st.session_state.history[-1] != formula:
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

# 主显示区 - 使用tabs紧凑组织
tab1, tab2 = st.tabs(["📊 可视化", "📈 数据分析"])

with tab1:
    try:
        # 使用matplotlib绘制
        import matplotlib
        matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'STSong', 'DejaVu Sans']
        matplotlib.rcParams['axes.unicode_minus'] = False
        
        # 保存到内存
        buf = io.BytesIO()
        plt.ioff()  # 关闭交互模式
        visualize_cube_matplotlib(current_state, 
                                 title=f"{st.session_state.history[-1]}" if st.session_state.history else "初始状态")
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        plt.close()
        
        st.image(buf, use_container_width=True)
        
    except Exception as e:
        st.error(f"❌ 可视化错误: {e}")

with tab2:
    if st.session_state.history:
        # 紧凑的两列布局
        data_col1, data_col2 = st.columns(2)
        
        with data_col1:
            st.markdown("##### 🔺 角块")
            corner_cycles = permutation_cycles(current_state.corners)
            corner_str = format_cycles(corner_cycles) if corner_cycles else 'identity'
            st.code(corner_str, language=None)
            
            corner_moved = sum(1 for i in range(8) if current_state.corners[i] != i)
            corner_ori_changed = sum(1 for x in current_state.corner_ori if x != 0)
            
            metric_cols = st.columns(2)
            metric_cols[0].metric("位置变", f"{corner_moved}/8")
            metric_cols[1].metric("朝向变", f"{corner_ori_changed}/8")
        
        with data_col2:
            st.markdown("##### 🔹 棱块")
            edge_cycles = permutation_cycles(current_state.edges)
            edge_str = format_cycles(edge_cycles) if edge_cycles else 'identity'
            st.code(edge_str, language=None)
            
            edge_moved = sum(1 for i in range(12) if current_state.edges[i] != i)
            edge_ori_changed = sum(1 for x in current_state.edge_ori if x != 0)
            
            metric_cols = st.columns(2)
            metric_cols[0].metric("位置变", f"{edge_moved}/12")
            metric_cols[1].metric("朝向变", f"{edge_ori_changed}/12")
        
        # 验证和状态
        st.markdown("---")
        status_cols = st.columns(2)
        
        with status_cols[0]:
            is_valid, msg = check_orientation_valid(current_state)
            if is_valid:
                st.success(f"✅ {msg}")
            else:
                st.error(f"❌ {msg}")
        
        with status_cols[1]:
            if current_state.is_solved():
                st.success("🎉 魔方已还原！")
            else:
                st.info(f"📝 已执行 {len(st.session_state.history)} 步")
    else:
        st.info("👆 输入公式开始分析")

# 历史记录 - 折叠显示
if st.session_state.history:
    with st.expander(f"📜 操作历史 ({len(st.session_state.history)}步)", expanded=False):
        st.caption(" → ".join(st.session_state.history))

# 页脚 - 精简
st.divider()
footer_cols = st.columns([1, 2, 1])
with footer_cols[1]:
    st.caption("🎲 魔方置换群数学模型 | [编码参考](docs/ENCODING_REFERENCE.md) | [文档](docs/DOCS_INDEX.md)")

