#!/usr/bin/env python3
"""
自动创建所有缺失的服务文件
运行: python3 create_services.py
"""

import os

# 确保 services 目录存在
os.makedirs('services', exist_ok=True)

# 1. services/__init__.py
print("创建 services/__init__.py...")
with open('services/__init__.py', 'w', encoding='utf-8') as f:
    f.write('''"""
业务逻辑服务包
"""

from services.personality_analyzer import PersonalityAnalyzer
from services.career_predictor import CareerPredictor
from services.wealth_predictor import WealthPredictor
from services.love_analyzer import LoveAnalyzer
from services.fortune_analyzer import FortuneAnalyzer
from services.astrology_analyzer import AstrologyAnalyzer
from services.image_processor import ImageProcessor

__all__ = [
    'PersonalityAnalyzer',
    'CareerPredictor',
    'WealthPredictor',
    'LoveAnalyzer',
    'FortuneAnalyzer',
    'AstrologyAnalyzer',
    'ImageProcessor'
]
''')

# 2. services/image_processor.py
print("创建 services/image_processor.py...")
with open('services/image_processor.py', 'w', encoding='utf-8') as f:
    f.write('''"""
图像处理服务
"""

import cv2
import numpy as np
import os

class ImageProcessor:
    """图像处理器"""
    
    def __init__(self):
        """初始化处理器"""
        try:
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self.face_cascade = cv2.CascadeClassifier(cascade_path)
        except:
            self.face_cascade = None
    
    def extract_features(self, image_path):
        """提取图像特征"""
        try:
            img = cv2.imread(image_path)
            if img is None:
                return self._generate_default_features()
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            if self.face_cascade is not None:
                faces = self.face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))
                
                if len(faces) > 0:
                    x, y, w, h = faces[0]
                    face_roi = gray[y:y+h, x:x+w]
                    return self._extract_face_features(face_roi, img)
            
            return self._generate_default_features()
            
        except Exception as e:
            print(f"图像处理错误: {e}")
            return self._generate_default_features()
    
    def _extract_face_features(self, face_roi, original_img):
        """提取人脸特征"""
        h, w = face_roi.shape
        face_ratio = w / h if h > 0 else 1.0
        brightness = np.mean(face_roi)
        contrast = np.std(face_roi)
        
        try:
            laplacian = cv2.Laplacian(face_roi, cv2.CV_64F)
            texture = np.var(laplacian)
        except:
            texture = 100.0
        
        try:
            left_half = face_roi[:, :w//2]
            right_half = cv2.flip(face_roi[:, w//2:], 1)
            min_width = min(left_half.shape[1], right_half.shape[1])
            symmetry = np.corrcoef(
                left_half[:, :min_width].flatten(),
                right_half[:, :min_width].flatten()
            )[0, 1]
        except:
            symmetry = 0.8
        
        try:
            edges = cv2.Canny(face_roi, 100, 200)
            edge_density = np.sum(edges > 0) / (h * w)
        except:
            edge_density = 0.15
        
        return {
            'face_ratio': float(face_ratio),
            'brightness': float(brightness),
            'contrast': float(contrast),
            'texture': float(texture),
            'symmetry': float(symmetry),
            'edge_density': float(edge_density),
            'face_width': int(w),
            'face_height': int(h)
        }
    
    def _generate_default_features(self):
        """生成默认特征"""
        return {
            'face_ratio': 0.85,
            'brightness': 127.0,
            'contrast': 50.0,
            'texture': 100.0,
            'symmetry': 0.8,
            'edge_density': 0.15,
            'face_width': 200,
            'face_height': 235
        }
''')

