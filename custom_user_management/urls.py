from django.urls import path
from .views import UserApiKeyView

urlpatterns = [
    # ... vos autres URL ...
    path('api/user/api-key/', UserApiKeyView.as_view(), name='user-api-key'),
]
