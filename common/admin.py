from django.contrib import admin
from .models import UploadedFile

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'file_type', 'store_profile', 'uploaded_at')
    list_filter = ('file_type', 'store_profile')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('store_profile')
        return queryset

