@echo off
echo ================================
echo 命运预测系统启动脚本
echo ================================

REM 激活虚拟环境
if exist venv\ (
    call venv\Scripts\activate
    echo √ 虚拟环境已激活
) else (
    echo × 虚拟环境不存在，请先创建
    pause
    exit /b 1
)

REM 检查依赖
echo 检查依赖包...
pip install -q -r requirements.txt
echo √ 依赖包检查完成

REM 创建必要目录
if not exist logs mkdir logs
if not exist static\uploads mkdir static\uploads
if not exist backups mkdir backups
echo √ 目录结构检查完成

REM 数据库初始化
echo 检查数据库...
python init_db.py
echo √ 数据库就绪

REM 启动Flask应用
echo ================================
echo 启动Web服务...
echo 访问地址: http://localhost:5000
echo ================================
python run.py

pause