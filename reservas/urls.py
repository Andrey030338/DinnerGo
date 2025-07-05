# Importa la función 'path' para definir rutas y 'views' para vincularlas a funciones
from django.urls import path
from . import views  # Importa las vistas locales de esta app (reservas)

# Lista de URLs disponibles para esta app
urlpatterns = [

    # Ruta principal: muestra la lista de mesas disponibles
    # http://localhost:8000/reservas/
    path('', views.lista_mesas, name='lista_mesas'),

    # Ruta para hacer una reserva en una mesa específica (usa el id de la mesa)
    # http://localhost:8000/reservas/reserva/3/
    path('reserva/<int:mesa_id>/', views.hacer_reserva, name='hacer_reserva'),

    # Ruta que muestra la confirmación cuando la reserva se completa con éxito
    # http://localhost:8000/reservas/reserva-exitosa/5/
    path('reserva-exitosa/<int:reserva_id>/', views.reserva_exitosa, name='reserva_exitosa'),
]
