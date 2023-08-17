from django import forms

from files.models import UploadedFile


class UploadFileForm(forms.ModelForm):

    class Meta:
        model = UploadedFile
        fields = ('file',)
