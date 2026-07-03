#!/bin/bash
# 启动魔方置换群Web应用
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

if [ -x "$SCRIPT_DIR/venv/bin/python" ]; then
    PYTHON="$SCRIPT_DIR/venv/bin/python"
    STREAMLIT="$SCRIPT_DIR/venv/bin/streamlit"
    PIP="$SCRIPT_DIR/venv/bin/pip"
else
    PYTHON="python3"
    STREAMLIT="streamlit"
    PIP="pip3"
fi

export MPLCONFIGDIR="$SCRIPT_DIR/.cache/matplotlib"
mkdir -p "$MPLCONFIGDIR"

echo "🎲 魔方置换群数学模型 - Web应用"
echo "================================"
echo ""

# 检查Python
if ! command -v "$PYTHON" &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python"
    exit 1
fi

# 检查streamlit
if ! "$PYTHON" -c "import streamlit" 2> /dev/null; then
    echo "📦 正在安装依赖..."
    "$PIP" install streamlit matplotlib
fi

echo "🚀 启动Web应用..."
echo "💡 浏览器将自动打开 http://localhost:8501"
echo "💡 按 Ctrl+C 停止服务器"
echo ""

"$STREAMLIT" run web_app.py
