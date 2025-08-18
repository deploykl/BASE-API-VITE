from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

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
        queryset = Personal.objects.filter(activo=True)
        
        # Filtro para conductores (acepta true/false como string)
        es_conductor_param = self.request.query_params.get('es_conductor')
        if es_conductor_param in ['true', 'false']:
            es_conductor_value = es_conductor_param == 'true'
            queryset = queryset.filter(es_conductor=es_conductor_value)
            
        return queryset.order_by('apellido', 'nombre')
    
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