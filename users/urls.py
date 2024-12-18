from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserViewSet, UserLogout

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserViewSet.as_view({'post':'register'}), name='register'),
    path('logout/', UserLogout.as_view(), name='user-logout'),

]
