import logging
import smtplib
from .exceptions import ExtensionError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.mail import send_mail
from django.conf import settings

from files.models import UploadedFile

logger = logging.getLogger('main')


class FileCheck:

    def check_extension(self, file: InMemoryUploadedFile):
        if not file.name.endswith('.py'):
            raise ExtensionError('Загружаемый файл должен иметь расширение .py')


def send_notification(email, file_id, message):
    file_checked = UploadedFile.objects.get(id=file_id)
    try:
        send_mail(
            "Результат проверки",
            f"Файл {file_checked} проверен.\n{message}",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        file_checked.notification = True
        file_checked.save()
        logger.info(f'Сообщение для {email} отправлено')
    except smtplib.SMTPException as error:
        logger.error(f'Ошибка при отправке сообщения для {email}: {error}')
