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
        serializer.save(creado_por=self.request.user)