from rest_framework import serializers
from .models import Project, Stakeholder, CommissioningReport, OccupancyCertificate, ApprovedDrawings

from rest_framework import serializers
from django.contrib.auth import get_user_model
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

UserModel = get_user_model()

class StakeholderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stakeholder
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['created_by']


class CommissioningReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommissioningReport
        fields = '__all__'


class OccupancyCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OccupancyCertificate
        fields = '__all__'

class ApprovedDrawingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovedDrawings
        fields = '__all__'
