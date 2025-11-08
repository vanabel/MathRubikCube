# 📦 如何分享这个项目

有多种方式可以让其他人使用这个魔方模型：

---

## 🌐 方式1：在线Web应用（最推荐！）

### Streamlit Cloud部署（完全免费）

**优点**：
- ✅ 无需用户安装任何东西
- ✅ 直接在浏览器使用
- ✅ 自动更新
- ✅ 完全免费

**步骤**：

1. **推送到GitHub**
   ```bash
   git add .
   git commit -m "Add web app"
   git push origin main
   ```

2. **在Streamlit Cloud部署**
   - 访问 https://streamlit.io/cloud
   - 用GitHub账号登录
   - 点击"New app"
   - 选择仓库：`yourusername/MathRubikCube`
   - 主文件：`web_app.py`
   - 点击"Deploy"

3. **分享链接**
   - 获得类似 `https://mathrubik.streamlit.app` 的链接
   - 分享给任何人！

---

## 💻 方式2：本地安装（适合开发者）

### 一键启动脚本

**macOS/Linux**：
```bash
./start_web.sh
```

**Windows**：
```bash
start_web.bat
```

脚本会自动：
- 检查Python环境
- 安装依赖（如果需要）
- 启动Web服务器
- 打开浏览器

### 手动安装

```bash
# 1. 克隆代码
git clone https://github.com/yourusername/MathRubikCube.git
cd MathRubikCube

# 2. 安装依赖
pip install matplotlib streamlit

# 3. 运行Web应用
streamlit run web_app.py

# 或运行桌面GUI
python visualize.py -i
```

---

## 📱 方式3：在线Notebook（适合教学）

### Google Colab

1. **创建Colab Notebook**
   ```python
   # 第一个单元格：安装依赖
   !git clone https://github.com/yourusername/MathRubikCube.git
   %cd MathRubikCube
   !pip install matplotlib -q
   
   # 第二个单元格：导入和使用
   from cube import *
   from visualize import *
   
   analyze_algorithm("F R U R' U' F'")
   ```

2. **分享Notebook**
   - 文件 → 在GitHub中保存副本
   - 获得链接：`https://colab.research.google.com/github/...`

---

## 🐳 方式4：Docker容器（适合企业）

### 创建Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .
RUN pip install matplotlib streamlit

EXPOSE 8501
CMD ["streamlit", "run", "web_app.py", "--server.address", "0.0.0.0"]
```

### 使用Docker

```bash
# 构建
docker build -t rubik-cube .

# 运行
docker run -p 8501:8501 rubik-cube

# 访问 http://localhost:8501
```

---

## 📦 方式5：PyPI包（适合开源）

将来可以打包发布到PyPI，用户可以：

```bash
pip install rubik-cube-math
```

详见 [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

---

## 🎯 推荐给不同用户

### 给普通用户
→ **Streamlit Cloud在线链接**（无需安装）

### 给学生/教师
→ **Google Colab Notebook**（在线运行）

### 给开发者
→ **GitHub + 本地安装**（完整源码）

### 给企业用户
→ **Docker容器**（标准化部署）

---

## 📋 分发清单

在分享前确认：

- [ ] 代码已推送到GitHub
- [ ] README.md 包含清晰的安装说明
- [ ] requirements.txt 列出所有依赖
- [ ] 添加LICENSE文件
- [ ] 文档完整（docs/目录）
- [ ] 测试全部通过
- [ ] 示例可以运行

---

## 🌟 快速分享步骤

**最快方式（5分钟）**：

1. 推送到GitHub
   ```bash
   git remote add origin https://github.com/yourusername/MathRubikCube.git
   git push -u origin main
   ```

2. 部署到Streamlit Cloud
   - https://streamlit.io/cloud
   - New app → 选择仓库
   - Deploy

3. 分享链接给朋友！
   - `https://yourapp.streamlit.app`

---

**详细部署指南见 [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)**

