
from django.shortcuts import render,redirect
from django.http import HttpResponse
from rest_framework.response import Response
from .models import*
from rest_framework import viewsets
from . serializers import *
from django.contrib import messages
from .crypt import *
from django.db import IntegrityError, transaction
from django.core.mail import BadHeaderError, EmailMessage
import datetime
from django.utils.timezone import localtime
from rest_framework.views import APIView
import re
import pytz
est = pytz.timezone('America/Bogota')
from .autorizacion import * 
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


#usuario desde api
"""
class RegistrarUsuario(APIView):
    def post(self, request):
        print(request.data)
        if request.method == "POST":
            nombre = request.data["nombre"]
            correo = request.data["correo"]
            clave1 = request.data["password"]
            clave2 = request.data["confirmPassword"]
            nick = correo
            if nombre == "" or correo == "" or clave1 == "" or clave2 == "":
                return Response(data={'message': 'Todos los campos son obligatorios', 'respuesta': 400}, status=400)
            elif not re.fullmatch(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', correo):
                return Response(data={'message': 'El correo no es válido', 'respuesta': 400}, status=400)
            elif clave1 != clave2:
                return Response(data={'message': 'Las contraseñas no coinciden', 'respuesta': 400}, status=400)
            else:
                try:
                    q = Usuario(
                        nombre=nombre,
                        email=correo,
                        password=hash_password(clave1),
                    )
                    q.save()
                except Exception as e:
                    return Response(data={'message': 'El Usuario ya existe', 'respuesta': 409}, status=409)

        # Renderiza la misma página de registro con los mensajes de error
        return Response(data={'message': f'Usuario creado correctamente tu nick es: {nick}', 'respuesta': 201}, status=201)
"""