import subprocess

from django.conf import settings
from django.db.models import Q
from config.celery import app
from django.core.mail import send_mail

from files.models import UploadedFile, StateFile


@app.task()
def check_file_with_flake8_task():
    files = UploadedFile.objects.filter(
        Q(file_state=StateFile.NEW) | Q(file_state=StateFile.RELOAD),
        notification=False
    )
    for file in files:
        file_path = settings.MEDIA_ROOT + '/' + str(file.file)
        user_email = file.user.email

        try:
            result = subprocess.run(['flake8', file_path])
        except FileNotFoundError as error:
            return error.output.decode()
        if result.returncode != 0:
            file.error = result
            file.save()
            error_mesage = 'Есть ошибки!!!'
            send_notification_task.delay(user_email, file, error_mesage)
        else:
            message = 'Ошибок нет!!!'
            send_notification_task.delay(user_email, file, message)


@app.task()
def send_notification_task(email, file, messsage):
    send_mail(
        "Результат проверки",
        f"Файл {file} проверен.\n{messsage}",
        "support@example.com",
        [email],
        fail_silently=False,
    )
    file_checked = UploadedFile.objects.get(id=file.id)
    file_checked.notification = True
    file_checked.save()
