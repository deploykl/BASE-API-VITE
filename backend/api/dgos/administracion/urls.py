from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register(r'dependencia', DependenciaViewSet, basename='dependencia')
router.register(r'area', AreaViewSet, basename='area')
router.register(r'personal', PersonalViewSet, basename='personal')
router.register(r'vehiculo', VehiculoViewSet, basename='vehiculo')
router.register(r'comision', ComisionViewSet, basename='comision')


urlpatterns = router.urls
