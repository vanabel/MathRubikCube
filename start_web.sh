#!/bin/bash
# 启动魔方置换群Web应用

echo "🎲 魔方置换群数学模型 - Web应用"
echo "================================"
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python"
    exit 1
fi

# 检查streamlit
if ! python3 -c "import streamlit" 2> /dev/null; then
    echo "📦 正在安装依赖..."
    pip3 install streamlit matplotlib
fi

echo "🚀 启动Web应用..."
echo "💡 浏览器将自动打开 http://localhost:8501"
echo "💡 按 Ctrl+C 停止服务器"
echo ""

streamlit run web_app.py

