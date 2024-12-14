from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from users.permissions import IsAdminUser
from .models import (
    Project,
    Stakeholder,
    CommissioningReport,
    OccupancyCertificate,
    ApprovedDrawings,
    Reports,
    User,
)
from .serializers import (
    ProjectSerializer,
    StakeholderSerializer,
    CommissioningReportSerializer,
    OccupancyCertificateSerializer,
    ApprovedDrawingsSerializer,
    ReportsSerializer,
)
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_permissions(self):
        if self.action in ['list', 'approve', 'reject']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Project.objects.all()
        return Project.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        project = self.get_object()
        project.status = 'approved'
        project.save()
        logger.info(f"Project {project.id} approved by admin {request.user.username}")
        return Response({"message": "Project approved successfully"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        project = self.get_object()
        project.status = 'rejected'
        project.save()
        logger.info(f"Project {project.id} rejected by admin {request.user.username}")
        return Response({"message": "Project rejected successfully"}, status=status.HTTP_200_OK)


class StakeholderViewSet(viewsets.ModelViewSet):
    queryset = Stakeholder.objects.all()
    serializer_class = StakeholderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Stakeholder.objects.all()
        return Stakeholder.objects.filter(project__created_by=self.request.user)


class ApprovedDrawingsViewSet(viewsets.ModelViewSet):
    queryset = ApprovedDrawings.objects.all()
    serializer_class = ApprovedDrawingsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return ApprovedDrawings.objects.all()
        return ApprovedDrawings.objects.filter(project__created_by=self.request.user)


class ReportsViewSet(viewsets.ModelViewSet):
    queryset = Reports.objects.all()
    serializer_class = ReportsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Reports.objects.all()
        return Reports.objects.filter(project__created_by=self.request.user)


class CommissioningReportViewSet(viewsets.ModelViewSet):
    queryset = CommissioningReport.objects.all()
    serializer_class = CommissioningReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return CommissioningReport.objects.all()
        return CommissioningReport.objects.filter(project__created_by=self.request.user)

    @action(detail=False, methods=['post'])
    def submit_rating(self, request):
        project_id = request.data.get("project_id")
        ratings = request.data.get("ratings")

        try:
            project = Project.objects.get(id=project_id)
            total_score = sum(ratings.values())
            avg_score = total_score / len(ratings)

            report = CommissioningReport.objects.create(
                project=project,
                created_by=request.user,
                rating=avg_score,
                details=ratings,
            )

            if avg_score >= 7:
                project.status = "ready for occupancy"
            else:
                project.status = "failed commissioning"
            project.save()

            return Response(
                {
                    "message": f"Rating submitted. Average Score: {avg_score:.2f}",
                    "status": project.status,
                },
                status=status.HTTP_200_OK,
            )

        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)


class OccupancyCertificateViewSet(viewsets.ModelViewSet):
    queryset = OccupancyCertificate.objects.all()
    serializer_class = OccupancyCertificateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return OccupancyCertificate.objects.all()
        return OccupancyCertificate.objects.filter(project__created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def issue_certificate(self, request, pk=None):
        project = self.get_object()
        if project.status != "ready for occupancy":
            return Response({"error": "Project is not ready for occupancy"}, status=status.HTTP_400_BAD_REQUEST)

        certificate = OccupancyCertificate.objects.create(
            project=project,
            uploaded_by=request.user,
            certificate_file=request.data.get("certificate_file"),
        )

        logger.info(f"Certificate issued for project {project.id} by admin {request.user.username}")
        return Response({"message": "Occupancy certificate issued successfully"}, status=status.HTTP_200_OK)
