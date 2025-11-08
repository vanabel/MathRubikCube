# 🚀 快速入门指南

## 5分钟上手

### 1. 运行基础演示

```bash
python cube.py
```

这将展示：
- ✓ 基本操作（F, R, U）的循环结构
- ✓ 简单公式分析
- ✓ 交换子计算
- ✓ 嵌套交换子

### 2. 运行高级示例

```bash
python examples.py
```

这将展示：
- 交换子的性质
- 著名的魔方公式（Sune, Antisune, T-Perm等）
- 计算公式的阶
- 置换的复合
- 逆操作
- 寻找三循环
- 自定义交换子探索
- 为可视化准备数据

### 3. 交互式分析

```bash
python interactive.py
```

进入交互式模式，可以：
- 分析任意公式
- 计算交换子
- 计算公式的阶
- 求逆操作
- 比较公式

或者直接分析一个公式：

```bash
python interactive.py "[F, [R, U]]"
```

## 📚 常用命令

### 在交互式模式中

```
analyze F R U R' U' F'          # 分析一个公式
commutator R U                  # 计算交换子 [R, U]
order R U R' U'                 # 计算公式的阶
inverse R U R' U R U2 R'        # 计算逆
compare [R,U] | [U,R]           # 比较两个公式
moves                           # 显示所有操作
examples                        # 显示示例
help                            # 帮助
```

## 🎯 实用示例

### 示例1: 分析经典公式

```python
from cube import analyze_algorithm

# Sexy Move
analyze_algorithm("R U R' U'")

# Sune
analyze_algorithm("R U R' U R U2 R'")

# T-Perm
analyze_algorithm("R U R' U' R' F R2 U' R' U' R U R' F'")
```

### 示例2: 探索交换子

```python
from cube import *

# 简单交换子
analyze_algorithm("[R, U]")

# 嵌套交换子
analyze_algorithm("[F, [R, U]]")

# 双层嵌套
analyze_algorithm("[[F, R], [U, R]]")
```

### 示例3: 研究置换结构

```python
from cube import *

# 获取置换
corner_perm, edge_perm = get_algorithm_permutation("[F, [R, U]]")

# 循环分解
corner_cycles = permutation_cycles(corner_perm)
edge_cycles = permutation_cycles(edge_perm)

print(f"角块循环: {format_cycles(corner_cycles)}")
print(f"棱块循环: {format_cycles(edge_cycles)}")
```

### 示例4: 计算公式的阶

```python
from cube import *

alg = "R U R' U'"
state = CubeState()

count = 0
while count < 1000:
    state = apply_algorithm(state, alg)
    count += 1
    if state.is_solved():
        print(f"阶 = {count}")
        break
```

### 示例5: 验证公式互逆

```python
from cube import *

alg = "R U R' U R U2 R'"
moves = parse_algorithm(alg)
inverse = " ".join(invert_sequence(moves))

# 验证
combined = alg + " " + inverse
corner, edge = get_algorithm_permutation(combined)

# 应该得到恒等置换
print(f"是恒等? {corner == list(range(8)) and edge == list(range(12))}")
```

## 🎲 核心API

### 类

- `CubeState()` - 魔方状态
- `Move(name, corner_perm, edge_perm)` - 魔方操作

### 函数

**状态操作：**
- `apply_move(state, move)` - 应用单个操作
- `apply_algorithm(state, alg_str)` - 应用公式

**置换工具：**
- `apply_permutation(state, perm)` - 应用置换
- `compose_permutation(p, q)` - 复合置换
- `invert_permutation(p)` - 求逆置换
- `permutation_cycles(perm)` - 循环分解

**公式解析：**
- `parse_algorithm(alg_str)` - 解析公式字符串
- `invert_sequence(moves)` - 反转操作序列

**分析工具：**
- `get_algorithm_permutation(alg_str)` - 获取总置换
- `analyze_algorithm(alg_str)` - 完整分析
- `format_cycles(cycles)` - 格式化输出

## 🧮 数学背景速查

### 魔方记法
- `F`, `R`, `U` - 前、右、上面顺时针90°
- `F'`, `R'`, `U'` - 逆时针90°
- `F2`, `R2`, `U2` - 180°旋转

### 交换子
- `[A, B] = A B A⁻¹ B⁻¹`
- 交换子通常产生三循环
- 可以嵌套：`[F, [R, U]]`

### 循环表示
- `(0 1 2)` 表示 `0→1, 1→2, 2→0`
- `(0 1) (2 3)` 表示两个独立的2-循环
- 恒等置换表示为 `identity`

### 块编号

**角块 (0-7):**
```
    2---3
   /|  /|
  1---0 |    U (上)
  | 6-|-7
  |/  |/
  5---4        D (下)
```

**棱块 (0-11):**
- 0-3: U层 (UF, UL, UB, UR)
- 4-7: 中层 (FR, FL, BL, BR)  
- 8-11: D层 (DF, DL, DB, DR)

## 🔬 进阶探索

### 1. 寻找特定循环结构

```python
# 寻找三循环
for a in ["F", "R", "U"]:
    for b in ["F", "R", "U"]:
        if a != b:
            alg = f"[{a}, {b}]"
            corner, _ = get_algorithm_permutation(alg)
            cycles = permutation_cycles(corner)
            if any(len(c) == 3 for c in cycles):
                print(f"{alg}: {format_cycles(cycles)}")
```

### 2. 研究公式的周期性

```python
alg = "R U R' U'"
state = CubeState()

for i in range(1, 10):
    state = apply_algorithm(state, alg)
    corner_cycles = permutation_cycles(state.corners)
    print(f"第{i}次: {format_cycles(corner_cycles)}")
```

### 3. 构造自定义交换子

```python
# 测试不同的交换子组合
base = ["F", "R", "U", "F'", "R'", "U'"]

for a in base:
    for b in base:
        alg = f"[{a}, {b}]"
        corner, edge = get_algorithm_permutation(alg)
        c_cycles = permutation_cycles(corner)
        e_cycles = permutation_cycles(edge)
        
        # 只显示产生三循环的
        if any(len(c) == 3 for c in c_cycles):
            print(f"{alg}:")
            print(f"  角块: {format_cycles(c_cycles)}")
            print(f"  棱块: {format_cycles(e_cycles)}")
```

## 📖 延伸阅读

### 群论概念
- **群的阶**: 群中元素的个数（魔方群 ≈ 4.3×10¹⁹）
- **元素的阶**: 元素重复多少次回到单位元
- **生成元**: 能生成整个群的最小子集
- **交换子**: 度量两个元素"不交换"的程度

### 魔方代数
- 魔方群是 S₈ × S₁₂ 的子群
- 偶置换约束
- 朝向约束（未实现）
- 上帝之数: 20步

### 实用技巧
- **三循环分解**: 任何偶置换都可分解为三循环
- **交换子构造**: 用于构造特定的块循环
- **共轭操作**: `A X A⁻¹` 将 X 的作用"搬到"其他位置

## 🚀 下一步

1. **添加更多操作**: 实现 L, B, D
2. **添加朝向**: 完整的魔方状态
3. **可视化**: 显示块的移动
4. **算法库**: 收集常用公式
5. **求解器**: 自动寻找解法

## 💡 小技巧

- 使用 `F2` 而不是 `F F`
- 交换子用方括号：`[R, U]` 而不是手动展开
- 批处理模式快速测试：`python interactive.py "R U R' U'"`
- 查看示例获取灵感：`python examples.py`

祝你探索愉快！🎲

