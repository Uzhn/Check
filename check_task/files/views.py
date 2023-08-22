from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.mixins import PermissionRequiredMixin

from files.models import UploadedFile, StateFile
from files.forms import UploadFileForm
from services.extension import FileCheck
from services.exceptions import ExtensionError
from files.tasks import check_file_with_flake8


class UploadFileCreateView(CreateView, FileCheck):
    form_class = UploadFileForm
    template_name = 'files/upload_file.html'
    success_url = reverse_lazy('files:files_history')

    def form_valid(self, form):
        uploaded_file = form.cleaned_data['file']

        try:
            self.check_extension(uploaded_file)
        except ExtensionError as error:
            form.add_error('file', error)
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


class FileDetailView(DetailView):
    model = UploadedFile
    template_name = 'files/file_detail.html'
    context_object_name = 'file'

    def get_object(self, queryset=None):
        file_id = self.kwargs.get('file_id')
        return UploadedFile.objects.get(id=file_id)


class DeleteFileView(DeleteView):
    model = UploadedFile
    template_name = 'files/delete_file.html'
    success_url = reverse_lazy('files:files_history')
    context_object_name = 'file'


class ReloadFileView(View):
    def get(self, request, pk):
        file = get_object_or_404(UploadedFile, pk=pk, user=request.user)
        form = UploadFileForm(instance=file)
        context = {
            'file': file,
            'form': form,
        }
        return render(request, 'files/reload_file.html', context)

    def post(self, request, pk):
        if UploadedFile.objects.filter(pk=pk).exists():
            file = UploadedFile.objects.get(pk=pk)
            form = UploadFileForm(request.POST, request.FILES, instance=file)

            file_check = FileCheck()

            try:
                file_check.check_extension(request.FILES['file'])
            except ExtensionError as error:
                context = {
                    'file': file,
                    'form': form,
                    'error_message': error,
                }
                return render(request, 'files/reload_file.html', context)

            if form.is_valid():
                form.save()
                file.file_state = StateFile.RELOAD
                file.save()
                return redirect('files:files_history')

        return redirect('files:file_detail', pk=pk)


