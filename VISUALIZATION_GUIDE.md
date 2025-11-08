# 🎨 可视化使用指南

## 📖 概述

本项目提供了三种可视化方式来帮助你理解魔方的置换结构：

1. **文本可视化** - 在终端显示魔方状态
2. **图形可视化** - 使用matplotlib绘制彩色展开图
3. **轨迹追踪** - 显示块在公式执行过程中的运动路径

---

## 🚀 快速开始

### 基础用法

```bash
# 可视化一个公式的效果
python visualize.py "[F, [R, U]]"

# 可视化其他公式
python visualize.py "R U R' U'"
python visualize.py "[R, U]"
```

### 安装图形支持（可选）

```bash
pip install matplotlib
```

安装后可以看到彩色的图形化展示！

---

## 📊 文本可视化

### 功能说明

文本可视化会在终端显示：

- ✓ 魔方的3D立体图（ASCII艺术）
- ✓ 每个位置的块编号
- ✓ 标记哪些块被移动了
- ✓ 统计移动的块数量

### 使用示例

```python
from cube import *
from visualize import *

# 创建状态
state = apply_algorithm(CubeState(), "R U R' U'")

# 可视化
visualize_cube_text(state)
```

### 输出示例

```
============================================================
🎲 魔方状态可视化（文本版）
============================================================

【角块状态】
    UBL UBR
     2---3  
    /|  /|  
   1---0 |  ← UFR位置: 角块 4
   | 6-|-7  
   |/  |/   
   5---4    
    DFL DFR

当前角块置换:
  位置 0(UFR): 角块4(DFR) ← 移动了
  位置 1(UFL): 角块1(UFL)
  ...

【统计】
  移动的角块: 3/8
  移动的棱块: 2/12
============================================================
```

---

## 🎨 图形可视化

### 功能说明

使用matplotlib绘制：

- ✓ 魔方六个面的展开图
- ✓ 彩色标记（绿色=未动，红色=已动）
- ✓ 块编号标注
- ✓ 图例和统计信息

### 使用示例

```python
from cube import *
from visualize import *

# 创建状态
state = apply_algorithm(CubeState(), "[F, [R, U]]")

# 图形可视化（会打开窗口）
visualize_cube_matplotlib(state, title="嵌套交换子的效果")

# 💡 提示：将鼠标移到任意块上，会显示详细信息！
```

### 颜色说明

- 🟢 **绿色** - 角块，未移动
- 🔴 **红色** - 角块，已移动
- 🔵 **蓝色** - 棱块，未移动
- 🟠 **橙色** - 棱块，已移动

### 🖱️ 交互功能

**鼠标悬停**：将鼠标移到任意块上，会显示：
- 位置名称（如UFR、UFL）
- 位置编号
- 当前块的名称和编号
- 移动状态

### 展开图布局

```
        [上 U]
[左 L] [前 F] [右 R] [后 B]
        [下 D]
```

---

## 📍 块轨迹追踪

### 功能说明

追踪一个特定的块在公式执行过程中的运动：

- ✓ 显示每一步的位置变化
- ✓ 完整的运动轨迹
- ✓ 总移动次数统计

### 使用示例

```python
from visualize import *

# 追踪角块0的运动
visualize_block_trajectory("[F, [R, U]]", "corner", 0)

# 追踪棱块3的运动
visualize_block_trajectory("R U R' U'", "edge", 3)
```

### 输出示例

```
============================================================
📍 块运动轨迹: CORNER 0
公式: [F, [R, U]]
============================================================

初始位置: 0
第  1 步 F  :  0 →  1
第  2 步 R  :  1 (不动)
第  3 步 U  :  1 →  2
...
第 10 步 R' :  0 →  3

最终位置: 3

完整轨迹: 0 → 1 → 2 → 1 → 0 → 1 → 0 → 3
总移动次数: 7
============================================================
```

---

## 🎬 动画可视化

### 文本动画

逐步显示公式执行过程：

```python
from visualize import *

# 0.5秒延迟的动画
animate_algorithm_text("R U R' U'", delay=0.5)
```

### 图形动画（实验性）

```python
from visualize import *

# matplotlib动画
animate_algorithm_matplotlib("R U R' U'")
```

---

## 🎓 实用场景

### 场景1：理解交换子

```bash
# 可视化简单交换子
python visualize.py "[R, U]"

# 可视化嵌套交换子
python visualize.py "[F, [R, U]]"
```

**观察要点：**
- 看哪些块被移动了
- 注意三循环的形成

### 场景2：分析著名公式

```bash
# Sexy Move
python visualize.py "R U R' U'"

# Sune
python visualize.py "R U R' U R U2 R'"
```

**观察要点：**
- 块的循环结构
- 对称性

### 场景3：验证公式互逆

```python
from cube import *
from visualize import *

# 原公式
state1 = apply_algorithm(CubeState(), "R U R' U R U2 R'")
visualize_cube_text(state1)

# 原公式 + 逆
state2 = apply_algorithm(state1, "R U2 R' U' R U' R'")
visualize_cube_text(state2)  # 应该回到初始状态
```

