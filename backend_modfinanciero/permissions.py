from rest_framework.permissions import BasePermission
from backend_modfinanciero.models import PermisoPersonalizado

# Mapeo de número de rol al nombre usado en la tabla
ROLES = {
    1: 'admin',
    2: 'gerente',
    3: 'sprempleado',
    4: 'empleado',
}

class TienePermiso:
    def __init__(self, accion):
        self.accion = accion

    def __call__(self):
        class _Permiso(BasePermission):
            def has_permission(inner_self, request, view):
                if not request.user.is_authenticated:
                    return False

                rol_nombre = ROLES.get(request.user.rol)
                if not rol_nombre:
                    return False

                try:
                    permiso = PermisoPersonalizado.objects.get(accion=self.accion)
                    return getattr(permiso, rol_nombre, False)
                except PermisoPersonalizado.DoesNotExist:
                    return False

        return _Permiso()



    
class NoEditarAdministradores(BasePermission):
    def has_object_permission(self, request, view, obj):
        editor_rol = request.user.rol
        objetivo_rol = getattr(obj, 'rol', None)

        if editor_rol == 2:  # gerente
            return objetivo_rol not in [1, 2]

        if editor_rol == 3:  # sprempleado
            return objetivo_rol not in [1, 2, 3]
        
        if editor_rol == 4:  # empleado
            return objetivo_rol not in [1, 2, 3, 4]

        return True

def filtrar_queryset_por_rol(queryset, user, campo_rol='rol', prefijo=''):
   
    if user.rol == 1:
        return queryset
    elif user.rol == 2:
        return queryset.exclude(**{f"{prefijo}{campo_rol}": 1})
    elif user.rol == 3:
        return queryset.exclude(**{f"{prefijo}{campo_rol}__in": [1, 2]})
    elif user.rol == 4:
        return queryset.exclude(**{f"{prefijo}{campo_rol}__in": [1, 2, 3]})
    return queryset.none()