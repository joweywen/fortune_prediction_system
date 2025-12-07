"""
性格分析服务
基于Big Five模型和MBTI类型分析
"""

import numpy as np
import random

class PersonalityAnalyzer:
    """性格分析器"""
    
    def __init__(self):
        """初始化分析器"""
        self.big_five_traits = [
            'openness',      # 开放性
            'conscientiousness',  # 尽责性
            'extraversion',  # 外向性
            'agreeableness', # 宜人性
            'neuroticism'    # 神经质
        ]
        
        self.mbti_types = [
            'INTJ', 'INTP', 'ENTJ', 'ENTP',
            'INFJ', 'INFP', 'ENFJ', 'ENFP',
            'ISTJ', 'ISFJ', 'ESTJ', 'ESFJ',
            'ISTP', 'ISFP', 'ESTP', 'ESFP'
        ]
    
    def analyze(self, features):
        """
        分析性格特征
        
        Args:
            features: 图像特征字典
            
        Returns:
            dict: 性格分析结果
        """
        # 计算Big Five得分
        big_five = self._calculate_big_five(features)
        
        # 推断MBTI类型
        mbti = self._infer_mbti(big_five, features)
        
        # 生成性格描述
        description = self._generate_description(big_five, mbti)
        
        # 性格优势
        strengths = self._identify_strengths(big_five, mbti)
        
        # 发展建议
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
        # 基于特征计算（简化版）
        ratio = features.get('face_ratio', 0.85)
        brightness = features.get('brightness', 127) / 255
        contrast = features.get('contrast', 50) / 100
        symmetry = features.get('symmetry', 0.8)
        texture = min(features.get('texture', 100) / 200, 1.0)
        
        # 添加随机变化使结果多样化
        scores = {
            'openness': int(60 + brightness * 30 + random.randint(-5, 5)),
            'conscientiousness': int(55 + symmetry * 35 + random.randint(-5, 5)),
            'extraversion': int(50 + contrast * 40 + random.randint(-5, 5)),
            'agreeableness': int(65 + (1 - texture) * 25 + random.randint(-5, 5)),
            'neuroticism': int(45 + (1 - ratio) * 40 + random.randint(-5, 5))
        }
        
        # 确保分数在0-100范围内
        for key in scores:
            scores[key] = max(0, min(100, scores[key]))
        
        return scores
    
    def _infer_mbti(self, big_five, features):
        """推断MBTI类型"""
        # 基于Big Five推断MBTI
        e_i = 'E' if big_five['extraversion'] > 55 else 'I'
        s_n = 'N' if big_five['openness'] > 55 else 'S'
        t_f = 'T' if big_five['agreeableness'] < 55 else 'F'
        j_p = 'J' if big_five['conscientiousness'] > 55 else 'P'
        
        return e_i + s_n + t_f + j_p
    
    def _generate_description(self, big_five, mbti):
        """生成性格描述"""
        descriptions = {
            'INTJ': '策略家，具有独创性和战略思维，善于规划和执行复杂的计划。',
            'INTP': '逻辑学家，富有创造力的思考者，热衷于探索理论和抽象概念。',
            'ENTJ': '指挥官，天生的领导者，善于组织和激励他人实现目标。',
            'ENTP': '辩论家，聪明且好奇，享受智力挑战和创新思维。',
            'INFJ': '提倡者，理想主义且富有同情心，致力于帮助他人实现潜能。',
            'INFP': '调停者，诗意且善良，总是寻找生活的深层意义。',
            'ENFJ': '主人公，富有魅力的领导者，激励他人共同成长。',
            'ENFP': '竞选者，热情且富有创造力，善于发现新的可能性。',
            'ISTJ': '物流师，实际且负责任，注重细节和传统价值。',
            'ISFJ': '守卫者，温暖且尽职，致力于保护和支持他人。',
            'ESTJ': '总经理，高效的管理者，善于组织和执行计划。',
            'ESFJ': '执政官，关心他人的协调者，营造和谐的氛围。',
            'ISTP': '鉴赏家，大胆且实际，擅长使用工具和技术。',
            'ISFP': '探险家，灵活且迷人，享受当下的美好体验。',
            'ESTP': '企业家，精力充沛且善于把握机会的实干家。',
            'ESFP': '表演者，自发且热情，将快乐带给周围的人。'
        }
        
        base_desc = descriptions.get(mbti, '独特的个性，具有多方面的才能和潜力。')
        
        # 添加Big Five补充描述
        if big_five['openness'] > 70:
            base_desc += '思维开放，富有想象力。'
        if big_five['conscientiousness'] > 70:
            base_desc += '做事严谨，值得信赖。'
        if big_five['extraversion'] > 70:
            base_desc += '性格外向，善于社交。'
        
        return base_desc
    
    def _identify_strengths(self, big_five, mbti):
        """识别性格优势"""
        strengths = []
        
        # 基于Big Five识别优势
        if big_five['openness'] > 65:
            strengths.append('创新思维')
            strengths.append('适应能力强')
        if big_five['conscientiousness'] > 65:
            strengths.append('执行力强')
            strengths.append('注重细节')
        if big_five['extraversion'] > 65:
            strengths.append('沟通能力')
            strengths.append('团队协作')
        if big_five['agreeableness'] > 65:
            strengths.append('同理心')
            strengths.append('人际关系')
        if big_five['neuroticism'] < 40:
            strengths.append('情绪稳定')
            strengths.append('抗压能力')
        
        # 确保至少有3个优势
        if len(strengths) < 3:
            strengths.extend(['问题解决', '学习能力', '责任心'])
        
        return strengths[:5]
    
    def _generate_suggestions(self, big_five, mbti):
        """生成发展建议"""
        suggestions = []
        
        # 基于弱项给出建议
        if big_five['openness'] < 50:
            suggestions.append('尝试接触新事物，培养开放思维')
        if big_five['conscientiousness'] < 50:
            suggestions.append('加强计划性，提升执行效率')
        if big_five['extraversion'] < 50:
            suggestions.append('适度参与社交活动，扩展人脉')
        if big_five['agreeableness'] < 50:
            suggestions.append('多从他人角度考虑，增强同理心')
        if big_five['neuroticism'] > 60:
            suggestions.append('学习压力管理，保持情绪平衡')
        
        # 通用建议
        if len(suggestions) < 3:
            suggestions.extend([
                '持续学习新技能，提升综合能力',
                '保持工作生活平衡，注重身心健康',
                '建立良好的人际关系网络'
            ])
        
        return suggestions[:4]