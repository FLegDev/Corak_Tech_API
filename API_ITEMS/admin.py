from django.contrib import admin
from .models import Custom, Promotion, RefreshSchedule, Product

class CustomInline(admin.StackedInline):
    model = Custom
    can_delete = False
    readonly_fields = (
        'code_article', 'ADV_ID', 'updated_at', 'ADVCOND_CODE', 'ADVCARACT_MIN', 'CSTTOT_KEY',
        'ADVTYPE_ID', 'BINID', 'ADV_ACTIVE', 'DATE_EXTRACT', 'ADV_PROFIL', 'ADVCARACT_AMOUNT'
    )

class PromotionInline(admin.StackedInline):
    model = Promotion
    can_delete = False
    readonly_fields = ('code_article', 'updated_at', 'start', 'end',)

class RefreshScheduleInline(admin.StackedInline):
    model = RefreshSchedule
    can_delete = False
    readonly_fields = ('code_article', 'updated_at', 'date')

@admin.register(Custom)
class CustomAdmin(admin.ModelAdmin):
    list_display = (
        'store_profile','code_article','updated_at', 'ADV_ID', 'ADVCOND_CODE', 'ADVCARACT_MIN', 'CSTTOT_KEY',
        'ADVTYPE_ID', 'BINID', 'ADV_ACTIVE', 'DATE_EXTRACT', 'ADV_PROFIL', 'ADVCARACT_AMOUNT'
    )
    list_filter = ['store_profile','code_article']
    search_fields = ['code_article', 'store_profile']

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('store_profile', 'code_article','updated_at', 'start', 'end')
    list_filter = ['store_profile','code_article']
    search_fields = ['code_article', 'store_profile']

@admin.register(RefreshSchedule)
class RefreshScheduleAdmin(admin.ModelAdmin):
    list_display = ('store_profile', 'code_article', 'updated_at', 'date')
    list_filter = ['store_profile', 'code_article']
    search_fields = ['code_article', 'store_profile']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'store_profile',
        'code_article',
        'updated_at',
        'promo_message',
        'promo_condition',
        'promo_fid_card_message',
        'promo_mixing_message',
        'get_adv_id',
        'get_advcond_code',
        'get_advcaract_min',
        'get_csttot_key',
        'get_advtype_id',
        'get_binid',
        'get_adv_active',
        'get_date_extract',
        'get_adv_profil',
        'get_advcaract_amount',
        'get_promotion_start',
        'get_promotion_end',
    )
    list_filter = ['store_profile', 'code_article']
    search_fields = ['code_article', 'store_profile']
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        inlines = []
        if obj.custom:
            inlines.append(CustomInline(self.model, self.admin_site))
        if obj.promotion:
            inlines.append(PromotionInline(self.model, self.admin_site))
        if obj.refresh_schedules.exists():
            inlines.append(RefreshScheduleInline(self.model, self.admin_site))
        return inlines

    # Custom fields methods
    def get_adv_id(self, obj):
        return obj.custom.ADV_ID if obj.custom else "N/A"
    get_adv_id.short_description = "ADV_ID"

    def get_advcond_code(self, obj):
        return obj.custom.ADVCOND_CODE if obj.custom else "N/A"
    get_advcond_code.short_description = "ADVCOND_CODE"

    def get_advcaract_min(self, obj):
        return obj.custom.ADVCARACT_MIN if obj.custom else "N/A"
    get_advcaract_min.short_description = "ADVCARACT_MIN"

    def get_csttot_key(self, obj):
        return obj.custom.CSTTOT_KEY if obj.custom else "N/A"
    get_csttot_key.short_description = "CSTTOT_KEY"

    def get_advtype_id(self, obj):
        return obj.custom.ADVTYPE_ID if obj.custom else "N/A"
    get_advtype_id.short_description = "ADVTYPE_ID"

    def get_binid(self, obj):
        return obj.custom.BINID if obj.custom else "N/A"
    get_binid.short_description = "BINID"

    def get_adv_active(self, obj):
        return obj.custom.ADV_ACTIVE if obj.custom else "N/A"
    get_adv_active.short_description = "ADV_ACTIVE"

    def get_date_extract(self, obj):
        return obj.custom.DATE_EXTRACT if obj.custom else "N/A"
    get_date_extract.short_description = "DATE_EXTRACT"

    def get_adv_profil(self, obj):
        return obj.custom.ADV_PROFIL if obj.custom else "N/A"
    get_adv_profil.short_description = "ADV_PROFIL"

    def get_advcaract_amount(self, obj):
        return obj.custom.ADVCARACT_AMOUNT if obj.custom else "N/A"
    get_advcaract_amount.short_description = "ADVCARACT_AMOUNT"

    # Promotion fields methods
    def get_promotion_start(self, obj):
        return obj.promotion.start if obj.promotion else "N/A"
    get_promotion_start.short_description = "Start"

    def get_promotion_end(self, obj):
        return obj.promotion.end if obj.promotion else "N/A"
    get_promotion_end.short_description = "End"
