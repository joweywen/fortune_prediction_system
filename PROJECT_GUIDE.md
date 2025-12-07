# 命运预测系统 - 完整项目指南

## 📋 项目概述

这是一个基于Python Flask + React的全栈命运预测系统，通过分析用户上传的照片/视频，提供多维度的性格分析和命运预测。

### 核心功能

✅ **科学分析模块**
- 性格分析 (Big Five + MBTI)
- 职业预测与发展建议
- 财富积累趋势分析
- 感情稳定性评估
- 运势趋势预测

✅ **玄学分析模块**
- 星座分析（太阳/月亮/上升）
- 八字命理分析
- 五行强弱评估
- 开运建议

✅ **数据可视化**
- 多维度图表展示
- 日/月/年运势对比
- 交互式数据查询

## 🚀 快速开始

### 方式1: 使用快速启动脚本（推荐）

```bash
# 克隆项目
git clone https://github.com/joweywen/fortune_prediction_system.git
cd fortune_prediction_system

# 赋予执行权限
chmod +x quick-start.sh

# 运行快速启动
./quick-start.sh
```

### 方式2: 手动安装

```bash
# 1. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 创建必要目录
mkdir -p static/uploads logs backups

# 4. 配置环境变量
cp .env.example .env
# 编辑.env文件，设置密钥

# 5. 初始化数据库
python init_db.py

# 6. 启动应用
python run.py
```

## 📁 项目结构

```
fortune_prediction_system/
├── app.py                      # Flask主应用
├── run.py                      # 启动入口
├── config.py                   # 配置文件
├── init_db.py                  # 数据库初始化
├── requirements.txt            # Python依赖
├── .env.example               # 环境变量模板
├── models/                     # 数据模型
│   ├── __init__.py
│   ├── user.py                # 用户模型
│   └── prediction.py          # 预测模型
├── services/                   # 业务逻辑
│   ├── __init__.py
│   ├── image_processor.py     # 图像处理
│   ├── personality_analyzer.py # 性格分析
│   ├── career_predictor.py    # 职业预测
│   ├── wealth_predictor.py    # 财富预测
│   ├── love_analyzer.py       # 感情分析
│   ├── fortune_analyzer.py    # 运势分析
│   └── astrology_analyzer.py  # 玄学分析
├── static/                     # 静态文件
│   └── uploads/               # 上传文件
├── logs/                       # 日志文件
├── backups/                    # 备份文件
├── Dockerfile                  # Docker配置
├── docker-compose.yml          # Docker Compose配置
└── README.md                   # 项目说明
```

## 🔧 核心模块说明

### 1. 图像处理 (ImageProcessor)

使用OpenCV进行人脸检测和特征提取：

- 人脸检测
- 面部比例计算
- 特征量化
- 亮度/对比度分析

### 2. 性格分析 (PersonalityAnalyzer)

基于Big Five人格模型和MBTI类型：

```python
{
  "bigFive": {
    "openness": 75,        # 开放性
    "conscientiousness": 80, # 尽责性
    "extraversion": 65,     # 外向性
    "agreeableness": 70,    # 宜人性
    "neuroticism": 40       # 神经质
  },
  "mbti": "INTJ",
  "description": "策略家...",
  "strengths": ["创新思维", "执行力强"],
  "suggestions": ["提升社交能力"]
}
```

### 3. 职业预测 (CareerPredictor)

预测职业发展潜力：

- 最佳职业领域匹配
- 成功率评估
- 晋升时间线
- 职业发展建议

### 4. 财富预测 (WealthPredictor)

分析财富积累趋势：

- 当前财富指数
- 10年积累曲线
- 投资风险承受能力
- 财富峰值预测

### 5. 感情分析 (LoveAnalyzer)

评估感情状况：

- 稳定性评分
- 最佳匹配类型
- 吸引力指数
- 感情建议

### 6. 运势分析 (FortuneAnalyzer)

提供时运预测：

- 日运势（昨天/今天/明天）
- 月运势（上月/本月/下月）
- 年运势（去年/今年/明年）
- 幸运元素（颜色/数字/方位/时辰）

### 7. 玄学分析 (AstrologyAnalyzer)

传统命理分析：

- 星座配置
- 八字四柱
- 五行强弱
- 开运建议

## 🔌 API接口文档

### 认证接口

#### 注册
```http
POST /api/register
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}

Response:
{
  "message": "注册成功",
  "access_token": "eyJ0eXAi...",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  }
}
```

#### 登录
```http
POST /api/login
Content-Type: application/json

{
  "username": "testuser",
  "password": "password123"
}

Response:
{
  "message": "登录成功",
  "access_token": "eyJ0eXAi...",
  "user": {...}
}
```

### 预测接口

