"""
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
