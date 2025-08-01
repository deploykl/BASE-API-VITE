from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.views.generic import RedirectView  # <-- Importa esto
from django.contrib.auth.decorators import login_required  # Importa esto

urlpatterns = [
    path('', RedirectView.as_view(url='/api/schema/swagger/', permanent=False)),  # <-- Redirección
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
 # Protege estas rutas:
    path('api/schema/', login_required(SpectacularAPIView.as_view()), name='schema'),
    path('api/schema/swagger/', login_required(SpectacularSwaggerView.as_view(url_name='schema')), name='swagger-ui'),
    
        # Añade las URLs de autenticación de Django
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
