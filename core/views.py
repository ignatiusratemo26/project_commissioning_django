from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from permissions import IsAdminUser
from .models import Project, Stakeholder, CommissioningReport, OccupancyCertificate
from .serializers import ProjectSerializer, StakeholderSerializer, CommissioningReportSerializer, OccupancyCertificateSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

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
