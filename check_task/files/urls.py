from django.urls import path

from . import views

app_name = 'files'

urlpatterns = [
    path('upload_file/', views.UploadFileCreateView.as_view(), name='upload_file'),
    path('files_history/', views.FileHistoryView.as_view(), name='files_history'),
    path('file_detail/<int:file_id>/', views.FileDetailView.as_view(), name='file_detail'),
    path('file_delete/<int:pk>/', views.DeleteFileView.as_view(), name='file_delete'),
    path('file_reload/<int:pk>', views.ReloadFileView.as_view(), name='file_reload'),
]
