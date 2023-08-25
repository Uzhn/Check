import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery(__name__)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'check_file_with_flake8_task': {
        'task': 'files.tasks.check_file_with_flake8_task',
        'schedule': crontab(minute='*'),
    },
}
