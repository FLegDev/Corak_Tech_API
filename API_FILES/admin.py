# admin.py
from django.contrib import admin
from django.contrib import messages
from .models import UploadedFile, ParsedData
from .tasks import delete_uploaded_files_in_batches, delete_parsed_data_in_batches

def delete_all_uploaded_files(modeladmin, request, queryset):
    file_ids = list(queryset.values_list('id', flat=True))
    batch_size = 5000
    if len(file_ids) > batch_size:
        for start in range(0, len(file_ids), batch_size):
            delete_uploaded_files_in_batches.delay(file_ids[start:start + batch_size], batch_size=batch_size)
    else:
        delete_uploaded_files_in_batches.delay(file_ids, batch_size=batch_size)
    messages.success(request, f"La suppression des fichiers uploadés a été lancée en arrière-plan avec une taille de lot de {batch_size}.")

delete_all_uploaded_files.short_description = "Vider tous les fichiers uploadés"

def delete_all_parsed_data(modeladmin, request, queryset):
    file_ids = list(queryset.values_list('id', flat=True))
    batch_size = 5000
    if len(file_ids) > batch_size:
        for start in range(0, len(file_ids), batch_size):
            delete_parsed_data_in_batches.delay(file_ids[start:start + batch_size], batch_size=batch_size)
    else:
        delete_parsed_data_in_batches.delay(file_ids, batch_size=batch_size)
    messages.success(request, f"La suppression des données parsées a été lancée en arrière-plan avec une taille de lot de {batch_size}.")

delete_all_parsed_data.short_description = "Vider toutes les données parsées"

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ['file', 'uploaded_at', 'store_profile']
    list_filter = ['store_profile']  # Filtre par store_profile pour UploadedFile
    list_per_page = 100
    actions = [delete_all_uploaded_files]  # Ajouter l'action de suppression

@admin.register(ParsedData)
class ParsedDataAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ParsedData._meta.fields]
    list_filter = ['gencod_ean', 'updated_at', 'store_profile']
    search_fields = ['gencod_ean', 'main_label', 'secondary_label']
    list_per_page = 150
    actions = [delete_all_parsed_data]