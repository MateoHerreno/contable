from django.urls import path,include
from rest_framework import routers
from .import views
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView


router = routers.DefaultRouter()
router.register(r'perfiles', views.PerfilViewSet, basename='perfil')
router.register(r'empresas', views. EmpresaViewSet)
router.register(r'tiendas', views. TiendaViewSet)
router.register(r'usuarios', views. UsuarioViewSet)
router.register(r'proveedores', views. ProveedorViewSet)
router.register(r'clientes', views. ClienteViewSet)
router.register(r'cuentas_por_pagar', views. CuentaPorPagarViewSet)
router.register(r'cuentas_por_cobrar', views. CuentaPorCobrarViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),#obtener token de log
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),#refrescar token de log
    path('api/passwordRequest/', SolicitudRecuperacionAPIView.as_view(), name='password-reset-request'), #peticion para cambiar contraseña
    path('api/passwordReset/', PasswordResetAPIView.as_view(), name='password-reset'), # json para cambiar la contraseña
    path('api/recalcular_saldos/', RecalcularSaldosAPIView.as_view(), name='recalcular-saldos'),#post - dispara el calculo de saldos para guardarlos en la db clientes.saldo
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    
]


