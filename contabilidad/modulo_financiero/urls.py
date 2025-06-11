from django.urls import path,include
from rest_framework import routers
from .import views
from .views import *

router = routers.DefaultRouter()

router.register(r'empresas', views. EmpresaViewSet)
router.register(r'tiendas', views. TiendaViewSet)
router.register(r'usuarios', views. UsuarioViewSet)
router.register(r'proveedores', views. ProveedorViewSet)
router.register(r'clientes', views. ClienteViewSet)
router.register(r'cuentas_por_pagar', views. CuentaPorPagarViewSet)
router.register(r'cuentas_por_cobrar', views. CuentaPorCobrarViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('passwordRequest/', SolicitudRecuperacionAPIView.as_view(), name='password-reset-request'), #este endpoint espera el mail registrado en usuario
    path('passwordReset/', PasswordResetAPIView.as_view(), name='password-reset'),#este endpoint espera {"token":tokenenviado, "password":nuevo , "password2":confirmacion}
]


