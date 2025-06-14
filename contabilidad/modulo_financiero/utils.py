from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.core.mail import send_mail
from django.db.models import Sum
from django.http import FileResponse
from .models import Cliente,Proveedor
from io import BytesIO
import secrets

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

#funciones relacionadas con cuentas por cobrar y clientes________________________________________________________
# Actualizar saldos de clientes
def actualizar_saldos():
    # Actualizar saldos de clientes
    for cliente in Cliente.objects.all():
        total = cliente.cuentaporcobrar_set.aggregate(
            total=Sum('pendiente_por_pagar')
        )['total'] or 0
        cliente.saldo = total
        cliente.save()

    # Actualizar saldos de proveedores
    for proveedor in Proveedor.objects.all():
        total = proveedor.cuentaporpagar_set.aggregate(
            total=Sum('pendiente_por_pagar')
        )['total'] or 0
        proveedor.saldo = total
        proveedor.save()
#en esta funcion se organizan los numeros para un formato mas legible al devolverlos en la api
def format_decimal_humano(value):
    try:
        return f"{float(value):,.2f}"
    except (ValueError, TypeError):
        return value
    
#funcion para exportacion de pdfs______________________________________________________________________________________
#desde cxc filtrando por clientes y fechas (un cliente en un periodo especifico, o si no trae cliente solo la fecha especifica)
def generar_pdf_cxc(queryset, cliente=None):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    if cliente:
        titulo = f"Reporte CxC - Cliente: {cliente.nombre}"
    else:
        titulo = "Reporte Cuentas por Cobrar - General"

    pdf.setTitle(titulo)
    pdf.drawString(100, 750, titulo)
    pdf.drawString(100, 735, f"Total de cuentas: {queryset.count()}")

    y = 700
    for cuenta in queryset:
        pdf.drawString(100, y, f"{cuenta.fecha.strftime('%Y-%m-%d')} | Cliente {cuenta.cliente.nombre} | {cuenta.concepto} | ${cuenta.pendiente_por_pagar:,.0f}")
        y -= 15
        if y < 50:
            pdf.showPage()
            y = 750

    pdf.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='cxc_general.pdf')

#desde cxp filtrando por fechac y proveedor (si no trae cliente deve traer fecha especifica)
def generar_pdf_cxp(queryset, proveedor=None):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    if proveedor:
        titulo = f"Reporte CxP - Proveedor: {proveedor.nombre}"
    else:
        titulo = "Reporte Cuentas por Pagar - General"

    pdf.setTitle(titulo)
    pdf.drawString(100, 750, titulo)
    pdf.drawString(100, 735, f"Total de cuentas: {queryset.count()}")

    y = 700
    for cuenta in queryset:
        pdf.drawString(100, y, f"{cuenta.fecha.strftime('%Y-%m-%d')} | {cuenta.concepto} | ${cuenta.pendiente_por_pagar:,.0f}")
        y -= 15
        if y < 50:
            pdf.showPage()
            y = 750

    pdf.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='cxp_proveedor.pdf')