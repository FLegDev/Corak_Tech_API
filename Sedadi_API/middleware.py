import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('swagger')

class SwaggerLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_request(self, request):
        logger.debug(f"Swagger accessed: {request.path}")