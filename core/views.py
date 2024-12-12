from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsAdminUser
from .models import Project, Stakeholder, CommissioningReport, OccupancyCertificate, User
from .serializers import ProjectSerializer, StakeholderSerializer, CommissioningReportSerializer, OccupancyCertificateSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
import jwt
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import action
import logging
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            refresh = RefreshToken(response.data['refresh'])
            access_token = str(refresh.access_token)

            # Set the access token in a cookie
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,  # Set to True in production
                samesite='Lax'
            )

            # Optionally, set the refresh token in a cookie
            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                secure=False,  # Set to True in production
                samesite='Lax'
            )
        return response

    
class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.action == 'register':
            logging.debug("Register action: AllowAny permissions applied")
            return [permissions.AllowAny()]
        logging.debug("Other action: IsAuthenticated permissions applied")
        return [permissions.IsAuthenticated()]


    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)
    def list(self, request):
        return Response({'message': 'This is a list of users'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.AllowAny] )
    def register(self, request):
        serializer   = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        return Response({'message': 'This is a retrieve method'})

    def update(self, request, pk=None):
        return Response({'message': 'This is an update method'})

    def partial_update(self, request, pk=None):
        return Response({'message': 'This is a partial update method'})

    def destroy(self, request, pk=None):
        return Response({'message': 'This is a destroy method'})

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
