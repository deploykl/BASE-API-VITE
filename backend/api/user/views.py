from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.user.serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from api.permissions import IsSuperUser, HasModuleAccess
from django.http import JsonResponse
from django.views import View
from django.db import connection
from redis import Redis
from django.conf import settings
from datetime import datetime, timedelta  # Modifica esta línea
from django.utils import timezone

User = get_user_model()

class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    MAX_FAILED_ATTEMPTS = 3
    BLOCK_TIME_MINUTES = 5

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Validación básica de campos
        if not username or not password:
            return Response(
                {'detail': 'Las credenciales de autenticación no se proveyeron.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(username=username).first()

        # Verificar si el usuario está bloqueado temporalmente
        if user and user.login_blocked_until:
            if timezone.now() < user.login_blocked_until:
                remaining_time = (user.login_blocked_until - timezone.now()).seconds // 60
                return Response(
                    {
                        'detail': f'Cuenta bloqueada temporalmente. Intente nuevamente en {remaining_time} minutos.'
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            else:
                # Restablecer el bloqueo si el tiempo ha expirado
                user.login_blocked_until = None
                user.failed_login_attempts = 0
                user.save()

        # Validaciones de usuario
        if user is None:
            return Response(
                {'detail': 'Usuario no encontrado'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not user.check_password(password):
            # Incrementar el contador de intentos fallidos
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= self.MAX_FAILED_ATTEMPTS:
                user.login_blocked_until = timezone.now() + timedelta(minutes=self.BLOCK_TIME_MINUTES)
                user.save()
                return Response(
                    {
                        'detail': f'Demasiados intentos fallidos. Cuenta bloqueada por {self.BLOCK_TIME_MINUTES} minutos.'
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            
            user.save()
            remaining_attempts = self.MAX_FAILED_ATTEMPTS - user.failed_login_attempts
            return Response(
                {
                    'detail': 'Contraseña incorrecta',
                    'remaining_attempts': remaining_attempts
                }, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Si el login es exitoso, resetear los intentos fallidos
        if user.failed_login_attempts > 0 or user.login_blocked_until:
            user.failed_login_attempts = 0
            user.login_blocked_until = None
            user.save()

        if not user.is_active:
            return Response(
                {'detail': 'Cuenta desactivada'}, 
                status=status.HTTP_403_FORBIDDEN
            )

        # Resto de tu lógica de login...
        if user.is_superuser:
            modulos_activos = Modulo.objects.filter(is_active=True)
            modulos_asignados = Modulo.objects.all()
        else:
            modulos_activos = user.modulos.filter(is_active=True)
            modulos_asignados = user.modulos.all()
        
        modulos_activos_list = list(modulos_activos.values_list('codename', flat=True))
        
        if not user.is_superuser:
            if modulos_asignados.exists() and not modulos_activos.exists():
                modulos_desactivados = list(modulos_asignados.values('codename', 'description'))
                return Response(
                    {
                        'detail': 'Tienes módulos asignados pero están desactivados',
                        'modulos_desactivados': modulos_desactivados
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            elif not modulos_asignados.exists():
                return Response(
                    {'detail': 'No tienes módulos asignados. Contacta al administrador.'},
                    status=status.HTTP_403_FORBIDDEN
                )

        refresh = RefreshToken.for_user(user)
        
        user_data = {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'is_superuser': user.is_superuser,
            'is_staff': user.is_staff,
            'modulos': modulos_activos_list,
        }

        return Response(user_data, status=status.HTTP_200_OK)
    
class LogoutView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer  # Añade esto

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Crea un objeto RefreshToken a partir del token recibido
            token = RefreshToken(refresh_token)
            # Añade el token a la lista negra
            token.blacklist()
            return Response({"detail": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except InvalidToken:
            return Response({"detail": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer  # Añade esto

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(
            request.user, 
            data=request.data, 
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer  # Añade esto

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['current_password']):
                return Response(
                    {"current_password": "Contraseña actual incorrecta"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"detail": "Contraseña actualizada correctamente"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, HasModuleAccess]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'dni']
    ordering_fields = '__all__'
    ordering = ['-date_joined']
    required_module = 'Usuarios'  # Define el módulo requerido para esta vista

    def perform_create(self, serializer):
        user = serializer.save()
        user.created_by = self.request.user  # Asigna el creador
        user.save()  # Guarda el usuario

    def perform_update(self, serializer):
        user = serializer.save()
        user.updated_by = self.request.user  # Asigna quien actualizó
        user.updated_at=timezone.now()      # Fecha de actualización actual
        user.save()  # Guarda el usuario
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        user = self.get_object()
        user.is_active = True
        user.activated_at = timezone.now()
        user.activated_by = request.user
        user.save()
        return Response({'status': 'user activated'})

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        user = self.get_object()
        user.is_active = False
        user.deactivated_at = timezone.now()
        user.deactivated_by = request.user
        user.save()
        return Response({'status': 'user deactivated'})

    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @action(detail=True, methods=['post'])
    def make_staff(self, request, pk=None):
        user = self.get_object()
        user.is_staff = True
        user.save()
        return Response({'status': 'user promoted to staff'})
    
    @action(detail=True, methods=['post'])
    def remove_staff(self, request, pk=None):
        user = self.get_object()
        user.is_staff = False
        user.save()
        return Response({'status': 'user removed from staff'})
    
class ModuloViewSet(viewsets.ModelViewSet):
    serializer_class = ModuloSerializer
    permission_classes = [IsAuthenticated]
    ordering = ["id"]
    ordering_fields = "__all__"
    filter_backends = (DjangoFilterBackend, OrderingFilter)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Modulo.objects.all()  # Superusuarios ven todo
        return Modulo.objects.filter(is_active=True)  # Usuarios normales solo activos
    
    
class ModuloViewSetTEST(viewsets.ModelViewSet):
    serializer_class = ModuloSerializer
    permission_classes = [AllowAny]  # Permite acceso sin autenticación
    ordering = ["id"]
    ordering_fields = "__all__"
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    
    def get_queryset(self):
        return Modulo.objects.filter(is_active=True)
    
#VERTIFICAR CONEXION BACKEND
class HealthCheckView(View):
    def get(self, request):
        health_status = {
            'status': 'OK',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'services': {
                'database': False,
                'cache': False,
                'external_services': {}
            }
        }
        status_code = 200
        
        try:
            # Verificar base de datos
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                health_status['services']['database'] = True
        except Exception as e:
            health_status['status'] = 'DEGRADED'
            health_status['services']['database'] = False
            health_status['services']['database_error'] = str(e)
            status_code = 503

        try:
            # Verificar Redis si está configurado
            if hasattr(settings, 'REDIS_URL'):
                redis_conn = Redis.from_url(settings.REDIS_URL)
                health_status['services']['cache'] = redis_conn.ping()
        except Exception as e:
            health_status['status'] = 'DEGRADED'
            health_status['services']['cache'] = False
            health_status['services']['cache_error'] = str(e)
            status_code = 503

        return JsonResponse(health_status, status=status_code)