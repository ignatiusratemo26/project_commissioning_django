from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from users.permissions import IsAdminUser
from .models import Project, Stakeholder, CommissioningReport, OccupancyCertificate, User
from .serializers import ProjectSerializer, StakeholderSerializer, CommissioningReportSerializer, OccupancyCertificateSerializer
import logging
from rest_framework.views import APIView

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    # permission_classes = [IsAuthenticated, IsAdminUser]
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class StakeholderViewSet(viewsets.ModelViewSet):
    queryset = Stakeholder.objects.all()
    serializer_class = StakeholderSerializer
    permission_classes = [IsAuthenticated]


class CommissioningReportViewSet(viewsets.ModelViewSet):
    queryset = CommissioningReport.objects.all()
    serializer_class = CommissioningReportSerializer
    permission_classes = [IsAuthenticated]


class OccupancyCertificateViewSet(viewsets.ModelViewSet):
    queryset = OccupancyCertificate.objects.all()
    serializer_class = OccupancyCertificateSerializer
    permission_classes = [IsAuthenticated]
