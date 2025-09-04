from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register(r'consultas-externas', ConsultaExternaViewSet, basename='consultas-externas')
router.register(r'fuentes', FuentesViewSet, basename='fuentes')
router.register(r'tablero', TableroViewSet, basename='tablero')

urlpatterns = router.urls
