"""
运势分析服务
"""

import random
from datetime import datetime, timedelta

class FortuneAnalyzer:
    """运势分析器"""
    
    def analyze(self, features, personality):
        """分析运势"""
        big_five = personality['bigFive']
        
        # 日运势
        daily = self._generate_daily_fortune(big_five)
        
        # 月运势
        monthly = self._generate_monthly_fortune(big_five)
        
        # 年运势
        yearly = self._generate_yearly_fortune(big_five)
        
        # 幸运元素
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
        yesterday = today - timedelta(days=1)
        tomorrow = today + timedelta(days=1)
        
        base_score = 70
        
        return {
            'yesterday': self._calculate_day_score(base_score - 10),
            'today': self._calculate_day_score(base_score),
            'tomorrow': self._calculate_day_score(base_score + 5),
            'dates': {
                'yesterday': yesterday.strftime('%Y-%m-%d'),
                'today': today.strftime('%Y-%m-%d'),
                'tomorrow': tomorrow.strftime('%Y-%m-%d')
            }
        }
    
    def _generate_monthly_fortune(self, big_five):
        """生成月运势"""
        current_month = datetime.now().month
        months = []
        
        for i in range(-1, 2):
            month = (current_month + i - 1) % 12 + 1
            score = 60 + random.randint(-15, 25)
            score = max(45, min(95, score))
            months.append(score)
        
        return {
            'lastMonth': months[0],
            'current': months[1],
            'nextMonth': months[2]
        }
    
    def _generate_yearly_fortune(self, big_five):
        """生成年运势"""
        current_year = datetime.now().year
        
        last_year = 60 + random.randint(-10, 15)
        this_year = 65 + random.randint(-10, 20)
        next_year = 70 + random.randint(-10, 20)
        
        return {
            'lastYear': max(50, min(95, last_year)),
            'thisYear': max(50, min(95, this_year)),
            'nextYear': max(50, min(95, next_year)),
            'years': {
                'lastYear': current_year - 1,
                'thisYear': current_year,
                'nextYear': current_year + 1
            }
        }
    
    def _calculate_day_score(self, base):
        """计算单日分数"""
        score = base + random.randint(-8, 12)
        return max(40, min(100, score))
    
    def _generate_lucky_elements(self):
        """生成幸运元素"""
        colors = ['红色', '蓝色', '绿色', '紫色', '金色', '银色', '白色']
        numbers = list(range(1, 50))
        directions = ['东方', '南方', '西方', '北方', '东南', '西南', '东北', '西北']
        times = ['早晨6-9点', '上午9-12点', '下午2-5点', '傍晚5-8点']
        
        return {
            'color': random.choice(colors),
            'number': random.choice(numbers),
            'direction': random.choice(directions),
            'time': random.choice(times)
        }