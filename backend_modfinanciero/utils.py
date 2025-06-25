from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from django.core.mail import send_mail
from django.utils.timezone import now
from django.http import FileResponse
from django.db.models import Sum
from django.db.models import *
from decimal import Decimal
from io import BytesIO
from .models import *
import secrets
import pytz
bogota_tz = pytz.timezone('America/Bogota')



#funciones para recuperacion de contraseña por token_______________________________________________________________
def generar_token():
    token = secrets.token_urlsafe(6)  # token ~8 caracteres
    token = token[:8]  # asegúrate de que tenga exactamente 8 
    return f"{token[:4]}-{token[4:]}" #parte el token con un guion

def enviar_email_recuperacion(email, token):
    asunto = "Recuperación de contraseña"
    mensaje = (
        f"Hola,\n\n"
        f"Has solicitado cambiar tu contraseña.\n"
        f"Tu token de recuperación es:\n\n"
        f"{token}\n\n"
        f"Utiliza este token para cambiar tu contraseña en la aplicación.\n\n"
        f"Tambien puedes ir a la url... http://127.0.0.1:8000/api/passwordReset/ \n\n"
        f"¡Gracias!"
    )
    from_email = None  # usa el DEFAULT_FROM_EMAIL en "contable/contabilidad/contabilidad/setings.py"
    recipient_list = [email]
    send_mail(asunto, mensaje, from_email, recipient_list)

#funcion para devolver con comas los valores (mejor)
def format_decimal_humano(value):
    try:
        return f"{float(value):,.2f}"
    except (ValueError, TypeError):
        return value

#funciones relacionadas con cuentas por cobrar y clientes________________________________________________________
# Actualizar saldos de clientes y proveedores que cargan en cxc y cxp

def recalcular_saldos_proveedor(proveedor_id):
    cuentas = CuentaPorPagar.objects.filter(proveedor_id=proveedor_id).order_by('fecha', 'n_cxp')
    saldo_acumulado = Decimal('0')
    cuenta_mas_reciente = None
    for cuenta in cuentas:
        cuenta.saldo_anterior = saldo_acumulado
        cuenta.pendiente_por_pagar = cuenta.val_bruto + cuenta.saldo_anterior - cuenta.abonos
        cuenta.save()
        saldo_acumulado = cuenta.pendiente_por_pagar
        cuenta_mas_reciente = cuenta
    # Actualiza el saldo solo si hay al menos una cuenta
    if cuenta_mas_reciente:
        Proveedor.objects.filter(id=proveedor_id).update(saldo=cuenta_mas_reciente.pendiente_por_pagar)
    else:
        Proveedor.objects.filter(id=proveedor_id).update(saldo=Decimal('0'))

def recalcular_saldos_cliente(cliente_id):
    cuentas = CuentaPorCobrar.objects.filter(cliente_id=cliente_id).order_by('fecha', 'n_cxc')
    saldo_acumulado = Decimal('0')
    for cuenta in cuentas:
        cuenta.saldo_anterior = saldo_acumulado
        cuenta.pendiente_por_pagar = cuenta.neto_facturado + cuenta.saldo_anterior - cuenta.abonos
        cuenta.save()
        saldo_acumulado = cuenta.pendiente_por_pagar
    # Actualizar saldo total del cliente
    Cliente.objects.filter(id=cliente_id).update(saldo=saldo_acumulado)

