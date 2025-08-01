from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.gore.views import UserGoreViewSet , LoginView # asegúrate de que esto no cause un import circular

router = DefaultRouter()
router.register(r'gore_user', UserGoreViewSet, basename='gore_user')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login-gore'),  # Esta es la ruta con nombre 'login'

]
