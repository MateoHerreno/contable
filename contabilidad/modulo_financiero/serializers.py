from rest_framework import serializers
from .models import *

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'

class TiendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tienda
        fields = 'id','nombre','direccion','ciudad','empresa', 'cantidad_empleados',

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = 'id', 'nombre','email','password','telefono','is_active','tienda', 'rol',

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = 'id','nombre','nit','telefono','saldo',

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = 'id','nombre','nit','telefono','saldo',

class CuentaPorPagarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuentaPorPagar
        fields = 'fecha','n_cxp','proveedor','concepto','val_bruto','iva','neto_facturado','saldo_anterior','abonos','pendiente_por_pagar',

class CuentaPorCobrarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuentaPorCobrar
        fields = 'fecha','n_cxp','cliente','concepto','val_bruto','iva','retenciones','neto_facturado','saldo_anterior','abonos','pendiente_por_pagar',
