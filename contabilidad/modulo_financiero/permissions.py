from rest_framework.permissions import BasePermission

PERMISOS = {
    'create_usuario':   {'empleado':False , 'sprempleado':False, 'gerente':False, 'admin':True },
    'read_usuario':     {'empleado':False , 'sprempleado':False, 'gerente':True , 'admin':True },
    'update_usuario':   {'empleado':False , 'sprempleado':False, 'gerente':True , 'admin':True },
    'delete_usuario':   {'empleado':False , 'sprempleado':False, 'gerente':False, 'admin':True },
        
    'create_empresa':   {'empleado':False , 'sprempleado':False, 'gerente':False, 'admin':True },
    'read_empresa':     {'empleado':False , 'sprempleado':False, 'gerente':True , 'admin':True },
    'update_empresa':   {'empleado':False , 'sprempleado':True , 'gerente':True , 'admin':True },
    'delete_empresa':   {'empleado':False , 'sprempleado':False, 'gerente':False, 'admin':True },
    
    'create_tienda':    {'empleado':False , 'sprempleado':False, 'gerente':True , 'admin':True },
    'read_tienda':      {'empleado':False , 'sprempleado':True , 'gerente':True , 'admin':True },
    'update_tienda':    {'empleado':False , 'sprempleado':True , 'gerente':True , 'admin':True },
    'delete_tienda':    {'empleado':False , 'sprempleado':False, 'gerente':True , 'admin':True },
    
    'create_cliente':   {'empleado':False , 'sprempleado':True , 'gerente':True , 'admin':True },
    'read_cliente':     {'empleado':False , 'sprempleado':True , 'gerente':True , 'admin':True },
    'update_cliente':   {'empleado':False , 'sprempleado':True , 'gerente':True , 'admin':True },
    'delete_cliente':   {'empleado':False , 'sprempleado':False, 'gerente':False, 'admin':True },

    'create_proveedor': {'empleado':False , 'sprempleado':True , 'gerente':True , 'admin':True },
    'read_proveedor':   {'empleado':False , 'sprempleado':True , 'gerente':True , 'admin':True },
    'update_proveedor': {'empleado':False , 'sprempleado':True , 'gerente':True , 'admin':True },
    'delete_proveedor': {'empleado':False , 'sprempleado':False, 'gerente':False, 'admin':True },
    
    'create_cxc':       {'empleado':True  , 'sprempleado':True , 'gerente':True , 'admin':True },
    'read_cxc':         {'empleado':False , 'sprempleado':True , 'gerente':True , 'admin':True },
    'update_cxc':       {'empleado':False , 'sprempleado':True , 'gerente':True , 'admin':True },
    'delete_cxc':       {'empleado':False , 'sprempleado':False, 'gerente':False, 'admin':True },

    'create_cxp':       {'empleado':True  , 'sprempleado':True , 'gerente':True , 'admin':True },
    'read_cxp':         {'empleado':False , 'sprempleado':True , 'gerente':True , 'admin':True },
    'update_cxp':       {'empleado':False , 'sprempleado':True , 'gerente':True , 'admin':True },
    'delete_cxp':       {'empleado':False , 'sprempleado':False, 'gerente':False, 'admin':True },

    'recalcular_saldos':{'empleado':False , 'sprempleado':True , 'gerente':True , 'admin':True },

}

ROLES = {
    1: 'admin',
    2: 'gerente',
    3: 'sprempleado',
    4: 'empleado',
}

def TienePermiso(accion):
    class _TienePermisoInterno(BasePermission):
        def has_permission(self, request, view):
            if not request.user.is_authenticated:
                return False

            rol_nombre = ROLES.get(request.user.rol)
            if not rol_nombre:
                return False

            reglas = PERMISOS.get(accion)
            if not reglas:
                return False

            return reglas.get(rol_nombre, False)
    return _TienePermisoInterno

class NoEditarAdministradores(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Si el usuario actual es gerente y el objeto es un admin, no permitir
        return not (request.user.rol == 2 and getattr(obj, 'rol', None) == 1)