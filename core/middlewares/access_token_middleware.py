from django.utils.deprecation import MiddlewareMixin
import logging

class AccessTokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path == '/api/register/': 
            return
        access_token = request.COOKIES.get('access_token')
        if access_token:
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
