.PHONY: help install dev prod test clean docker-build docker-up docker-down backup

help:
	@echo "Fortune Prediction System - Makefile命令"
	@echo ""
	@echo "  make install      - 安装依赖"
	@echo "  make dev          - 启动开发环境"
	@echo "  make prod         - 启动生产环境"
	@echo "  make test         - 运行测试"
	@echo "  make clean        - 清理临时文件"
	@echo "  make docker-build - 构建Docker镜像"
	@echo "  make docker-up    - 启动Docker服务"
	@echo "  make docker-down  - 停止Docker服务"
	@echo "  make backup       - 备份数据库"
	@echo ""

install:
	python -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	@echo "依赖安装完成！"

dev:
	. venv/bin/activate && python run.py

prod:
	. venv/bin/activate && gunicorn -c gunicorn_config.py app:app

test:
	. venv/bin/activate && python -m pytest tests/ -v

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	find . -type f -name '.coverage' -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	@echo "清理完成！"

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d
	@echo "服务启动完成！"
	@echo "Web: http://localhost:5000"
	@echo "Flower: http://localhost:5555"

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

backup:
	. venv/bin/activate && python scripts/backup.py

migrate:
	. venv/bin/activate && python init_db.py

create-admin:
	. venv/bin/activate && python scripts/create_admin.py

maintenance:
	. venv/bin/activate && python scripts/maintenance.py all