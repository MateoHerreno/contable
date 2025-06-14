from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin
from .authentication import CustomUserManager
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

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
    telefono = models.IntegerField(null=False, blank=True, default='0')
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

class CuentaPorPagar(models.Model):
    fecha = models.DateTimeField(default = timezone.now)
    n_cxp =  models.AutoField(primary_key=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    concepto = models.TextField(blank=False, null=False)
    val_bruto = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    iva = models.DecimalField(max_digits=15, decimal_places=2,default=0,validators=[MinValueValidator(0)] )
    neto_facturado = models.DecimalField(max_digits=15, decimal_places=2,default=0,validators=[MinValueValidator(0)])
    saldo_anterior = models.DecimalField(max_digits=15, decimal_places=2)
    abonos = models.DecimalField(max_digits=15, decimal_places=2, default=0,validators=[MinValueValidator(0)])
    pendiente_por_pagar = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.proveedor.nombre} - cxp:{self.n_cxp}"

class CuentaPorCobrar(models.Model):
    fecha = models.DateTimeField(default=timezone.now)
    n_cxc = models.AutoField(primary_key=True)
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    concepto = models.TextField(blank=False, null=False)  # obligatorio
    val_bruto = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    iva = models.DecimalField(max_digits=15, decimal_places=2,default=0,validators=[MinValueValidator(0)] )
    retenciones = models.DecimalField(max_digits=15, decimal_places=2,default=0,validators=[MinValueValidator(0)])
    neto_facturado = models.DecimalField(max_digits=15, decimal_places=2,default=0,validators=[MinValueValidator(0)])
    saldo_anterior = models.DecimalField(max_digits=15, decimal_places=2)
    abonos = models.DecimalField(max_digits=15, decimal_places=2, default=0,validators=[MinValueValidator(0)])
    pendiente_por_pagar = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.cliente.nombre} - cxc:{self.n_cxc}"

class PermisoPersonalizado(models.Model):
    accion = models.CharField(max_length=100, unique=True)

    admin = models.BooleanField(default=False)
    gerente = models.BooleanField(default=False)
    sprempleado = models.BooleanField(default=False)
    empleado = models.BooleanField(default=False)

    def __str__(self):
        return self.accion