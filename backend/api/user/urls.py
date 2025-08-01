from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from api.user.views import *
from django.contrib.auth import views as auth_views  # Importa esto

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='users')

urlpatterns = [  
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('login/', LoginView.as_view(), name='login'),  # Esta es la ruta con nombre 'login'
    path('logout/', LogoutView.as_view(), name='logout'),

    #path('register/', RegisterView.as_view(), name='register'),
    #path('password/reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    #path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
] + router.urls


