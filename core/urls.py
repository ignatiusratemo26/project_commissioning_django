from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, StakeholderViewSet, CommissioningReportViewSet, OccupancyCertificateViewSet, UserViewSet
from rest_framework_simplejwt.views import TokenRefreshView
from core.views import CustomTokenObtainPairView

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('projects', ProjectViewSet)
router.register('stakeholders', StakeholderViewSet)
router.register('reports', CommissioningReportViewSet)
router.register('certificates', OccupancyCertificateViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserViewSet.as_view({'post': 'register'}), name='register'),

]
