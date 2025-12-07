
"""
命运预测系统 - 启动文件
运行此文件启动Flask应用
"""

from app import app
import os

if __name__ == '__main__':
    # 确保必要的目录存在
    os.makedirs('static/uploads', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    os.makedirs('backups', exist_ok=True)
    
    # 启动应用
    print("=" * 50)
    print("命运预测系统启动中...")
    print("访问地址: http://localhost:5000")
    print("=" * 50)
    
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        threaded=True
    )