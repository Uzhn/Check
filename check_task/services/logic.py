from .exceptions import ExtensionError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.mail import send_mail

from files.models import UploadedFile


class FileCheck:

    def check_extension(self, file: InMemoryUploadedFile):
        if not file.name.endswith('.py'):
            raise ExtensionError('Загружаемый файл должен иметь расширение .py')


def send_notification(email, file_id, message):
    file_checked = UploadedFile.objects.get(id=file_id)
    send_mail(
        "Результат проверки",
        f"Файл {file_checked} проверен.\n{message}",
        "support@example.com",
        [email],
        fail_silently=False,
    )
    file_checked.notification = True
    file_checked.save()
