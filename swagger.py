from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf.urls.static import static
from django.conf import settings
from .filters import CustomOpenAPISchemaGenerator  # Importez votre filtre personnalisé

schema_view = get_schema_view(
    openapi.Info(
        title="API_Corak ESL",
        default_version='v1',
        description="API pour ESL",
        terms_of_service="URL des termes de service",
        contact=openapi.Contact(email="contact@monapi.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny,],
    generator_class=CustomOpenAPISchemaGenerator,  # Utilisez le filtre personnalisé ici
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ardoise/monoprix/', include('ardoise.ardoise_urls')),
    path('api_items/stores/', include('API_ITEMS.API_ITEMS_urls')),
    path('api/stores/', include('API_FILES.API_FILES_urls')),
    path('api/stores/', include('common.urls')),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)