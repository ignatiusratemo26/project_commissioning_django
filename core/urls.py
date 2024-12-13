from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, StakeholderViewSet, CommissioningReportViewSet, OccupancyCertificateViewSet
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register('projects', ProjectViewSet)
router.register('stakeholders', StakeholderViewSet)
router.register('reports', CommissioningReportViewSet)
router.register('certificates', OccupancyCertificateViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
