from rest_framework.response import Response
from rest_framework import status
from custom_user_management.models import Corak_API_userProfile

class StoreProfileAPIViewMixin(object):
    def get_store_profile(self, store_number):
        try:
            store_profile = Corak_API_userProfile.objects.get(store_number=store_number)
            print(f"Store profile trouvé pour {store_number}: {store_profile}")
            return store_profile
        except Corak_API_userProfile.DoesNotExist:
            print(f"Aucun store profile trouvé pour {store_number}")
            return None

    def get_serializer_context(self):
        context = super(StoreProfileAPIViewMixin, self).get_serializer_context()
        store_number = self.kwargs.get('store_number')
        store_profile = self.get_store_profile(store_number)
        if store_profile:
            context.update({'store_profile': store_profile})
        return context

    def assign_code_article_from_id(self, request_data):
        object_id = request_data.get('id')
        if object_id:
            request_data['code_article'] = object_id
        return request_data

    def create_or_update_object(self, serializer_class, request_data, store_profile):
        code_article = request_data.get('code_article')
        obj, created = serializer_class.Meta.model.objects.update_or_create(
            code_article=code_article,
            store_profile=store_profile,
            defaults=request_data
        )
        return obj, created
