from rest_framework import serializers
from .models import Project, Stakeholder, CommissioningReport, OccupancyCertificate, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

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
