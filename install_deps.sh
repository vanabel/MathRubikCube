#!/bin/bash

echo "======================================================================"
echo "🚀 安装项目依赖"
echo "======================================================================"

# 检查是否在项目目录
if [ ! -f "cube.py" ]; then
    echo "❌ 请在项目根目录运行此脚本"
    exit 1
fi

# 检查venv是否存在
if [ -d "venv" ]; then
    echo "✓ 发现虚拟环境: venv"
    
    # 激活虚拟环境
    echo "激活虚拟环境..."
    source venv/bin/activate
    
    # 显示Python信息
    echo ""
    echo "Python信息:"
    echo "  路径: $(which python)"
    echo "  版本: $(python --version)"
    
    # 检查matplotlib是否已安装
    echo ""
    echo "检查matplotlib..."
    if python -c "import matplotlib" 2>/dev/null; then
        VERSION=$(python -c "import matplotlib; print(matplotlib.__version__)")
        echo "  ✓ matplotlib已安装，版本: $VERSION"
    else
        echo "  ✗ matplotlib未安装"
        echo ""
        echo "正在安装matplotlib..."
        pip install matplotlib
        
        if [ $? -eq 0 ]; then
            echo "  ✓ matplotlib安装成功！"
        else
            echo "  ✗ matplotlib安装失败"
            exit 1
        fi
    fi
    
    # 验证安装
    echo ""
    echo "======================================================================"
    echo "验证安装"
    echo "======================================================================"
    
    python -c "
import matplotlib
import matplotlib.pyplot as plt
print('✓ matplotlib 版本:', matplotlib.__version__)
print('✓ 后端:', matplotlib.get_backend())
print('✓ 安装成功！')
"
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "======================================================================"
        echo "✅ 安装完成！"
        echo "======================================================================"
        echo ""
        echo "现在你可以使用："
        echo "  1. 图形可视化:"
        echo "     python visualize.py \"[F, [R, U]]\""
        echo ""
        echo "  2. 交互式GUI:"
        echo "     python visualize.py -i"
        echo ""
        echo "  3. 测试悬停:"
        echo "     python test_hover.py"
        echo ""
        echo "记得先激活虚拟环境:"
        echo "     source venv/bin/activate"
        echo "======================================================================"
    else
        echo "❌ 验证失败"
        exit 1
    fi
    
else
    echo "❌ 未找到虚拟环境 venv"
    echo ""
    echo "创建虚拟环境："
    echo "  python3 -m venv venv"
    echo ""
    echo "然后重新运行此脚本："
    echo "  bash install_deps.sh"
    exit 1
fi