### 场景4：探索新公式

```python
from visualize import *

# 自己设计的公式
my_formula = "[F, [R, [U, F]]]"

# 可视化效果
visualize_cube_text(apply_algorithm(CubeState(), my_formula))

# 追踪角块0
visualize_block_trajectory(my_formula, "corner", 0)
```

---

## 🔧 高级用法

### 比较不同公式

```python
from cube import *
from visualize import *

formulas = [
    "[R, U]",
    "[U, R]",
    "[F, R]"
]

for f in formulas:
    print(f"\n公式: {f}")
    state = apply_algorithm(CubeState(), f)
    
    corner_cycles = permutation_cycles(state.corners)
    print(f"角块循环: {format_cycles(corner_cycles)}")
    
    # 可选：显示图形
    # visualize_cube_matplotlib(state, title=f)
```

### 批量可视化

```python
from cube import *
from visualize import *

# 研究所有简单交换子
base_moves = ["F", "R", "U"]

for i, a in enumerate(base_moves):
    for b in base_moves[i+1:]:
        formula = f"[{a}, {b}]"
        print(f"\n{'='*60}")
        print(f"交换子: {formula}")
        print(f"{'='*60}")
        
        state = apply_algorithm(CubeState(), formula)
        visualize_cube_text(state)
```

### 轨迹对比

```python
from visualize import *

formula = "[F, [R, U]]"

# 追踪多个块
for i in range(4):
    print(f"\n追踪角块 {i}:")
    visualize_block_trajectory(formula, "corner", i)
```

---

## 📚 API 参考

### visualize_cube_text(state, show_legend=True)

文本方式可视化魔方状态

**参数:**
- `state`: CubeState 对象
- `show_legend`: 是否显示图例

### visualize_cube_matplotlib(state, title="魔方状态")

图形方式可视化魔方状态

**参数:**
- `state`: CubeState 对象
- `title`: 图表标题

**依赖:** matplotlib

### visualize_block_trajectory(alg_str, block_type, block_id)

追踪块的运动轨迹

**参数:**
- `alg_str`: 公式字符串
- `block_type`: "corner" 或 "edge"
- `block_id`: 块的编号 (0-7 for corners, 0-11 for edges)

### animate_algorithm_text(alg_str, delay=0.5)

文本动画演示

**参数:**
- `alg_str`: 公式字符串
- `delay`: 每步延迟（秒）

### animate_algorithm_matplotlib(alg_str)

图形动画演示（实验性）

**参数:**
- `alg_str`: 公式字符串

**依赖:** matplotlib

---

## 💡 技巧和提示

### 提示1：理解块编号

角块编号（0-7）：
```
    2---3
   /|  /|
  1---0 |
  | 6-|-7
  |/  |/
  5---4
```

- 0-3: 上层
- 4-7: 下层

### 提示2：识别三循环

三循环在输出中显示为 `(a b c)`，表示：
- 位置a的块 → 位置b
- 位置b的块 → 位置c
- 位置c的块 → 位置a

### 提示3：使用图形可视化

如果文本可视化不够直观，安装matplotlib后使用图形版本：

```bash
pip install matplotlib
python -c "from visualize import *; visualize_cube_matplotlib(apply_algorithm(CubeState(), '[F, [R, U]]'))"
```

### 提示4：保存图片

```python
import matplotlib.pyplot as plt
from visualize import *

state = apply_algorithm(CubeState(), "[F, [R, U]]")
visualize_cube_matplotlib(state)
plt.savefig("cube_state.png", dpi=150, bbox_inches='tight')
```

---

## 🐛 故障排除

### Q: matplotlib导入失败？

**A:** 安装matplotlib：
```bash
pip install matplotlib
```

### Q: 文本显示乱码？

**A:** 确保终端支持UTF-8编码

### Q: 图形窗口不显示？

**A:** 尝试：
```python
import matplotlib
matplotlib.use('TkAgg')  # 或 'Qt5Agg'
```

### Q: 想要更好的可视化？

**A:** 
1. 安装matplotlib获得彩色图形
2. 未来版本将支持3D可视化
3. 可以自己扩展 `visualize.py`

---

## 🎯 学习路径

1. **初学者**
   - 先用文本可视化理解基本概念
   - 观察简单公式的效果
   - 使用轨迹追踪理解块的移动

2. **进阶**
   - 安装matplotlib使用图形可视化
   - 比较不同公式的效果
   - 探索交换子的性质

3. **高级**
   - 自己设计公式
   - 研究循环结构
   - 扩展可视化功能

---

## 📖 延伸阅读

- `README.md` - 项目总览
- `QUICKSTART.md` - 快速入门
- `cube.py` - 核心算法实现
- `examples.py` - 更多示例

---

**🎨 享受可视化带来的直观理解！**

