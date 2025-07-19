from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import FileResponse, HttpResponse
from django.utils.timezone import make_aware, now
from django.db.models import Sum, F
from django.db import transaction

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from calendar import monthrange
from datetime import datetime
from io import BytesIO


from .models import (
    Perfil,
    Empresa,
    Tienda,
    Usuario,
    Proveedor,
    Cliente,
    ConceptoCXP,
    ConceptoCXC,
    CuentaPorPagar,
    CuentaPorCobrar,
    NotaCredito,
    EstadoResultadosMensual,
)

from .serializers import (
    PerfilSerializer,
    EmpresaSerializer,
    TiendaSerializer,
    UsuarioSerializer,
    ProveedorSerializer,
    ClienteSerializer,
    ConceptoCXPSerializer,
    ConceptoCXCSerializer,
    CuentaPorPagarSerializer,
    CuentaPorCobrarSerializer,
    NotaCreditoSerializer,
    PasswordResetSerializer,
    CustomTokenObtainPairSerializer,
    
)

from .permissions import (
    TienePermiso,
    NoEditarAdministradores, 
    filtrar_queryset_por_rol,
    )

from .utils import (
    recalcular_saldos_todos_clientes,
    recalcular_saldos_cliente,
    recalcular_saldos_todos_proveedores,
    recalcular_saldos_proveedor,
    generar_pdf_cxc,
    generar_pdf_estres,
    enviar_email_recuperacion,
    generar_token,
    generar_pdf_cxp,
    generar_excel_cxp,
    calcular_y_guardar_estado_resultados,
    generar_excel_cxc,
    generar_excel_estres
)



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
    queryset = Perfil.objects.all()  
    serializer_class = PerfilSerializer

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

    def list(self, request, *args, **kwargs):
        # Recálculo en batch: un solo bulk_update
        recalcular_saldos_todos_clientes()  
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        # 1. Obtenemos la instancia original
        cliente = self.get_object()
        # 2. Recalculamos su saldo en BD
        recalcular_saldos_cliente(cliente.id)  
        # 3. Forzamos refrescar del campo 'saldo' desde la BD
        cliente.refresh_from_db(fields=['saldo'])
        # 4. Serializamos y devolvemos ya con el saldo actualizado
        serializer = self.get_serializer(cliente)
        return Response(serializer.data)

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

    def list(self, request, *args, **kwargs):
        recalcular_saldos_todos_proveedores()
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        # 1. Obtenemos la instancia
        proveedor = self.get_object()
        # 2. Recalculamos su saldo en BD  
        recalcular_saldos_proveedor(proveedor.id)  
        # 3. Forzamos refrescar solo el campo 'saldo'  
        proveedor.refresh_from_db(fields=['saldo'])
        # 4. Serializamos y devolvemos con el saldo actualizado
        serializer = self.get_serializer(proveedor)
        return Response(serializer.data)
    
class ConceptoCXPViewSet(viewsets.ModelViewSet):
    queryset = ConceptoCXP.objects.all()
    serializer_class = ConceptoCXPSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [TienePermiso('create_conceptocxp')()]
        elif self.action in ['update', 'partial_update']:
            return [TienePermiso('update_conceptocxp')()]
        elif self.action == 'destroy':
            return [TienePermiso('delete_conceptocxp')()]
        return [TienePermiso('read_conceptocxp')()]

