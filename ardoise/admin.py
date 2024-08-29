from django.contrib import admin
from .models import Certificates, CustomDetail, Product

# Personnalisation pour Certificate
@admin.register(Certificates)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('store_profile', 'code_article', 'updated_at', 'fairTrade', 'organic', 'environmentallyFriendly',)
    search_fields = ('store_profile','code_article', 'updated_at',)
    list_filter = ('store_profile', 'fairTrade', 'organic', 'environmentallyFriendly','updated_at',)

# Personnalisation pour CustomDetail
@admin.register(CustomDetail)
class CustomDetailAdmin(admin.ModelAdmin):
    list_display = ('store_profile', 'code_article', 'updated_at', 'libelle_cr_auto', 'libelle_lg_auto', 'geeti1_auto', 'promo_gold_auto', 'type_auto', 'traitement_auto', 'conditionnement_auto')
    search_fields = ('code_article', 'store_profile', 'libelle_lg_auto', 'updated_at', 'promo_gold_auto',)
    list_filter = ('store_profile', 'type_auto', 'traitement_auto', 'updated_at','promo_gold_auto')

# Personnalisation pour Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('store_profile', 'code_article', 'updated_at', 'get_price', 'get_capacity', 'get_unit_price_unit', 'get_currency', 'get_custom', 'get_certificates',)
    search_fields = ('store_profile', 'code_article', 'updated_at', 'detail__libelle_cr_auto', 'detail__libelle_lg_auto',)
    list_filter = ('store_profile', 'unitPriceUnit', 'updated_at', 'currency',)

    def get_price(self, obj):
        return obj.price
    get_price.short_description = 'Prix'

    def get_capacity(self, obj):
        return obj.capacity
    get_capacity.short_description = 'Capacité'

    def get_unit_price_unit(self, obj):
        return obj.unitPriceUnit
    get_unit_price_unit.short_description = 'Unité de prix unitaire'

    def get_currency(self, obj):
        return obj.currency
    get_currency.short_description = 'Devise'

    def get_custom(self, obj):
        if obj.custom:
            return f"{obj.custom.libelle_cr_auto}, {obj.custom.libelle_lg_auto}"
        return "Pas d'objet Custom"
    get_custom.short_description = 'Détails personnalisés'

    def get_certificates(self, obj):
        if obj.certificates:
            return f"Commerce équitable: {obj.certificates.fairTrade}, Bio: {obj.certificates.organic}, Éco-responsable: {obj.certificates.environmentallyFriendly}"
        return "Pas de certificats"
    get_certificates.short_description = 'Certificat'

# Personnalisation pour Ardoise
