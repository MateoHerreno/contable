
from rest_framework.response import Response
from .models import*
from rest_framework import viewsets,status
from . serializers import *
from django.core.mail import BadHeaderError, EmailMessage
from rest_framework.views import APIView
import pytz
est = pytz.timezone('America/Bogota')
from .utils import generar_token, enviar_email_recuperacion

# Create your views here.

# API with rest framework

class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

class TiendaViewSet(viewsets.ModelViewSet):
    queryset = Tienda.objects.all()
    serializer_class = TiendaSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class CuentaPorPagarViewSet(viewsets.ModelViewSet):
    queryset = CuentaPorPagar.objects.all()
    serializer_class = CuentaPorPagarSerializer

class CuentaPorCobrarViewSet(viewsets.ModelViewSet):
    queryset = CuentaPorCobrar.objects.all()
    serializer_class = CuentaPorCobrarSerializer

class PasswordResetAPIView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Contraseña actualizada correctamente."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SolicitudRecuperacionAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            usuario = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            return Response({'error': 'No existe un usuario con ese email, envia un post json- "email": "usuario@correo.com"  '}, status=status.HTTP_404_NOT_FOUND)
        
        token = generar_token()
        usuario.token_recuperar = token
        usuario.save()
        
        enviar_email_recuperacion(usuario.email, token)
        return Response({'mensaje': 'Token de recuperación enviado a tu email.'}, status=status.HTTP_200_OK)
    