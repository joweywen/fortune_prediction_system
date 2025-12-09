"""
命运预测系统 - Flask主应用
修复完善版本
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import json
from config import Config

# 创建Flask应用
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# 初始化扩展
db = SQLAlchemy(app)
jwt = JWTManager(app)

# 定义用户模型
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    predictions = db.relationship('Prediction', backref='user', lazy='dynamic', cascade='all, delete-orphan')

# 定义预测模型
class Prediction(db.Model):
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    image_path = db.Column(db.String(500), nullable=False)
    personality_data = db.Column(db.Text)
    career_data = db.Column(db.Text)
    wealth_data = db.Column(db.Text)
    love_data = db.Column(db.Text)
    fortune_data = db.Column(db.Text)
    astrology_data = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

# 导入服务
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

# 文件验证
def allowed_file(filename):
    """检查文件类型是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# API路由
@app.route('/')
def index():
    """首页"""
    return jsonify({
        'name': '命运预测系统',
        'version': '1.0.0',
        'status': 'running'
    })

@app.route('/api/register', methods=['POST'])
def register():
    """用户注册"""
    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        # 验证输入
        if not username or not email or not password:
            return jsonify({'error': '请填写所有字段'}), 400
        
        # 检查用户是否存在
        if User.query.filter_by(username=username).first():
            return jsonify({'error': '用户名已存在'}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({'error': '邮箱已被注册'}), 400
        
        # 创建用户
        hashed_password = generate_password_hash(password)
        user = User(username=username, email=email, password_hash=hashed_password)
        
        db.session.add(user)
        db.session.commit()
        
        # 生成token
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': '注册成功',
            'access_token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'注册失败: {str(e)}'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """用户登录"""
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': '请填写用户名和密码'}), 400
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({'error': '用户名或密码错误'}), 401
        
        # 更新最后登录时间
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': '登录成功',
            'access_token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'登录失败: {str(e)}'}), 500

@app.route('/api/upload', methods=['POST'])
@jwt_required()
def upload_and_analyze():
    """上传文件并分析"""
    try:
        user_id = get_jwt_identity()
        
        if 'file' not in request.files:
            return jsonify({'error': '未上传文件'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': '文件名为空'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': '不支持的文件格式'}), 400
        
        # 保存文件
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{user_id}_{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # 提取特征
        features = image_processor.extract_features(filepath)
        
        # 多维度分析
        personality = personality_analyzer.analyze(features)
        career = career_predictor.predict(features, personality)
        wealth = wealth_predictor.predict(features, personality, career)
        love = love_analyzer.analyze(features, personality)
        fortune = fortune_analyzer.analyze(features, personality)
        astrology = astrology_analyzer.analyze(features)
        
        # 生成建议
        daily_advice = generate_daily_advice(fortune, personality)
        monthly_advice = generate_monthly_advice(fortune, wealth, love)
        yearly_advice = generate_yearly_advice(career, wealth, love)
        
        # 保存预测结果
        prediction = Prediction(
            user_id=user_id,
            image_path=filepath,
            personality_data=json.dumps(personality, ensure_ascii=False),
            career_data=json.dumps(career, ensure_ascii=False),
            wealth_data=json.dumps(wealth, ensure_ascii=False),
            love_data=json.dumps(love, ensure_ascii=False),
            fortune_data=json.dumps(fortune, ensure_ascii=False),
            astrology_data=json.dumps(astrology, ensure_ascii=False)
        )
        
        db.session.add(prediction)
        db.session.commit()
        
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
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'分析失败: {str(e)}'}), 500

@app.route('/api/predictions', methods=['GET'])
@jwt_required()
def get_predictions():
    """获取用户的所有预测记录"""
    try:
        user_id = get_jwt_identity()
        predictions = Prediction.query.filter_by(user_id=user_id).order_by(
            Prediction.created_at.desc()
        ).all()
        
        results = []
        for pred in predictions:
            fortune_data = json.loads(pred.fortune_data) if pred.fortune_data else {}
            results.append({
                'id': pred.id,
                'created_at': pred.created_at.isoformat(),
                'fortune_summary': fortune_data.get('daily', {})
            })
        
        return jsonify({'predictions': results}), 200
        
    except Exception as e:
        return jsonify({'error': f'获取记录失败: {str(e)}'}), 500

