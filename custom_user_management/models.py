from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Corak_API_userProfile(models.Model) :

    account = models.OneToOneField(User, on_delete=models.CASCADE)

    # Ajoutez vos champs supplémentaires ici
    store_name = models.CharField(max_length=255, blank=True, null=True)
    store_address = models.CharField(max_length=255, blank=True, null=True)
    store_number = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    corak_id = models.CharField(max_length=100, blank=True, null=True)

    # Pour la connexion à l'API ESL
    esl_api_key = models.CharField(max_length=255, blank=True, null=True)
    zkong_public_key = models.CharField(max_length=255, blank=True, null=True)
    zkong_base_url = models.CharField(max_length=255, blank=True, null=True, default="https://esl-eu.zkong.com")
    zkong_user_name = models.CharField(max_length=30, blank=True, null=True)
    zkong_user_password = models.CharField(max_length=255, blank=True, null=True)

    # Info préalables aux requêtes
    zkong_agency_id = models.CharField(max_length=255, blank=True, null=True)
    zkong_merchant_id = models.CharField(max_length=255, blank=True, null=True)
    zkong_store_id = models.CharField(max_length=255, blank=True, null=True)
    zkong_crypted_password =  models.CharField(max_length=255, blank=True, null=True)
    zkong_authorization =   models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Endpoints
    zkong_login_endpoint = models.CharField(max_length=255, blank=True, null=True, default="/zk/user/login")
    zkong_batch_import_endpoint = models.CharField(max_length=255, blank=True, null=True, default="/zk/item/batchImportItem")
    zkong_batch_delete_endpoint = models.CharField(max_length=255, blank=True, null=True, default="/zk/item/batchDeleteItem")
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        # Utilisez l'attribut que vous souhaitez pour représenter cet utilisateur
        # Par exemple, si vous souhaitez utiliser le nom associé au compte utilisateur :
        return self.account.get_full_name() or self.account.username