# 3. services/personality_analyzer.py
print("创建 services/personality_analyzer.py...")
with open('services/personality_analyzer.py', 'w', encoding='utf-8') as f:
    f.write('''"""
性格分析服务
"""

import random

class PersonalityAnalyzer:
    """性格分析器"""
    
    def __init__(self):
        self.mbti_types = [
            'INTJ', 'INTP', 'ENTJ', 'ENTP',
            'INFJ', 'INFP', 'ENFJ', 'ENFP',
            'ISTJ', 'ISFJ', 'ESTJ', 'ESFJ',
            'ISTP', 'ISFP', 'ESTP', 'ESFP'
        ]
    
    def analyze(self, features):
        """分析性格特征"""
        big_five = self._calculate_big_five(features)
        mbti = self._infer_mbti(big_five, features)
        description = self._generate_description(big_five, mbti)
        strengths = self._identify_strengths(big_five, mbti)
        suggestions = self._generate_suggestions(big_five, mbti)
        
        return {
            'bigFive': big_five,
            'mbti': mbti,
            'description': description,
            'strengths': strengths,
            'suggestions': suggestions
        }
    
    def _calculate_big_five(self, features):
        """计算Big Five得分"""
        ratio = features.get('face_ratio', 0.85)
        brightness = features.get('brightness', 127) / 255
        contrast = features.get('contrast', 50) / 100
        symmetry = features.get('symmetry', 0.8)
        texture = min(features.get('texture', 100) / 200, 1.0)
        
        scores = {
            'openness': int(60 + brightness * 30 + random.randint(-5, 5)),
            'conscientiousness': int(55 + symmetry * 35 + random.randint(-5, 5)),
            'extraversion': int(50 + contrast * 40 + random.randint(-5, 5)),
            'agreeableness': int(65 + (1 - texture) * 25 + random.randint(-5, 5)),
            'neuroticism': int(45 + (1 - ratio) * 40 + random.randint(-5, 5))
        }
        
        for key in scores:
            scores[key] = max(0, min(100, scores[key]))
        
        return scores
    
    def _infer_mbti(self, big_five, features):
        """推断MBTI类型"""
        e_i = 'E' if big_five['extraversion'] > 55 else 'I'
        s_n = 'N' if big_five['openness'] > 55 else 'S'
        t_f = 'T' if big_five['agreeableness'] < 55 else 'F'
        j_p = 'J' if big_five['conscientiousness'] > 55 else 'P'
        return e_i + s_n + t_f + j_p
    
    def _generate_description(self, big_five, mbti):
        """生成性格描述"""
        descriptions = {
            'INTJ': '策略家，具有独创性和战略思维。',
            'INTP': '逻辑学家，富有创造力的思考者。',
            'ENTJ': '指挥官，天生的领导者。',
            'ENTP': '辩论家，聪明且好奇。',
            'INFJ': '提倡者，理想主义且富有同情心。',
            'INFP': '调停者，诗意且善良。',
            'ENFJ': '主人公，富有魅力的领导者。',
            'ENFP': '竞选者，热情且富有创造力。',
            'ISTJ': '物流师，实际且负责任。',
            'ISFJ': '守卫者，温暖且尽职。',
            'ESTJ': '总经理，高效的管理者。',
            'ESFJ': '执政官，关心他人的协调者。',
            'ISTP': '鉴赏家，大胆且实际。',
            'ISFP': '探险家，灵活且迷人。',
            'ESTP': '企业家，精力充沛。',
            'ESFP': '表演者，自发且热情。'
        }
        return descriptions.get(mbti, '独特的个性。')
    
    def _identify_strengths(self, big_five, mbti):
        """识别性格优势"""
        strengths = []
        if big_five['openness'] > 65:
            strengths.extend(['创新思维', '适应能力强'])
        if big_five['conscientiousness'] > 65:
            strengths.extend(['执行力强', '注重细节'])
        if big_five['extraversion'] > 65:
            strengths.extend(['沟通能力', '团队协作'])
        if len(strengths) < 3:
            strengths.extend(['问题解决', '学习能力'])
        return strengths[:5]
    
    def _generate_suggestions(self, big_five, mbti):
        """生成发展建议"""
        suggestions = []
        if big_five['openness'] < 50:
            suggestions.append('尝试接触新事物')
        if big_five['conscientiousness'] < 50:
            suggestions.append('加强计划性')
        if len(suggestions) < 3:
            suggestions.extend(['持续学习新技能', '保持工作生活平衡'])
        return suggestions[:4]
''')