#funcion para exportacion de pdfs______________________________________________________________________________________
#desde cxc filtrando por clientes y fechas (un cliente en un periodo especifico, o si no trae cliente solo la fecha especifica)
def generar_pdf_cxc(queryset, cliente=None):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    ancho_pagina, alto_pagina = letter
    y = alto_pagina - 50

    empresa = Empresa.objects.first()
    nombre_empresa = empresa.nombre if empresa else "Empresa"

    fecha_generacion = now().astimezone(bogota_tz).strftime('%Y-%m-%d %H:%M:%S')
    titulo = f"Reporte Cuentas por Cobrar - {'Cliente: ' + cliente.nombre if cliente else 'General'}"

    pdf.setTitle(titulo)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, nombre_empresa)
    y -= 20
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(50, y, titulo)
    y -= 15
    pdf.setFont("Helvetica", 9)
    pdf.drawString(50, y, f"Generado: {fecha_generacion}")
    y -= 15
    pdf.drawString(50, y, f"Total de cuentas: {queryset.count()}")
    y -= 20

    encabezado = [
        "Fecha", "#CxC", "Cliente", "Concep.", "Bruto",
        "IVA", "Reten.", "Neto Fact.", "Saldo Ant.", "Abonos", "Pend. Pago"
    ]

    x_positions = [40, 90, 140, 250, 320, 370, 420, 470, 520, 570, 620]
    pdf.setFont("Helvetica-Bold", 6.5)
    for i, col in enumerate(encabezado):
        pdf.drawString(x_positions[i], y, col)
    y -= 10
    pdf.line(40, y, 680, y)
    y -= 8

    pdf.setFont("Helvetica", 5)
    total_neto = 0
    total_abonos = 0
    total_pendiente = 0

    for cuenta in queryset:
        datos = [
            cuenta.fecha.strftime('%Y-%m-%d'),
            str(cuenta.n_cxc),
            cuenta.cliente.nombre,
            cuenta.conceptoFijo.nombre,
            f"{cuenta.val_bruto:,.0f}",
            f"{cuenta.iva:,.0f}",
            f"{cuenta.retenciones:,.0f}",
            f"{cuenta.neto_facturado:,.0f}",
            f"{cuenta.saldo_anterior:,.0f}",
            f"{cuenta.abonos:,.0f}",
            f"{cuenta.pendiente_por_pagar:,.0f}"
        ]

        for i, dato in enumerate(datos):
            pdf.drawString(x_positions[i], y, str(dato))

        total_neto += cuenta.neto_facturado
        total_abonos += cuenta.abonos
        total_pendiente += cuenta.pendiente_por_pagar


        y -= 10
        if y < 50:
            pdf.showPage()
            y = alto_pagina - 50

    # Totales finales
    y -= 5
    pdf.line(40, y, 680, y)
    y -= 12
    pdf.setFont("Helvetica-Bold", 8)
    pdf.drawString(40, y, f"Total facturado: ${total_neto:,.2f}")
    y -= 12
    pdf.drawString(40, y, f"Total pagado: ${total_abonos:,.2f}")
    y -= 12
    pdf.drawString(40, y, f"Total adeudado total: ${total_pendiente:,.2f}")

    pdf.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='cuentas_por_cobrar.pdf')

#desde cxp filtrando por fechac y proveedor (si no trae cliente deve traer fecha especifica)
def generar_pdf_cxp(queryset, proveedor=None):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    ancho_pagina, alto_pagina = letter
    y = alto_pagina - 50

    empresa = Empresa.objects.first()
    nombre_empresa = empresa.nombre if empresa else "Empresa"

    fecha_generacion = now().astimezone(bogota_tz).strftime('%Y-%m-%d %H:%M:%S')
    titulo = f"Reporte Cuentas por Pagar "

    pdf.setTitle(titulo)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, nombre_empresa)
    y -= 20
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(50, y, titulo)
    y -= 15
    pdf.setFont("Helvetica", 9)
    pdf.drawString(50, y, f"Generado: {fecha_generacion}")
    y -= 15
    pdf.drawString(50, y, f"Total de cuentas: {queryset.count()}")
    y -= 20

    encabezado = [
        "Fecha", "#CxP", "Proveedor", "Concep.", "Valor",
        "Saldo Ant.", "Abonos", "Pend.Pag."
    ]
    x_positions = [40, 90, 140, 250, 320, 400, 470, 540]

    pdf.setFont("Helvetica-Bold", 6.5)
    for i, col in enumerate(encabezado):
        pdf.drawString(x_positions[i], y, col)
    y -= 10
    pdf.line(40, y, 680, y)
    y -= 8

    pdf.setFont("Helvetica", 5)
    total_bruto = 0
    total_abonos = 0
    total_pendiente = 0

    for cuenta in queryset:
        datos = [
            cuenta.fecha.strftime('%Y-%m-%d'),
            str(cuenta.n_cxp),
            cuenta.proveedor.nombre,
            cuenta.conceptoFijo.nombre,
            f"{cuenta.val_bruto:,.0f}",
            f"{cuenta.saldo_anterior:,.0f}",
            f"{cuenta.abonos:,.0f}",
            f"{cuenta.pendiente_por_pagar:,.0f}"
        ]

        for i, dato in enumerate(datos):
            pdf.drawString(x_positions[i], y, str(dato))

        total_bruto += cuenta.val_bruto
        total_abonos += cuenta.abonos
        total_pendiente += cuenta.pendiente_por_pagar
        y -= 10

        if y < 50:
            pdf.showPage()
            y = alto_pagina - 50

    y -= 5
    pdf.line(40, y, 680, y)
    y -= 12
    pdf.setFont("Helvetica-Bold", 8)
    pdf.drawString(40, y, f"Valor total: ${total_bruto:,.2f}")
    y -= 12
    pdf.drawString(40, y, f"Total abonos: ${total_abonos:,.2f}")
    y -= 12
    pdf.drawString(40, y, f"Total pend. pag. : ${total_pendiente:,.2f}")

    pdf.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='cxp_reporte.pdf')

