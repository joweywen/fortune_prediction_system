# 命运预测系统 - 完整项目结构

## 📁 项目文件结构

```
fortune_prediction_system/
│
├── 📄 核心应用文件
│   ├── app.py                          # Flask主应用（修复完善版）
│   ├── run.py                          # 应用启动入口
│   ├── config.py                       # 配置管理
│   ├── init_db.py                      # 数据库初始化脚本
│   └── requirements.txt                # Python依赖包列表
│
├── 📂 models/                          # 数据模型层
│   ├── __init__.py                    # 模块初始化
│   ├── user.py                        # 用户模型
│   └── prediction.py                  # 预测记录模型
│
├── 📂 services/                        # 业务逻辑层（7个分析服务）
│   ├── __init__.py                    # 服务模块初始化
│   ├── image_processor.py             # 图像处理服务（OpenCV人脸检测）
│   ├── personality_analyzer.py        # 性格分析（Big Five + MBTI）
│   ├── career_predictor.py            # 职业预测（成功率、晋升预测）
│   ├── wealth_predictor.py            # 财富预测（积累趋势、投资建议）
│   ├── love_analyzer.py               # 感情分析（稳定性、匹配度）
│   ├── fortune_analyzer.py            # 运势分析（日/月/年运势）
│   └── astrology_analyzer.py          # 玄学分析（星座、八字、五行）
│
├── 📂 static/                          # 静态资源目录
│   ├── uploads/                       # 用户上传文件存储
│   │   └── .gitkeep                   # Git保留空目录
│   └── images/                        # 系统图片资源
│
├── 📂 templates/                       # 前端模板（可选）
│   └── index.html                     # 完整的React前端应用
│
├── 📂 tests/                           # 测试文件
│   ├── __init__.py                    # 测试模块初始化
│   └── test_api.py                    # API接口测试
│
├── 📂 scripts/                         # 工具脚本
│   ├── backup.py                      # 数据库备份脚本
│   ├── create_admin.py                # 创建管理员账户
│   └── maintenance.py                 # 系统维护脚本
│
├── 📂 logs/                            # 日志文件目录
│   ├── app.log                        # 应用日志
│   └── error.log                      # 错误日志
│
├── 📂 backups/                         # 备份文件目录
│   └── .gitkeep
│
├── 🐳 Docker相关
│   ├── Dockerfile                     # Docker镜像构建文件
│   ├── docker-compose.yml             # Docker Compose配置
│   └── .dockerignore                  # Docker忽略文件
│
├── 📋 配置文件
│   ├── .env.example                   # 环境变量模板
│   ├── .env                           # 环境变量（需自行创建）
│   ├── .gitignore                     # Git忽略文件
│   ├── gunicorn_config.py             # Gunicorn生产配置
│   └── celery_app.py                  # Celery异步任务配置
│
├── 🚀 启动脚本
│   ├── quick-start.sh                 # Linux/Mac快速启动
│   ├── start.sh                       # Linux/Mac标准启动
│   ├── start.bat                      # Windows启动脚本
│   └── check_project.py               # 项目完整性检查
│
├── 📖 文档
│   ├── README.md                      # 项目说明文档
│   ├── DEPLOYMENT.md                  # 部署指南
│   ├── PROJECT_GUIDE.md               # 项目完整指南
│   └── API.md                         # API接口文档
│
└── 🛠️ 其他
    ├── Makefile                       # Make命令配置
    ├── LICENSE                        # 开源许可证
    └── fortune_prediction.db          # SQLite数据库（运行后生成）
```

---

## 📝 核心文件详细说明

### 1. **app.py** - Flask主应用
```python
# 功能：
- 用户认证（注册/登录）- JWT Token
- 文件上传处理
- 7大分析模块调用
- RESTful API接口
- 数据库操作（SQLAlchemy）
- 错误处理和日志记录

# 主要路由：
POST /api/register          # 用户注册
POST /api/login             # 用户登录
POST /api/upload            # 上传并分析
GET  /api/predictions       # 获取预测列表
GET  /api/prediction/<id>   # 获取预测详情
GET  /api/dashboard/stats   # 仪表盘统计
GET  /api/health            # 健康检查
```

