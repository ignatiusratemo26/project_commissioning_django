from rest_framework import serializers
from .models import Project, Stakeholder, CommissioningReport, OccupancyCertificate, User

from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

UserModel = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = '__all__'
        
        def create(self, clean_data):
            user = UserModel.objects.create_user(
                email=clean_data['email'],
                password=clean_data['password']
            )
            user.save()
            refresh = RefreshToken.for_user(user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                **clean_data
            }

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        """
        Validate user credentials.
        """
        email = data.get('email')
        password = data.get('password')

        # Attempt to authenticate
        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        
        # Attach user to validated_data for later use
        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['email','password', 'username' 'phone_number', 'first_name', 'last_name']

        
        
class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=True, min_length=8)

    def validate(self, data):
        """
        Check that the two password entries match.
        """
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
    

class StakeholderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stakeholder
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    stakeholders = StakeholderSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'


class CommissioningReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommissioningReport
        fields = '__all__'


class OccupancyCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OccupancyCertificate
        fields = '__all__'
