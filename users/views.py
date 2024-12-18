from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
import logging
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import PasswordSerializer, UserSerializer, UserRegisterSerializer

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):

    serializer_class = UserSerializer
    permission_classes=[AllowAny]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        # Return only the currently authenticated user's details
        return User.objects.filter(id=self.request.user.id)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
        
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # This uses the `create` method in `UserRegisterSerializer`, which hashes the password
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    @action(detail=True, methods=['post', 'put'], permission_classes=[IsAuthenticated])
    def set_password(self, request, *args, **kwargs):
        user = self.request.user
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
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
