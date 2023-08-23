import os

from celery import Celery
# from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery(__name__)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# CELERY_BEAT_SCHEDULE = {
#     'check_files_with_flake8': {
#         'task': 'files.tasks.check_file_with_flake8',
#         'schedule': crontab(minute='*/1'),
#     },
# }