#exportar pdf estado de resultados
def generar_pdf_estres(anio, mes):
    # Buscar la instancia
    try:
        instancia = EstadoResultadosMensual.objects.get(anio=anio, mes=mes)
    except EstadoResultadosMensual.DoesNotExist:
        from rest_framework.response import Response
        return Response({'error': 'No existe estado de resultados guardado para ese periodo.'}, status=404)

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 50

    empresa = Empresa.objects.first()
    nombre_empresa = empresa.nombre if empresa else "Empresa"
    fecha_generacion = now().strftime('%Y-%m-%d %H:%M:%S')
    titulo = f"Estado de Resultados - {mes}/{anio}"

    pdf.setTitle(titulo)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, nombre_empresa)
    y -= 20
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(50, y, titulo)
    y -= 15
    pdf.setFont("Helvetica", 9)
    pdf.drawString(50, y, f"Generado: {fecha_generacion}")
    y -= 25

    def seccion(nombre_seccion, detalle, total, y, mayusculas=True):
        titulo = nombre_seccion.upper() if mayusculas else nombre_seccion
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(50, y, titulo)
        y -= 15
        pdf.setFont("Helvetica", 8)
        for nombre, valor in detalle.items():
            texto = f"{nombre:<40} ${valor:,.2f}"
            pdf.drawRightString(width - 50, y, texto)
            y -= 12
            if y < 50:
                pdf.showPage()
                y = height - 50
        y -= 5
        pdf.setFont("Helvetica", 8.5)
        pdf.drawRightString(width - 50, y, f"total   :  ${total:,.2f}")
        y -= 20
        return y

    y = seccion("INGRESOS", instancia.ingresos_detalle, instancia.ingresos_total, y, mayusculas=True)
    y = seccion("COSTOS DE OPERACIÓN", instancia.costos_operacion_detalle, instancia.costos_operacion_total, y, mayusculas=True)

    # Utilidad bruta alineada a la izquierda en mayúsculas
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawCentredString(width / 2, y, f"UTILIDAD BRUTA: ${instancia.utilidad_bruta:,.2f}")
    y -= 20

    y = seccion("GASTOS ADMINISTRATIVOS", instancia.gastos_administrativos_detalle, instancia.gastos_administrativos_total, y, mayusculas=True)

    # Utilidad operacional alineada a la izquierda en mayúsculas
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawCentredString(width / 2, y, f"UTILIDAD OPERACIONAL: ${instancia.utilidad_operacional:,.2f}")
    y -= 20

    y = seccion("OTROS COSTOS", instancia.otros_costos_detalle, instancia.otros_costos_total, y, mayusculas=True)

    # Utilidad antes de impuestos alineada a la izquierda en mayúsculas
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawCentredString(width / 2, y, f"UTILIDAD ANTES DE IMPUESTOS: ${instancia.utilidad_antes_impuestos:,.2f}")
    y -= 20
    

    y = seccion("GASTOS POR IMPUESTOS", instancia.impuestos_detalle, instancia.gastos_impuestos, y, mayusculas=True)

    # Utilidad neta en mayúsculas y centrada
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawCentredString(width / 2, y, f"UTILIDAD NETA: ${instancia.utilidad_neta:,.2f}")
    y -= 30

    pdf.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f'estres_{anio}_{mes}.pdf')


