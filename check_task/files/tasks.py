import subprocess

from django.conf import settings
from django.db.models import Q
from config.celery import app

from files.models import UploadedFile


@app.task()
def check_file_with_flake8():
    files = UploadedFile.objects.filter(
        Q(file_state='new') | Q(file_state='reload'),
        notification=False
    )
    for file in files:
        file_path = settings.MEDIA_ROOT + '/' + str(file.file)
        try:
            output = subprocess.check_output(['flake8', file_path], stderr=subprocess.STDOUT)
            print(output)
        except subprocess.CalledProcessError as error:
            return error.output.decode()


@app.task()
def send_notification():
    pass
