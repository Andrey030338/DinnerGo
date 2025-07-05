from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.db.models import Q

# Backend personalizado para permitir inicio de sesión usando nombre o correo electrónico
class AutenticacionPorNombreOCorreo(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            # Buscar al usuario usando el nombre (first_name) o el correo electrónico
            usuario = User.objects.get(Q(first_name=username) | Q(email=username))
            
            # Verificar que la contraseña proporcionada sea correcta
            if usuario.check_password(password):
                return usuario
        except User.DoesNotExist:
            # Si no se encuentra el usuario, retornar None
            return None

    def get_user(self, user_id):
        try:
            # Obtener el usuario por su ID primario
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            # Si no existe el usuario, retornar None
            return None
