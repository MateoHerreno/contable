
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import viewsets,status
from rest_framework.views import APIView
from rest_framework import permissions
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.http import FileResponse
from calendar import monthrange
from datetime import datetime
from io import BytesIO
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


    """def get_permissions(self):
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
        return [TienePermiso('read_usuario')()]"""

class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

    """def get_permissions(self):
        if self.action == 'create':
            return [TienePermiso('create_empresa')()]
        elif self.action in ['update', 'partial_update']:
            return [TienePermiso('update_empresa')()]
        elif self.action == 'destroy':
            return [TienePermiso('delete_empresa')()]
        return [TienePermiso('read_empresa')()]
"""
class TiendaViewSet(viewsets.ModelViewSet):
    queryset = Tienda.objects.all()
    serializer_class = TiendaSerializer

    """def get_permissions(self):
        if self.action == 'create':
            return [TienePermiso('create_tienda')()]
        elif self.action in ['update', 'partial_update']:
            return [TienePermiso('update_tienda')()]
        elif self.action == 'destroy':
            return [TienePermiso('delete_tienda')()]
        return [TienePermiso('read_tienda')()]"""

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    """def get_queryset(self):
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
        return [TienePermiso('read_usuario')()]"""

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

    """def get_permissions(self):
        if self.action == 'create':
            return [TienePermiso('create_proveedor')()]
        elif self.action in ['update', 'partial_update']:
            return [TienePermiso('update_proveedor')()]
        elif self.action == 'destroy':
            return [TienePermiso('delete_proveedor')()]
        return [TienePermiso('read_proveedor')()]"""

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    """def get_permissions(self):
        if self.action == 'create':
            return [TienePermiso('create_cliente')()]
        elif self.action in ['update', 'partial_update']:
            return [TienePermiso('update_cliente')()]
        elif self.action == 'destroy':
            return [TienePermiso('delete_cliente')()]
        return [TienePermiso('read_cliente')()]"""

class ConceptoCXPViewSet(viewsets.ModelViewSet):
    queryset = ConceptoCXP.objects.all()
    serializer_class = ConceptoCXPSerializer

    """def get_permissions(self):
        if self.action == 'create':
            return [TienePermiso('create_conceptocxp')()]
        elif self.action in ['update', 'partial_update']:
            return [TienePermiso('update_conceptocxp')()]
        elif self.action == 'destroy':
            return [TienePermiso('delete_conceptocxp')()]
        return [TienePermiso('read_conceptocxp')()]"""

class ConceptoCXCViewSet(viewsets.ModelViewSet):
    queryset = ConceptoCXC.objects.all()
    serializer_class = ConceptoCXCSerializer

    """def get_permissions(self):
        if self.action == 'create':
            return [TienePermiso('create_conceptocxc')()]
        elif self.action in ['update', 'partial_update']:
            return [TienePermiso('update_conceptocxc')()]
        elif self.action == 'destroy':
            return [TienePermiso('delete_conceptocxc')()]
        return [TienePermiso('read_conceptocxc')()]"""

class CuentaPorPagarViewSet(viewsets.ModelViewSet):
    queryset = CuentaPorPagar.objects.all()
    serializer_class = CuentaPorPagarSerializer

    """def get_permissions(self):
        if self.action == 'create':
            return [TienePermiso('create_cxp')()]
        elif self.action in ['update', 'partial_update']:
            return [TienePermiso('update_cxp')()]
        elif self.action == 'destroy':
            return [TienePermiso('delete_cxp')()]
        return [TienePermiso('read_cxp')()]"""

class CuentaPorCobrarViewSet(viewsets.ModelViewSet):
    queryset = CuentaPorCobrar.objects.all()
    serializer_class = CuentaPorCobrarSerializer

    """def get_permissions(self):
        if self.action == 'create':
            return [TienePermiso('create_cxc')()]
        elif self.action in ['update', 'partial_update']:
            return [TienePermiso('update_cxc')()]
        elif self.action == 'destroy':
            return [TienePermiso('delete_cxc')()]
        return [TienePermiso('read_cxc')()]"""

class NotaCreditoViewSet(viewsets.ModelViewSet):
    queryset = NotaCredito.objects.select_related('cuenta').all()
    serializer_class = NotaCreditoSerializer

    """def get_permissions(self):
        if self.action == 'create':
            return [TienePermiso('create_notacredito')()]
        elif self.action in ['update', 'partial_update']:
            return [TienePermiso('update_notacredito')()]
        elif self.action == 'destroy':
            return [TienePermiso('delete_notacredito')()]
        return [TienePermiso('read_notacredito')()]"""

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
    #permission_classes = [IsAuthenticated, TienePermiso('recalcular_saldos')]

    def post(self, request):
        actualizar_saldos()
        return Response({
            "mensaje": "Saldos de clientes y proveedores actualizados correctamente."
        })
    
class ExportarCxCPorFechaAPIView(APIView):

    #permission_classes = [IsAuthenticated, TienePermiso('exportar_cxc_fecha')]

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
    #permission_classes = [IsAuthenticated, TienePermiso('exportar_cxc_cliente_fecha')]

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
    #permission_classes = [IsAuthenticated, TienePermiso('exportar_cxp_proveedor_fecha')]

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
    #permission_classes = [IsAuthenticated, TienePermiso('exportar_cxp_fecha')]

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
    
