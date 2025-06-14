
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import viewsets,status
from rest_framework.views import APIView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .serializers import *
from .permissions import*
from .models import*
from .utils import *

#desde aca es donde sale la documentacion de swagger   
schema_view = get_schema_view(
   openapi.Info(
      title="APIContable",
      default_version='v1',
      description="Documentación automática de la API contable",),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# API con rest framework
class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()  # Necesario para que router registre automáticamente
    serializer_class = PerfilSerializer

    def get_queryset(self):
        # Aplica seguridad jerárquica basada en roles
        return filtrar_queryset_por_rol(
            super().get_queryset(),
            self.request.user,
            campo_rol='rol',
            prefijo='usuario__'  # Perfil → Usuario
        )

    def get_permissions(self):
        if self.action == 'create':
            return [TienePermiso('create_usuario')()]
        elif self.action in ['update', 'partial_update']:
            return [
                TienePermiso('update_usuario')(),
                NoEditarAdministradores()
            ]
        elif self.action == 'destroy':
            return [
                TienePermiso('delete_usuario')(),
                NoEditarAdministradores()
            ]
        return [TienePermiso('read_usuario')()]

class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [TienePermiso('create_empresa')()]
        elif self.action in ['update', 'partial_update']:
            return [TienePermiso('update_empresa')()]
        elif self.action == 'destroy':
            return [TienePermiso('delete_empresa')()]
        return [TienePermiso('read_empresa')()]

class TiendaViewSet(viewsets.ModelViewSet):
    queryset = Tienda.objects.all()
    serializer_class = TiendaSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [TienePermiso('create_tienda')()]
        elif self.action in ['update', 'partial_update']:
            return [TienePermiso('update_tienda')()]
        elif self.action == 'destroy':
            return [TienePermiso('delete_tienda')()]
        return [TienePermiso('read_tienda')()]

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def get_queryset(self):
        # Solo ver usuarios de rol inferior
        return filtrar_queryset_por_rol(
            super().get_queryset(),
            self.request.user,
            campo_rol='rol'  # Usuario.rol directamente
        )

    def get_permissions(self):
        if self.action == 'create':
            return [TienePermiso('create_usuario')()]
        elif self.action in ['update', 'partial_update']:
            return [
                TienePermiso('update_usuario')(),
                NoEditarAdministradores()
            ]
        elif self.action == 'destroy':
            return [
                TienePermiso('delete_usuario')(),
                NoEditarAdministradores()
            ]
        return [TienePermiso('read_usuario')()]

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [TienePermiso('create_proveedor')()]
        elif self.action in ['update', 'partial_update']:
            return [TienePermiso('update_proveedor')()]
        elif self.action == 'destroy':
            return [TienePermiso('delete_proveedor')()]
        return [TienePermiso('read_proveedor')()]

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [TienePermiso('create_cliente')()]
        elif self.action in ['update', 'partial_update']:
            return [TienePermiso('update_cliente')()]
        elif self.action == 'destroy':
            return [TienePermiso('delete_cliente')()]
        return [TienePermiso('read_cliente')()]

class CuentaPorPagarViewSet(viewsets.ModelViewSet):
    queryset = CuentaPorPagar.objects.all()
    serializer_class = CuentaPorPagarSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [TienePermiso('create_cxp')()]
        elif self.action in ['update', 'partial_update']:
            return [TienePermiso('update_cxp')()]
        elif self.action == 'destroy':
            return [TienePermiso('delete_cxp')()]
        return [TienePermiso('read_cxp')()]

class CuentaPorCobrarViewSet(viewsets.ModelViewSet):
    queryset = CuentaPorCobrar.objects.all()
    serializer_class = CuentaPorCobrarSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [TienePermiso('create_cxc')()]
        elif self.action in ['update', 'partial_update']:
            return [TienePermiso('update_cxc')()]
        elif self.action == 'destroy':
            return [TienePermiso('delete_cxc')()]
        return [TienePermiso('read_cxc')()]

class PasswordResetAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Contraseña actualizada correctamente."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SolicitudRecuperacionAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        try:
            usuario = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            return Response({'error': 'No existe un usuario con ese email, envia un post json- "email": "usuario@correo.com"  '}, status=status.HTTP_404_NOT_FOUND)
        
        token = generar_token()
        usuario.token_recuperar = token
        usuario.save()
        
        enviar_email_recuperacion(usuario.email, token)
        return Response({'mensaje': 'Token de recuperación enviado a tu email.'}, status=status.HTTP_200_OK)

class RecalcularSaldosAPIView(APIView):
    permission_classes = [IsAuthenticated, TienePermiso('recalcular_saldos')]

    def post(self, request):
        actualizar_saldos()
        return Response({
            "mensaje": "Saldos de clientes y proveedores actualizados correctamente."
        })
    
class ExportarCxCPorFechaAPIView(APIView):

    permission_classes = [IsAuthenticated, TienePermiso('exportar_cxc_fecha')]

    def get(self, request):
        fecha_inicio = request.query_params.get('desde')
        fecha_fin = request.query_params.get('hasta')

        if not fecha_inicio or not fecha_fin:
            return Response({'error': 'Debe especificar "desde" y "hasta".'}, status=400)

        cuentas = CuentaPorCobrar.objects.filter(fecha__range=[fecha_inicio, fecha_fin]).order_by('fecha')

        if not cuentas.exists():
            return Response({'error': 'No se encontraron cuentas en el rango indicado.'}, status=404)

        return generar_pdf_cxc(cuentas, cliente=None)
    
class ExportarCxCPorClienteYFechaAPIView(APIView):
    permission_classes = [IsAuthenticated, TienePermiso('exportar_cxc_cliente_fecha')]

    def get(self, request):
        cliente_id = request.query_params.get('cliente')
        fecha_inicio = request.query_params.get('desde')
        fecha_fin = request.query_params.get('hasta')

        if not cliente_id or not fecha_inicio or not fecha_fin:
            return Response({'error': 'Debe especificar cliente, desde y hasta.'}, status=400)

        cliente = Cliente.objects.filter(id=cliente_id).first()
        if not cliente:
            return Response({'error': 'Cliente no encontrado.'}, status=404)

        cuentas = CuentaPorCobrar.objects.filter(
            cliente=cliente,
            fecha__range=[fecha_inicio, fecha_fin]
        ).order_by('fecha')

        if not cuentas.exists():
            return Response({'error': 'No se encontraron cuentas para el cliente en el rango indicado.'}, status=404)

        return generar_pdf_cxc(cuentas, cliente)
    
class ExportarCxPPorProveedorYFechaAPIView(APIView):
    permission_classes = [IsAuthenticated, TienePermiso('exportar_cxp_proveedor_fecha')]

    def get(self, request):
        proveedor_id = request.query_params.get('proveedor')
        fecha_inicio = request.query_params.get('desde')
        fecha_fin = request.query_params.get('hasta')

        if not proveedor_id or not fecha_inicio or not fecha_fin:
            return Response({'error': 'Debe especificar proveedor, desde y hasta.'}, status=400)

        proveedor = Proveedor.objects.filter(id=proveedor_id).first()
        if not proveedor:
            return Response({'error': 'Proveedor no encontrado.'}, status=404)

        cuentas = CuentaPorPagar.objects.filter(
            proveedor=proveedor,
            fecha__range=[fecha_inicio, fecha_fin]
        ).order_by('fecha')

        if not cuentas.exists():
            return Response({'error': 'No se encontraron cuentas para el proveedor en el rango indicado.'}, status=404)

        return generar_pdf_cxp(cuentas, proveedor)
    
class ExportarCxPPorFechaAPIView(APIView):
    permission_classes = [IsAuthenticated, TienePermiso('exportar_cxp_fecha')]

    def get(self, request):
        fecha_inicio = request.query_params.get('desde')
        fecha_fin = request.query_params.get('hasta')

        if not fecha_inicio or not fecha_fin:
            return Response({'error': 'Debe especificar "desde" y "hasta".'}, status=400)

        cuentas = CuentaPorPagar.objects.filter(
            fecha__range=[fecha_inicio, fecha_fin]
        ).order_by('fecha')

        if not cuentas.exists():
            return Response({'error': 'No se encontraron cuentas por pagar en el rango indicado.'}, status=404)

        return generar_pdf_cxp(cuentas, proveedor=None)