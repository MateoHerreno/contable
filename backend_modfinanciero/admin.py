
from django.contrib import admin
from .models import *
from django.utils.html import mark_safe
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Configuración básica para hacer cruds en la base de datos desde superuser

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['nombre','id']
    search_fields = ['nombre']
    ordering = ('id',)

@admin.register(Empresa)   # ← Aquí va el modelo dentro de los paréntesis
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'nit', 'telefono', 'get_perfiles']
    search_fields = ['nombre', 'nit']
    filter_horizontal = ['perfiles']
    ordering = ('id',)

    def get_perfiles(self, obj):
        return ", ".join(p.nombre for p in obj.perfiles.all())
    get_perfiles.short_description = 'Perfiles'

@admin.register(Tienda)
class TiendaAdmin(admin.ModelAdmin):
    list_display = ['id','nombre', 'direccion', 'ciudad', 'empresa','cantidad_usuarios']
    ordering = ('id',)
    def cantidad_usuarios(self, obj):
        return obj.usuario_set.count()
    cantidad_usuarios.short_description = 'Cantidad de Usuarios'

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'nombre', 'tienda', 'rol', 'is_active')
    search_fields = ('email', 'nombre', 'telefono')
    ordering = ('id',)


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'nit', 'telefono', 'saldo']
    search_fields = ['nombre', 'nit']
    ordering = ('id',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'nit', 'telefono', 'saldo']
    search_fields = ['nombre', 'nit']
    ordering = ('id',)

@admin.register(ConceptoCXP)
class ConceptoCXPAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre']
    search_fields = ['nombre']

@admin.register(ConceptoCXC)
class ConceptoCXCAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre']
    search_fields = ['nombre']

@admin.register(CuentaPorPagar)
class CuentaPorPagarAdmin(admin.ModelAdmin):
    list_display = ['n_cxp', 'proveedor', 'fecha', 'val_bruto', 'pendiente_por_pagar']
    search_fields = ['n_cxp', 'proveedor__nombre']
    ordering = ('fecha','proveedor')

@admin.register(CuentaPorCobrar)
class CuentaPorCobrarAdmin(admin.ModelAdmin):
    list_display = ['n_cxc', 'cliente', 'fecha', 'val_bruto', 'pendiente_por_pagar']
    search_fields = ['n_cxc', 'cliente__nombre']
    ordering = ('fecha','cliente')

@admin.register(PermisoPersonalizado)
class PermisoPersonalizadoAdmin(admin.ModelAdmin):
    list_display = ('accion', 'admin', 'gerente', 'sprempleado', 'empleado')
    list_editable = ('admin', 'gerente', 'sprempleado', 'empleado')
    search_fields = ('accion',)


@admin.register(NotaCredito)
class NotaCreditoAdmin(admin.ModelAdmin):
    list_display = ['id', 'cuenta', 'creada']
    search_fields = ['descripcion', 'cuenta__cliente__nombre']

@admin.register(EstadoResultadosMensual)
class EstadoResultadosMensualAdmin(admin.ModelAdmin):
    list_display = ('anio', 'mes', 'ingresos_total', 'utilidad_neta', 'creado')
    list_filter = ('anio', 'mes')
    ordering = ('-anio', '-mes')
    readonly_fields = (
        'anio', 'mes', 'ingresos_total', 'costos_operacion_total',
        'utilidad_bruta', 'gastos_administrativos_total',
        'utilidad_operacional', 'otros_costos_total',
        'utilidad_antes_impuestos', 'gastos_impuestos', 'utilidad_neta',
        'ingresos_detalle', 'costos_operacion_detalle',
        'gastos_administrativos_detalle', 'otros_costos_detalle',
        'impuestos_detalle', 'creado'
    )
    search_fields = ('anio', 'mes')
    fieldsets = (
        ('Periodo', {
            'fields': ('anio', 'mes', 'creado')
        }),
        ('Totales', {
            'fields': (
                'ingresos_total', 'costos_operacion_total', 'utilidad_bruta',
                'gastos_administrativos_total', 'utilidad_operacional',
                'otros_costos_total', 'utilidad_antes_impuestos',
                'gastos_impuestos', 'utilidad_neta',
            )
        }),
        ('Detalles agrupados (JSON)', {
            'fields': (
                'ingresos_detalle', 'costos_operacion_detalle',
                'gastos_administrativos_detalle', 'otros_costos_detalle',
                'impuestos_detalle'
            )
        }),
    )