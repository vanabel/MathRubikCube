# 🚀 部署与分发指南

本文档说明如何分发和部署魔方置换群数学模型。

---

## 📦 方案1：本地使用（最简单）

### 给其他用户

**步骤1：分享代码**
```bash
# 克隆或下载代码
git clone https://github.com/yourusername/MathRubikCube.git
cd MathRubikCube
```

**步骤2：安装依赖**
```bash
# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install matplotlib
```

**步骤3：运行**
```bash
# 方式1：交互式GUI
python visualize.py -i

# 方式2：命令行分析
python -c "from cube import *; analyze_algorithm('F R U R\\' U\\' F\\'')"

# 方式3：交互式命令行
python interactive.py
```

---

## 🌐 方案2：Web应用（Streamlit）

### 本地运行Web界面

**步骤1：安装Streamlit**
```bash
pip install streamlit matplotlib
```

**步骤2：启动Web应用**
```bash
streamlit run web_app.py
```

**步骤3：访问**
- 浏览器自动打开 http://localhost:8501
- 或手动访问上述地址

### 部署到云端（免费）

#### 选项A：Streamlit Cloud（推荐）

1. **准备GitHub仓库**
   ```bash
   git add .
   git commit -m "Add web app"
   git push origin main
   ```

2. **部署到Streamlit Cloud**
   - 访问 https://streamlit.io/cloud
   - 登录并连接GitHub
   - 选择仓库和分支
   - 主文件：`web_app.py`
   - 点击"Deploy"

3. **分享链接**
   - 获得类似 `https://yourapp.streamlit.app` 的链接
   - 任何人都可以访问！

#### 选项B：Hugging Face Spaces

1. **创建Space**
   - 访问 https://huggingface.co/spaces
   - 创建新Space，选择Streamlit
   
2. **上传文件**
   - 上传所有`.py`文件
   - 上传`requirements.txt`
   - 创建`README.md`

3. **配置**
   ```yaml
   # 创建 .streamlit/config.toml
   [server]
   headless = true
   port = 7860
   ```

4. **访问**
   - 获得 `https://huggingface.co/spaces/username/appname`

---

## 🐳 方案3：Docker容器

### 创建Dockerfile

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir matplotlib streamlit

# 复制代码
COPY . .

# 暴露端口
EXPOSE 8501

# 启动命令
CMD ["streamlit", "run", "web_app.py", "--server.address", "0.0.0.0"]
```

### 构建和运行

```bash
# 构建镜像
docker build -t rubik-cube-app .

# 运行容器
docker run -p 8501:8501 rubik-cube-app

# 访问
# http://localhost:8501
```

### 分发Docker镜像

```bash
# 推送到Docker Hub
docker tag rubik-cube-app username/rubik-cube-app
docker push username/rubik-cube-app

# 其他用户使用
docker pull username/rubik-cube-app
docker run -p 8501:8501 username/rubik-cube-app
```

---

## 📦 方案4：PyPI包（高级）

### 创建包结构

```
MathRubikCube/
├── setup.py
├── rubik_cube/
│   ├── __init__.py
│   ├── cube.py
│   ├── visualize.py
│   └── ...
└── README.md
```

### setup.py示例

```python
from setuptools import setup, find_packages

setup(
    name="rubik-cube-math",
    version="1.0.0",
    description="魔方置换群数学模型",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "matplotlib>=3.3.0",
    ],
    extras_require={
        "web": ["streamlit>=1.28.0"],
    },
    entry_points={
        "console_scripts": [
            "rubik-gui=rubik_cube.visualize:interactive_cube_gui",
        ],
    },
)
```

### 发布到PyPI

```bash
# 安装工具
pip install build twine

# 构建
python -m build

# 上传
twine upload dist/*
```

### 用户安装

```bash
# 基础版
pip install rubik-cube-math

# 包含Web界面
pip install rubik-cube-math[web]

# 使用
python -m rubik_cube.visualize -i
# 或
rubik-gui
```

---

## 📱 方案5：Jupyter Notebook

### 创建交互式Notebook

```python
# notebook/demo.ipynb
from cube import *
from visualize import *
import ipywidgets as widgets

# 创建交互控件
formula_input = widgets.Text(
    description='公式:',
    placeholder='F R U R\' U\' F\''
)

output = widgets.Output()

def on_apply(b):
    with output:
        output.clear_output()
        state = apply_algorithm(CubeState(), formula_input.value)
        visualize_cube_matplotlib(state)

button = widgets.Button(description="应用")
button.on_click(on_apply)

display(formula_input, button, output)
```

### 分享方式

1. **GitHub + Binder**
   - 添加 `requirements.txt`
   - 推送到GitHub
   - 访问 https://mybinder.org
   - 输入仓库地址
   - 生成可交互链接！

2. **Google Colab**
   - 上传到GitHub
   - 访问 `https://colab.research.google.com/github/username/repo/blob/main/demo.ipynb`

---

## 🌟 推荐方案对比

| 方案 | 难度 | 用户友好度 | 适用场景 |
|------|------|------------|---------|
| **本地使用** | ⭐ | ⭐⭐ | 开发者、学习者 |
| **Streamlit Cloud** | ⭐⭐ | ⭐⭐⭐⭐⭐ | **通用推荐** |
| **Docker** | ⭐⭐⭐ | ⭐⭐⭐ | 企业部署 |
| **PyPI包** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 开源项目 |
| **Jupyter** | ⭐⭐ | ⭐⭐⭐⭐ | 教学、演示 |

---

## 🎯 快速开始推荐

### 对于普通用户
```bash
# 1. 下载代码
git clone <repo-url>
cd MathRubikCube

# 2. 安装依赖
pip install matplotlib streamlit

# 3. 启动Web界面
streamlit run web_app.py
```

### 对于开发者
```bash
# 1. 克隆仓库
git clone <repo-url>
cd MathRubikCube

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行GUI
python visualize.py -i
```

---

## 📚 相关资源

- **Streamlit文档**: https://docs.streamlit.io
- **Docker文档**: https://docs.docker.com
- **PyPI指南**: https://packaging.python.org
- **Binder**: https://mybinder.org

---

## 💡 提示

1. **Streamlit Cloud**是最简单的分享方式，完全免费
2. **GitHub Pages**不适合这个项目（需要后端Python）
3. 确保`requirements.txt`包含所有依赖
4. 添加`.gitignore`忽略`venv/`和`__pycache__/`
5. 为公开分发添加适当的LICENSE文件

---

**最后更新：2025-11-08**