#funciones para exportar a excel______________________________________________________________________________________
def generar_excel_cxc(queryset, cliente=None):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Cuentas por Cobrar"

    headers = [
        "Fecha", "#CxC", "Cliente", "Concepto", "Bruto",
        "IVA", "Retenciones", "Neto Facturado", "Saldo Ant.", "Abonos", "Pendiente"
    ]
    ws.append(headers)

    for cuenta in queryset:
        fila = [
            cuenta.fecha.strftime('%Y-%m-%d'),
            cuenta.n_cxc,
            cuenta.cliente.nombre,
            cuenta.conceptoFijo.nombre,
            float(cuenta.val_bruto),
            float(cuenta.iva),
            float(cuenta.retenciones),
            float(cuenta.neto_facturado),
            float(cuenta.saldo_anterior),
            float(cuenta.abonos),
            float(cuenta.pendiente_por_pagar),
        ]
        ws.append(fila)

    stream = BytesIO()
    wb.save(stream)
    stream.seek(0)
    return stream

def generar_excel_cxp(queryset, proveedor=None):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Cuentas por Pagar"

    headers = [
        "Fecha", "#CxP", "Proveedor", "Concepto", "Valor",
        "Saldo Ant.", "Abonos", "Pendiente"
    ]
    ws.append(headers)

    for cuenta in queryset:
        fila = [
            cuenta.fecha.strftime('%Y-%m-%d'),
            cuenta.n_cxp,
            cuenta.proveedor.nombre,
            cuenta.conceptoFijo.nombre,
            float(cuenta.val_bruto),
            float(cuenta.saldo_anterior),
            float(cuenta.abonos),
            float(cuenta.pendiente_por_pagar),
        ]
        ws.append(fila)

    stream = BytesIO()
    wb.save(stream)
    stream.seek(0)
    return stream

def generar_excel_estres(instancia):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Estado de Resultados"

    ws.append(["Estado de Resultados", f"{instancia.mes}/{instancia.anio}"])
    ws.append(["Fecha de generación", now().strftime('%Y-%m-%d %H:%M:%S')])
    ws.append([])

    def agregar_seccion(titulo, detalle, total):
        ws.append([titulo])
        for key, value in detalle.items():
            ws.append(["", key, float(value)])
        ws.append(["", "Total", float(total)])
        ws.append([])

    agregar_seccion("INGRESOS", instancia.ingresos_detalle, instancia.ingresos_total)
    agregar_seccion("COSTOS DE OPERACIÓN", instancia.costos_operacion_detalle, instancia.costos_operacion_total)
    ws.append(["", "UTILIDAD BRUTA", float(instancia.utilidad_bruta)])
    ws.append([])

    agregar_seccion("GASTOS ADMINISTRATIVOS", instancia.gastos_administrativos_detalle, instancia.gastos_administrativos_total)
    ws.append(["", "UTILIDAD OPERACIONAL", float(instancia.utilidad_operacional)])
    ws.append([])

    agregar_seccion("OTROS COSTOS", instancia.otros_costos_detalle, instancia.otros_costos_total)
    ws.append(["", "UTILIDAD ANTES DE IMPUESTOS", float(instancia.utilidad_antes_impuestos)])
    ws.append([])

    agregar_seccion("GASTOS POR IMPUESTOS", instancia.impuestos_detalle, instancia.gastos_impuestos)
    ws.append(["", "UTILIDAD NETA", float(instancia.utilidad_neta)])

    stream = BytesIO()
    wb.save(stream)
    stream.seek(0)
    return stream
