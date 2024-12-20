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
    ApprovedDrawings
)
from .serializers import (
    ProjectSerializer,
    StakeholderSerializer,
    CommissioningReportSerializer,
    OccupancyCertificateSerializer,
    ApprovedDrawingsSerializer,
)
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'approve', 'reject']:
            self.permission_classes = [IsAuthenticated]
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

    def get_permissions(self):
        # Allow anyone to view the list of stakeholders
        if self.action == 'list':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        """
        Override to allow filtering stakeholders by project query parameter.
        Example: /stakeholders/?project=<project_id>
        """
        project_id = self.request.query_params.get("project")
        queryset = Stakeholder.objects.all()

        if project_id:
            queryset = queryset.filter(project_id=project_id)

        # Admins can see everything; others are restricted
        if self.request.user.is_authenticated and self.request.user.role != 'admin':
            queryset = queryset.filter(project__created_by=self.request.user)

        return queryset

class ApprovedDrawingsViewSet(viewsets.ModelViewSet):
    queryset = ApprovedDrawings.objects.all()
    serializer_class = ApprovedDrawingsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter ApprovedDrawings based on user role.
        """
        if self.request.user.role == 'admin':
            return ApprovedDrawings.objects.all()
        return ApprovedDrawings.objects.filter(project__created_by=self.request.user)

    def perform_create(self, serializer):
        """
        Override to save the ApprovedDrawings and update the project's approved_docs field.
        """
        approved_drawings = serializer.save()  # Save the uploaded drawings instance
        project = approved_drawings.project   # Get the associated project

        # Update the project's approved_docs field with the file paths
        project.approved_docs.update({
            "architectural": approved_drawings.architectural.url if approved_drawings.architectural else '',
            "structural": approved_drawings.structural.url if approved_drawings.structural else '',
            "proposed_sewer": approved_drawings.proposed_sewer.url if approved_drawings.proposed_sewer else '',
            "proposed_water": approved_drawings.proposed_water.url if approved_drawings.proposed_water else '',
            "proposed_electricity": approved_drawings.proposed_electricity.url if approved_drawings.proposed_electricity else '',
        })
        project.save()

    def perform_update(self, serializer):
        """
        Handle updates to ApprovedDrawings and sync with the project's approved_docs.
        """
        approved_drawings = serializer.save()
        project = approved_drawings.project

        # Update the approved_docs field with the updated file paths
        project.approved_docs.update({
            "architectural": approved_drawings.architectural.url if approved_drawings.architectural else '',
            "structural": approved_drawings.structural.url if approved_drawings.structural else '',
            "proposed_sewer": approved_drawings.proposed_sewer.url if approved_drawings.proposed_sewer else '',
            "proposed_water": approved_drawings.proposed_water.url if approved_drawings.proposed_water else '',
            "proposed_electricity": approved_drawings.proposed_electricity.url if approved_drawings.proposed_electricity else '',
        })
        project.save()


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
    
    @action(detail=False, methods=['get'], url_path='by-project')
    def get_by_project(self, request):
        """
        Retrieve the occupancy certificate for a given project ID.
        """
        project_id = request.query_params.get('project_id')

        if not project_id:
            return Response({"error": "Project ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            certificate = OccupancyCertificate.objects.get(project_id=project_id)
            serializer = self.get_serializer(certificate)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except OccupancyCertificate.DoesNotExist:
            return Response({"error": "Occupancy certificate not found for the given project."},
                            status=status.HTTP_404_NOT_FOUND)
