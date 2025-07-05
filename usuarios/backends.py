from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.db.models import Q

class AutenticacionPorNombreOCorreo(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            # Buscar por username (nombre de usuario) o por email
            usuario = User.objects.get(Q(username=username) | Q(email=username))
            
            # Verificamos si la contraseña coincide
            if usuario.check_password(password):
                return usuario
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None