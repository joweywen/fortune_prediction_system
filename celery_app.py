from celery import Celery
from celery.schedules import crontab
from app import app

def make_celery(app):
    """创建Celery实例"""
    celery = Celery(
        app.import_name,
        backend=app.config.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0'),
        broker=app.config.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    )
    celery.conf.update(app.config)
    
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask
    return celery

celery = make_celery(app)

# 定时任务配置
celery.conf.beat_schedule = {
    'daily-backup': {
        'task': 'tasks.backup_database',
        'schedule': crontab(hour=2, minute=0),  # 每天凌晨2点
    },
    'weekly-cleanup': {
        'task': 'tasks.cleanup_old_data',
        'schedule': crontab(day_of_week=0, hour=3, minute=0),  # 每周日凌晨3点
    },
    'hourly-stats': {
        'task': 'tasks.generate_hourly_stats',
        'schedule': crontab(minute=0),  # 每小时
    },
}

# 定义任务
@celery.task(name='tasks.backup_database')
def backup_database_task():
    """数据库备份任务"""
    from scripts.backup import backup_database
    return backup_database()

@celery.task(name='tasks.cleanup_old_data')
def cleanup_old_data_task():
    """清理旧数据任务"""
    from scripts.maintenance import cleanup_old_predictions, cleanup_old_images
    cleanup_old_predictions(90)
    cleanup_old_images(90)
    return True

@celery.task(name='tasks.generate_hourly_stats')
def generate_hourly_stats_task():
    """生成小时统计任务"""
    from scripts.maintenance import generate_statistics
    return generate_statistics()