# 4. services/career_predictor.py
print("创建 services/career_predictor.py...")
with open('services/career_predictor.py', 'w', encoding='utf-8') as f:
    f.write('''"""
职业预测服务
"""

import random

class CareerPredictor:
    """职业预测器"""
    
    def __init__(self):
        self.career_fields = {
            'INTJ': ['战略规划', '系统架构', '科研开发'],
            'INTP': ['数据科学', '研究分析', '软件开发'],
            'ENTJ': ['企业管理', '项目管理', '战略咨询'],
            'ENTP': ['创新顾问', '市场策略', '产品经理'],
        }
    
    def predict(self, features, personality):
        """预测职业发展"""
        mbti = personality['mbti']
        big_five = personality['bigFive']
        
        best_fields = self.career_fields.get(mbti, ['综合管理', '专业咨询'])
        success_rate = self._calculate_success_rate(big_five)
        career_trend = self._generate_career_trend(big_five)
        promotion_timeline = self._predict_promotion(big_five, success_rate)
        career_advice = ['持续学习提升技能', '建立职场人际关系']
        
        return {
            'bestFields': best_fields,
            'successRate': success_rate,
            'careerTrend': career_trend,
            'promotionTimeline': promotion_timeline,
            'advice': career_advice
        }
    
    def _calculate_success_rate(self, big_five):
        """计算职业成功率"""
        base_rate = 50
        base_rate += (big_five['conscientiousness'] - 50) * 0.4
        base_rate += (big_five['extraversion'] - 50) * 0.2
        base_rate += random.randint(-5, 10)
        return int(max(40, min(95, base_rate)))
    
    def _generate_career_trend(self, big_five):
        """生成职业发展趋势"""
        trend = []
        for i in range(5):
            trend.append({
                'year': 2025 + i,
                'score': 60 + i * 5 + random.randint(-3, 5)
            })
        return trend
    
    def _predict_promotion(self, big_five, success_rate):
        """预测晋升时间线"""
        return [
            {'position': '资深专员', 'years': 2, 'probability': 85},
            {'position': '主管', 'years': 4, 'probability': 75},
            {'position': '经理', 'years': 6, 'probability': 65}
        ]
''')

# 5. services/wealth_predictor.py
print("创建 services/wealth_predictor.py...")
with open('services/wealth_predictor.py', 'w', encoding='utf-8') as f:
    f.write('''"""
财富预测服务
"""

import random
from datetime import datetime

class WealthPredictor:
    """财富预测器"""
    
    def predict(self, features, personality, career):
        """预测财富趋势"""
        big_five = personality['bigFive']
        success_rate = career['successRate']
        
        current_trend = self._calculate_current_trend(big_five, success_rate)
        accumulation_trend = self._generate_accumulation_trend(big_five, success_rate)
        investment_advice = self._generate_investment_advice(big_five)
        peak_year = self._predict_peak_year(big_five, success_rate)
        
        return {
            'current_trend': current_trend,
            'accumulationTrend': accumulation_trend,
            'investmentAdvice': investment_advice,
            'peakYear': peak_year,
            'riskTolerance': self._calculate_risk_tolerance(big_five)
        }
    
    def _calculate_current_trend(self, big_five, success_rate):
        """计算当前财富趋势分数"""
        base = 55
        base += (big_five['conscientiousness'] - 50) * 0.3
        base += (success_rate - 50) * 0.4
        base += random.randint(-5, 10)
        return int(max(40, min(95, base)))
    
    def _generate_accumulation_trend(self, big_five, success_rate):
        """生成财富积累趋势"""
        current_year = datetime.now().year
        trend = []
        for i in range(10):
            trend.append({
                'year': current_year + i,
                'score': 50 + i * 4 + random.randint(-2, 5)
            })
        return trend
    
    def _generate_investment_advice(self, big_five):
        """生成投资建议"""
        advice = []
        if big_five['openness'] > 65:
            advice.append('可考虑创新型投资')
        if big_five['conscientiousness'] > 70:
            advice.append('适合长期价值投资')
        else:
            advice.append('建议建立理财规划')
        advice.append('保持应急储备金')
        return advice
    
    def _predict_peak_year(self, big_five, success_rate):
        """预测财富峰值年份"""
        return datetime.now().year + 15 + random.randint(-2, 3)
    
    def _calculate_risk_tolerance(self, big_five):
        """计算风险承受能力"""
        tolerance = 50
        tolerance += (big_five['openness'] - 50) * 0.3
        tolerance += (50 - big_five['neuroticism']) * 0.5
        return max(20, min(90, int(tolerance)))
''')

