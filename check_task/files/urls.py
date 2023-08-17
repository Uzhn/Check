from django.urls import path

from . import views

app_name = 'files'

urlpatterns = [
    path('upload_file/', views.UploadFileCreateView.as_view(), name='upload_file'),
    path('files_history/', views.FileHistoryView.as_view(), name='files_history'),
]