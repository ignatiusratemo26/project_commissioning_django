from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, StakeholderViewSet, CommissioningReportViewSet, OccupancyCertificateViewSet

router = DefaultRouter()
router.register('projects', ProjectViewSet)
router.register('stakeholders', StakeholderViewSet)
router.register('reports', CommissioningReportViewSet)
router.register('certificates', OccupancyCertificateViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
]
