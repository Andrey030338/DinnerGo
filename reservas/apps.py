# Importa la clase base que permite configurar una app en Django
from django.apps import AppConfig


# Clase de configuración para la app 'reservas'
class ReservasConfig(AppConfig):
    # Define el tipo de campo automático por defecto para los modelos (id largo y seguro)
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Nombre interno de la aplicación (debe coincidir con el nombre de la carpeta de la app)
    name = 'reservas'
