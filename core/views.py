from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from core.permissions import IsAdminUser
from .models import Project, Stakeholder, CommissioningReport, OccupancyCertificate, User
from .serializers import ProjectSerializer, StakeholderSerializer, CommissioningReportSerializer, OccupancyCertificateSerializer, UserSerializer
from django.conf import settings
from rest_framework_simplejwt.settings import api_settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework.decorators import api_view
import logging
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.middleware.csrf import get_token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import MyTokenObtainPairSerializer, UserLoginSerializer, UserRegisterSerializer, PasswordSerializer
from .validation import custom_validation

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):

    serializer_class = UserSerializer
    permission_classes=[IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        # Return only the currently authenticated user's details
        return User.objects.filter(id=self.request.user.id)
    
    def list(self, request, *args, **kwargs):
        """
        Override the list method to return only the current user's data without pagination.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post', 'put'])
    def set_password(self, request, *args, **kwargs):
        user = self.request.user
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRegister(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        clean_data = custom_validation(request.data)
        serializer = UserRegisterSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(clean_data)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    **serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    throttle_scope = 'login'
      
class UserLogin(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            # Log errors for debugging
            logger.debug(f"Login failed with errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogout(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            # Extract the refresh token from the request
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                # Create a RefreshToken object to blacklist it
                token = RefreshToken(refresh_token)
                token.blacklist()  # Optional: Requires `djangorestframework-simplejwt` blacklist feature

            return Response({'message': 'Logged out successfully'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