class EstadoResultadosAPIView(APIView):
    #permission_classes = [IsAuthenticated, TienePermiso('ver_estres')]

    def get(self, request):
        hoy = datetime.now().date()
        anio = request.query_params.get('anio')
        mes = request.query_params.get('mes')

        # → Si se envían año y mes específicos
        if anio and mes:
            anio = int(anio)
            mes = int(mes)
            existente = EstadoResultadosMensual.objects.filter(anio=anio, mes=mes).first()
            if existente:
                return Response(self._formatear_salida(existente))
            return Response({"error": "Ese mes aún no tiene estado de resultados calculado."}, status=404)

        # → Si NO se envía anio/mes: buscar el último mes con datos en CxC o CxP
        ultima_fecha_cxc = CuentaPorCobrar.objects.order_by('-fecha').values_list('fecha', flat=True).first()
        ultima_fecha_cxp = CuentaPorPagar.objects.order_by('-fecha').values_list('fecha', flat=True).first()

        if not ultima_fecha_cxc and not ultima_fecha_cxp:
            return Response({"error": "No hay datos contables disponibles."}, status=404)

        ultima_fecha = max(ultima_fecha_cxc or datetime.min, ultima_fecha_cxp or datetime.min)
        anio = ultima_fecha.year
        mes = ultima_fecha.month

        existente = EstadoResultadosMensual.objects.filter(anio=anio, mes=mes).first()
        if existente:
            return Response(self._formatear_salida(existente))

        # Si no existe aún: decidir si se guarda o no
        es_ultimo_dia_mes_actual = (
            hoy.year == anio and hoy.month == mes and
            hoy.day == monthrange(hoy.year, hoy.month)[1]
        )

        instancia = self._calcular_estado(anio, mes)

        if es_ultimo_dia_mes_actual:
            instancia.save()

        return Response(self._formatear_salida(instancia))

    def _calcular_estado(self, anio, mes):
        from .models import EstadoResultadosMensual

        fecha_inicio = datetime(anio, mes, 1)
        fecha_fin = datetime(anio, mes, monthrange(anio, mes)[1], 23, 59, 59)

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

        # Crear instancia (aún no guardada)
        return EstadoResultadosMensual(
            anio=anio,
            mes=mes,
            ingresos_total=ingresos_total,
            costos_operacion_total=costos_operacion_total,
            utilidad_bruta=utilidad_bruta,
            gastos_administrativos_total=gastos_admon_total,
            utilidad_operacional=utilidad_operacional,
            otros_costos_total=otros_costos_total,
            utilidad_antes_impuestos=utilidad_antes_impuestos,
            gastos_impuestos=gastos_impuestos,
            utilidad_neta=utilidad_neta,
            ingresos_detalle=ingresos_detalle,
            costos_operacion_detalle=costos_operacion_detalle,
            gastos_administrativos_detalle=gastos_admon_detalle,
            otros_costos_detalle=otros_costos_detalle,
            impuestos_detalle=impuestos_detalle
        )

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

class ExportarEstresPDFAPIView(APIView):
    #permission_classes = [IsAuthenticated, TienePermiso('exportar_estres')]

    def get(self, request):
        anio = request.query_params.get('anio')
        mes = request.query_params.get('mes')

        if not anio or not mes:
            return Response({'error': 'Debe proporcionar año y mes como parámetros.'}, status=400)

        try:
            estado = EstadoResultadosMensual.objects.get(anio=anio, mes=mes)
        except EstadoResultadosMensual.DoesNotExist:
            return Response({'error': 'No se encontró un estado de resultados guardado para ese periodo.'}, status=404)

        # Generar PDF
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        pdf.setTitle(f"Estado de Resultados - {mes}/{anio}")

        y = 750
        def escribir(texto, indent=0):
            nonlocal y
            pdf.drawString(50 + indent, y, texto)
            y -= 15
            if y < 50:
                pdf.showPage()
                y = 750

        escribir(f"Estado de Resultados - {mes}/{anio}")
        escribir(f"Ingresos: ${estado.ingresos_total:,.2f}")
        for k, v in estado.ingresos_detalle.items():
            escribir(f"{k}: ${v:,.2f}", indent=20)

        escribir(f"Costos de Operación: ${estado.costos_operacion_total:,.2f}")
        for k, v in estado.costos_operacion_detalle.items():
            escribir(f"{k}: ${v:,.2f}", indent=20)

        escribir(f"Utilidad Bruta: ${estado.utilidad_bruta:,.2f}")

        escribir(f"Gastos Administrativos: ${estado.gastos_administrativos_total:,.2f}")
        for k, v in estado.gastos_administrativos_detalle.items():
            escribir(f"{k}: ${v:,.2f}", indent=20)

        escribir(f"Utilidad Operacional: ${estado.utilidad_operacional:,.2f}")

        escribir(f"Otros Costos: ${estado.otros_costos_total:,.2f}")
        for k, v in estado.otros_costos_detalle.items():
            escribir(f"{k}: ${v:,.2f}", indent=20)

        escribir(f"Utilidad Antes de Impuestos: ${estado.utilidad_antes_impuestos:,.2f}")

        escribir(f"Gastos por Impuestos: ${estado.gastos_impuestos:,.2f}")
        for k, v in estado.impuestos_detalle.items():
            escribir(f"{k}: ${v:,.2f}", indent=20)

        escribir(f"Utilidad Neta: ${estado.utilidad_neta:,.2f}")

        pdf.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f"estres_{anio}_{mes}.pdf")