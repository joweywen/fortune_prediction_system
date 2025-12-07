"""
数据库初始化脚本
创建所有必要的数据库表
"""

from app import app, db
from models.user import User
from models.prediction import Prediction

def init_database():
    """初始化数据库"""
    with app.app_context():
        print("正在创建数据库表...")
        
        # 创建所有表
        db.create_all()
        
        print("✓ 数据库表创建完成")
        
        # 检查是否有用户
        user_count = User.query.count()
        prediction_count = Prediction.query.count()
        
        print(f"✓ 当前用户数: {user_count}")
        print(f"✓ 当前预测记录数: {prediction_count}")
        
        print("\n数据库初始化完成！")

if __name__ == '__main__':
    init_database()