class ConceptoCXCViewSet(viewsets.ModelViewSet):
    queryset = ConceptoCXC.objects.all()
    serializer_class = ConceptoCXCSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [TienePermiso('create_conceptocxc')()]
        elif self.action in ['update', 'partial_update']:
            return [TienePermiso('update_conceptocxc')()]
        elif self.action == 'destroy':
            return [TienePermiso('delete_conceptocxc')()]
        return [TienePermiso('read_conceptocxc')()]

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
    
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        # Guardamos el proveedor para recálculo tras borrar la CxP
        instancia = self.get_object()
        # bloquea el proveedor antes de eliminar
        Proveedor.objects.select_for_update().get(pk=instancia.proveedor_id)
        self.perform_destroy(instancia)
        recalcular_saldos_proveedor(instancia.proveedor_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

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
    
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        # Guardamos el cliente para recálculo tras borrar
        instancia = self.get_object()
        Cliente.objects.select_for_update().get(pk=instancia.cliente_id)
        self.perform_destroy(instancia)
        recalcular_saldos_cliente(instancia.cliente_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class NotaCreditoViewSet(viewsets.ModelViewSet):
    queryset = NotaCredito.objects.select_related('cuenta').all()
    serializer_class = NotaCreditoSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [TienePermiso('create_notacredito')()]
        elif self.action in ['update', 'partial_update']:
            return [TienePermiso('update_notacredito')()]
        elif self.action == 'destroy':
            return [TienePermiso('delete_notacredito')()]
        return [TienePermiso('read_notacredito')()]

#views de recuperacion de contraseña
class PasswordReset(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Contraseña actualizada correctamente."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SolicitudRecuperacion(APIView):
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

#views de exportacion de pdf y exel y el estres
class ExportarCxcPorFecha(APIView):
    permission_classes = [IsAuthenticated, TienePermiso('exportar_cxc_fecha')]
    def post(self, request):
        fecha_inicio = request.data.get('fecha_inicio')
        fecha_fin = request.data.get('fecha_fin')

        if not fecha_inicio or not fecha_fin:
            return Response({'error': 'Debe enviar "fecha_inicio" y "fecha_fin" en el cuerpo JSON.'}, status=400)

        cuentas = CuentaPorCobrar.objects.filter(
            fecha__range=[fecha_inicio, fecha_fin]
        ).order_by('fecha')

        if not cuentas.exists():
            return Response({'error': 'No se encontraron cuentas en el rango indicado.'}, status=404)

        return generar_pdf_cxc(cuentas, cliente=None)
    
class ExportarCxcPorClienteYFecha(APIView):
    permission_classes = [IsAuthenticated, TienePermiso('exportar_cxc_cliente_fecha')]
    def post(self, request):
        cliente_id = request.data.get('cliente')
        fecha_inicio = request.data.get('fecha_inicio')
        fecha_fin = request.data.get('fecha_fin')

        if not cliente_id or not fecha_inicio or not fecha_fin:
            return Response({'error': 'Debe enviar "fecha_inicio" y "fecha_fin" en el cuerpo JSON.'}, status=400)

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

class ExportarCxpPorFecha(APIView):
    permission_classes = [IsAuthenticated, TienePermiso('exportar_cxp_fecha')]
    def post(self, request):
        fecha_inicio = request.data.get('fecha_inicio')
        fecha_fin = request.data.get('fecha_fin')

        if not fecha_inicio or not fecha_fin:
            return Response({'error': 'Debe enviar "fecha_inicio" y "fecha_fin" en el cuerpo JSON.'}, status=400)

        cuentas = CuentaPorPagar.objects.filter(
            fecha__range=[fecha_inicio, fecha_fin]
        ).order_by('fecha')

        if not cuentas.exists():
            return Response({'error': 'No se encontraron cuentas por pagar en el rango indicado.'}, status=404)

        return generar_pdf_cxp(cuentas, proveedor=None)
    
class ExportarCxpPorProveedorYFecha(APIView):
    permission_classes = [IsAuthenticated, TienePermiso('exportar_cxp_proveedor_fecha')]
    def post(self, request):
        proveedor_id = request.data.get('proveedor')
        fecha_inicio = request.data.get('fecha_inicio')
        fecha_fin = request.data.get('fecha_fin')

        if not proveedor_id or not fecha_inicio or not fecha_fin:
            return Response({'error': 'Debe enviar "fecha_inicio" y "fecha_fin" en el cuerpo JSON.'}, status=400)

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
    
class EstadoResultados(APIView):
    permission_classes = [IsAuthenticated, TienePermiso('ver_estres')]

    def post(self, request):
        hoy = datetime.now().date()

        # 1) Leer año/mes de body JSON o de query params
        anio = request.data.get('anio') or request.query_params.get('anio')
        mes  = request.data.get('mes')  or request.query_params.get('mes')

        # 2) Si vienen ambos, convertir a int; si no, buscar último mes disponible
        if anio is not None and mes is not None:
            try:
                anio = int(anio)
                mes  = int(mes)
            except ValueError:
                return Response(
                    {"error": "Los valores de 'anio' y 'mes' deben ser enteros."},
                    status=400
                )
        else:
            # buscar fecha más reciente entre CxC y CxP
            ultima_cxc = CuentaPorCobrar.objects.order_by('-fecha') \
                             .values_list('fecha', flat=True).first()
            ultima_cxp = CuentaPorPagar.objects.order_by('-fecha') \
                             .values_list('fecha', flat=True).first()
            if not ultima_cxc and not ultima_cxp:
                return Response(
                    {"error": "No hay datos contables disponibles."},
                    status=404
                )
            fechas = [f for f in (ultima_cxc, ultima_cxp) if f]
            ultima = max(fechas)
            anio = ultima.year
            mes  = ultima.month

        # 3) VALIDACIÓN ADICIONAL: asegurarnos de que haya al menos un registro
        tiene_cxc = CuentaPorCobrar.objects.filter(
            fecha__year=anio, fecha__month=mes
        ).exists()
        tiene_cxp = CuentaPorPagar.objects.filter(
            fecha__year=anio, fecha__month=mes
        ).exists()

        if not tiene_cxc and not tiene_cxp:
            return Response(
                {"error": f"No existen registros de CxC ni CxP para {anio}-{mes:02d}."},
                status=404
            )

        # 4) Si pasamos la validación, calculamos y devolvemos el estado de resultados
        instancia = self._calcular_estado(anio, mes)
        resultado = self._formatear_salida(instancia)
        return Response(resultado)

    def _calcular_estado(self, anio, mes):
        from .models import EstadoResultadosMensual

        fecha_inicio = make_aware(datetime(anio, mes, 1))
        fecha_fin = make_aware(datetime(anio, mes, monthrange(anio, mes)[1], 23, 59, 59))

        cxp_qs = CuentaPorPagar.objects.filter(fecha__range=(fecha_inicio, fecha_fin))
        cxc_qs = CuentaPorCobrar.objects.filter(fecha__range=(fecha_inicio, fecha_fin))

        def sumar_por_concepto(queryset, modelo_concepto):
            resultado = {}
            for concepto in modelo_concepto.objects.all():
                total = queryset.filter(conceptoFijo=concepto).aggregate(suma=Sum('val_bruto'))['suma'] or 0
                resultado[concepto.nombre] = float(total)
            return resultado

        ingresos_detalle = sumar_por_concepto(cxc_qs, ConceptoCXC)
        ingresos_total = sum(ingresos_detalle.values())

        costos_op = ["nomina", "servicios", "otrosOperativos"]
        costos_operacion_detalle = {
            k: float(cxp_qs.filter(conceptoFijo__nombre=k).aggregate(suma=Sum('val_bruto'))['suma'] or 0)
            for k in costos_op
        }
        costos_operacion_total = sum(costos_operacion_detalle.values())
        utilidad_bruta = ingresos_total - costos_operacion_total

        admon = ["honorariosADMON", "honorariosCONT", "segSocial", "otrosADMON"]
        gastos_admon_detalle = {
            k: float(cxp_qs.filter(conceptoFijo__nombre=k).aggregate(suma=Sum('val_bruto'))['suma'] or 0)
            for k in admon
        }
        gastos_admon_total = sum(gastos_admon_detalle.values())
        utilidad_operacional = utilidad_bruta - gastos_admon_total

        otros_costos_detalle = {
            "gastosBancarios": float(cxp_qs.filter(conceptoFijo__nombre="gastosBancarios").aggregate(suma=Sum('val_bruto'))['suma'] or 0)
        }
        otros_costos_total = sum(otros_costos_detalle.values())
        utilidad_antes_impuestos = utilidad_operacional - otros_costos_total

        impuestos_detalle = {
            "impuestos": float(cxc_qs.filter(conceptoFijo__nombre="impuestos").aggregate(suma=Sum('val_bruto'))['suma'] or 0)
        }
        gastos_impuestos = sum(impuestos_detalle.values())
        utilidad_neta = utilidad_antes_impuestos - gastos_impuestos

        # Guardar o actualizar
        estado, creado = EstadoResultadosMensual.objects.update_or_create(
            anio=anio,
            mes=mes,
            defaults={
                "ingresos_total": ingresos_total,
                "ingresos_detalle": ingresos_detalle,
                "costos_operacion_total": costos_operacion_total,
                "costos_operacion_detalle": costos_operacion_detalle,
                "utilidad_bruta": utilidad_bruta,
                "gastos_administrativos_total": gastos_admon_total,
                "gastos_administrativos_detalle": gastos_admon_detalle,
                "utilidad_operacional": utilidad_operacional,
                "otros_costos_total": otros_costos_total,
                "otros_costos_detalle": otros_costos_detalle,
                "utilidad_antes_impuestos": utilidad_antes_impuestos,
                "gastos_impuestos": gastos_impuestos,
                "impuestos_detalle": impuestos_detalle,
                "utilidad_neta": utilidad_neta,
            }
        )
        return estado

    def _formatear_salida(self, instancia):
        return {
            "anio": instancia.anio,
            "mes": instancia.mes,
            "ingresos": {
                "detalle": instancia.ingresos_detalle,
                "total": float(instancia.ingresos_total)
            },
            "costos_operacion": {
                "detalle": instancia.costos_operacion_detalle,
                "total": float(instancia.costos_operacion_total)
            },
            "utilidad_bruta": float(instancia.utilidad_bruta),
            "gastos_administrativos": {
                "detalle": instancia.gastos_administrativos_detalle,
                "total": float(instancia.gastos_administrativos_total)
            },
            "utilidad_operacional": float(instancia.utilidad_operacional),
            "otros_costos": {
                "detalle": instancia.otros_costos_detalle,
                "total": float(instancia.otros_costos_total)
            },
            "utilidad_antes_impuestos": float(instancia.utilidad_antes_impuestos),
            "gastos_impuestos": {
                "detalle": instancia.impuestos_detalle,
                "total": float(instancia.gastos_impuestos)
            },
            "utilidad_neta": float(instancia.utilidad_neta),
        }

class ExportarEstresFecha(APIView):
    permission_classes = [IsAuthenticated, TienePermiso('exportar_estres')]

    def post(self, request):
        anio = request.data.get('anio')
        mes = request.data.get('mes')

        if not anio or not mes:
            return Response({'error': 'Debe enviar "anio" y "mes".'}, status=400)

        try:
            anio = int(anio)
            mes = int(mes)
            estado = calcular_y_guardar_estado_resultados(anio, mes)
        except Exception as e:
            return Response({'error': f'Error al calcular el estado: {str(e)}'}, status=500)

        return generar_pdf_estres(anio, mes)

class ExportarExcelCxcPorFecha(APIView):
    permission_classes = [IsAuthenticated, TienePermiso('exportar_excel_cxc_fecha')]
    def post(self, request):
        fecha_inicio = request.data.get('fecha_inicio')
        fecha_fin = request.data.get('fecha_fin')

        if not fecha_inicio or not fecha_fin:
            return Response({'error': 'Debe enviar "fecha_inicio" y "fecha_fin".'}, status=400)

        cuentas = CuentaPorCobrar.objects.filter(fecha__range=[fecha_inicio, fecha_fin])
        if not cuentas.exists():
            return Response({'error': 'No se encontraron cuentas en el rango indicado.'}, status=404)

        excel_file = generar_excel_cxc(cuentas)
        response = HttpResponse(excel_file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=cuentas_por_cobrar.xlsx'
        return response

class ExportarExcelCxcPorClienteYFecha(APIView):
    permission_classes = [IsAuthenticated, TienePermiso('exportar_excel_cxc_cliente_fecha')]
    def post(self, request):
        cliente_id = request.data.get('cliente')
        fecha_inicio = request.data.get('fecha_inicio')
        fecha_fin = request.data.get('fecha_fin')

        if not cliente_id or not fecha_inicio or not fecha_fin:
            return Response({'error': 'Debe enviar cliente, fecha_inicio y fecha_fin.'}, status=400)

        cliente = Cliente.objects.filter(id=cliente_id).first()
        if not cliente:
            return Response({'error': 'Cliente no encontrado.'}, status=404)

        cuentas = CuentaPorCobrar.objects.filter(cliente=cliente, fecha__range=[fecha_inicio, fecha_fin])
        if not cuentas.exists():
            return Response({'error': 'No se encontraron cuentas para el cliente en el rango indicado.'}, status=404)

        excel_file = generar_excel_cxc(cuentas, cliente=cliente)
        response = HttpResponse(excel_file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=cuentas_por_cobrar_cliente.xlsx'
        return response

class ExportarExcelCxpPorFecha(APIView):
    permission_classes = [IsAuthenticated, TienePermiso('exportar_excel_cxp_fecha')]
    def post(self, request):
        fecha_inicio = request.data.get('fecha_inicio')
        fecha_fin = request.data.get('fecha_fin')

        if not fecha_inicio or not fecha_fin:
            return Response({'error': 'Debe enviar "fecha_inicio" y "fecha_fin".'}, status=400)

        cuentas = CuentaPorPagar.objects.filter(fecha__range=[fecha_inicio, fecha_fin])
        if not cuentas.exists():
            return Response({'error': 'No se encontraron cuentas por pagar en el rango indicado.'}, status=404)

        excel_file = generar_excel_cxp(cuentas)
        response = HttpResponse(excel_file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=cuentas_por_pagar.xlsx'
        return response

class ExportarExcelCxpPorProveedorYFecha(APIView):
    permission_classes = [IsAuthenticated, TienePermiso('exportar_excel_cxp_proveedor_fecha')]
    def post(self, request):
        proveedor_id = request.data.get('proveedor')
        fecha_inicio = request.data.get('fecha_inicio')
        fecha_fin = request.data.get('fecha_fin')

        if not proveedor_id or not fecha_inicio or not fecha_fin:
            return Response({'error': 'Debe enviar proveedor, fecha_inicio y fecha_fin.'}, status=400)

        proveedor = Proveedor.objects.filter(id=proveedor_id).first()
        if not proveedor:
            return Response({'error': 'Proveedor no encontrado.'}, status=404)

        cuentas = CuentaPorPagar.objects.filter(proveedor=proveedor, fecha__range=[fecha_inicio, fecha_fin])
        if not cuentas.exists():
            return Response({'error': 'No se encontraron cuentas para el proveedor en el rango indicado.'}, status=404)

        excel_file = generar_excel_cxp(cuentas, proveedor=proveedor)
        response = HttpResponse(excel_file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=cuentas_por_pagar_proveedor.xlsx'
        return response

class ExportarExcelEstres(APIView):
    permission_classes = [IsAuthenticated, TienePermiso('exportar_excel_estres')]

    def post(self, request):
        anio = request.data.get('anio')
        mes = request.data.get('mes')

        if not anio or not mes:
            return Response({'error': 'Debe enviar anio y mes.'}, status=400)

        try:
            anio = int(anio)
            mes = int(mes)
            instancia = calcular_y_guardar_estado_resultados(anio, mes)
        except Exception as e:
            return Response({'error': f'Error al calcular el estado: {str(e)}'}, status=500)

        excel_file = generar_excel_estres(instancia)
        response = HttpResponse(excel_file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=estado_resultados.xlsx'
        return response

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# views para el dashboard 7 enpoins que devuelven datos utiles
# 1. Resumen general
class DashboardResumenView(APIView):
    permission_classes = [IsAuthenticated, TienePermiso('ver_dashboard')]

    def get(self, request):
        hoy = now()
        anio = hoy.year
        mes = hoy.month

        ingresos = CuentaPorCobrar.objects.filter(fecha__year=anio, fecha__month=mes).aggregate(total=Sum('val_bruto'))['total'] or 0
        egresos = CuentaPorPagar.objects.filter(fecha__year=anio, fecha__month=mes).aggregate(total=Sum('val_bruto'))['total'] or 0
        utilidad = EstadoResultadosMensual.objects.filter(anio=anio, mes=mes).first()
        utilidad_neta = utilidad.utilidad_neta if utilidad else ingresos - egresos

        return Response({
            'ingresos': ingresos,
            'egresos': egresos,
            'utilidad_neta': utilidad_neta
        })

# 2. CxC por concepto (solo mes actual)
class CXCConceptosView(APIView):
    permission_classes = [IsAuthenticated, TienePermiso('ver_dashboard')]

    def get(self, request):
        hoy = now()
        anio = hoy.year
        mes = hoy.month

        datos = (CuentaPorCobrar.objects
                 .filter(fecha__year=anio, fecha__month=mes)
                 .values('conceptoFijo__nombre')
                 .annotate(total=Sum('val_bruto'))
                 .order_by('conceptoFijo__nombre'))
        return Response(datos)

# 3. CxP por concepto (solo mes actual)
class CXPConceptosView(APIView):
    permission_classes = [IsAuthenticated, TienePermiso('ver_dashboard')]

    def get(self, request):
        hoy = now()
        anio = hoy.year
        mes = hoy.month

        datos = (CuentaPorPagar.objects
                 .filter(fecha__year=anio, fecha__month=mes)
                 .values('conceptoFijo__nombre')
                 .annotate(total=Sum('val_bruto'))
                 .order_by('conceptoFijo__nombre'))
        return Response(datos)

# 4. Evolución mensual (mantiene todo el año, agrupado por mes)
class EvolucionMensualView(APIView):
    permission_classes = [IsAuthenticated, TienePermiso('ver_dashboard')]

    def get(self, request):
        hoy = now()
        anio = hoy.year

        cxc = (CuentaPorCobrar.objects
               .filter(fecha__year=anio)
               .values('fecha__month')
               .annotate(total=Sum('val_bruto'))
               .order_by('fecha__month'))

        cxp = (CuentaPorPagar.objects
               .filter(fecha__year=anio)
               .values('fecha__month')
               .annotate(total=Sum('val_bruto'))
               .order_by('fecha__month'))

        return Response({'cxc': list(cxc), 'cxp': list(cxp)})

# 5. CxC: recaudado vs pendiente (solo mes actual)
class CXCResumenView(APIView):
    permission_classes = [IsAuthenticated, TienePermiso('ver_dashboard')]

    def get(self, request):
        hoy = now()
        anio = hoy.year
        mes = hoy.month

        queryset = CuentaPorCobrar.objects.filter(fecha__year=anio, fecha__month=mes)
        recaudado = queryset.filter(neto_facturado__lte=F('abonos')).aggregate(suma=Sum('neto_facturado'))['suma'] or 0
        total = queryset.aggregate(suma=Sum('neto_facturado'))['suma'] or 0
        pendiente = total - recaudado
        return Response({'recaudado': recaudado, 'pendiente': pendiente})

# 6. CxP: pagado vs pendiente (solo mes actual)
class CXPResumenView(APIView):
    permission_classes = [IsAuthenticated, TienePermiso('ver_dashboard')]

    def get(self, request):
        hoy = now()
        anio = hoy.year
        mes = hoy.month

        queryset = CuentaPorPagar.objects.filter(fecha__year=anio, fecha__month=mes)
        pagado = queryset.filter(val_bruto__lte=F('abonos')).aggregate(suma=Sum('val_bruto'))['suma'] or 0
        total = queryset.aggregate(suma=Sum('val_bruto'))['suma'] or 0
        pendiente = total - pagado
        return Response({'pagado': pagado, 'pendiente': pendiente})
