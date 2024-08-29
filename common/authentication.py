import logging
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token

logger = logging.getLogger(__name__)

class CustomTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        # Obtenez le token de l'en-tête personnalisé au lieu de l'en-tête 'Authorization'
        token_key = request.headers.get('Ocp-Apim-Subscription-Key')
        logger.info(f"Received token key: {token_key}")
        
        if not token_key:
            return None
        
        return self.authenticate_credentials(token_key)

    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            logger.error("Invalid token")
            raise AuthenticationFailed('Invalid token')
        
        if not token.user.is_active:
            logger.error("User inactive or deleted")
            raise AuthenticationFailed('User inactive or deleted')
        
        return (token.user, token)
