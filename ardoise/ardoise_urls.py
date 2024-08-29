from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('<str:store_number>/products/', views.ProductListView.as_view(), name='product-list-create'),
    path('stores/<str:store_number>/products/<int:pk>/', views.ProductRetrieveUpdateDestroyView.as_view(), name='ardoiseProduct-retrieve-update-destroy'),
    path('stores/<str:store_number>/customdetails/', views.CustomDetailListCreateView.as_view(), name='customdetail-list-create'),
    path('stores/<str:store_number>/customdetails/<int:pk>/', views.CustomDetailDetailView.as_view(), name='customdetail-retrieve-update-destroy'),
    path('stores/<str:store_number>/certificates/', views.CertificateListCreateView.as_view(), name='certificate-list-create'),
    path('stores/<str:store_number>/certificates/<int:pk>/', views.CertificateDetailView.as_view(), name='certificate-retrieve-update-destroy'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
