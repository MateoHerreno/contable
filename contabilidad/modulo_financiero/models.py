from django.contrib.auth.models import AbstractUser,PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from .authentication import CustomUserManager
from django.db.models import JSONField
from django.utils import timezone
from django.db import models

class Perfil(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

    @staticmethod
    def inicializar_perfiles():
        perfiles = ["comerciante", "fabricante", "servicios"] 
        for nombre in perfiles:
            Perfil.objects.get_or_create(nombre=nombre)

class Empresa(models.Model):
    nombre = models.CharField(max_length=100)
    nit = models.IntegerField(default=0)
    telefono = models.CharField(max_length=20, default=0)
    perfiles = models.ManyToManyField(Perfil, blank=True)

    def __str__(self):
        return f"{self.nombre}"
    
class Tienda(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre

    def cantidad_usuarios(self):
        return self.usuario_set.count()

class Usuario(AbstractUser, PermissionsMixin):
    username = None
    first_name = None
    last_name = None
    groups = None

    nombre = models.CharField(max_length=254)
    email = models.EmailField(max_length=254, unique=True, blank=False, null=True)
    password = models.CharField(max_length=254, blank=False, null=True)
    token_recuperar = models.CharField(max_length=254, blank=False, null=False, default='sin cambios pendientes ')
    telefono = models.CharField(null=False, blank=True, default=0)
    is_active = models.BooleanField(default=True)
    tienda = models.ForeignKey('Tienda', on_delete=models.CASCADE, null=True, blank=True)

    ROLES = (
        (1, "admin"),
        (2, "gerente"),
        (3, "sprempleado"),
        (4, "empleado"),
    )
    rol = models.IntegerField(choices=ROLES, default=4)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nombre"]

    objects = CustomUserManager()

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        # Protección contra asignar un rol superior
        usuario_modificando = getattr(self, '_modificado_por', None)

        if usuario_modificando and isinstance(usuario_modificando, Usuario):
            if self.rol < usuario_modificando.rol:
                raise ValidationError("No tienes permiso para asignar un rol superior al tuyo.")

        super().save(*args, **kwargs)

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    nit = models.IntegerField( default=0)
    telefono = models.CharField(max_length=20, default=0)
    saldo = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    nit = models.IntegerField(default=0)
    telefono = models.CharField(max_length=20, default=0)
    saldo = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    def __str__(self):
        return self.nombre
    
class ConceptoCXP(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre
    
    @staticmethod
    def inicializar_ccxp():
        conceptos = [
        "nomina",
        "servicios",
        "otrosOperativos",
        "honorariosADMON",
        "honorariosCONT",
        "segSocial",
        "otrosADMON",
        "impuestos",
        "gastosBancarios",
        ]
        for nombre in conceptos:
            ConceptoCXP.objects.get_or_create(nombre=nombre)

class ConceptoCXC(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre
    
    @staticmethod
    def inicializar_ccxc():
        conceptos = [
        "VentaProductos",
        "VentaServicios",
        "OtrosIngresos"
        ]
        for nombre in conceptos:
            ConceptoCXC.objects.get_or_create(nombre=nombre)

class CuentaPorPagar(models.Model):
    fecha = models.DateTimeField(default = timezone.now)
    n_cxp =  models.AutoField(primary_key=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    conceptoFijo = models.ForeignKey(ConceptoCXP, on_delete=models.PROTECT)
    conceptoDetalle = models.TextField(null=False, default=1)
    val_bruto = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    saldo_anterior = models.DecimalField(max_digits=15, decimal_places=2)
    abonos = models.DecimalField(max_digits=15, decimal_places=2, default=0,validators=[MinValueValidator(0)])
    pendiente_por_pagar = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.proveedor.nombre} - cxp : {self.n_cxp}"

class CuentaPorCobrar(models.Model):
    fecha = models.DateTimeField(default=timezone.now)
    n_cxc = models.AutoField(primary_key=True)
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    conceptoFijo = models.ForeignKey(ConceptoCXC, on_delete=models.PROTECT)
    conceptoDetalle = models.TextField(blank=True, null=True)  # obligatorio
    val_bruto = models.DecimalField(max_digits=15, decimal_places=2,)
    iva = models.DecimalField(max_digits=15, decimal_places=2,default=0,validators=[MinValueValidator(0)] )
    retenciones = models.DecimalField(max_digits=15, decimal_places=2,default=0,validators=[MinValueValidator(0)])
    neto_facturado = models.DecimalField(max_digits=15, decimal_places=2,default=0,validators=[MinValueValidator(0)])
    saldo_anterior = models.DecimalField(max_digits=15, decimal_places=2)
    abonos = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    pendiente_por_pagar = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.cliente.nombre} - cxc : {self.n_cxc}"

class NotaCredito(models.Model):
    cuenta = models.OneToOneField('CuentaPorCobrar',on_delete=models.CASCADE,related_name='notacredito')
    descripcion = models.TextField()
    creada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Nota de crédito para CxC {self.cuenta.n_cxc}"
    
class EstadoResultadosMensual(models.Model):
    anio = models.PositiveIntegerField()
    mes = models.PositiveSmallIntegerField(choices=[(i, _(str(i))) for i in range(1, 13)])
    ingresos_total = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    costos_operacion_total = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    utilidad_bruta = models.DecimalField(max_digits=15, decimal_places=2)
    gastos_administrativos_total = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    utilidad_operacional = models.DecimalField(max_digits=15, decimal_places=2)
    otros_costos_total = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    utilidad_antes_impuestos = models.DecimalField(max_digits=15, decimal_places=2)
    gastos_impuestos = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    utilidad_neta = models.DecimalField(max_digits=15, decimal_places=2)
    # DESGLOSE POR CONCEPTO (agrupaciones)
    ingresos_detalle = JSONField(default=dict)
    costos_operacion_detalle = JSONField(default=dict)
    gastos_administrativos_detalle = JSONField(default=dict)
    otros_costos_detalle = JSONField(default=dict)
    impuestos_detalle = JSONField(default=dict)
    creado = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('anio', 'mes')
        verbose_name = "Estado de Resultados Mensual"
        verbose_name_plural = "Estados de Resultados Mensuales"

    def __str__(self):
        return f"Estado de Resultados - {self.mes}/{self.anio}"

class PermisoPersonalizado(models.Model):

    accion = models.CharField(max_length=100, unique=True)

    admin = models.BooleanField(default=False)
    gerente = models.BooleanField(default=False)
    sprempleado = models.BooleanField(default=False)
    empleado = models.BooleanField(default=False)

    def __str__(self):
        return self.accion
    
