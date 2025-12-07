
"""
预测数据模型
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

class Prediction(db.Model):
    """预测模型"""
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    image_path = db.Column(db.String(500), nullable=False)
    
    # JSON存储各类预测数据
    personality_data = db.Column(db.Text)  # 性格分析
    career_data = db.Column(db.Text)  # 职业预测
    wealth_data = db.Column(db.Text)  # 财富预测
    love_data = db.Column(db.Text)  # 感情分析
    fortune_data = db.Column(db.Text)  # 运势分析
    astrology_data = db.Column(db.Text)  # 玄学分析
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<Prediction {self.id}>'
    
    @property
    def personality_dict(self):
        return json.loads(self.personality_data) if self.personality_data else {}
    
    @property
    def career_dict(self):
        return json.loads(self.career_data) if self.career_data else {}
    
    @property
    def wealth_dict(self):
        return json.loads(self.wealth_data) if self.wealth_data else {}
    
    @property
    def love_dict(self):
        return json.loads(self.love_data) if self.love_data else {}
    
    @property
    def fortune_dict(self):
        return json.loads(self.fortune_data) if self.fortune_data else {}
    
    @property
    def astrology_dict(self):
        return json.loads(self.astrology_data) if self.astrology_data else {}
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'personality': self.personality_dict,
            'career': self.career_dict,
            'wealth': self.wealth_dict,
            'love': self.love_dict,
            'fortune': self.fortune_dict,
            'astrology': self.astrology_dict
        }