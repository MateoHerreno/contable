from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Perfil

@receiver(post_migrate)
def inicializar_perfiles(sender, **kwargs):
    Perfil.inicializar_perfiles()
