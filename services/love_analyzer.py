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
