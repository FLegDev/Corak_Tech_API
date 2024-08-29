from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views


urlpatterns = [
    path('monoprix_fr_<str:store_number>/items/files/monoprix_fr_<str:contremarque>.eeg', views.FileUploadView.as_view(), name='API_FILES'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
