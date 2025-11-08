# 🔧 中文字体显示修复说明

## 问题描述

使用matplotlib显示中文时出现警告：
```
UserWarning: Glyph XXXXX missing from font(s) DejaVu Sans.
```

## 已修复内容

✅ 在 `visualize.py` 中添加了中文字体支持配置：

```python
# 配置中文字体支持
matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'STSong', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
```

## 字体优先级

程序会按以下顺序尝试使用字体：

1. **Arial Unicode MS** - macOS 系统自带，完美支持中文
2. **SimHei** (黑体) - Windows/Linux 常见中文字体
3. **STSong** (宋体) - 另一个常见中文字体
4. **DejaVu Sans** - 默认备用字体

## 验证修复

运行可视化程序：

```bash
python visualize.py "R U R' U'"
```

现在应该：
- ✅ 不再出现字体警告（或大幅减少）
- ✅ 中文字符正常显示
- ✅ 图例、标题、标签都能正确显示

## 如果仍有警告

### 方案1：安装推荐字体

**macOS:**
- Arial Unicode MS 已内置
- 如需其他字体：`brew install font-wqy-microhei`

**Ubuntu/Debian:**
```bash
sudo apt-get install fonts-wqy-microhei fonts-wqy-zenhei
```

**Windows:**
- SimHei/STSong 通常已内置
- 确保在控制面板中已安装中文字体

### 方案2：查看可用字体

```python
from matplotlib.font_manager import FontManager
import matplotlib.pyplot as plt

fm = FontManager()
# 查找所有包含"中文"、"SimHei"等的字体
fonts = [f.name for f in fm.ttflist if 'Arial' in f.name or 'Sim' in f.name or 'ST' in f.name]
print("可用的中文字体:", set(fonts))
```

### 方案3：手动指定字体

如果你知道系统中某个支持中文的字体，可以修改 `visualize.py`：

```python
# 修改这一行，添加你系统中的字体名称
matplotlib.rcParams['font.sans-serif'] = ['你的字体名称', 'Arial Unicode MS', 'SimHei']
```

### 方案4：抑制警告（不推荐）

如果只是想隐藏警告而不影响功能：

```python
import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')
```

## 常见字体名称参考

| 系统 | 推荐字体 | 字体名称 |
|------|---------|---------|
| macOS | Arial Unicode MS | `'Arial Unicode MS'` |
| macOS | 苹方 | `'PingFang SC'` |
| Windows | 黑体 | `'SimHei'` |
| Windows | 宋体 | `'SimSun'` |
| Linux | 文泉驿微米黑 | `'WenQuanYi Micro Hei'` |
| Linux | 文泉驿正黑 | `'WenQuanYi Zen Hei'` |

## 测试中文显示

运行以下命令测试：

```python
from visualize import *
import matplotlib.pyplot as plt

# 测试中文显示
fig, ax = plt.subplots()
ax.text(0.5, 0.5, '魔方置换群', fontsize=20, ha='center')
ax.set_title('中文测试')
plt.show()
```

如果中文能正常显示，说明配置成功！

## 补充说明

- 警告不影响程序功能，只是提示字体不包含某些字符
- 即使有警告，matplotlib也会用方框或其他字符代替
- 本次修复已经设置了多个备用字体，大多数系统都能正常显示

---

**✅ 修复已完成！现在可以正常使用可视化功能了。**

