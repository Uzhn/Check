from django.contrib import admin

from files.models import UploadedFile


class UploadedFilesAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "file", "file_state", "notification", "uploaded_date")
    empty_value_display = "-пусто-"


admin.site.register(UploadedFile, UploadedFilesAdmin)
