from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django import forms
from django.utils.timezone import is_aware
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .models import Export2Zkong, ZkongLog
from custom_user_management.models import Corak_API_userProfile
import pandas as pd
from io import BytesIO
import zipfile
import json
import logging

from .Corak_ESL_API import BatchDelete, ZkongAuth, ZkongAPI
from import_export.admin import ImportExportModelAdmin

logger = logging.getLogger('corak_esl')

def delete_all_products(modeladmin, request, queryset):
    count, _ = Export2Zkong.objects.all().delete()
    messages.success(request, f"{count} produits ont été supprimés avec succès.")

delete_all_products.short_description = "Vider les produits Export2Zkong"


def delete_locally(modeladmin, request, queryset):
    count = queryset.count()
    queryset.delete()
    messages.success(request, f"{count} articles supprimés localement.")

delete_locally.short_description = "Supprimer les articles sélectionnés localement"


def batch_delete_from_zkong(modeladmin, request, queryset):
    barcodes_to_delete = list(queryset.values_list('barCode', flat=True))

    if not barcodes_to_delete:
        messages.error(request, "Aucun article sélectionné pour suppression.")
        return

    if len(barcodes_to_delete) > 500:
        messages.error(request, "Le nombre d'articles dépasse la limite de 500.")
        return

    auth = ZkongAuth(request.user)
    batch_delete = BatchDelete(auth)

    result_message = batch_delete.execute_batch_delete(barcodes_to_delete)
    if 'successful' in result_message.lower():
        messages.success(request, result_message)
    else:
        messages.error(request, result_message)

batch_delete_from_zkong.short_description = "Supprimer les articles sélectionnés de Zkong"


def delete_locally_and_zkong(modeladmin, request, queryset):
    barcodes_to_delete = list(queryset.values_list('barCode', flat=True))

    if not barcodes_to_delete:
        messages.error(request, "Aucun article sélectionné pour suppression.")
        return

    if len(barcodes_to_delete) > 500:
        messages.error(request, "Le nombre d'articles dépasse la limite de 500.")
        return

    auth = ZkongAuth(request.user)
    batch_delete = BatchDelete(auth)

    result_message = batch_delete.execute_batch_delete(barcodes_to_delete)
    if 'successful' in result_message.lower():
        queryset.delete()
        messages.success(request, f"Articles supprimés de Zkong et localement: {result_message}")
    else:
        messages.error(request, f"Échec de la suppression sur Zkong: {result_message}")

delete_locally_and_zkong.short_description = "Supprimer les articles sélectionnés de Zkong et localement"


def batch_import_to_zkong(modeladmin, request, queryset):
    # Authentification
    auth = ZkongAuth(request.user)
    api = ZkongAPI(auth)

    # Préparation des données
    articles_to_import = []
    for obj in queryset:
        article_data = {
            "store_profile": obj.store_profile,
            "barCode": obj.barCode,
            "updated_at": obj.updated_at.isoformat() if obj.updated_at else None,
            "custFeature50": obj.custFeature50,
            "attrCategory": obj.attrCategory,
            "attrName": obj.attrName,
            "productCode": obj.productCode,
            "productSku": obj.productSku,
            "itemTitle": obj.itemTitle,
            "shortTitle": obj.shortTitle,
            "classLevel": obj.classLevel,
            "productArea": obj.productArea,
            "unit": obj.unit,
            "qrCode": obj.qrCode,
            "nfcUrl": obj.nfcUrl,
            "spec": obj.spec,
            "originalPrice": float(obj.originalPrice) if obj.originalPrice else None,
            "price": float(obj.price) if obj.price else None,
            "memberPrice": float(obj.memberPrice) if obj.memberPrice else None,
            "stock1": obj.stock1,
            "stock2": obj.stock2,
            "stock3": obj.stock3,
            "proStartTime": obj.proStartTime.isoformat() if obj.proStartTime else None,
            "proEndTime": obj.proEndTime.isoformat() if obj.proEndTime else None,
            "promotionText": obj.promotionText,
            "custFeature1": obj.custFeature1,
            "custFeature2": obj.custFeature2,
            "custFeature3": obj.custFeature3,
        }
        articles_to_import.append(article_data)

    # Envoi des données à l'API Zkong
    try:
        api.updated_articles = articles_to_import
        api.batch_import_updated_articles()
        messages.success(request, "Les articles sélectionnés ont été importés avec succès vers Zkong.")
    except Exception as e:
        messages.error(request, f"Une erreur s'est produite lors de l'importation : {e}")

