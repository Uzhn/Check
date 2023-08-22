from .exceptions import ExtensionError
from django.core.files.uploadedfile import InMemoryUploadedFile


class FileCheck:

    def check_extension(self, file: InMemoryUploadedFile):
        if not file.name.endswith('.py'):
            raise ExtensionError('Загружаемый файл должен иметь расширение .py')

