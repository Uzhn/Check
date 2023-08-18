from django.contrib.auth import login
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('files:files_history')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
