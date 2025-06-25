
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import viewsets,status
from rest_framework.views import APIView
from rest_framework import permissions
from django.utils.timezone import make_aware
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.http import FileResponse,HttpResponse
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

    def get(self, request):
        hoy = datetime.now().date()
        anio = request.query_params.get('anio')
        mes = request.query_params.get('mes')

        if anio and mes:
            anio = int(anio)
            mes = int(mes)
        else:
            # Buscar la fecha más reciente entre CxC y CxP
            ultima_fecha_cxc = CuentaPorCobrar.objects.order_by('-fecha').values_list('fecha', flat=True).first()
            ultima_fecha_cxp = CuentaPorPagar.objects.order_by('-fecha').values_list('fecha', flat=True).first()

            if not ultima_fecha_cxc and not ultima_fecha_cxp:
                return Response({"error": "No hay datos contables disponibles."}, status=404)

            ultima_fecha = max(ultima_fecha_cxc or datetime.min, ultima_fecha_cxp or datetime.min)
            anio = ultima_fecha.year
            mes = ultima_fecha.month

        instancia = self._calcular_estado(anio, mes)
        return Response(self._formatear_salida(instancia))

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
    #permission_classes = [IsAuthenticated, TienePermiso('exportar_estres')]

    def post(self, request):
        anio = request.data.get('anio')
        mes = request.data.get('mes')

        if not anio or not mes:
            return Response({'error': 'Debe enviar "anio" y "mes".'}, status=400)

        try:
            estado = EstadoResultadosMensual.objects.get(anio=anio, mes=mes)
        except EstadoResultadosMensual.DoesNotExist:
            return Response({'error': 'No se encontró estado de resultados para ese periodo.'}, status=404)

        return generar_pdf_estres(estado, anio, mes)

class ExportarExcelCxcPorFecha(APIView):
    permission_classes = [IsAuthenticated, TienePermiso('exportar_excel_cxc_fecha')()]
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
    permission_classes = [IsAuthenticated, TienePermiso('exportar_excel_cxc_cliente_fecha')()]
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
    permission_classes = [IsAuthenticated, TienePermiso('exportar_excel_cxp_fecha')()]
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
    permission_classes = [IsAuthenticated, TienePermiso('exportar_excel_cxp_proveedor_fecha')()]
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
    permission_classes = [IsAuthenticated, TienePermiso('exportar_excel_estres')()]
    def post(self, request):
        anio = request.data.get('anio')
        mes = request.data.get('mes')

        if not anio or not mes:
            return Response({'error': 'Debe enviar anio y mes.'}, status=400)

        try:
            instancia = EstadoResultadosMensual.objects.get(anio=anio, mes=mes)
        except EstadoResultadosMensual.DoesNotExist:
            return Response({'error': 'No se encontró estado de resultados para ese periodo.'}, status=404)

        excel_file = generar_excel_estres(instancia)
        response = HttpResponse(excel_file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=estado_resultados.xlsx'
        return response
