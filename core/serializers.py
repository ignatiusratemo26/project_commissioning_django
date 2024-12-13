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
