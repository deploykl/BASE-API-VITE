from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register(r'anexo', AnexoViewSet, basename='anexo')
router.register(r'condicion', ConditionViewSet, basename='condicion')
router.register(r'nivel', NivelViewSet, basename='nivel')
router.register(r'dependencia', DependenciaViewSet, basename='dependencia')
router.register(r'area', AreaViewSet, basename='area')
router.register(r'profesion', ProfesionViewSet, basename='profesion')
router.register(r'cargo', CargoViewSet, basename='cargo')
router.register(r'regimen', RegimenViewSet, basename='regimen')
router.register(r'grupo_ocupacional', GrupoOcupacionalViewSet, basename='grupo_ocupacional')
router.register(r'estado', EstadoViewSet, basename='estado')
router.register(r'generica', GenericaViewSet, basename='generica')
router.register(r'personal', PersonalViewSet, basename='personal')
router.register(r'vehiculo', VehiculoViewSet, basename='vehiculo')
router.register(r'comision', ComisionViewSet, basename='comision')


urlpatterns = router.urls