@app.route('/api/prediction/<int:prediction_id>', methods=['GET'])
@jwt_required()
def get_prediction_detail(prediction_id):
    """获取预测详情"""
    try:
        user_id = get_jwt_identity()
        prediction = Prediction.query.filter_by(
            id=prediction_id, 
            user_id=user_id
        ).first()
        
        if not prediction:
            return jsonify({'error': '预测记录不存在'}), 404
        
        return jsonify({
            'id': prediction.id,
            'created_at': prediction.created_at.isoformat(),
            'personality': json.loads(prediction.personality_data) if prediction.personality_data else {},
            'career': json.loads(prediction.career_data) if prediction.career_data else {},
            'wealth': json.loads(prediction.wealth_data) if prediction.wealth_data else {},
            'love': json.loads(prediction.love_data) if prediction.love_data else {},
            'fortune': json.loads(prediction.fortune_data) if prediction.fortune_data else {},
            'astrology': json.loads(prediction.astrology_data) if prediction.astrology_data else {}
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'获取详情失败: {str(e)}'}), 500

@app.route('/api/dashboard/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    """获取仪表盘统计"""
    try:
        user_id = get_jwt_identity()
        latest_prediction = Prediction.query.filter_by(user_id=user_id).order_by(
            Prediction.created_at.desc()
        ).first()
        
        if not latest_prediction:
            return jsonify({'error': '暂无预测数据'}), 404
        
        fortune_data = json.loads(latest_prediction.fortune_data) if latest_prediction.fortune_data else {}
        wealth_data = json.loads(latest_prediction.wealth_data) if latest_prediction.wealth_data else {}
        love_data = json.loads(latest_prediction.love_data) if latest_prediction.love_data else {}
        career_data = json.loads(latest_prediction.career_data) if latest_prediction.career_data else {}
        
        return jsonify({
            'daily': fortune_data.get('daily', {}),
            'monthly': fortune_data.get('monthly', {}),
            'yearly': fortune_data.get('yearly', {}),
            'wealth_trend': wealth_data.get('accumulationTrend', []),
            'love_score': love_data.get('stabilityScore', 0),
            'career_fields': career_data.get('bestFields', [])
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'获取统计失败: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({'status': 'healthy'}), 200

# 辅助函数
def generate_daily_advice(fortune, personality):
    """生成今日建议"""
    score = fortune.get('daily', {}).get('today', 70)
    mbti = personality.get('mbti', 'INFP')
    
    advice = f"今日运势指数{score}分。"
    
    if score >= 80:
        advice += "今天是行动的好日子，适合推进重要计划。"
    elif score >= 60:
        advice += "今天整体运势平稳，稳步推进即可。"
    else:
        advice += "今天宜静不宜动，专注内在提升。"
    
    if mbti[0] == 'E':
        advice += "多与他人交流会带来好运。"
    else:
        advice += "独处思考会帮助你获得灵感。"
    
    return advice

def generate_monthly_advice(fortune, wealth, love):
    """生成本月建议"""
    fortune_score = fortune.get('monthly', {}).get('current', 70)
    wealth_score = wealth.get('current_trend', 70)
    love_score = love.get('stabilityScore', 70)
    
    advice = f"本月综合运势{fortune_score}分。"
    
    if wealth_score >= 70:
        advice += "财运亨通，可考虑适度投资。"
    
    if love_score >= 70:
        advice += "感情稳定，深化关系的好时机。"
    else:
        advice += "感情需要更多关注和沟通。"
    
    return advice

def generate_yearly_advice(career, wealth, love):
    """生成今年建议"""
    career_rate = career.get('successRate', 70)
    peak_year = wealth.get('peakYear', 2030)
    
    advice = f"今年职业成功率预测为{career_rate}%。"
    
    if career_rate >= 75:
        advice += "是事业发展的关键年份。"
    
    advice += f"财富峰值预计在{peak_year}年。"
    advice += "平衡工作与生活，注重身心健康。"
    
    return advice

# 错误处理
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': '资源未找到'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': '服务器内部错误'}), 500

# 主程序
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("数据库初始化完成")
    
    print("=" * 50)
    print("命运预测系统启动")
    print("访问地址: http://localhost:5000")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)