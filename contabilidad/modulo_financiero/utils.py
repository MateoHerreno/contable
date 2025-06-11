import secrets
from django.core.mail import send_mail

def generar_token():
    return secrets.token_urlsafe(16)

def enviar_email_recuperacion(email, token):
    asunto = "Recuperación de contraseña"
    mensaje = (
        f"Hola,\n\n"
        f"Has solicitado cambiar tu contraseña.\n"
        f"Tu token de recuperación es:\n\n"
        f"{token}\n\n"
        f"Utiliza este token para cambiar tu contraseña en la aplicación.\n\n"
        f"¡Gracias!"
    )
    from_email = None  # usa el DEFAULT_FROM_EMAIL en "software contable/contabilidad/contabilidad/setings.py"
    recipient_list = [email]
    send_mail(asunto, mensaje, from_email, recipient_list)