#### 上传分析
```http
POST /api/upload
Authorization: Bearer {token}
Content-Type: multipart/form-data

file: [图片/视频文件]

Response:
{
  "prediction_id": 1,
  "personality": {...},
  "career": {...},
  "wealth": {...},
  "love": {...},
  "fortune": {...},
  "astrology": {...},
  "advice": {
    "daily": "今日建议...",
    "monthly": "本月建议...",
    "yearly": "今年建议..."
  }
}
```

#### 获取预测列表
```http
GET /api/predictions
Authorization: Bearer {token}

Response:
{
  "predictions": [
    {
      "id": 1,
      "created_at": "2025-01-15T10:30:00",
      "fortune_summary": {...}
    }
  ]
}
```

#### 获取预测详情
```http
GET /api/prediction/{id}
Authorization: Bearer {token}

Response:
{
  "id": 1,
  "created_at": "2025-01-15T10:30:00",
  "personality": {...},
  "career": {...},
  "wealth": {...},
  "love": {...},
  "fortune": {...},
  "astrology": {...}
}
```

#### 仪表盘统计
```http
GET /api/dashboard/stats
Authorization: Bearer {token}

Response:
{
  "daily": {
    "yesterday": 75,
    "today": 82,
    "tomorrow": 78
  },
  "monthly": {
    "lastMonth": 70,
    "current": 80,
    "nextMonth": 75
  },
  "yearly": {
    "lastYear": 72,
    "thisYear": 78,
    "nextYear": 82
  },
  "wealth_trend": [...],
  "love_score": 85,
  "career_fields": ["战略规划", "系统架构"]
}
```

## 🐳 Docker部署

### 使用Docker Compose（推荐）

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

服务访问：
- Web应用: http://localhost:5000
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### 单独使用Docker

```bash
# 构建镜像
docker build -t fortune-prediction .

# 运行容器
docker run -d -p 5000:5000 \
  -v $(pwd)/static/uploads:/app/static/uploads \
  fortune-prediction
```

## 🛠️ 开发指南

### 环境变量配置

复制 `.env.example` 到 `.env` 并配置：

```bash
# Flask配置
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret

# 数据库配置
DATABASE_URL=sqlite:///fortune_prediction.db

# Redis配置（可选）
REDIS_URL=redis://localhost:6379/0

# 文件上传
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216
```

### 数据库管理

```bash
# 初始化数据库
python init_db.py

# 创建管理员（如果有该脚本）
python scripts/create_admin.py

# 数据库备份
python scripts/backup.py
```

### 运行测试

```bash
# 运行所有测试
python -m pytest tests/ -v

# 运行特定测试
python -m pytest tests/test_api.py -v

# 查看覆盖率
python -m pytest --cov=. tests/
```

## ⚙️ 配置说明

### 数据库选择

**开发环境（SQLite）**
```python
DATABASE_URL=sqlite:///fortune_prediction.db
```

**生产环境（PostgreSQL）**
```python
DATABASE_URL=postgresql://user:pass@localhost:5432/fortune_db
```

### 文件存储

默认本地存储：
```python
UPLOAD_FOLDER=static/uploads
```

可扩展到云存储（AWS S3、阿里云OSS等）

## 🔒 安全建议

1. **更改默认密钥**
   - 生产环境必须设置强密钥
   - 使用 `python -c "import secrets; print(secrets.token_hex(32))"`生成

2. **启用HTTPS**
   ```bash
   # 使用Let's Encrypt免费证书
   sudo certbot --nginx -d your-domain.com
   ```

3. **配置防火墙**
   ```bash
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```

4. **定期备份**
   - 配置自动备份脚本
   - 测试恢复流程

## 📊 性能优化

1. **使用Gunicorn**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

2. **配置Nginx反向代理**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
       }
   }
   ```

3. **启用Redis缓存**
   - 缓存预测结果
   - Session存储

4. **CDN加速**
   - 静态资源CDN分发
   - 图片压缩优化

## ❓ 常见问题

### Q: 数据库连接失败
```bash
# 检查数据库文件权限
chmod 644 fortune_prediction.db

# 重新初始化
python init_db.py
```

### Q: 文件上传失败
```bash
# 检查上传目录权限
chmod 755 static/uploads

# 检查Nginx配置
client_max_body_size 16M;
```

### Q: 人脸检测失败
- 确保照片清晰
- 人脸正面朝向
- 光线充足
- 如果持续失败，系统会使用默认特征

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 📮 联系方式

- GitHub: https://github.com/joweywen/fortune_prediction_system
- Issues: https://github.com/joweywen/fortune_prediction_system/issues

---

**⚠️ 免责声明**

本系统的预测结果仅供娱乐参考，不构成任何专业建议。请理性对待分析结果。