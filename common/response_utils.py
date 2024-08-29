import logging
from django.http import JsonResponse
from django.utils import timezone

logger = logging.getLogger('common')

def log_request(request, response):
    # Détermine le nom de l'application à partir des noms de fichiers de log
    application_name = get_application_name_from_logfile()
    level = 'INFO' if response.status_code < 400 else 'ERROR'
    message = f"Request {request.method} {request.get_full_path()} returned status {response.status_code}"

# Remplacer 'COMMON' par 'jsonRequests'
    if application_name == 'COMMON':
        application_name = 'jsonRequests'

    LogEntry.objects.create(
        application=application_name,
        level=level,
        message=message,
        timestamp=timezone.now()
    )

def get_application_name_from_logfile():
    # Liste des fichiers de log
    log_files = {
        'api_files.log': 'API_FILES',
        'api_items.log': 'API_ITEMS',
        'ardoise.log': 'Ardoise',
        'celery_tasks.log': 'Celery Tasks',
        'celery.log': 'Celery',
        'common.log': 'jsonRequests',
        'corak_esl.log': 'Corak_ESL',
        'custom_user_management.log': 'Custom User Management',
        'django_error.log': 'Django Error',
        'django.log': 'Django',
    }
    for handler in logger.handlers:
        for log_file, app_name in log_files.items():
            if handler.baseFilename.endswith(log_file):
                return app_name
    return 'unknown'

def build_response(status_code, message, request=None):
    response_data = {
        'status_code': status_code,
        'message': message,
    }

    if request and status_code in [400, 401, 403]:
        response_data['headers'] = {
            'Authorization': request.headers.get('Authorization', 'Aucun'),
            'Ocp-Apim-Subscription-Key': request.headers.get('Ocp-Apim-Subscription-Key', 'Aucun'),
            'User-Agent': request.headers.get('User-Agent', 'Inconnu'),
            'Accept': request.headers.get('Accept', 'Inconnu'),
            'Host': request.headers.get('Host', 'Inconnu'),
            'Accept-Encoding': request.headers.get('Accept-Encoding', 'Inconnu'),
            'Connection': request.headers.get('Connection', 'Inconnu'),
            'Content-Type': request.headers.get('Content-Type', 'Inconnu'),
            'Content-Length': request.headers.get('Content-Length', 'Inconnu'),
        }

    return JsonResponse(response_data, status=status_code)

def response_201(request, message="Created"):
    return build_response(201, message, request)

def response_401(request, message="Unauthorized"):
    return build_response(401, message, request)

def response_402(request, message="Payment Required"):
    return build_response(402, message, request)

def response_403(request, message="Forbidden"):
    return build_response(403, message, request)

def response_404(request, message="Not Found"):
    return build_response(404, message, request)

def response_500(request, message="Internal Server Error"):
    return build_response(500, message, request)

def response_502(request, message="Bad Gateway", exception=None):
    return build_response(502, message, request, exception)

def response_503(request, message="Service Unavailable"):
    return build_response(503, message, request)

def response_400(request, message="Bad Request"):
    return build_response(400, message, request)

