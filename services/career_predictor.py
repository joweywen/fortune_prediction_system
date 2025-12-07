"""
职业预测服务
基于性格特征预测职业发展
"""

import random

class CareerPredictor:
    """职业预测器"""
    
    def __init__(self):
        """初始化预测器"""
        self.career_fields = {
            'INTJ': ['战略规划', '系统架构', '科研开发', '管理咨询'],
            'INTP': ['数据科学', '研究分析', '软件开发', '理论研究'],
            'ENTJ': ['企业管理', '项目管理', '战略咨询', '创业'],
            'ENTP': ['创新顾问', '市场策略', '产品经理', '商业开发'],
            'INFJ': ['心理咨询', '教育培训', '人力资源', '社会工作'],
            'INFP': ['创意写作', '艺术设计', '辅导咨询', '非营利组织'],
            'ENFJ': ['培训师', '公关传播', '人才发展', '团队建设'],
            'ENFP': ['市场营销', '品牌策划', '创意产业', '活动策划'],
            'ISTJ': ['财务审计', '质量管理', '行政管理', '法律合规'],
            'ISFJ': ['护理保健', '客户服务', '行政支持', '教育辅导'],
            'ESTJ': ['运营管理', '销售管理', '生产管理', '物流管理'],
            'ESFJ': ['客户关系', '人力资源', '活动协调', '零售管理'],
            'ISTP': ['技术维修', '工程设计', '数据分析', '应急处理'],
            'ISFP': ['艺术创作', '美容美发', '烹饪艺术', '摄影设计'],
            'ESTP': ['销售业务', '危机处理', '体育竞技', '创业投资'],
            'ESFP': ['表演艺术', '活动主持', '娱乐产业', '销售推广']
        }
    
    def predict(self, features, personality):
        """
        预测职业发展
        
        Args:
            features: 图像特征
            personality: 性格分析结果
            
        Returns:
            dict: 职业预测结果
        """
        mbti = personality['mbti']
        big_five = personality['bigFive']
        
        # 最适合的职业领域
        best_fields = self._get_best_fields(mbti)
        
        # 职业成功率
        success_rate = self._calculate_success_rate(big_five)
        
        # 职业发展趋势
        career_trend = self._generate_career_trend(big_five)
        
        # 晋升预测
        promotion_timeline = self._predict_promotion(big_five, success_rate)
        
        # 职业建议
        career_advice = self._generate_career_advice(mbti, big_five)
        
        return {
            'bestFields': best_fields,
            'successRate': success_rate,
            'careerTrend': career_trend,
            'promotionTimeline': promotion_timeline,
            'advice': career_advice
        }
    
    def _get_best_fields(self, mbti):
        """获取最适合的职业领域"""
        return self.career_fields.get(mbti, ['综合管理', '专业咨询', '技术开发', '创意产业'])
    
    def _calculate_success_rate(self, big_five):
        """计算职业成功率"""
        # 综合考虑各项特质
        base_rate = 50
        
        # 尽责性影响最大
        base_rate += (big_five['conscientiousness'] - 50) * 0.4
        
        # 外向性
        base_rate += (big_five['extraversion'] - 50) * 0.2
        
        # 开放性
        base_rate += (big_five['openness'] - 50) * 0.2
        
        # 情绪稳定性
        base_rate += (50 - big_five['neuroticism']) * 0.2
        
        # 添加随机因素
        base_rate += random.randint(-5, 10)
        
        return int(max(40, min(95, base_rate)))
    
    def _generate_career_trend(self, big_five):
        """生成职业发展趋势"""
        current_year = 2025
        trend = []
        
        base_score = 60
        growth_rate = (big_five['conscientiousness'] + big_five['openness']) / 200
        
        for i in range(5):
            year = current_year + i
            score = int(base_score + i * 6 * growth_rate + random.randint(-3, 5))
            score = max(50, min(95, score))
            
            trend.append({
                'year': year,
                'score': score,
                'description': self._get_trend_description(score)
            })
        
        return trend
    
    def _get_trend_description(self, score):
        """获取趋势描述"""
        if score >= 85:
            return '事业巅峰期，把握机遇'
        elif score >= 75:
            return '稳步上升，发展顺利'
        elif score >= 65:
            return '平稳发展，积累经验'
        else:
            return '调整期，蓄势待发'
    
    def _predict_promotion(self, big_five, success_rate):
        """预测晋升时间线"""
        base_years = 3
        
        # 根据成功率调整
        if success_rate >= 80:
            base_years = 2
        elif success_rate < 60:
            base_years = 4
        
        timeline = [
            {
                'position': '资深专员',
                'years': base_years,
                'probability': min(95, success_rate + 15)
            },
            {
                'position': '主管/经理',
                'years': base_years + 2,
                'probability': min(90, success_rate + 5)
            },
            {
                'position': '高级经理',
                'years': base_years + 4,
                'probability': success_rate
            },
            {
                'position': '总监',
                'years': base_years + 7,
                'probability': max(40, success_rate - 15)
            }
        ]
        
        return timeline
    
    def _generate_career_advice(self, mbti, big_five):
        """生成职业建议"""
        advice = []
        
        # 基于MBTI的建议
        if mbti[0] == 'I':
            advice.append('发挥深度思考优势，在专业领域深耕')
        else:
            advice.append('利用社交优势，扩展职业网络')
        
        if mbti[1] == 'N':
            advice.append('关注创新机会，把握未来趋势')
        else:
            advice.append('注重实践经验，稳扎稳打发展')
        
        # 基于Big Five的建议
        if big_five['conscientiousness'] < 60:
            advice.append('提升计划性和执行力')
        
        if big_five['openness'] > 70:
            advice.append('寻找创新型项目和挑战')
        
        advice.append('持续学习提升专业技能')
        advice.append('建立良好的职场人际关系')
        
        return advice[:5]