### 2. **run.py** - 启动入口
```python
# 功能：
- 创建必要目录
- 启动Flask应用
- 开发环境配置
```

### 3. **config.py** - 配置管理
```python
# 配置项：
- SECRET_KEY              # Flask密钥
- JWT_SECRET_KEY          # JWT密钥
- DATABASE_URL            # 数据库连接
- UPLOAD_FOLDER           # 上传目录
- MAX_CONTENT_LENGTH      # 最大文件大小
- ALLOWED_EXTENSIONS      # 允许的文件类型
```

### 4. **requirements.txt** - Python依赖
```txt
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-JWT-Extended==4.5.3
Flask-CORS==4.0.0
Pillow==10.1.0
opencv-python==4.8.1.78
numpy==1.26.2
pandas==2.1.3
scikit-learn==1.3.2
face-recognition==1.3.0
PyJWT==2.8.0
python-dotenv==1.0.0
bcrypt==4.1.1
redis==5.0.1
celery==5.3.4
gunicorn==21.2.0
```

---

## 🔧 服务模块说明

### services/image_processor.py
```python
# 功能：图像处理和特征提取
- 人脸检测（OpenCV Haar Cascade）
- 面部特征提取（比例、亮度、对比度等）
- 特征量化
- 默认特征生成（检测失败时）
```

### services/personality_analyzer.py
```python
# 功能：性格分析
- Big Five人格评分（0-100分）
  - Openness（开放性）
  - Conscientiousness（尽责性）
  - Extraversion（外向性）
  - Agreeableness（宜人性）
  - Neuroticism（神经质）
- MBTI类型推断（16种类型）
- 性格描述生成
- 优势识别
- 发展建议
```

### services/career_predictor.py
```python
# 功能：职业预测
- 最佳职业领域匹配
- 职业成功率预测（40-95%）
- 5年职业发展趋势
- 晋升时间线预测
- 职业发展建议
```

### services/wealth_predictor.py
```python
# 功能：财富预测
- 当前财富趋势评分
- 10年财富积累曲线
- 投资风险承受能力
- 财富峰值年份预测
- 投资建议
```

### services/love_analyzer.py
```python
# 功能：感情分析
- 感情稳定性评分
- MBTI最佳匹配类型
- 6个月感情趋势
- 吸引力指数
- 感情建议
```

### services/fortune_analyzer.py
```python
# 功能：运势分析
- 日运势（昨天/今天/明天）
- 月运势（上月/本月/下月）
- 年运势（去年/今年/明年）
- 幸运元素（颜色/数字/方位/时辰）
```

### services/astrology_analyzer.py
```python
# 功能：玄学分析
- 星座分析（太阳/月亮/上升）
- 八字四柱（年月日时）
- 五行强弱分析
- 喜用神推算
- 开运建议
```

---

## 🗄️ 数据模型说明

### models/user.py - 用户模型
```python
class User:
    id              # 用户ID
    username        # 用户名（唯一）
    email           # 邮箱（唯一）
    password_hash   # 密码哈希
    created_at      # 创建时间
    last_login      # 最后登录时间
    is_active       # 是否激活
    is_admin        # 是否管理员
    predictions     # 关联的预测记录
```

### models/prediction.py - 预测模型
```python
class Prediction:
    id                  # 预测ID
    user_id             # 用户ID（外键）
    image_path          # 图片路径
    personality_data    # 性格分析结果（JSON）
    career_data         # 职业预测结果（JSON）
    wealth_data         # 财富预测结果（JSON）
    love_data           # 感情分析结果（JSON）
    fortune_data        # 运势分析结果（JSON）
    astrology_data      # 玄学分析结果（JSON）
    created_at          # 创建时间
```

---

## 🎨 前端应用说明

