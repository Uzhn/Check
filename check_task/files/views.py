from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
# from django.shortcuts import redirect

from files.models import UploadedFile
from files.forms import UploadFileForm


class UploadFileCreateView(LoginRequiredMixin, CreateView):
    model = UploadedFile
    form_class = UploadFileForm
    template_name = 'files/upload_file.html'
    success_url = 'files/file_history.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class FileHistoryView(ListView):
    model = UploadedFile
    template_name = 'files/file_history.html'

    def get_queryset(self):
        files = super().get_queryset()
        return files.filter(user=self.request.user)






