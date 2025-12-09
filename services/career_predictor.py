"""
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
