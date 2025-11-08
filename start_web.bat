@echo off
REM 启动魔方置换群Web应用 (Windows)

echo 🎲 魔方置换群数学模型 - Web应用
echo ================================
echo.

REM 检查Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到Python，请先安装Python
    pause
    exit /b 1
)

REM 检查streamlit
python -c "import streamlit" 2>nul
if %errorlevel% neq 0 (
    echo 📦 正在安装依赖...
    pip install streamlit matplotlib
)

echo 🚀 启动Web应用...
echo 💡 浏览器将自动打开 http://localhost:8501
echo 💡 按 Ctrl+C 停止服务器
echo.

streamlit run web_app.py

pause

