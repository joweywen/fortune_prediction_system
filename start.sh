#!/bin/bash

echo "================================"
echo "命运预测系统启动脚本"
echo "================================"

# 激活虚拟环境
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✓ 虚拟环境已激活"
else
    echo "✗ 虚拟环境不存在，请先创建"
    exit 1
fi

# 检查依赖
echo "检查依赖包..."
pip install -q -r requirements.txt
echo "✓ 依赖包检查完成"

# 创建必要目录
mkdir -p logs
mkdir -p static/uploads
mkdir -p backups
echo "✓ 目录结构检查完成"

# 数据库迁移
echo "检查数据库..."
python init_db.py
echo "✓ 数据库就绪"

# 启动Celery (后台)
echo "启动后台任务..."
celery -A celery_app.celery worker --loglevel=info --detach
celery -A celery_app.celery beat --loglevel=info --detach
echo "✓ 后台任务启动完成"

# 启动Flask应用
echo "================================"
echo "启动Web服务..."
echo "访问地址: http://localhost:5000"
echo "================================"

if [ "$1" == "prod" ]; then
    # 生产环境
    gunicorn -c gunicorn_config.py app:app
else
    # 开发环境
    python run.py
fi
