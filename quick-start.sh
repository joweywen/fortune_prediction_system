#!/bin/bash

echo "========================================="
echo "命运预测系统 - 快速启动脚本"
echo "========================================="
echo ""

# 检查Python版本
echo "检查Python版本..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python版本: $python_version"

if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python 3.9+"
    exit 1
fi

# 创建虚拟环境
echo ""
echo "创建虚拟环境..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ 虚拟环境创建完成"
else
    echo "✓ 虚拟环境已存在"
fi

# 激活虚拟环境
echo ""
echo "激活虚拟环境..."
source venv/bin/activate
echo "✓ 虚拟环境已激活"

# 升级pip
echo ""
echo "升级pip..."
pip install --upgrade pip -q
echo "✓ pip升级完成"

# 安装依赖
echo ""
echo "安装项目依赖..."
pip install -r requirements.txt -q
echo "✓ 依赖安装完成"

# 创建必要目录
echo ""
echo "创建必要目录..."
mkdir -p static/uploads logs backups
touch static/uploads/.gitkeep
echo "✓ 目录结构创建完成"

# 检查配置文件
echo ""
echo "检查配置文件..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✓ 已从.env.example创建.env文件"
        echo "⚠ 请编辑.env文件，设置密钥等配置"
    else
        echo "⚠ 未找到.env.example文件"
    fi
else
    echo "✓ .env文件已存在"
fi

# 初始化数据库
echo ""
echo "初始化数据库..."
python3 init_db.py
echo "✓ 数据库初始化完成"

# 启动应用
echo ""
echo "========================================="
echo "准备启动应用..."
echo "访问地址: http://localhost:5000"
echo "按 Ctrl+C 停止服务"
echo "========================================="
echo ""

# 询问是否立即启动
read -p "是否立即启动应用? (Y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
    python3 run.py
else
    echo ""
    echo "准备完成！运行以下命令启动应用:"
    echo "  source venv/bin/activate"
    echo "  python3 run.py"
    echo ""
fi