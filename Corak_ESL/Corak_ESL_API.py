# Corak_ESL_API.py

import os
import json
import requests
from datetime import datetime, timedelta
from decimal import Decimal
import dotenv
from custom_user_management.models import Corak_API_userProfile
import logging

logger = logging.getLogger('corak_esl')

dotenv.load_dotenv()

class ZkongAuth:
    def __init__(self, user):
        self.user_profile = Corak_API_userProfile.objects.get(account=user)
        self.account = self.user_profile.zkong_user_name
        self.password = self.user_profile.zkong_user_password
        self.login_type = 3
        self.token = None
        self.token_expiry = datetime.now()

    def login(self):
        data = {
            "account": self.account,
            "password": self.password,
            "loginType": self.login_type
        }
        try:
            response = requests.post(f"{self.user_profile.zkong_base_url}{self.user_profile.zkong_login_endpoint}", json=data)
            response.raise_for_status()
            response_data = response.json()
            if response_data.get("success"):
                self.token = response_data["data"]["token"]
                self.token_expiry = datetime.now() + timedelta(hours=1)
        except requests.exceptions.RequestException as e:
            logger.error(f"Login request failed: {e}")
            raise

    def get_token(self):
        if self.token is None or datetime.now() >= self.token_expiry:
            self.login()
        return self.token


class ZkongAPI:
    def __init__(self, auth):
        self.auth = auth
        self.user_profile = auth.user_profile
        self.updated_articles = []

    def is_token_valid(self):
        return self.auth.token is not None and datetime.now() < self.auth.token_expiry

    def get_auth_headers(self):
        return {
            "Authorization": f"{self.auth.get_token()}",
            "Content-Type": "application/json;charset=utf-8"
        }

    def add_updated_article(self, article_data):
        if isinstance(article_data, str):
            article_data = json.loads(article_data)

        for key, value in article_data.items():
            if isinstance(value, Decimal):
                article_data[key] = float(value)

        self.updated_articles.append(article_data)

    def batch_import_updated_articles(self):
        if not self.updated_articles:
            logger.info("Pas de mises à jour à traiter.")
            return

        if not self.is_token_valid():
            logger.info("Token not valid, logging in...")
            self.auth.login()

        batch_size = 20000
        for i in range(0, len(self.updated_articles), batch_size):
            batch = self.updated_articles[i:i+batch_size]

            data = {
                "agencyId": self.user_profile.zkong_agency_id,
                "merchantId": self.user_profile.zkong_merchant_id,
                "storeId": self.user_profile.zkong_store_id,
                "unitName": 1,
                "itemList": batch
            }

            logger.info(f"Sending batch {i // batch_size + 1} to Zkong API with data: {json.dumps(data, default=decimal_default)}")

            data_json = json.dumps(data, default=decimal_default)
            headers = self.get_auth_headers()

            try:
                response = requests.post(f"{self.user_profile.zkong_base_url}{self.user_profile.zkong_batch_import_endpoint}",
                                         data=data_json,
                                         headers=headers)
                response.raise_for_status()
                response_data = response.json()
                if response_data.get("success"):
                    logger.info(f"Importation par lots réussie pour le lot {i // batch_size + 1}.")
                else:
                    logger.error(f"Échec de l'importation par lots pour le lot {i // batch_size + 1}: {response_data.get('message')}")
            except requests.exceptions.RequestException as e:
                logger.error(f"Erreur lors de l'importation par lots pour le lot {i // batch_size + 1}: {e}")

class BatchDelete:
    def __init__(self, auth):
        self.auth = auth
        self.user_profile = auth.user_profile

    def get_auth_headers(self):
        return {
            "Authorization": f"{self.auth.get_token()}",
            "Content-Type": "application/json;charset=utf-8"
        }

    def execute_batch_delete(self, barcodes_to_delete):
        if not barcodes_to_delete:
            return "Aucun article à supprimer."

        if len(barcodes_to_delete) > 500:
            return "Le nombre d'articles dépasse la limite de 500."

        data = {
            "storeId": self.user_profile.zkong_store_id,
            "list": barcodes_to_delete
        }
        headers = self.get_auth_headers()

        data_json = json.dumps(data)
        logger.info(f"Requête de suppression en lot envoyée: {data_json}")

        try:
            response = requests.delete(f"{self.user_profile.zkong_base_url}{self.user_profile.zkong_batch_delete_endpoint}",
                                       headers=headers, data=data_json)
            response.raise_for_status()
            response_data = response.json()

            logger.info(f"Réponse de la suppression en lot: {response_data}")

            if response_data.get('success'):
                barcodes_to_delete.clear()
                return "Batch delete successful."
            else:
                return f"Batch delete failed: {response_data.get('message', 'No message')}."
        except requests.exceptions.RequestException as e:
            barcodes_to_delete.clear()
            return f"An error occurred: {e}"

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)

def export_updated_articles_to_zkong(user):
    auth = ZkongAuth(user)
    api = ZkongAPI(auth)

    updated_articles = Export2Zkong.objects.filter(store_profile=auth.user_profile).values()

    for article_data in updated_articles:
        api.add_updated_article(article_data)

    api.batch_import_updated_articles()
