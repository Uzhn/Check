from django import forms

from files.models import UploadedFile
from users.models import CustomUser


class UploadFileForm(forms.ModelForm):

    class Meta:
        model = UploadedFile
        fields = ('file',)
