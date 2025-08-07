from django.utils import timezone
from django.contrib.auth import logout

from django.utils import timezone

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_login_str = request.session.get('last_login')
            
            if last_login_str:
                # Parsear usando timezone (soporta strings ISO)
                last_login = timezone.datetime.fromisoformat(last_login_str)
                idle_time = timezone.now() - last_login
                if idle_time > timezone.timedelta(hours=8):
                    logout(request)
            
            # Guardar como string ISO
            request.session['last_login'] = timezone.now().isoformat()

        return self.get_response(request)