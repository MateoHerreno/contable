from django.db import models
from django.contrib.auth.models import AbstractUser
from .authentication import CustomUserManager
from django.utils import timezone

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
        return f"{self.nombre} - {[p.nombre for p in self.perfiles.all()]}"
    
class Tienda(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    cantidad_empleados = models.IntegerField(null = False, default=0)

    def __str__(self):
        return self.nombre

class Usuario(AbstractUser):
    username = None
    is_superuser = None
    first_name = None
    last_name = None
    is_staff = None
    groups = None
    nombre = models.CharField(max_length=254)
    email = models.EmailField(max_length=254, unique=True,blank=False,null=True)
    password = models.CharField(max_length=254,blank=False,null=True)
    token_recuperar = models.CharField(max_length=254,blank=False,null=False,default=0)
    telefono =models.IntegerField(null=False,blank=True,default='0')
    is_active = models.BooleanField(default=True)
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE, null=True, blank=True)
    ROLES = (
        (1, "administrador"),
        (2, "gerente"),
        (3, "super_empleado"),
        (4, "empleado"), 
    )
    rol=models.IntegerField(choices=ROLES,default=4)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nombre"]
    objects = CustomUserManager()
    def __str__(self):
        return self.nombre

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
    concepto = models.TextField(blank=True, null=True)
    val_bruto = models.DecimalField(max_digits=15, decimal_places=2)
    iva = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    neto_facturado = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    saldo_anterior = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    abonos = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    pendiente_por_pagar = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.proveedor.nombre} - cxp:{self.n_cxp}"

class CuentaPorCobrar(models.Model):
    fecha = models.DateTimeField(default = timezone.now)
    n_cxc =  models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    concepto = models.TextField(blank=True, null=True)
    val_bruto = models.DecimalField(max_digits=15, decimal_places=2)
    iva = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    retenciones = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    neto_facturado = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    saldo_anterior = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    abonos = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    pendiente_por_pagar = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.cliente.nombre} - cxc:{self.n_cxc}"
