from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, StakeholderViewSet, CommissioningReportViewSet, OccupancyCertificateViewSet, UserViewSet, MyTokenObtainPairView, UserRegister, UserLogin
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('projects', ProjectViewSet)
router.register('stakeholders', StakeholderViewSet)
router.register('reports', CommissioningReportViewSet)
router.register('certificates', OccupancyCertificateViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegister.as_view(), name= 'user-register'),
    path('login/', UserLogin.as_view(), name='user-login')

]
