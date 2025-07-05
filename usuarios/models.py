from django.contrib.auth.models import User  # Importamos el modelo de usuario que viene por defecto en Django
from django.db import models  # Importamos las herramientas para definir modelos (tablas)

# Creamos el modelo PerfilUsuario para guardar información adicional del usuario
"""class PerfilUsuario(models.Model):
    # Conectamos el perfil a un solo usuario (relación uno a uno)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    # Campo para guardar el número de teléfono del usuario
    telefono = models.CharField(max_length=20)

    # Esta función hace que al imprimir el perfil se vea el nombre del usuario
    def __str__(self):
        return self.usuario.username"""
class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20)
    verificado = models.BooleanField(default=False)  # NUEVO CAMPO

    def __str__(self):
        return self.usuario.username
