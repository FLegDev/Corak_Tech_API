from django.urls import path
from .views import FileUploadView



urlpatterns = [
       path('monoprix_fr_<str:store_number>/items', FileUploadView.as_view(), name='API_ITEMS'),
    #path('stores/<str:store_number>/upload/', FileUploadView.as_view(), name='file-upload'),

]
