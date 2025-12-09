"""预测数据模型"""
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
    personality_data = db.Column(db.Text)
    career_data = db.Column(db.Text)
    wealth_data = db.Column(db.Text)
    love_data = db.Column(db.Text)
    fortune_data = db.Column(db.Text)
    astrology_data = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # 关系
    user = db.relationship('User', backref=db.backref('predictions', lazy='dynamic'))
    
    def __repr__(self):
        return f'<Prediction {self.id}>'
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'personality': json.loads(self.personality_data) if self.personality_data else {},
            'career': json.loads(self.career_data) if self.career_data else {},
            'wealth': json.loads(self.wealth_data) if self.wealth_data else {},
            'love': json.loads(self.love_data) if self.love_data else {},
            'fortune': json.loads(self.fortune_data) if self.fortune_data else {},
            'astrology': json.loads(self.astrology_data) if self.astrology_data else {}
        }
