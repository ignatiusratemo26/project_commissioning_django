from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProjectViewSet,
    StakeholderViewSet,
    ApprovedDrawingsViewSet,
    CommissioningReportViewSet,
    OccupancyCertificateViewSet,
    NotificationViewSet,
)

# Initialize router for automatic URL routing
router = DefaultRouter()

# Register viewsets with the router
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'stakeholders', StakeholderViewSet, basename='stakeholder')
router.register(r'approved-drawings', ApprovedDrawingsViewSet, basename='approveddrawings')
router.register(r'commissioning-reports', CommissioningReportViewSet, basename='commissioningreport')
router.register(r'occupancy-certificates', OccupancyCertificateViewSet, basename='occupancycertificate')
router.register(r'notifications', NotificationViewSet, basename='notification')

# Include all registered routes in the urlpatterns
urlpatterns = [
    path('', include(router.urls)),
]
