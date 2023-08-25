import subprocess

from django.conf import settings
from config.celery import app

from files.models import UploadedFile, StateFile
from services.helper import format_error_lines
from services.logic import send_notification


@app.task()
def check_file_with_flake8_task():
    files = UploadedFile.objects.filter(notification=False)
    for file in files:
        file_path = settings.MEDIA_ROOT + '/' + str(file.file)
        user_email = file.user.email
        result = subprocess.run(['flake8', file_path], stdout=subprocess.PIPE)
        if result.returncode != 0:
            split_errors = result.stdout.decode().splitlines()
            formatted_lines = format_error_lines(split_errors)
            file.errors = formatted_lines
            file.save()
            error_message = 'Есть ошибки!!!'
            send_notification_task.delay(user_email, file.id, error_message)
        else:
            message = 'Ошибок нет!!!'
            send_notification_task.delay(user_email, file.id, message)


@app.task()
def send_notification_task(email, file_id, message):
    send_notification(email, file_id, message)

