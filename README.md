````markdown
# 综合命运预测系统

一个基于Python Flask + React的全栈命运预测系统，集成了性格分析、职业预测、财富分析、感情预测和玄学分析等多个模块。

## 功能特性

### 科学分析模块
- **性格分析**: Big Five人格特质 + MBTI类型分析
- **职业预测**: 基于性格的职业成功率预测和发展建议
- **财富预测**: 财富积累趋势和投资建议
- **感情分析**: 感情稳定性和最佳匹配分析
- **运势分析**: 基于数据的时运趋势预测

### 玄学分析模块
- **星座分析**: 太阳、月亮、上升星座
- **八字命理**: 四柱八字分析
- **五行分析**: 五行强弱和喜用神
- **开运建议**: 幸运颜色、方位、时辰等

### 数据展示
- 日/月/年维度的多维度数据图表
- 交互式数据可视化
- 个性化行事建议
- 历史预测记录查询

## 技术栈

### 后端
- Python 3.9+
- Flask 3.0
- SQLAlchemy (ORM)
- JWT认证
- OpenCV (图像处理)
- Face Recognition (人脸识别)
- NumPy, Pandas (数据分析)

### 前端
- React 18
- Tailwind CSS
- Lucide Icons
- Recharts (数据可视化)

## 快速开始

### 1. 环境要求
```bash
Python 3.9+
pip
virtualenv (推荐)
```

### 2. 安装依赖
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置环境变量
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件，设置密钥
```

### 4. 初始化数据库
```bash
python init_db.py
```

### 5. 启动应用
```bash
python run.py
```

访问: http://localhost:5000

## Docker部署
```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

## API文档

### 认证接口

#### 注册
````
POST /api/register
Content-Type: application/json

{
  "username": "string",
  "email": "string",
  "password": "string"
}
````

#### 登录
````
POST /api/login
Content-Type: application/json

{
  "username": "string",
  "password": "string"
}
````

### 预测接口

#### 上传分析
````
POST /api/upload
Authorization: Bearer {token}
Content-Type: multipart/form-data

file: image/video file
````

#### 获取预测列表
````
GET /api/predictions
Authorization: Bearer {token}
````

#### 获取预测详情
````
GET /api/prediction/{id}
Authorization: Bearer {token}
````

#### 获取仪表盘统计
````
GET /api/dashboard/stats
Authorization: Bearer {token}
````

## 项目结构
````
fortune_prediction_system/
├── app.py                      # Flask主应用
├── config.py                   # 配置文件
├── requirements.txt            # 依赖包
├── models/                     # 数据模型
│   ├── user.py                # 用户模型
│   └── prediction.py          # 预测模型
├── services/                   # 业务逻辑
│   ├── personality_analyzer.py
│   ├── career_predictor.py
│   ├── wealth_predictor.py
│   ├── love_analyzer.py
│   ├── fortune_analyzer.py
│   ├── astrology_analyzer.py
│   └── image_processor.py
├── static/                     # 静态文件
│   └── uploads/               # 上传文件目录
└── tests/                      # 测试文件
    └── test_api.py
````

## 核心算法说明

### 1. 性格分析算法
基于面部特征和Big Five模型，通过以下步骤:
- 人脸检测和关键点提取
- 面部特征量化
- Big Five评分计算
- MBTI类型推断

### 2. 预测模型
使用多维度特征融合:
- 性格特质权重
- 历史数据趋势
- 随机因素模拟
- 时间序列预测

### 3. 玄学分析
结合传统命理学:
- 星座配置生成
- 八字四柱推算
- 五行生克关系
- 吉凶趋势判断

## 注意事项

1. 本系统预测结果仅供娱乐参考，不构成任何专业建议
2. 图像处理需要清晰的人脸照片以获得最佳分析效果
3. 首次运行需要下载face_recognition模型，可能需要时间
4. 生产环境请务必更改SECRET_KEY和JWT_SECRET_KEY
5. 建议使用HTTPS部署以保护用户隐私

## 性能优化建议

1. 使用Redis缓存预测结果
2. 异步处理图像分析任务
3. CDN加速静态资源
4. 数据库查询优化和索引
5. 使用Gunicorn+Nginx部署

## 未来规划

- [ ] 增加更多AI模型支持
- [ ] 实时视频分析功能
- [ ] 社交分享功能
- [ ] 付费高级分析功能
- [ ] 移动端App开发
- [ ] 多语言支持

## 许可证

MIT License

## 联系方式

如有问题或建议，请提交Issue或Pull Request。
````

### 20. .gitignore文件
````gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# 虚拟环境
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# 数据库
*.db
*.sqlite
*.sqlite3

# 上传文件
static/uploads/*
!static/uploads/.gitkeep

# 环境变量
.env
.env.local

# 日志
*.log

# 操作系统
.DS_Store
Thumbs.db

# 测试
.coverage
htmlcov/
.pytest_cache/
````

## 完整部署指南

### 生产环境部署步骤

1. **服务器准备**
````bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装必要软件
sudo apt install python3-pip python3-venv nginx -y
````

2. **克隆项目**
````bash
git clone <your-repo-url>
cd fortune_prediction_system
````

3. **配置虚拟环境**
````bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
````

4. **配置Gunicorn**
创建 `gunicorn_config.py`:
````python
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = "info"
````

5. **配置Nginx**
创建 `/etc/nginx/sites-available/fortune_prediction`:
````nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /path/to/your/project/static;
    }
}
````

6. **创建Systemd服务**
创建 `/etc/systemd/system/fortune_prediction.service`:
````ini
[Unit]
Description=Fortune Prediction System
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/project
Environment="PATH=/path/to/your/project/venv/bin"
ExecStart=/path/to/your/project/venv/bin/gunicorn -c gunicorn_config.py app:app

[Install]
WantedBy=multi-user.target
````

7. **启动服务**
````bash
sudo systemctl enable fortune_prediction
sudo systemctl start fortune_prediction
sudo systemctl enable nginx
sudo systemctl restart nginx
````

## 🎉 完成！

现在你拥有了一个完整的命运预测系统！系统包含：

✅ **完整的后端Flask应用**
- 用户认证系统
- 图像处理和特征提取
- 多维度预测模型
- RESTful API

✅ **交互式前端界面**
- 用户登录/注册
- 文件上传
- 数据可视化仪表盘
- 详细分析展示

✅ **数据持久化**
- SQLite数据库
- 用户信息存储
- 预测结果保存

✅ **完整文档**
- API文档
- 部署指南
- 测试脚本

你可以根据需要进一步定制和扩展功能！


fortune_prediction_system/
├── app.py                      # Flask主应用
├── requirements.txt            # 依赖包
├── config.py                   # 配置文件
├── models/                     # 数据模型
│   ├── __init__.py
│   ├── user.py
│   ├── prediction.py
│   └── analysis.py
├── services/                   # 业务逻辑层
│   ├── __init__.py
│   ├── personality_analyzer.py # Big Five + MBTI分析
│   ├── career_predictor.py    # 职业预测
│   ├── wealth_predictor.py    # 财富预测
│   ├── love_analyzer.py       # 感情分析
│   ├── fortune_analyzer.py    # 运势分析
│   ├── astrology_analyzer.py  # 星座/八字分析
│   └── image_processor.py     # 图像处理
├── utils/                      # 工具函数
│   ├── __init__.py
│   ├── auth.py
│   └── database.py
├── static/                     # 静态文件
│   ├── uploads/
│   └── images/
└── templates/                  # 前端模板 (如需要)
    └── index.html