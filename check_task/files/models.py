import os
from django.db import models

from users.models import CustomUser


class StateFile(models.TextChoices):
    """Состояния файла."""
    NEW = 'new'
    RELOAD = 'reload'


class UploadedFile(models.Model):
    """Модель загружаемого файла."""
    user = models.ForeignKey(CustomUser, related_name='files', on_delete=models.CASCADE,
                             blank=True, null=True)
    file = models.FileField(upload_to='uploaded_files/')
    file_state = models.CharField(choices=StateFile.choices, default=StateFile.NEW, max_length=10)
    is_checked = models.BooleanField(default=False)
    notification = models.BooleanField(default=False)
    errors = models.TextField(blank=True, null=True)
    uploaded_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
        ordering = ('-uploaded_date',)

    def __str__(self):
        return os.path.basename(self.file.name)
