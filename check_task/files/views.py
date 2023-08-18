from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
# from django.shortcuts import redirect

from files.models import UploadedFile
from files.forms import UploadFileForm
from utils.extension import check_extension


class UploadFileCreateView(CreateView):
    form_class = UploadFileForm
    template_name = 'files/upload_file.html'
    success_url = reverse_lazy('files:files_history')

    def form_valid(self, form):
        uploaded_file = form.cleaned_data['file']
        if not uploaded_file.name.endswith('.py'):
            form.add_error('file', 'Загружаемый файл должен иметь расширение .py')
            return self.form_invalid(form)
        form.instance.user = self.request.user
        return super().form_valid(form)


class FileHistoryView(ListView):
    model = UploadedFile
    template_name = 'files/file_history.html'
    context_object_name = 'files'

    def get_queryset(self):
        files = super().get_queryset()
        if self.request.user.is_authenticated:
            return files.filter(user=self.request.user)
