from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import *
from decimal import Decimal, ROUND_HALF_UP
from django.db.models import Sum
from .utils import*
from datetime import datetime

class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = '__all__'

class EmpresaSerializer(serializers.ModelSerializer):
    perfiles_nombres = serializers.SerializerMethodField()

    class Meta:
        model = Empresa
        fields = '__all__'
        extra_fields = ['perfiles_nombres']

    def get_perfiles_nombres(self, obj):
        return [p.nombre for p in obj.perfiles.all()]

class TiendaSerializer(serializers.ModelSerializer):
    cantidad_usuarios = serializers.SerializerMethodField()
    class Meta:
        model = Tienda
        fields = ['id','nombre','direccion','ciudad','empresa', 'cantidad_usuarios',]
    def get_cantidad_usuarios(self, obj):
        return obj.usuario_set.count()

class UsuarioSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        write_only=True,
        label="confirm password",
        required=False  # Solo se validará si es necesario
    )
    tienda = serializers.PrimaryKeyRelatedField(
        queryset=Tienda.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Usuario
        fields = [
            'id', 'nombre', 'email', 'password', 'password2', 'telefono',
            'is_active', 'tienda', 'rol'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep.pop('password', None)
        rep.pop('password2', None)  # Oculta también password2 si por alguna razón se incluye
        return rep

    def validate(self, data):
        password = data.get('password')
        password2 = self.initial_data.get('password2')

        if self.instance is None:
            # Crear: ambos campos deben estar y coincidir
            if not password or not password2:
                raise serializers.ValidationError({
                    'password2': 'Debes confirmar la contraseña.'
                })
            if password != password2:
                raise serializers.ValidationError({
                    'password2': 'Las contraseñas no coinciden.'
                })

        else:
            # Editar: solo se valida si se incluye una contraseña
            if password:
                if not password2:
                    raise serializers.ValidationError({
                        'password2': 'Debes confirmar la nueva contraseña.'
                    })
                if password != password2:
                    raise serializers.ValidationError({
                        'password2': 'Las contraseñas no coinciden.'
                    })

        return data

    def validate_email(self, value):
        usuario_actual = self.instance
        if Usuario.objects.exclude(pk=usuario_actual.pk if usuario_actual else None).filter(email=value).exists():
            raise serializers.ValidationError("Este correo ya está registrado por otro usuario.")
        return value

    def validate_rol(self, value):
        request = self.context.get('request')
        if request and hasattr(request.user, 'rol'):
            if value < request.user.rol:
                raise serializers.ValidationError("No puedes asignar un rol superior al tuyo.")
        return value

    def create(self, validated_data):
        validated_data.pop('password2', None)
        password = validated_data.pop('password')
        usuario = Usuario(**validated_data)
        usuario.set_password(password)

        request = self.context.get('request')
        if request and request.user.is_authenticated:
            usuario._modificado_por = request.user

        usuario.save()
        return usuario

    def update(self, instance, validated_data):
        validated_data.pop('password2', None)
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        request = self.context.get('request')
        if request and request.user.is_authenticated:
            instance._modificado_por = request.user

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
    saldo = serializers.SerializerMethodField()
    class Meta:
        model = Proveedor
        fields = ['id', 'nombre', 'nit', 'telefono', 'saldo']
    def get_saldo(self, obj):
        return format_decimal_humano(obj.saldo)

class ClienteSerializer(serializers.ModelSerializer):
    saldo = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'nit', 'telefono', 'saldo']
    def get_saldo(self, obj):
        return format_decimal_humano(obj.saldo)
    
class ConceptoCXPSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConceptoCXP
        fields = '__all__'

class ConceptoCXCSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConceptoCXC
        fields = '__all__'

class CuentaPorCobrarSerializer(serializers.ModelSerializer):
    descripcion_nota_credito = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        help_text="Descripción para nota de crédito si valor bruto es negativo"
    )

    class Meta:
        model = CuentaPorCobrar
        fields = '__all__'
        read_only_fields = ('fecha', 'neto_facturado', 'saldo_anterior', 'pendiente_por_pagar')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # Formatear números
        """for field in [
            'val_bruto', 'iva', 'retenciones', 'neto_facturado',
            'saldo_anterior', 'abonos', 'pendiente_por_pagar'
        ]:
            if rep.get(field) is not None:
                rep[field] = format_decimal_humano(rep[field])"""

        if rep.get('fecha'):
            try:
                fecha_obj = datetime.fromisoformat(rep['fecha'].replace('Z', '+00:00'))
                rep['fecha'] = fecha_obj.strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                pass 
        # Mostrar descripción de nota de crédito si existe
        try:
            rep['nota_credito'] = {
                'descripcion': instance.notacredito.descripcion
            }
        except NotaCredito.DoesNotExist:
            rep['nota_credito'] = None  # o simplemente no incluirlo
        return rep
    
    def validate(self, data):
        val_bruto = data.get('val_bruto')
        descripcion = self.initial_data.get('descripcion_nota_credito', '').strip()

        if val_bruto is not None and val_bruto < 0:
            if not descripcion:
                if not self.instance:
                    # Es creación y no se envió descripción
                    raise serializers.ValidationError({
                        'descripcion_nota_credito': 'Debes proporcionar una descripción si el valor bruto es negativo.'
                    })
                else:
                    # Es edición: verificar si ya hay nota existente
                    from backend_modfinanciero.models import NotaCredito
                    tiene_nota = NotaCredito.objects.filter(cuenta=self.instance).exists()
                    if not tiene_nota:
                        raise serializers.ValidationError({
                            'descripcion_nota_credito': 'Debes proporcionar una descripción si el valor bruto es negativo.'
                        })

        return data

    def create(self, validated_data):

        cliente = validated_data['cliente']
        conceptoFijo = validated_data.get('conceptoFijo')
        descripcion_nc = self.initial_data.get('descripcion_nota_credito', '').strip()
        val_bruto = validated_data.get('val_bruto')
        abonos = validated_data.get('abonos') or Decimal('0')
        iva_pct = validated_data.pop('iva', 0)
        retenciones_pct = validated_data.pop('retenciones', 0)

        if iva_pct not in [0, 5, 19]:
            raise serializers.ValidationError({'iva': 'Solo se permiten valores de IVA: 0, 5 o 19.'})
        if not (0 <= retenciones_pct <= 12):
            raise serializers.ValidationError({'retenciones': 'Las retenciones deben estar entre 0% y 12%.'})

        iva = (val_bruto * Decimal(iva_pct) / Decimal(100)).quantize(Decimal('1.'), rounding=ROUND_HALF_UP)
        retenciones = (val_bruto * Decimal(retenciones_pct) / Decimal(100)).quantize(Decimal('1.'), rounding=ROUND_HALF_UP)
        neto_facturado = val_bruto + iva - retenciones

        cuenta = CuentaPorCobrar.objects.create(
            cliente=cliente,
            conceptoFijo=conceptoFijo,
            conceptoDetalle=validated_data.get('conceptoDetalle'),
            val_bruto=val_bruto,
            iva=iva,
            retenciones=retenciones,
            neto_facturado=neto_facturado,
            abonos=abonos,
            saldo_anterior=Decimal('0'),              # ← valor temporal
            pendiente_por_pagar=Decimal('0')          # ← valor temporal
        )

        if val_bruto < 0:
            NotaCredito.objects.create(
                cuenta=cuenta,
                descripcion=descripcion_nc
            )

        recalcular_saldos_cliente(cliente.id)
        return cuenta

    def update(self, instance, validated_data):
        from backend_modfinanciero.models import NotaCredito
        from backend_modfinanciero.utils import recalcular_saldos_cliente

        for campo in ['fecha', 'saldo_anterior', 'neto_facturado', 'pendiente_por_pagar']:
            validated_data.pop(campo, None)

        instance.conceptoFijo = validated_data.get('conceptoFijo', instance.conceptoFijo)
        instance.conceptoDetalle = validated_data.get('conceptoDetalle', instance.conceptoDetalle)
        instance.val_bruto = validated_data.get('val_bruto', instance.val_bruto)

        if 'iva' in validated_data:
            iva_pct = validated_data.pop('iva')
            if iva_pct not in [0, 5, 19]:
                raise serializers.ValidationError({'iva': 'Solo se permiten valores de IVA: 0, 5 o 19.'})
            instance.iva = (instance.val_bruto * Decimal(iva_pct) / Decimal(100)).quantize(Decimal('1.'), rounding=ROUND_HALF_UP)

        if 'retenciones' in validated_data:
            retenciones_pct = validated_data.pop('retenciones')
            if not (0 <= retenciones_pct <= 12):
                raise serializers.ValidationError({'retenciones': 'Las retenciones deben estar entre 0% y 12.'})
            instance.retenciones = (instance.val_bruto * Decimal(retenciones_pct) / Decimal(100)).quantize(Decimal('1.'), rounding=ROUND_HALF_UP)

        instance.abonos = validated_data.get('abonos', instance.abonos or Decimal('0'))
        instance.neto_facturado = instance.val_bruto + instance.iva - instance.retenciones
        instance.saldo_anterior = Decimal('0')            # valor temporal
        instance.pendiente_por_pagar = Decimal('0')       # valor temporal
        instance.save()

        # Nota de crédito (si corresponde)
        if instance.val_bruto < 0:
            descripcion_nc = self.initial_data.get('descripcion_nota_credito', '').strip()
            nota_existente = NotaCredito.objects.filter(cuenta=instance).first()

            if descripcion_nc:
                NotaCredito.objects.update_or_create(
                    cuenta=instance,
                    defaults={'descripcion': descripcion_nc}
                )
            elif not nota_existente:
                raise serializers.ValidationError({
                    'descripcion_nota_credito': 'Debes proporcionar una descripción si el valor bruto es negativo.'
                })
        else:
            NotaCredito.objects.filter(cuenta=instance).delete()

        # Recalcular saldos completos del cliente
        recalcular_saldos_cliente(instance.cliente.id)
        return instance
     
class CuentaPorPagarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuentaPorPagar
        fields = '__all__'
        read_only_fields = ('fecha', 'saldo_anterior', 'pendiente_por_pagar')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        """for field in ['val_bruto', 'saldo_anterior', 'abonos', 'pendiente_por_pagar']:
            if rep.get(field) is not None:
                rep[field] = format_decimal_humano(rep[field])"""
        if rep.get('fecha'):
            try:
                fecha_obj = datetime.fromisoformat(rep['fecha'].replace('Z', '+00:00'))
                rep['fecha'] = fecha_obj.strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                pass
        return rep

    def create(self, validated_data):
        from backend_modfinanciero.utils import recalcular_saldos_proveedor

        proveedor = validated_data['proveedor']
        conceptoFijo = validated_data.get('conceptoFijo')
        val_bruto = validated_data.get('val_bruto', Decimal('0'))
        abonos = validated_data.get('abonos') or Decimal('0')

        # Validaciones
        if val_bruto < 0:
            raise serializers.ValidationError({'val_bruto': 'El valor bruto no puede ser negativo.'})
        if abonos < 0:
            raise serializers.ValidationError({'abonos': 'Los abonos no pueden ser negativos.'})

        # Crear con valores temporales
        cuenta = CuentaPorPagar.objects.create(
            proveedor=proveedor,
            conceptoFijo=conceptoFijo,
            conceptoDetalle=validated_data.get('conceptoDetalle'),
            val_bruto=val_bruto,
            abonos=abonos,
            saldo_anterior=Decimal('0'),
            pendiente_por_pagar=Decimal('0')
        )

        # Recalcular todas las cuentas del proveedor
        recalcular_saldos_proveedor(proveedor.id)
        return cuenta

    def update(self, instance, validated_data):
        from backend_modfinanciero.utils import recalcular_saldos_proveedor

        for campo in ['fecha', 'saldo_anterior', 'pendiente_por_pagar']:
            validated_data.pop(campo, None)

        instance.conceptoFijo = validated_data.get('conceptoFijo', instance.conceptoFijo)
        instance.conceptoDetalle = validated_data.get('conceptoDetalle', instance.conceptoDetalle)
        instance.val_bruto = validated_data.get('val_bruto', instance.val_bruto)
        instance.abonos = validated_data.get('abonos', instance.abonos or Decimal('0'))

        # Validaciones
        if instance.val_bruto < 0:
            raise serializers.ValidationError({'val_bruto': 'El valor bruto no puede ser negativo.'})
        if instance.abonos < 0:
            raise serializers.ValidationError({'abonos': 'Los abonos no pueden ser negativos.'})

        # Valores temporales antes de recalcular
        instance.saldo_anterior = Decimal('0')
        instance.pendiente_por_pagar = Decimal('0')
        instance.save()

        # Recalcular historial completo
        recalcular_saldos_proveedor(instance.proveedor.id)
        return instance

class NotaCreditoSerializer(serializers.ModelSerializer):
    cuenta = serializers.PrimaryKeyRelatedField(queryset=CuentaPorCobrar.objects.filter(val_bruto__lt=0))

    class Meta:
        model = NotaCredito
        fields = ['id', 'cuenta', 'descripcion', 'creada']
        read_only_fields = ['id', 'creada']
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if rep.get('fecha'):
            try:
                fecha_obj = datetime.fromisoformat(rep['fecha'].replace('Z', '+00:00'))
                rep['fecha'] = fecha_obj.strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                pass
        return rep
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Obtener los tokens base
        data = super().validate(attrs)

        # Añadir datos adicionales
        data.update({
            'rol': self.user.rol,
            'nombre': self.user.nombre,
        })

        return data