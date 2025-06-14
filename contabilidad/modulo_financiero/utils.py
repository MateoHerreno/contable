import secrets
from django.core.mail import send_mail
from django.db.models import Sum
from .models import Cliente,Proveedor
from django.db.models import Sum

#funciones para recuperacion de tokens____________________________________________________________________________
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