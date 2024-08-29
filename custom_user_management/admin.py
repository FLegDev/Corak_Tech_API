from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from custom_user_management.models import Corak_API_userProfile
from django.utils.safestring import mark_safe  # Import pour afficher les images dans l'admin

class CustomUserProfileInline(admin.StackedInline):

        model =Corak_API_userProfile



class CorakAPIUserAdmin(UserAdmin):

    inlines = (CustomUserProfileInline, )

    def get_store_number(self, obj):
        # Assurez-vous que le profil utilisateur lié existe pour éviter les erreurs
        if hasattr(obj, 'corak_api_userprofile'):
            return obj.corak_api_userprofile.store_number
        return None
    get_store_number.short_description = 'Numéro de magasin'  # Optionnel: Définit le nom de la colonne
# Incluez la méthode dans list_display
    list_display = ('username', 'get_store_number', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ['username', 'email', 'group']

fieldsets = (
        ('Informations personnelles', {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
        # Ajoutez d'autres fieldsets selon vos besoins
        ('Informations Magasin,', {'fields': ('store_group','store_name', 'store_address', 'store_number', 'phone_number',
                                              'email', 'postal_code', 'store_address', 'city', 'corak_id')}),

)

admin.site.unregister(User)
admin.site.register(User, CorakAPIUserAdmin,)

# Register your models here.
