from django.urls import path,include
from rest_framework import routers
from .import views
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView


router = routers.DefaultRouter()
router.register(r'perfiles', PerfilViewSet) # este no se usa en front
router.register(r'empresas', EmpresaViewSet)
router.register(r'tiendas',  TiendaViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'proveedores', ProveedorViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'conceptoscxp', ConceptoCXPViewSet) # este no se usa en front
router.register(r'conceptoscxc', ConceptoCXCViewSet) # este no se usa en front
router.register(r'cxp', CuentaPorPagarViewSet)
router.register(r'cxc', CuentaPorCobrarViewSet)
router.register(r'notacredito', NotaCreditoViewSet) # deve proporcionarse con cxc


urlpatterns = [
    #swagger para documentacion de la api
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    #urls de datos contables
    path('api/', include(router.urls)),
    path('api/estres/', EstadoResultados.as_view(), name='estres'),
    #urls de login
    path('api/token/', TokenObtainPairView.as_view(), name='token'),
    path('api/refresh/', TokenRefreshView.as_view(), name='refresh'),
    #urls de recueperacion de contraseña
    path('api/passrequest/', SolicitudRecuperacion.as_view(), name='passrequest'), 
    path('api/passreset/', PasswordReset.as_view(), name='passreset'), 
    #url de exportar pfds
    path('api/pdfcxcfecha/', ExportarCxcPorFecha.as_view(), name='pdfcxcfecha'),
    path('api/pdfcxpfecha/', ExportarCxpPorFecha.as_view(), name='pdfcxpfecha'),
    path('api/pdfcxcclif/', ExportarCxcPorClienteYFecha.as_view(), name='pdfcxcclientefecha'),
    path('api/pdfcxpclif/', ExportarCxpPorProveedorYFecha.as_view(), name='pdfcxpclientefecha'),
    path('api/pdfestres/', ExportarEstresFecha.as_view(), name='pdfestres'), 
    #url de exports exels
    path('api/excelcxcfecha/', ExportarExcelCxcPorFecha.as_view(), name='excelcxcfecha'),
    path('api/excelcxcclif/', ExportarExcelCxcPorClienteYFecha.as_view(), name='excelcxcclientefecha'),
    path('api/excelcxpfecha/', ExportarExcelCxpPorFecha.as_view(), name='excelcxpfecha'),
    path('api/excelcxpclif/', ExportarExcelCxpPorProveedorYFecha.as_view(), name='excelcxpproveedorfecha'),
    path('api/excelestres/', ExportarExcelEstres.as_view(), name='excelestres'),
]


