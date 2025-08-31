from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from .models import Personal
from api.services.userServices import PersonalAccessService
from rest_framework.decorators import action
from rest_framework.response import Response
# Create your views here.
class DependenciaViewSet(viewsets.ModelViewSet):
    queryset = Dependencia.objects.all()  # Añade esta línea
    serializer_class = DependenciaSerializer
    permission_classes = [IsAuthenticated] 
    ordering = ["id"]
    ordering_fields = "__all__"
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    
# Create your views here.
class PersonalViewSet(viewsets.ModelViewSet):
    queryset = Personal.objects.all()  # Añade esta línea
    serializer_class = PersonalSerializer
    permission_classes = [IsAuthenticated] 
    ordering = ["id"]
    ordering_fields = "__all__"
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    #filterset_fields = ['es_conductor', 'activo', 'dependencia'] # se filtra asi 

    def get_queryset(self):
        queryset = Personal.objects.all()  # ← MUESTRA TODOS
        
        # Filtro para conductores (acepta true/false como string)
        es_conductor_param = self.request.query_params.get('es_conductor')
        if es_conductor_param in ['true', 'false']:
            es_conductor_value = es_conductor_param == 'true'
            queryset = queryset.filter(es_conductor=es_conductor_value)
            
        return queryset.order_by('apellido', 'nombre')
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def habilitar_acceso(self, request, pk=None):
        personal = self.get_object()
        
        # Obtener módulos del request
        modulos_ids = request.data.get('modulos', [])
        
        success, message = PersonalAccessService.habilitar_acceso(
            personal, 
            request.user, 
            modulos_ids=modulos_ids,
            enviar_email=True
        )
        return Response({'success': success, 'message': message})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def deshabilitar_acceso(self, request, pk=None):
        personal = self.get_object()
        success, message = PersonalAccessService.deshabilitar_acceso(personal, request.user)
        return Response({'success': success, 'message': message})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def resetear_password(self, request, pk=None):
        personal = self.get_object()
        success, message = PersonalAccessService.resetear_password(
            personal, request.user, enviar_email=True
        )
        return Response({'success': success, 'message': message})
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def estado_acceso(self, request, pk=None):
        personal = self.get_object()
        return Response({
            'acceso': personal.acceso,
            'email': personal.email,
            'username': personal.user.username if personal.user else None,
            'fecha_habilitacion': personal.fecha_habilitacion_acceso.isoformat() if personal.fecha_habilitacion_acceso else None,
            'habilitado_por': personal.habilitado_por.get_full_name() if personal.habilitado_por else None
        })
        
# Create your views here.
class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()  # Añade esta línea
    serializer_class = VehiculoSerializer
    permission_classes = [IsAuthenticated] 
    ordering = ["id"]
    ordering_fields = "__all__"
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    
# Create your views here.
class ComisionViewSet(viewsets.ModelViewSet):
    queryset = Comision.objects.all()  # Añade esta línea
    serializer_class = ComisionSerializer
    permission_classes = [IsAuthenticated] 
    ordering = ["id"]
    ordering_fields = "__all__"
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        