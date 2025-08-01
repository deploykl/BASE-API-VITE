from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets, permissions
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from api.permissions import JerarquiaPermissions
from .serializers import UserGoreSerializer
from .models import *
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Q
User = get_user_model()

class UserGoreViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserGoreSerializer
    permission_classes = [IsAuthenticated, JerarquiaPermissions]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.nivel_acceso == 'ADMIN':
            return super().get_queryset()
        
        queryset = super().get_queryset()
        
        if user.nivel_acceso == 'REGIONAL':
            # Regional puede ver usuarios de su departamento, sus redes y hospitales
            return queryset.filter(
                Q(departamento=user.departamento) | 
                Q(red__departamento=user.departamento) |
                Q(hospital__red__departamento=user.departamento)
            )
        elif user.nivel_acceso == 'RED':
            # Red puede ver usuarios de su red y sus hospitales
            return queryset.filter(
                Q(red=user.red) |
                Q(hospital__red=user.red))
        elif user.nivel_acceso == 'HOSPITAL':
            # Hospital solo puede ver usuarios de su hospital
            return queryset.filter(hospital=user.hospital)
        
        return queryset.none()
    
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'detail': 'Se requieren nombre de usuario y contraseña'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(username=username).first()

        if user is None or not user.check_password(password):
            return Response(
                {'detail': 'Credenciales inválidas'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not user.is_active:
            return Response(
                {'detail': 'Cuenta desactivada'}, 
                status=status.HTTP_403_FORBIDDEN
            )

        refresh = RefreshToken.for_user(user)
        user_data = UserGoreSerializer(user).data
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': user_data  # Incluye todos los datos del usuario serializados
        }, status=status.HTTP_200_OK)