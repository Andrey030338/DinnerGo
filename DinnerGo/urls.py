"""
Configuración de URLs para el proyecto DinnerGo.

Este archivo se encarga de redirigir las URLs que escribe el usuario
(en el navegador) hacia las vistas correspondientes en tus apps.

Documentación oficial: https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

# Importa el panel de administración de Django
from django.contrib import admin

# Importa las funciones necesarias para definir rutas
from django.urls import path, include

# Importa configuraciones del proyecto (por ejemplo, DEBUG, MEDIA_URL, MEDIA_ROOT)
from django.conf import settings

# Importa función para servir archivos multimedia en desarrollo
from django.conf.urls.static import static


# Lista principal de URLs del proyecto
urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta al panel de administración (/admin)

    # Ruta principal que carga las URLs definidas en la app 'usuarios'
    # Por ejemplo, /login o /registro podrían estar aquí
    path('', include('usuarios.urls')),  
    
    # Ruta para acceder a las URLs de la app 'reservas'
    # Todas las URLs que empiecen con /reservas/ se buscarán en reservas/urls.py
    path('reservas/', include('reservas.urls')),
]


# Si estás en modo desarrollo (DEBUG=True), permite servir archivos multimedia (imágenes, etc.)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Esto hace que las imágenes que subas con MEDIA se puedan ver desde el navegador