### templates/index.html - React单页应用
```javascript
// 组件结构：
App
├── LoginView（登录/注册界面）
├── Navigation（导航栏）
├── DashboardView（仪表盘）
│   ├── FortuneCards（运势卡片）
│   ├── WealthTrendChart（财富趋势图）
│   ├── LoveScore（爱情指数）
│   └── CareerFields（职业领域）
├── UploadView（上传界面）
└── ResultView（分析结果）
    ├── PersonalityAnalysis（性格分析）
    ├── AdviceCards（建议卡片）
    └── BackButton（返回按钮）

// 主要功能：
- 用户认证（JWT Token存储）
- 文件上传（FormData）
- 数据可视化（Recharts图表）
- 响应式设计（Tailwind CSS）
- 错误处理和加载状态
```

---

## 🚀 启动方式

### 方式1：快速启动（推荐）
```bash
# Linux/Mac
chmod +x quick-start.sh
./quick-start.sh

# Windows
start.bat
```

### 方式2：手动启动
```bash
# 1. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 初始化数据库
python init_db.py

# 4. 启动应用
python run.py
```

### 方式3：Docker启动
```bash
# 使用Docker Compose
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

---

## 🧪 测试说明

### tests/test_api.py - API测试
```python
# 测试覆盖：
- 用户注册/登录
- 文件上传
- API认证
- 数据查询
- 服务模块功能
- 错误处理
```

### 运行测试
```bash
# 运行所有测试
python -m pytest tests/ -v

# 查看覆盖率
python -m pytest --cov=. tests/
```

---

## 📦 数据库说明

### SQLite数据库文件
```
fortune_prediction.db
├── users表
│   ├── 索引：username, email
│   └── 外键关系：predictions
└── predictions表
    ├── 索引：user_id, created_at
    └── JSON字段：6个分析结果
```

### 数据库操作
```bash
# 初始化
python init_db.py

# 备份
python scripts/backup.py

# 查看数据
sqlite3 fortune_prediction.db
sqlite> .tables
sqlite> SELECT * FROM users;
```

---

## 🛠️ 工具脚本说明

### check_project.py - 项目检查
```python
# 检查内容：
✓ Python版本（3.9+）
✓ 核心文件完整性
✓ 模块导入
✓ 目录结构
✓ 配置文件
✓ 依赖包安装
```

### scripts/backup.py - 数据库备份
```python
# 功能：
- 自动备份数据库
- 压缩备份文件
- 保留最近7天备份
- 定时任务支持
```

### scripts/maintenance.py - 系统维护
```python
# 功能：
- 清理旧预测记录（90天）
- 清理临时文件
- 生成统计报告
- 数据库优化
```

---

## 🔐 安全配置

### .env文件配置
```bash
# 必须修改的配置
SECRET_KEY=your-super-secret-key-change-me
JWT_SECRET_KEY=your-jwt-secret-key-change-me

# 数据库配置
DATABASE_URL=sqlite:///fortune_prediction.db

# 可选配置
REDIS_URL=redis://localhost:6379/0
```

### 生成密钥
```python
import secrets
print(secrets.token_hex(32))
```

---

## 📊 API接口文档

### 完整API列表
```
认证接口：
POST   /api/register        # 注册
POST   /api/login           # 登录

预测接口：
POST   /api/upload          # 上传分析（需认证）
GET    /api/predictions     # 预测列表（需认证）
GET    /api/prediction/:id  # 预测详情（需认证）
GET    /api/dashboard/stats # 仪表盘（需认证）

系统接口：
GET    /api/health          # 健康检查
GET    /                    # 系统信息
```

---

## 🌐 部署架构

### 开发环境
```
Flask Built-in Server (127.0.0.1:5000)
└── SQLite数据库
```

### 生产环境
```
Nginx (80/443)
└── Gunicorn (多进程)
    └── Flask应用
        ├── PostgreSQL数据库
        ├── Redis缓存
        └── Celery异步任务
```

---

## 📄 许可证
MIT License - 开源免费使用

## 🤝 贡献
欢迎提交Issue和Pull Request

## 📮 支持
- GitHub: https://github.com/joweywen/fortune_prediction_system
- Issues: https://github.com/joweywen/fortune_prediction_system/issues