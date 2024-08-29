from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

class CustomAuthMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Vérifiez si la réponse est une erreur d'authentification ou de permission
        if response.status_code in [201, 401, 403, 405]:
            # Récupère les valeurs d'en-tête
            auth_header = request.headers.get('Authorization', 'Aucun')
            ocp_apim_key = request.headers.get('Ocp-Apim-Subscription-Key', 'Aucun')
            user_agent = request.headers.get('User-Agent', 'Inconnu')
            accept = request.headers.get('Accept', 'Inconnu')
            host = request.headers.get('Host', 'Inconnu')
            accept_encoding = request.headers.get('Accept-Encoding', 'Inconnu')
            connection = request.headers.get('Connection', 'Inconnu')
            content_type = request.headers.get('Content-Type', 'Inconnu')
            content_length = request.headers.get('Content-Length', 'Inconnu')

            # Construit le contenu modifié de la réponse
            new_content = {
                'error': 'Authentication or permission error',
                'status_code': response.status_code,
                'headers': {
                    'Authorization': auth_header,
                    'Ocp-Apim-Subscription-Key': ocp_apim_key,
                    'User-Agent': user_agent,
                    'Accept': accept,
                    'Host': host,
                    'Accept-Encoding': accept_encoding,
                    'Connection': connection,
                    'Content-Type': content_type,
                    'Content-Length': content_length
                }
            }
            return JsonResponse(new_content, status=response.status_code)

        return response
