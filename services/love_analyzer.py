"""
感情分析服务
"""

import random

class LoveAnalyzer:
    """感情分析器"""
    
    def __init__(self):
        self.mbti_compatibility = {
            'INTJ': ['ENFP', 'ENTP', 'INFJ'],
            'INTP': ['ENTJ', 'ESTJ', 'INFJ'],
            'ENTJ': ['INTP', 'INFP', 'ENFP'],
            'ENTP': ['INTJ', 'INFJ', 'ENFJ'],
            'INFJ': ['ENFP', 'ENTP', 'INTJ'],
            'INFP': ['ENFJ', 'ENTJ', 'INFJ'],
            'ENFJ': ['INFP', 'ISFP', 'INTP'],
            'ENFP': ['INTJ', 'INFJ', 'ENTJ'],
            'ISTJ': ['ESTP', 'ESFP', 'ISFJ'],
            'ISFJ': ['ESFP', 'ESTP', 'ISTJ'],
            'ESTJ': ['ISTP', 'INTP', 'ISFP'],
            'ESFJ': ['ISFP', 'ISTP', 'ESFP'],
            'ISTP': ['ESTJ', 'ESFJ', 'ESTP'],
            'ISFP': ['ESFJ', 'ENFJ', 'ESTJ'],
            'ESTP': ['ISTJ', 'ISFJ', 'ISTP'],
            'ESFP': ['ISTJ', 'ISFJ', 'ESFJ']
        }
    
    def analyze(self, features, personality):
        """分析感情状况"""
        big_five = personality['bigFive']
        mbti = personality['mbti']
        
        # 感情稳定性评分
        stability_score = self._calculate_stability(big_five)
        
        # 最佳匹配类型
        best_matches = self._get_best_matches(mbti)
        
        # 感情趋势
        love_trend = self._generate_love_trend(big_five)
        
        # 感情建议
        relationship_advice = self._generate_advice(big_five, mbti)
        
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
        base += (big_five['conscientiousness'] - 50) * 0.3
        base += (50 - big_five['neuroticism']) * 0.3
        base += random.randint(-5, 5)
        return int(max(40, min(95, base)))
    
    def _get_best_matches(self, mbti):
        """获取最佳匹配类型"""
        return self.mbti_compatibility.get(mbti, ['ENFP', 'INFJ', 'ENTJ'])
    
    def _generate_love_trend(self, big_five):
        """生成感情趋势"""
        months = ['本月', '下月', '第三月', '第四月', '第五月', '第六月']
        trend = []
        base_score = 65
        
        for i, month in enumerate(months):
            score = base_score + random.randint(-10, 15)
            score = max(50, min(95, score))
            trend.append({
                'month': month,
                'score': score
            })
        
        return trend
    
    def _generate_advice(self, big_five, mbti):
        """生成感情建议"""
        advice = []
        
        if big_five['extraversion'] < 50:
            advice.append('多参与社交活动，扩展交友圈')
        
        if big_five['agreeableness'] < 55:
            advice.append('学会换位思考，理解对方需求')
        
        if big_five['neuroticism'] > 65:
            advice.append('保持情绪稳定，增强安全感')
        
        if big_five['openness'] > 70:
            advice.append('寻找志同道合的伴侣')
        
        advice.append('保持真诚沟通，建立信任')
        advice.append('给予彼此适当的个人空间')
        
        return advice[:4]
    
    def _calculate_attractiveness(self, big_five):
        """计算吸引力指数"""
        score = 50
        score += (big_five['extraversion'] - 50) * 0.3
        score += (big_five['agreeableness'] - 50) * 0.3
        score += (big_five['openness'] - 50) * 0.2
        score += (50 - big_five['neuroticism']) * 0.2
        return int(max(40, min(95, score)))