from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

app_name = 'API_ITEMS'

urlpatterns = [
    path('monoprix_fr_<str:store_number>/items/', views.ProductListView.as_view(), name='item-list-create'),
    path('monoprix_fr_<str:store_number>/items/<int:pk>/', views.ProductRetrieveUpdateDestroyView.as_view(), name='item-retrieve-update-destroy'),
    path('monoprix_fr_<str:store_number>/customs/', views.CustomListView.as_view(), name='custom-list-create'),
    path('monoprix_fr_<str:store_number>/customs/<int:pk>/', views.CustomRetrieveUpdateDestroyView.as_view(), name='custom-retrieve-update-destroy'),
    path('monoprix_fr_<str:store_number>/promotions/', views.PromotionListView.as_view(), name='promotion-list-create'),
    path('monoprix_fr_<str:store_number>/promotions/<int:pk>/', views.PromotionRetrieveUpdateDestroyView.as_view(), name='promotion-retrieve-update-destroy'),
    path('monoprix_fr_<str:store_number>/receive_api_data/', views.ProductListView.as_view(), name='receive_api_data'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
