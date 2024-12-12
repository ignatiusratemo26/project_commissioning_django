from rest_framework.authtoken.models import Token
from core.models import User

user = User.objects.get(username='your_username')
token, created = Token.objects.get_or_create(user=user)
print(token.key)
