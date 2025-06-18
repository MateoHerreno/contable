from rest_framework import serializers
from .models import *
from decimal import Decimal, ROUND_HALF_UP
from django.db.models import Sum
from .utils import*

class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = '__all__'

class EmpresaSerializer(serializers.ModelSerializer):
    perfiles = serializers.PrimaryKeyRelatedField(many=True,queryset=Perfil.objects.all())
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
            'id', 'nombre', 'email', 'password', 'password2', 'telefono',
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
        validated_data.pop('password2')
        password = validated_data.pop('password')
        usuario = Usuario(**validated_data)
        usuario.set_password(password)

        # Seguridad extra: pasa el usuario autenticado al modelo
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            usuario._modificado_por = request.user

        usuario.save()
        return usuario

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        # Seguridad extra: pasa el usuario autenticado al modelo
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
        for field in [
            'val_bruto', 'iva', 'retenciones', 'neto_facturado',
            'saldo_anterior', 'abonos', 'pendiente_por_pagar'
        ]:
            if rep.get(field) is not None:
                rep[field] = format_decimal_humano(rep[field])
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
        if val_bruto < 0 and not descripcion:
            raise serializers.ValidationError({
                'descripcion_nota_credito': 'Debes proporcionar una descripción si el valor bruto es negativo.'
            })
        return data

    def create(self, validated_data):
        from modulo_financiero.models import NotaCredito

        cliente = validated_data['cliente']
        conceptoFijo = validated_data.get('conceptoFijo')
        descripcion_nc = self.initial_data.get('descripcion_nota_credito', '').strip()
        val_bruto = validated_data.get('val_bruto',)
        abonos = validated_data.get('abonos') or Decimal('0')

        iva_pct = validated_data.pop('iva', 0)
        if iva_pct not in [0, 5, 19]:
            raise serializers.ValidationError({'iva': 'Solo se permiten valores de IVA: 0, 5 o 19.'})

        retenciones_pct = validated_data.pop('retenciones', 0)
        if not (0 <= retenciones_pct <= 12):
            raise serializers.ValidationError({'retenciones': 'Las retenciones deben estar entre 0% y 12%.'})

        iva = (val_bruto * Decimal(iva_pct) / Decimal(100)).quantize(Decimal('1.'), rounding=ROUND_HALF_UP)
        retenciones = (val_bruto * Decimal(retenciones_pct) / Decimal(100)).quantize(Decimal('1.'), rounding=ROUND_HALF_UP)

        saldo_anterior = cliente.cuentaporcobrar_set.aggregate(
            total=Sum('pendiente_por_pagar')
        )['total'] or Decimal('0')

        neto_facturado = val_bruto + iva - retenciones
        pendiente_por_pagar = neto_facturado + saldo_anterior - abonos

        cuenta = CuentaPorCobrar.objects.create(
            cliente=cliente,
            conceptoFijo=conceptoFijo,
            conceptoDetalle=validated_data.get('conceptoDetalle'),
            val_bruto=val_bruto,
            iva=iva,
            retenciones=retenciones,
            neto_facturado=neto_facturado,
            saldo_anterior=saldo_anterior,
            abonos=abonos,
            pendiente_por_pagar=pendiente_por_pagar
        )

        if val_bruto < 0:
            NotaCredito.objects.create(
                cuenta=cuenta,
                descripcion=descripcion_nc
            )

        cliente.saldo = pendiente_por_pagar
        cliente.save()
        return cuenta

    def update(self, instance, validated_data):
        from modulo_financiero.models import NotaCredito

        descripcion_nc = self.initial_data.get('descripcion_nota_credito', '').strip()

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
                raise serializers.ValidationError({'retenciones': 'Las retenciones deben estar entre 0% y 12%.'})
            instance.retenciones = (instance.val_bruto * Decimal(retenciones_pct) / Decimal(100)).quantize(Decimal('1.'), rounding=ROUND_HALF_UP)

        instance.abonos = validated_data.get('abonos', instance.abonos or Decimal('0'))
        instance.neto_facturado = instance.val_bruto + instance.iva - instance.retenciones
        instance.pendiente_por_pagar = instance.neto_facturado + instance.saldo_anterior - instance.abonos
        instance.save()

        if instance.val_bruto < 0:
            if not descripcion_nc:
                raise serializers.ValidationError({
                    'descripcion_nota_credito': 'Debes proporcionar una descripción si el valor bruto es negativo.'
                })
            NotaCredito.objects.update_or_create(
                cuenta=instance,
                defaults={'descripcion': descripcion_nc}
            )
        else:
            NotaCredito.objects.filter(cuenta=instance).delete()

        cuentas_cliente = CuentaPorCobrar.objects.filter(cliente=instance.cliente).exclude(pk=instance.pk)
        cuenta_mas_reciente = cuentas_cliente.order_by('-fecha', '-n_cxc').first()
        if not cuenta_mas_reciente or instance.fecha > cuenta_mas_reciente.fecha:
            instance.cliente.saldo = instance.pendiente_por_pagar
            instance.cliente.save()

        return instance
     
class CuentaPorPagarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuentaPorPagar
        fields = '__all__'
        read_only_fields = ('fecha', 'saldo_anterior', 'pendiente_por_pagar')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        for field in ['val_bruto', 'saldo_anterior', 'abonos', 'pendiente_por_pagar']:
            if rep.get(field) is not None:
                rep[field] = format_decimal_humano(rep[field])
        return rep

    def create(self, validated_data):
        proveedor = validated_data['proveedor']
        conceptoFijo = validated_data.get('conceptoFijo')
        val_bruto = validated_data.get('val_bruto', Decimal('0'))
        abonos = validated_data.get('abonos') or Decimal('0')

        # Validaciones
        if val_bruto < 0:
            raise serializers.ValidationError({'val_bruto': 'El valor bruto no puede ser negativo.'})
        if abonos < 0:
            raise serializers.ValidationError({'abonos': 'Los abonos no pueden ser negativos.'})

        saldo_anterior = proveedor.cuentaporpagar_set.aggregate(
            total=Sum('pendiente_por_pagar')
        )['total'] or Decimal('0')

        pendiente_por_pagar = val_bruto + saldo_anterior - abonos

        cuenta = CuentaPorPagar.objects.create(
            proveedor=proveedor,
            conceptoFijo=conceptoFijo,
            conceptoDetalle=validated_data.get('conceptoDetalle'),
            val_bruto=val_bruto,
            saldo_anterior=saldo_anterior,
            abonos=abonos,
            pendiente_por_pagar=pendiente_por_pagar
        )

        proveedor.saldo = pendiente_por_pagar
        proveedor.save()

        return cuenta

    def update(self, instance, validated_data):
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

        saldo_anterior = instance.proveedor.cuentaporpagar_set.exclude(pk=instance.pk).aggregate(
            total=Sum('pendiente_por_pagar')
        )['total'] or Decimal('0')

        instance.saldo_anterior = saldo_anterior
        instance.pendiente_por_pagar = instance.val_bruto + saldo_anterior - instance.abonos
        instance.save()

        cuentas = CuentaPorPagar.objects.filter(proveedor=instance.proveedor).exclude(pk=instance.pk)
        mas_reciente = cuentas.order_by('-fecha', '-n_cxp').first()

        if not mas_reciente or instance.fecha > mas_reciente.fecha:
            instance.proveedor.saldo = instance.pendiente_por_pagar
            instance.proveedor.save()

        return instance

class NotaCreditoSerializer(serializers.ModelSerializer):
    cuenta = serializers.PrimaryKeyRelatedField(queryset=CuentaPorCobrar.objects.filter(val_bruto__lt=0))

    class Meta:
        model = NotaCredito
        fields = ['id', 'cuenta', 'descripcion', 'creada']
        read_only_fields = ['id', 'creada']