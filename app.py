from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

db = SQLAlchemy(app)
jwt = JWTManager(app)

# 导入模型和服务
from models.user import User
from models.prediction import Prediction
from services.personality_analyzer import PersonalityAnalyzer
from services.career_predictor import CareerPredictor
from services.wealth_predictor import WealthPredictor
from services.love_analyzer import LoveAnalyzer
from services.fortune_analyzer import FortuneAnalyzer
from services.astrology_analyzer import AstrologyAnalyzer
from services.image_processor import ImageProcessor

# 初始化服务
personality_analyzer = PersonalityAnalyzer()
career_predictor = CareerPredictor()
wealth_predictor = WealthPredictor()
love_analyzer = LoveAnalyzer()
fortune_analyzer = FortuneAnalyzer()
astrology_analyzer = AstrologyAnalyzer()
image_processor = ImageProcessor()

@app.route('/api/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if User.query.filter_by(username=username).first():
        return jsonify({'error': '用户名已存在'}), 400
    
    hashed_password = generate_password_hash(password)
    user = User(username=username, email=email, password_hash=hashed_password)
    
    db.session.add(user)
    db.session.commit()
    
    access_token = create_access_token(identity=user.id)
    return jsonify({
        'message': '注册成功',
        'access_token': access_token,
        'user': {'id': user.id, 'username': user.username, 'email': user.email}
    }), 201

@app.route('/api/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': '用户名或密码错误'}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify({
        'message': '登录成功',
        'access_token': access_token,
        'user': {'id': user.id, 'username': user.username, 'email': user.email}
    }), 200

@app.route('/api/upload', methods=['POST'])
@jwt_required()
def upload_and_analyze():
    """上传照片/视频并进行分析"""
    user_id = get_jwt_identity()
    
    if 'file' not in request.files:
        return jsonify({'error': '未上传文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '文件名为空'}), 400
    
    # 保存文件
    filename = f"{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # 图像处理和特征提取
    features = image_processor.extract_features(filepath)
    
    # 多维度分析
    personality = personality_analyzer.analyze(features)
    career = career_predictor.predict(features, personality)
    wealth = wealth_predictor.predict(features, personality, career)
    love = love_analyzer.analyze(features, personality)
    fortune = fortune_analyzer.analyze(features, personality)
    astrology = astrology_analyzer.analyze(features)
    
    # 保存预测结果
    prediction = Prediction(
        user_id=user_id,
        image_path=filepath,
        personality_data=personality,
        career_data=career,
        wealth_data=wealth,
        love_data=love,
        fortune_data=fortune,
        astrology_data=astrology,
        created_at=datetime.utcnow()
    )
    
    db.session.add(prediction)
    db.session.commit()
    
    # 生成综合建议
    daily_advice = generate_daily_advice(fortune, personality)
    monthly_advice = generate_monthly_advice(fortune, wealth, love)
    yearly_advice = generate_yearly_advice(career, wealth, love)
    
    return jsonify({
        'prediction_id': prediction.id,
        'personality': personality,
        'career': career,
        'wealth': wealth,
        'love': love,
        'fortune': fortune,
        'astrology': astrology,
        'advice': {
            'daily': daily_advice,
            'monthly': monthly_advice,
            'yearly': yearly_advice
        }
    }), 200

@app.route('/api/predictions', methods=['GET'])
@jwt_required()
def get_predictions():
    """获取用户的所有预测记录"""
    user_id = get_jwt_identity()
    predictions = Prediction.query.filter_by(user_id=user_id).order_by(Prediction.created_at.desc()).all()
    
    results = []
    for pred in predictions:
        results.append({
            'id': pred.id,
            'created_at': pred.created_at.isoformat(),
            'fortune_summary': {
                'daily': pred.fortune_data['daily'],
                'monthly': pred.fortune_data['monthly'],
                'yearly': pred.fortune_data['yearly']
            }
        })
    
    return jsonify({'predictions': results}), 200

@app.route('/api/prediction/<int:prediction_id>', methods=['GET'])
@jwt_required()
def get_prediction_detail(prediction_id):
    """获取特定预测的详细信息"""
    user_id = get_jwt_identity()
    prediction = Prediction.query.filter_by(id=prediction_id, user_id=user_id).first()
    
    if not prediction:
        return jsonify({'error': '预测记录不存在'}), 404
    
    return jsonify({
        'id': prediction.id,
        'created_at': prediction.created_at.isoformat(),
        'personality': prediction.personality_data,
        'career': prediction.career_data,
        'wealth': prediction.wealth_data,
        'love': prediction.love_data,
        'fortune': prediction.fortune_data,
        'astrology': prediction.astrology_data
    }), 200

def generate_daily_advice(fortune, personality):
    """生成今日建议"""
    score = fortune['daily']['today']
    mbti = personality['mbti']
    
    advice = f"今日运势指数{score}分。"
    
    if score >= 80:
        advice += "今天是行动的好日子，适合推进重要计划和决策。"
    elif score >= 60:
        advice += "今天整体运势平稳，适合稳步推进日常事务。"
    else:
        advice += "今天宜静不宜动，专注于内在提升和反思。"
    
    if mbti.startswith('E'):
        advice += "多与他人交流会带来好运。"
    else:
        advice += "独处思考会帮助你获得灵感。"
    
    return advice

def generate_monthly_advice(fortune, wealth, love):
    """生成本月建议"""
    fortune_score = fortune['monthly']['current']
    wealth_score = wealth['current_trend']
    love_score = love['stabilityScore']
    
    advice = f"本月综合运势{fortune_score}分。"
    
    if wealth_score >= 70:
        advice += "财运亨通，可考虑适度投资。"
    
    if love_score >= 70:
        advice += "感情稳定，是深化关系的好时机。"
    else:
        advice += "感情需要更多关注和沟通。"
    
    return advice

def generate_yearly_advice(career, wealth, love):
    """生成今年建议"""
    career_rate = career['successRate']
    
    advice = f"今年职业成功率预测为{career_rate}%。"
    
    if career_rate >= 75:
        advice += "是事业发展的关键年份，把握机遇积极进取。"
    
    advice += f"财富积累预计在{wealth['peakYear']}年达到峰值。"
    advice += "整体运势向好，建议平衡工作与生活，注重身心健康。"
    
    return advice

@app.route('/api/dashboard/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    """获取仪表盘统计数据"""
    user_id = get_jwt_identity()
    latest_prediction = Prediction.query.filter_by(user_id=user_id).order_by(Prediction.created_at.desc()).first()
    
    if not latest_prediction:
        return jsonify({'error': '暂无预测数据'}), 404
    
    return jsonify({
        'daily': latest_prediction.fortune_data['daily'],
        'monthly': latest_prediction.fortune_data['monthly'],
        'yearly': latest_prediction.fortune_data['yearly'],
        'wealth_trend': latest_prediction.wealth_data['accumulationTrend'],
        'love_score': latest_prediction.love_data['stabilityScore'],
        'career_fields': latest_prediction.career_data['bestFields']
    }), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)