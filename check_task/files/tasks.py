import subprocess
import smtplib
import logging

from django.conf import settings
from config.celery import app

from files.models import UploadedFile, StateFile
from services.helper import format_error_lines
from services.logic import send_notification

logger = logging.getLogger('main')


@app.task()
def check_file_with_flake8_task():
    files = UploadedFile.objects.filter(is_checked=False)
    for file in files:
        file_path = settings.MEDIA_ROOT + '/' + str(file.file)
        user_email = file.user.email

        try:
            result = subprocess.run(['flake8', file_path], stdout=subprocess.PIPE)
            file.is_checked = True
            file.save()
            logger.info(f'Файл {file} проверен')
        except FileNotFoundError as error:
            logger.error(f'Ошибка при проверке файла: {file}')
            raise FileNotFoundError(f'Ошибка при проверке файла: {file}. Ошибка: {error}')

        if result.returncode:
            split_errors = result.stdout.decode().splitlines()
            formatted_lines = format_error_lines(split_errors)
            file.errors = formatted_lines
            file.save()
        error_message = 'Есть ошибки!!!'
        message = 'Ошибок нет!!!'
        send_notification_task.delay(
            user_email,
            file.id,
            error_message if result.returncode else message
        )


@app.task()
def send_notification_task(email, file_id, message):
    send_notification(email, file_id, message)
