# 📚 文档索引

本项目包含完整的文档体系，帮助你理解和使用魔方置换群模型。

---

## 🚀 快速开始

### 新手入门（按顺序阅读）

1. **README.md** - 项目总览
   - 项目介绍
   - 功能特性
   - 快速开始

2. **QUICKSTART.md** - 5分钟快速入门
   - 快速上手指南
   - 基本使用示例
   - 常用命令

3. **ENCODING_REFERENCE.md** ⭐ 核心参考
   - 块的位置编码（角块0-7，棱块0-11）
   - 朝向编码（角块0-2，棱块0-1）
   - 所有基本操作的详细效果
   - **必读！理解模型的基础**

---

## 📖 核心概念

### 数学模型

4. **POSITION_VS_ORIENTATION.md** - 位置vs朝向
   - 两个独立维度的解释
   - OLL vs PLL的区别
   - 为什么F操作会影响下层
   - 常见误解澄清

5. **MOVES_REFERENCE.md** - 操作快速参考
   - 18种操作列表
   - 循环分解
   - 12个三循环交换子
   - 常用公式

---

## 🎨 使用指南

### 可视化

6. **VISUALIZATION_GUIDE.md** - 可视化完整指南
   - 三种可视化方式
   - 使用示例
   - API参考
   - 故障排除

7. **INTERACTIVE_GUI_GUIDE.md** - 交互式GUI指南
   - GUI使用方法
   - 鼠标悬停功能
   - 撤销/重置功能
   - 快捷键

---

## 🔧 安装和配置

### 环境设置

8. **INSTALL_MATPLOTLIB.md** - 安装matplotlib
   - 安装步骤
   - 不同平台说明
   - 故障排除
   - 虚拟环境配置

9. **FONT_FIX.md** - 中文字体修复
   - matplotlib中文显示问题
   - 字体配置方法
   - 不同系统的解决方案

---

## 📊 项目信息

### 概览

10. **PROJECT_SUMMARY.md** - 项目总结
    - 完整功能列表
    - 技术亮点
    - 开发路线图
    - 成就总结

11. **LICENSE** - MIT许可证
    - 开源许可

12. **requirements.txt** - 依赖列表
    - Python包依赖

---

## 🎯 按需求查找

### 我想了解...

**基本概念**
- → ENCODING_REFERENCE.md（编码系统）
- → POSITION_VS_ORIENTATION.md（位置vs朝向）

**快速上手**
- → README.md（总览）
- → QUICKSTART.md（5分钟入门）

**操作参考**
- → MOVES_REFERENCE.md（18种操作）
- → ENCODING_REFERENCE.md第五节（基本操作效果）

**可视化**
- → VISUALIZATION_GUIDE.md（完整指南）
- → INTERACTIVE_GUI_GUIDE.md（GUI使用）

**朝向功能**
- → ENCODING_REFERENCE.md第三节（朝向编码）
- → POSITION_VS_ORIENTATION.md（概念解释）

**安装问题**
- → INSTALL_MATPLOTLIB.md（安装matplotlib）
- → FONT_FIX.md（字体问题）

**验证公式**
- → ENCODING_REFERENCE.md第八节（常见公式）
- → 运行 `python verify_formula.py "公式"`

---

## 📝 文档使用建议

### 首次使用

1. 阅读 **README.md** 了解项目
2. 阅读 **ENCODING_REFERENCE.md** 理解编码（⭐重要）
3. 按照 **QUICKSTART.md** 运行示例
4. 阅读 **INTERACTIVE_GUI_GUIDE.md** 使用GUI

### 深入学习

1. **POSITION_VS_ORIENTATION.md** - 理解核心概念
2. **MOVES_REFERENCE.md** - 掌握所有操作
3. **VISUALIZATION_GUIDE.md** - 学会可视化工具

### 问题排查

1. 安装问题 → **INSTALL_MATPLOTLIB.md**
2. 字体问题 → **FONT_FIX.md**
3. 公式验证 → `python verify_formula.py`
4. 理解错误 → **POSITION_VS_ORIENTATION.md**

---

## 🎓 学习路径

### 初级（1-2小时）

- [ ] 阅读 README.md
- [ ] 阅读 ENCODING_REFERENCE.md 第1-2节（位置编码）
- [ ] 运行 `python cube.py`
- [ ] 运行 `python visualize.py -i`
- [ ] 尝试基本操作：F, R, U

### 中级（3-5小时）

- [ ] 阅读 ENCODING_REFERENCE.md 第3-5节（朝向和操作）
- [ ] 阅读 POSITION_VS_ORIENTATION.md
- [ ] 阅读 MOVES_REFERENCE.md
- [ ] 在GUI中测试各种公式
- [ ] 理解交换子和循环

### 高级（5+小时）

- [ ] 阅读所有文档
- [ ] 研究朝向守恒定律
- [ ] 设计自己的公式
- [ ] 阅读源代码
- [ ] 扩展功能

---

## 📂 文档完整列表

### 核心文档（必读）

1. ⭐ **ENCODING_REFERENCE.md** - 编码系统完整参考
2. **README.md** - 项目总览
3. **POSITION_VS_ORIENTATION.md** - 核心概念

### 使用指南

4. **QUICKSTART.md** - 快速入门
5. **INTERACTIVE_GUI_GUIDE.md** - GUI使用
6. **VISUALIZATION_GUIDE.md** - 可视化指南
7. **MOVES_REFERENCE.md** - 操作参考

### 技术文档

8. **INSTALL_MATPLOTLIB.md** - 安装指南
9. **FONT_FIX.md** - 字体修复
10. **PROJECT_SUMMARY.md** - 项目总结

### 配置文件

11. **requirements.txt** - 依赖列表
12. **LICENSE** - 开源许可

---

## 🔗 快速链接

### 在线验证工具

- [Alg Cubing](https://alg.cubing.net/) - 公式3D可视化
- [Ruwix Solver](https://ruwix.com/online-puzzle-simulators/3x3x3-rubiks-cube-solver/) - 在线魔方
- [algdb.net](https://algdb.net/) - 公式数据库

### 推荐阅读顺序

```
1. README.md
      ↓
2. ENCODING_REFERENCE.md (⭐核心)
      ↓
3. QUICKSTART.md
      ↓
4. INTERACTIVE_GUI_GUIDE.md
      ↓
5. POSITION_VS_ORIENTATION.md
      ↓
6. 其他文档按需阅读
```

---

**💡 提示：遇到任何疑问，先查看 ENCODING_REFERENCE.md！**

**最后更新：2025-11-08**

