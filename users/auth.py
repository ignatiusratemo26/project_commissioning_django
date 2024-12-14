import jwt
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.settings import api_settings

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
         # Skip authentication for the register endpoint
        if request.path == '/users-api/register/': 
            return None
        header = self.get_header(request)
        if header is None:
            raw_token = request.COOKIES.get('access_token')
        else:
            raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
    
    def get_validated_token(self, raw_token):
        try:
            return UntypedToken(raw_token)
        except TokenError as e:
            raise InvalidToken(str(e))
