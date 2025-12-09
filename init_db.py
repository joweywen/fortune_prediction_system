"""数据库初始化脚本"""
from app import app, db

def init_database():
    """初始化数据库"""
    with app.app_context():
        print("正在创建数据库表...")
        
        # 删除所有表（如果存在）
        db.drop_all()
        
        # 创建所有表
        db.create_all()
        
        print("✓ 数据库表创建完成")
        print("\n数据库初始化完成！")

if __name__ == '__main__':
    init_database()
