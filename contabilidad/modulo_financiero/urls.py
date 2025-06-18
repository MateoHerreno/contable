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
router.register(r'conceptoscxp', ConceptoCXPViewSet)
router.register(r'conceptoscxc', ConceptoCXCViewSet)
router.register(r'cxp', views. CuentaPorPagarViewSet)
router.register(r'cxc', views. CuentaPorCobrarViewSet)
router.register(r'notaCredito', NotaCreditoViewSet)


urlpatterns = [
    #swagger para documentacion de la api
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    #urls funcionales
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),#obtener token de log
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),#refrescar token de log
    path('api/passwordRequest/', SolicitudRecuperacionAPIView.as_view(), name='password-reset-request'), #peticion para cambiar contraseña
    path('api/passwordReset/', PasswordResetAPIView.as_view(), name='password-reset'), # json para cambiar la contraseña
    path('api/calcusaldos/', RecalcularSaldosAPIView.as_view(), name='recalcular-saldos'),#post - dispara el calculo de saldos para guardarlos en la db clientes.saldo
    path('api/estres/', EstadoResultadosAPIView.as_view(), name='estado-resultados'),# get- acopañar de fecha y año en ete formato /api/estres/?anio=2025&mes=6
    path('api/exportarestres/', ExportarEstresPDFAPIView.as_view(), name='exportar-estres'),
    path('api/exportcxcfecha/', ExportarCxCPorFechaAPIView.as_view(), name='exportar-cxc-fecha'),
    path('api/exportcxpfecha/', ExportarCxPPorFechaAPIView.as_view(), name='exportar-cxp-fecha'),
    path('api/exportcxcclienfecha/', ExportarCxCPorClienteYFechaAPIView.as_view(), name='exportar-cxc-cliente-fecha'),
    path('api/exportcxpprovefecha/', ExportarCxPPorProveedorYFechaAPIView.as_view(), name='exportar-cxp-proveedor-fecha'),
]