batch_import_to_zkong.short_description = "Importer les articles sélectionnés vers Zkong"


def export_as_excel(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]

    # Convert datetime fields to naive datetimes (without timezone)
    df = pd.DataFrame(list(queryset.values(*field_names)))
    for field in df.select_dtypes(include=['datetime64[ns, UTC]']).columns:
        df[field] = df[field].dt.tz_localize(None)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename={meta}.xls'
    df.to_excel(response, index=False)
    return response

export_as_excel.short_description = "Exporter en fichier Excel"


def export_as_json(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename={meta}.json'
    df = pd.DataFrame(list(queryset.values(*field_names)))
    response.write(df.to_json(orient='records'))
    return response

export_as_json.short_description = "Exporter en fichier JSON"


def export_as_batchDelete_json(modeladmin, request, queryset):
    total_objects = queryset.count()
    objects_per_file = 2000
    total_files = (total_objects // objects_per_file) + (1 if total_objects % objects_per_file > 0 else 0)
    file_list = []

    user_profile = Corak_API_userProfile.objects.get(account=request.user)
    zkong_store_id = user_profile.zkong_store_id

    for file_num in range(total_files):
        start = file_num * objects_per_file
        end = start + objects_per_file
        barcodes = []

        for obj in queryset[start:end]:
            barcodes.append(obj.barCode)

        response_data = {
            "storeId": zkong_store_id,
            "list": barcodes
        }

        file_content = json.dumps(response_data, indent=4)
        file_list.append((f'batchDelete_{file_num + 1}.json', file_content))

    # Create a zip file in memory
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for file_name, file_content in file_list:
            zip_file.writestr(file_name, file_content)
    zip_buffer.seek(0)

    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=batchDelete_files.zip'
    return response

export_as_batchDelete_json.short_description = "Exporter les articles sélectionnés en batchDelete JSON (max 2000 par fichier)"


class ImportForm(forms.Form):
    excel_file = forms.FileField()


def import_from_excel(modeladmin, request):
    if 'apply' in request.POST:
        file = request.FILES['excel_file']
        df = pd.read_excel(file)
        for _, row in df.iterrows():
            Export2Zkong.objects.update_or_create(**row.to_dict())
        messages.success(request, "Les données ont été importées avec succès.")
        return HttpResponseRedirect(request.get_full_path())
    form = ImportForm()
    payload = {"form": form}
    return render(request, 'admin/import_form.html', payload)

import_from_excel.short_description = "Importer depuis un fichier Excel"


@admin.register(Export2Zkong)
class Export2ZkongAdmin(admin.ModelAdmin):
    list_display = [
        'store_profile',
        'barCode',
        'updated_at',
        'custFeature50',
        'attrCategory',
        'attrName',
        'productCode',
        'productSku',
        'itemTitle',
        'shortTitle',
        'classLevel',
        'productArea',
        'unit',
        'qrCode',
        'nfcUrl',
        'spec',
        'originalPrice',
        'price',
        'memberPrice',
        'stock1',
        'stock2',
        'stock3',
        'proStartTime',
        'proEndTime',
        'promotionText',
        'custFeature1',
        'custFeature2',
        'custFeature3',
    ]
    search_fields = ['itemTitle', 'barCode']
    list_filter = ['unit', 'store_profile', 'barCode', 'attrName']
    actions = [delete_locally, batch_delete_from_zkong, delete_locally_and_zkong, batch_import_to_zkong, export_as_excel, export_as_json, export_as_batchDelete_json, delete_all_products]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-excel/', self.admin_site.admin_view(import_from_excel))
        ]
        return my_urls + urls

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        user_profile = Corak_API_userProfile.objects.get(account=request.user)
        return qs.filter(store_profile__store_number=user_profile.store_number)


@admin.register(ZkongLog)
class ZkongLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'level', 'message']
    search_fields = ['message', 'level']
    list_filter = ['level', 'timestamp']
    actions = ['export_to_log_and_delete']


def export_to_log_and_delete(modeladmin, request, queryset):
    logger = logging.getLogger(__name__)
    for log in queryset:
        message = f"{log.timestamp} - {log.level} - {log.message}"
        logger.info(message)
        log.delete()

export_to_log_and_delete.short_description = "Exporter les logs sélectionnés vers un fichier et les supprimer"
