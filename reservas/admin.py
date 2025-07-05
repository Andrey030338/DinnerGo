# Importa el sistema de administración de Django
from django.contrib import admin

# Importa los modelos que quieres que aparezcan en el panel de administración
from .models import Restaurante, Mesa, Reserva, Plato

# Register your models here. (Registra aquí tus modelos)

# Registrar cada modelo en el panel de administración
# Esto permite que puedas gestionarlos visualmente desde /admin

admin.site.register(Restaurante)  # Permite crear, editar y eliminar restaurantes
admin.site.register(Mesa)         # Permite gestionar las mesas disponibles
admin.site.register(Reserva)      # Permite ver y administrar las reservas hechas
admin.site.register(Plato)        # Permite crear, editar y eliminar platos del menú
