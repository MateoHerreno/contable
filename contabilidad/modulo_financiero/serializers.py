from rest_framework import serializers
from .models import *

class EmpresaSerializer(serializers.ModelSerializer):
    perfiles = serializers.StringRelatedField(many=True)
    class Meta:
        model = Empresa
        fields = '__all__'

class TiendaSerializer(serializers.ModelSerializer):
    cantidad_usuarios = serializers.SerializerMethodField()
    class Meta:
        model = Tienda
        fields = ['id','nombre','direccion','ciudad','empresa', 'cantidad_usuarios',]
    def get_cantidad_usuarios(self, obj):
        return obj.usuario_set.count()

class UsuarioSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, label="confirm password")

    class Meta:
        model = Usuario
        fields = [
             'id','nombre', 'email', 'password','password2', 'telefono', 
            'is_active', 'tienda', 'rol'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep.pop('password', None)
        return rep

    def validate(self, data):
        password = data.get('password')
        password2 = self.initial_data.get('password2')  # lee el dato directamente del request
        if password != password2:
            raise serializers.ValidationError({
                'password2': 'Las contraseñas no coinciden.'
            })
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        usuario = Usuario(**validated_data)
        usuario.set_password(password)
        usuario.save()
        return usuario

    def validate_email(self, value):
        usuario_actual = self.instance
        if Usuario.objects.exclude(pk=usuario_actual.pk if usuario_actual else None).filter(email=value).exists():
            raise serializers.ValidationError("Este correo ya está registrado por otro usuario.")
        return value

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token_recuperar = serializers.CharField()
    nueva_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    confirmar_password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        if data['nueva_password'] != data['confirmar_password']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        return data

    def save(self):
        email = self.validated_data['email']
        token = self.validated_data['token_recuperar']
        nueva_password = self.validated_data['nueva_password']

        try:
            usuario = Usuario.objects.get(email=email, token_recuperar=token)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError("Email o token de recuperación inválido.")

        usuario.set_password(nueva_password)
        usuario.token_recuperar = 0  # Limpia el token
        usuario.save()
        return usuario

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
