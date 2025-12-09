#!/bin/bash

echo "========================================="
echo "命运预测系统 - 完全修复版启动脚本"
echo "========================================="
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "当前目录: $SCRIPT_DIR"
echo ""

# 检查Python
echo "检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "✗ 未找到Python3"
    exit 1
fi

python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python版本: $python_version"
echo ""

# 删除旧的虚拟环境（如果损坏）
if [ -d "venv" ] && [ ! -f "venv/bin/activate" ]; then
    echo "检测到损坏的虚拟环境，正在删除..."
    rm -rf venv
    echo "✓ 旧环境已删除"
fi

# 创建虚拟环境
echo "设置虚拟环境..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    if [ $? -eq 0 ]; then
        echo "✓ 虚拟环境已创建"
    else
        echo "✗ 虚拟环境创建失败"
        echo "尝试安装 python3-venv:"
        echo "  sudo apt-get install python3-venv"
        exit 1
    fi
else
    echo "✓ 虚拟环境已存在"
fi
echo ""

# 激活虚拟环境
echo "激活虚拟环境..."
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "✓ 虚拟环境已激活"
    echo "Python路径: $(which python3)"
else
    echo "✗ 找不到 venv/bin/activate"
    exit 1
fi
echo ""

# 升级pip
echo "升级pip..."
python3 -m pip install --upgrade pip
echo "✓ pip已升级"
echo ""

# 安装依赖
echo "安装项目依赖（可能需要几分钟）..."
python3 -m pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✓ 依赖安装完成"
else
    echo "✗ 依赖安装失败"
    echo ""
    echo "尝试使用镜像源安装:"
    python3 -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    if [ $? -ne 0 ]; then
        echo "✗ 镜像源安装也失败，请检查网络连接"
        exit 1
    fi
    echo "✓ 使用镜像源安装成功"
fi
echo ""

# 创建必要目录
echo "创建项目目录..."
mkdir -p static/uploads logs backups tests
touch static/uploads/.gitkeep
echo "✓ 目录结构已创建"
echo ""

# 配置环境变量
echo "检查配置文件..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✓ 已创建.env文件"
    else
        echo "⚠ 未找到.env.example，创建默认配置"
        cat > .env << 'ENVEOF'
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production
JWT_SECRET_KEY=dev-jwt-secret-change-in-production
DATABASE_URL=sqlite:///fortune_prediction.db
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216
ENVEOF
        echo "✓ 已创建默认.env文件"
    fi
else
    echo "✓ .env文件已存在"
fi
echo ""

# 初始化数据库
echo "初始化数据库..."
python3 init_db.py
if [ $? -eq 0 ]; then
    echo "✓ 数据库初始化完成"
else
    echo "✗ 数据库初始化失败"
    exit 1
fi
echo ""

# 运行检查
if [ -f "check_project.py" ]; then
    echo "运行项目完整性检查..."
    python3 check_project.py
    echo ""
fi

# 启动应用
echo "========================================="
echo "启动Web服务..."
echo "访问地址: http://localhost:5000"
echo "按 Ctrl+C 停止服务"
echo "========================================="
echo ""

python3 run.py
