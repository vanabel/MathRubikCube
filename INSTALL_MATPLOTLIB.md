# 📦 安装 Matplotlib 指南

## ⚠️ 重要提示

**图形可视化和交互式GUI需要安装matplotlib！**

文本可视化（在终端显示）不需要matplotlib，可以直接使用。

## 🚀 快速安装

### 方法1: 使用pip（推荐）

```bash
pip install matplotlib
```

### 方法2: 使用pip3

```bash
pip3 install matplotlib
```

### 方法3: 使用conda（如果你用Anaconda）

```bash
conda install matplotlib
```

## ✅ 验证安装

安装后，运行以下命令验证：

```bash
python -c "import matplotlib; print('✓ matplotlib 版本:', matplotlib.__version__)"
```

应该看到：
```
✓ matplotlib 版本: 3.x.x
```

## 🎮 安装后可用的功能

### 1. 图形可视化

```bash
python visualize.py "[F, [R, U]]"
```

会显示：
- ✅ 彩色的魔方展开图
- ✅ 图例
- ✅ 统计信息
- ✅ 鼠标悬停提示

### 2. 交互式GUI ✨

```bash
python visualize.py -i
```

功能：
- ✅ 输入公式实时查看效果
- ✅ 撤销/重置按钮
- ✅ 历史记录
- ✅ 鼠标悬停显示块信息

### 3. 图形动画（实验性）

```python
from visualize import *
animate_algorithm_matplotlib("R U R' U'")
```

## 🐛 安装问题排查

### 问题1: pip命令找不到

**解决：**
```bash
# macOS/Linux
python3 -m pip install matplotlib

# Windows
python -m pip install matplotlib
```

### 问题2: 权限错误

**解决：**
```bash
# 用户级安装
pip install --user matplotlib
```

### 问题3: 虚拟环境

如果使用虚拟环境：

```bash
# 激活虚拟环境
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows

# 然后安装
pip install matplotlib
```

### 问题4: 多个Python版本

```bash
# 查看Python版本
python --version
python3 --version

# 使用正确的版本安装
python3.11 -m pip install matplotlib
```

## 📊 不同平台的注意事项

### macOS

通常需要：
```bash
pip3 install matplotlib
```

可能需要安装额外的依赖：
```bash
brew install python-tk  # 如果需要TkAgg后端
```

### Linux (Ubuntu/Debian)

```bash
# 安装matplotlib
pip3 install matplotlib

# 如果需要TkAgg后端
sudo apt-get install python3-tk

# 如果需要Qt后端
pip3 install PyQt5
```

### Windows

```bash
pip install matplotlib
```

通常开箱即用。

## 🧪 安装后测试

### 测试1: 基本导入

```bash
python -c "import matplotlib.pyplot as plt; plt.plot([1,2,3]); print('✓ matplotlib正常')"
```

### 测试2: 悬停测试

```bash
python test_hover.py
```

将鼠标移到蓝色块上，应该显示黄色提示框。

### 测试3: 完整GUI

```bash
python visualize.py -i
```

输入 `F` 并按Enter，查看效果。

## 💡 如果不想安装matplotlib

你仍然可以使用：

### 1. 文本可视化 ✅

```bash
python -c "from visualize import *; visualize_cube_text(apply_algorithm(CubeState(), 'F R U'))"
```

### 2. 命令行交互工具 ✅

```bash
python interactive.py
```

### 3. 核心功能 ✅

```bash
python cube.py
python examples.py
```

这些都**不需要**matplotlib！

## 📝 总结

| 功能 | 需要matplotlib | 备注 |
|------|---------------|------|
| cube.py | ❌ 不需要 | 核心功能 |
| examples.py | ❌ 不需要 | 示例分析 |
| interactive.py | ❌ 不需要 | 命令行交互 |
| test_cube.py | ❌ 不需要 | 单元测试 |
| visualize.py (文本) | ❌ 不需要 | 文本可视化 |
| visualize.py (图形) | ✅ 需要 | 图形可视化 |
| visualize.py -i (GUI) | ✅ 需要 | 交互式GUI |

---

**推荐：安装matplotlib以获得最佳体验！** 🎨