# 6. services/love_analyzer.py
print("创建 services/love_analyzer.py...")
with open('services/love_analyzer.py', 'w', encoding='utf-8') as f:
    f.write('''"""
感情分析服务
"""

import random

class LoveAnalyzer:
    """感情分析器"""
    
    def __init__(self):
        self.mbti_compatibility = {
            'INTJ': ['ENFP', 'ENTP', 'INFJ'],
            'INTP': ['ENTJ', 'ESTJ', 'INFJ'],
        }
    
    def analyze(self, features, personality):
        """分析感情状况"""
        big_five = personality['bigFive']
        mbti = personality['mbti']
        
        stability_score = self._calculate_stability(big_five)
        best_matches = self.mbti_compatibility.get(mbti, ['ENFP', 'INFJ', 'ENTJ'])
        love_trend = self._generate_love_trend(big_five)
        relationship_advice = ['保持真诚沟通', '给予彼此空间']
        
        return {
            'stabilityScore': stability_score,
            'bestMatches': best_matches,
            'loveTrend': love_trend,
            'advice': relationship_advice,
            'attractiveness': self._calculate_attractiveness(big_five)
        }
    
    def _calculate_stability(self, big_five):
        """计算感情稳定性"""
        base = 60
        base += (big_five['agreeableness'] - 50) * 0.4
        base += (50 - big_five['neuroticism']) * 0.3
        base += random.randint(-5, 5)
        return int(max(40, min(95, base)))
    
    def _generate_love_trend(self, big_five):
        """生成感情趋势"""
        months = ['本月', '下月', '第三月', '第四月', '第五月', '第六月']
        return [{'month': m, 'score': 65 + random.randint(-10, 15)} for m in months]
    
    def _calculate_attractiveness(self, big_five):
        """计算吸引力指数"""
        score = 50
        score += (big_five['extraversion'] - 50) * 0.3
        score += (big_five['agreeableness'] - 50) * 0.3
        return int(max(40, min(95, score)))
''')

# 7. services/fortune_analyzer.py
print("创建 services/fortune_analyzer.py...")
with open('services/fortune_analyzer.py', 'w', encoding='utf-8') as f:
    f.write('''"""
运势分析服务
"""

import random
from datetime import datetime, timedelta

class FortuneAnalyzer:
    """运势分析器"""
    
    def analyze(self, features, personality):
        """分析运势"""
        big_five = personality['bigFive']
        
        daily = self._generate_daily_fortune(big_five)
        monthly = self._generate_monthly_fortune(big_five)
        yearly = self._generate_yearly_fortune(big_five)
        lucky_elements = self._generate_lucky_elements()
        
        return {
            'daily': daily,
            'monthly': monthly,
            'yearly': yearly,
            'luckyElements': lucky_elements
        }
    
    def _generate_daily_fortune(self, big_five):
        """生成日运势"""
        today = datetime.now()
        return {
            'yesterday': 70 + random.randint(-10, 10),
            'today': 75 + random.randint(-10, 15),
            'tomorrow': 72 + random.randint(-10, 12),
            'dates': {
                'yesterday': (today - timedelta(days=1)).strftime('%Y-%m-%d'),
                'today': today.strftime('%Y-%m-%d'),
                'tomorrow': (today + timedelta(days=1)).strftime('%Y-%m-%d')
            }
        }
    
    def _generate_monthly_fortune(self, big_five):
        """生成月运势"""
        return {
            'lastMonth': 60 + random.randint(-10, 15),
            'current': 70 + random.randint(-10, 20),
            'nextMonth': 72 + random.randint(-10, 18)
        }
    
    def _generate_yearly_fortune(self, big_five):
        """生成年运势"""
        current_year = datetime.now().year
        return {
            'lastYear': 65 + random.randint(-10, 15),
            'thisYear': 72 + random.randint(-10, 20),
            'nextYear': 75 + random.randint(-10, 20),
            'years': {
                'lastYear': current_year - 1,
                'thisYear': current_year,
                'nextYear': current_year + 1
            }
        }
    
    def _generate_lucky_elements(self):
        """生成幸运元素"""
        colors = ['红色', '蓝色', '绿色', '紫色', '金色']
        directions = ['东方', '南方', '西方', '北方']
        times = ['早晨6-9点', '上午9-12点', '下午2-5点']
        
        return {
            'color': random.choice(colors),
            'number': random.randint(1, 49),
            'direction': random.choice(directions),
            'time': random.choice(times)
        }
''')

