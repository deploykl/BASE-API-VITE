from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSuperUser(BasePermission):
    """
    Permite el acceso solo a superusuarios.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class HasModuleAccess(BasePermission):
    """
    Permite el acceso solo si el usuario tiene asignado el módulo requerido o es superusuario.
    """
    def has_permission(self, request, view):
        # Superusuarios tienen acceso a todo
        if request.user.is_superuser:
            return True
            
        # Obtener el nombre del módulo requerido (puedes definirlo en la vista)
        required_module = getattr(view, 'required_module', None)
        
        if not required_module:
            return False
            
        # Verificar si el usuario tiene el módulo asignado
        return request.user.modulos.filter(codename=required_module, is_active=True).exists()
    
class IsOwnerOrReadOnly(BasePermission):
    """
    Permiso personalizado para que solo el creador pueda modificar o eliminar,
    pero los superusuarios pueden hacer todo.
    """
    def has_object_permission(self, request, view, obj):
        # Los métodos SAFE (GET, HEAD, OPTIONS) están permitidos para todos
        if request.method in SAFE_METHODS:
            return True
        
        # Los superusuarios pueden hacer cualquier operación
        if request.user and request.user.is_superuser:
            return True
            
        # Para métodos de escritura (PUT, PATCH, DELETE), solo el creador
        return obj.created_by == request.user
    
class JerarquiaPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
            
        if request.method == 'POST':
            nivel_destino = request.data.get('nivel_acceso', 'HOSPITAL')
            return request.user.puede_crear_usuario(nivel_destino)
        
        return True
    
    def has_object_permission(self, request, view, obj):
        return request.user.puede_ver_usuario(obj)