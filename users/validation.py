from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

UserModel = get_user_model()

def custom_validation(data): 
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    # Check if email exists
    if not username or UserModel.objects.filter(username=username).exists():
        raise ValidationError('choose another email')

    # Check if password is valid
    if not password or len(password) < 8:
        raise ValidationError('choose another password, min 8 characters')

    return data
