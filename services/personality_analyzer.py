"""
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
