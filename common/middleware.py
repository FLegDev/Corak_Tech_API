import logging
from django.core.management import call_command
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class LoadLogsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Call the load_logs command
        try:
            call_command('load_logs')
        except Exception as e:
            logger.error(f"Error loading logs: {e}")

        response = self.get_response(request)
        return response


class SwaggerLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/swagger') or request.path.startswith('/swagger/'):
            logger.debug(f'Swagger accessed: {request.path}')
        return None