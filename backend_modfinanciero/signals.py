from django.conf import settings
from django.db.models.signals import post_migrate
from django.dispatch import receiver

import json
import os

from .models import (
    Perfil,
    ConceptoCXP,
    ConceptoCXC,
    PermisoPersonalizado,
)

@receiver(post_migrate)
def inicializar_perfiles(sender, **kwargs):
    if sender.name != 'backend_modfinanciero':
        return
    Perfil.inicializar_perfiles()


@receiver(post_migrate)
def crear_conceptos_cxp(sender, **kwargs):
    if sender.name != 'backend_modfinanciero':
        return
    ConceptoCXP.inicializar_ccxp()
    
@receiver(post_migrate)
def crear_conceptos_cxc(sender, **kwargs):
    if sender.name != 'backend_modfinanciero':
        return
    ConceptoCXC.inicializar_ccxc()

@receiver(post_migrate)
def cargar_permisos_definidos(sender, **kwargs):
    if sender.name != 'backend_modfinanciero':
        return
    ruta = os.path.join(settings.BASE_DIR, 'backend_modfinanciero', 'zpermisos_definidos.json')
    if os.path.exists(ruta):
        with open(ruta, 'r', encoding='utf-8') as f:
            permisos = json.load(f)
            for p in permisos:
                PermisoPersonalizado.objects.update_or_create(
                    accion=p["accion"],
                    defaults={
                        "admin": p.get("admin", False),
                        "gerente": p.get("gerente", False),
                        "sprempleado": p.get("sprempleado", False),
                        "empleado": p.get("empleado", False),
                    }
                )