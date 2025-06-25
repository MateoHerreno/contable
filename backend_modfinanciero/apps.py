from django.apps import AppConfig
from django.contrib import admin
from django.utils.html import mark_safe


class ModuloFinancieroConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend_modfinanciero'

    def ready(self):
        import backend_modfinanciero.signals