# 8. services/astrology_analyzer.py
print("创建 services/astrology_analyzer.py...")
with open('services/astrology_analyzer.py', 'w', encoding='utf-8') as f:
    f.write('''"""
玄学分析服务
"""

import random

class AstrologyAnalyzer:
    """玄学分析器"""
    
    def __init__(self):
        self.zodiac_signs = ['白羊座', '金牛座', '双子座', '巨蟹座', '狮子座', '处女座',
                            '天秤座', '天蝎座', '射手座', '摩羯座', '水瓶座', '双鱼座']
        self.elements = ['金', '木', '水', '火', '土']
    
    def analyze(self, features):
        """玄学分析"""
        zodiac = self._generate_zodiac_analysis()
        bazi = self._generate_bazi_analysis()
        wuxing = self._generate_wuxing_analysis()
        suggestions = self._generate_mystical_suggestions()
        
        return {
            'zodiac': zodiac,
            'bazi': bazi,
            'wuxing': wuxing,
            'suggestions': suggestions
        }
    
    def _generate_zodiac_analysis(self):
        """生成星座分析"""
        sun_sign = random.choice(self.zodiac_signs)
        moon_sign = random.choice(self.zodiac_signs)
        rising_sign = random.choice(self.zodiac_signs)
        
        return {
            'sunSign': sun_sign,
            'moonSign': moon_sign,
            'risingSign': rising_sign,
            'description': f'太阳{sun_sign}，月亮{moon_sign}，上升{rising_sign}。'
        }
    
    def _generate_bazi_analysis(self):
        """生成八字分析"""
        stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        
        return {
            'yearPillar': random.choice(stems) + random.choice(branches),
            'monthPillar': random.choice(stems) + random.choice(branches),
            'dayPillar': random.choice(stems) + random.choice(branches),
            'hourPillar': random.choice(stems) + random.choice(branches),
            'description': '四柱配置平衡，命格稳健。'
        }
    
    def _generate_wuxing_analysis(self):
        """生成五行分析"""
        scores = {element: random.randint(50, 95) for element in self.elements}
        strongest = max(scores, key=scores.get)
        weakest = min(scores, key=scores.get)
        
        return {
            'scores': scores,
            'strongest': strongest,
            'weakest': weakest,
            'favorableElement': weakest,
            'description': f'五行以{strongest}为旺，建议补{weakest}。'
        }
    
    def _generate_mystical_suggestions(self):
        """生成开运建议"""
        return {
            'luckyColor': random.choice(['红色', '金色', '绿色', '蓝色']),
            'luckyStone': random.choice(['水晶', '玛瑙', '翡翠', '琥珀']),
            'luckyDirection': random.choice(['东方', '南方', '西方', '北方']),
            'luckyNumber': random.randint(1, 9),
            'advice': ['多接触自然', '保持积极心态', '定期冥想']
        }
''')

print("\n✓ 所有服务文件创建完成！")
print("\n现在可以运行:")
print("  python3 init_db.py")
print("  python3 run.py")