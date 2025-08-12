# api/user/middleware.py
from ipware import get_client_ip
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import DisallowedHost
from api.user.models import UserAudit
import logging

logger = logging.getLogger(__name__)

class JWTAuditMiddleware:
    """
    Middleware para registrar auditoría de acceso de usuarios,
    capturando IP real incluso detrás de proxies.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            
            if self._should_log_request(request):
                self._log_access(request)
                
            return response
        except Exception as e:
            logger.error(f"Error en JWTAuditMiddleware: {str(e)}", exc_info=True)
            raise

    def _should_log_request(self, request):
        """Determina si se debe registrar el acceso"""
        return (
            hasattr(request, 'user') and 
            request.user.is_authenticated and
            not hasattr(request, '_jwt_audit_logged') and
            not request.path.startswith('/admin/') and  # Excluir admin
            request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'] and  # Solo métodos HTTP principales
            not request.path.startswith('/static/') and  # Excluir archivos estáticos
            not request.path.startswith('/media/') and  # Excluir archivos multimedia
            not any(ext in request.path for ext in ['.js', '.css', '.png', '.jpg', '.jpeg', '.gif', '.ico'])  # Excluir archivos estáticos
        )
            

    def _log_access(self, request):
        """Registra el acceso del usuario"""
        try:
            client_ip = self._get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
            
            UserAudit.objects.create(
                user=request.user,
                ip_address=client_ip,
                device_type=self._detect_device(user_agent),
                user_agent=user_agent,
                session_key=self._get_session_key(request),
                login_date=timezone.now()
            )
            request._jwt_audit_logged = True
            
        except Exception as e:
            logger.error(f"Error al registrar acceso: {str(e)}", exc_info=True)

    def _get_client_ip(self, request):
        """Obtiene IP considerando proxy inverso Nginx"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip or '0.0.0.0'
    
    def _get_session_key(self, request):
        """Obtiene session_key de forma segura"""
        if hasattr(request, 'session') and request.session.session_key:
            return request.session.session_key
        return None

    def _detect_device(self, user_agent):
        """Detecta tipo de dispositivo mejorado"""
        if not user_agent:
            return 'OTHER'
            
        user_agent = user_agent.lower()
        
        mobile_keywords = [
            'mobile', 'android', 'iphone', 'ipod', 
            'blackberry', 'windows phone'
        ]
        
        tablet_keywords = [
            'tablet', 'ipad', 'kindle', 'silk'
        ]
        
        if any(kw in user_agent for kw in mobile_keywords):
            return 'MOBILE'
        elif any(kw in user_agent for kw in tablet_keywords):
            return 'TABLET'
        return 'PC'