"""
API接口测试
"""

import unittest
import json
import os
import sys
from io import BytesIO

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db, User, Prediction

class FortuneAPITestCase(unittest.TestCase):
    """API测试用例"""
    
    def setUp(self):
        """测试前设置"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        """测试后清理"""
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_index(self):
        """测试首页"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('name', data)
        self.assertEqual(data['status'], 'running')
    
    def test_register(self):
        """测试用户注册"""
        response = self.app.post('/api/register',
            data=json.dumps({
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('access_token', data)
        self.assertEqual(data['user']['username'], 'testuser')
    
    def test_register_duplicate_username(self):
        """测试重复用户名注册"""
        # 第一次注册
        self.app.post('/api/register',
            data=json.dumps({
                'username': 'testuser',
                'email': 'test1@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        # 第二次注册相同用户名
        response = self.app.post('/api/register',
            data=json.dumps({
                'username': 'testuser',
                'email': 'test2@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_login(self):
        """测试用户登录"""
        # 先注册
        self.app.post('/api/register',
            data=json.dumps({
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        # 登录
        response = self.app.post('/api/login',
            data=json.dumps({
                'username': 'testuser',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('access_token', data)
    
    def test_login_wrong_password(self):
        """测试错误密码登录"""
        # 先注册
        self.app.post('/api/register',
            data=json.dumps({
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        # 错误密码登录
        response = self.app.post('/api/login',
            data=json.dumps({
                'username': 'testuser',
                'password': 'wrongpassword'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 401)
    
    def test_upload_no_token(self):
        """测试无token上传"""
        response = self.app.post('/api/upload')
        self.assertEqual(response.status_code, 401)
    
    def test_predictions_no_token(self):
        """测试无token获取预测列表"""
        response = self.app.get('/api/predictions')
        self.assertEqual(response.status_code, 401)
    
    def test_health_check(self):
        """测试健康检查"""
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    def get_auth_token(self):
        """获取认证token"""
        response = self.app.post('/api/register',
            data=json.dumps({
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        data = json.loads(response.data)
        return data['access_token']
    
    def test_dashboard_stats_no_data(self):
        """测试无数据时的仪表盘"""
        token = self.get_auth_token()
        response = self.app.get('/api/dashboard/stats',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_prediction_detail_not_found(self):
        """测试不存在的预测详情"""
        token = self.get_auth_token()
        response = self.app.get('/api/prediction/999',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        self.assertEqual(response.status_code, 404)

class ServiceTestCase(unittest.TestCase):
    """服务模块测试"""
    
    def test_personality_analyzer(self):
        """测试性格分析器"""
        from services.personality_analyzer import PersonalityAnalyzer
        
        analyzer = PersonalityAnalyzer()
        features = {
            'face_ratio': 0.85,
            'brightness': 127,
            'contrast': 50,
            'texture': 100,
            'symmetry': 0.8,
            'edge_density': 0.15
        }
        
        result = analyzer.analyze(features)
        
        self.assertIn('bigFive', result)
        self.assertIn('mbti', result)
        self.assertIn('description', result)
        self.assertIn('strengths', result)
        self.assertIn('suggestions', result)
        
        # 检查Big Five分数范围
        for trait, score in result['bigFive'].items():
            self.assertGreaterEqual(score, 0)
            self.assertLessEqual(score, 100)
    
    def test_career_predictor(self):
        """测试职业预测器"""
        from services.career_predictor import CareerPredictor
        
        predictor = CareerPredictor()
        personality = {
            'mbti': 'INTJ',
            'bigFive': {
                'openness': 75,
                'conscientiousness': 80,
                'extraversion': 50,
                'agreeableness': 60,
                'neuroticism': 40
            }
        }
        features = {}
        
        result = predictor.predict(features, personality)
        
        self.assertIn('bestFields', result)
        self.assertIn('successRate', result)
        self.assertIn('careerTrend', result)
        self.assertIn('advice', result)
        
        # 检查成功率范围
        self.assertGreaterEqual(result['successRate'], 0)
        self.assertLessEqual(result['successRate'], 100)
    
    def test_fortune_analyzer(self):
        """测试运势分析器"""
        from services.fortune_analyzer import FortuneAnalyzer
        
        analyzer = FortuneAnalyzer()
        personality = {
            'bigFive': {
                'openness': 70,
                'conscientiousness': 75,
                'extraversion': 60,
                'agreeableness': 65,
                'neuroticism': 45
            }
        }
        features = {}
        
        result = analyzer.analyze(features, personality)
        
        self.assertIn('daily', result)
        self.assertIn('monthly', result)
        self.assertIn('yearly', result)
        self.assertIn('luckyElements', result)
        
        # 检查日运势
        daily = result['daily']
        self.assertIn('today', daily)
        self.assertIn('yesterday', daily)
        self.assertIn('tomorrow', daily)

class ImageProcessorTestCase(unittest.TestCase):
    """图像处理测试"""
    
    def test_generate_default_features(self):
        """测试默认特征生成"""
        from services.image_processor import ImageProcessor
        
        processor = ImageProcessor()
        features = processor._generate_default_features()
        
        self.assertIn('face_ratio', features)
        self.assertIn('brightness', features)
        self.assertIn('contrast', features)
        self.assertIn('texture', features)
        self.assertIn('symmetry', features)
        self.assertIn('edge_density', features)

if __name__ == '__main__':
    unittest.main()