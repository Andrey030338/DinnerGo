from django.urls import path  # Importamos la función path para definir las rutas
from . import views  # Importamos nuestras vistas personalizadas
from django.contrib.auth import views as auth_views  # Importamos las vistas de autenticación de Django
from . import views  # (opcional, ya está importado arriba)

# Lista de rutas que Django usará para esta aplicación
urlpatterns = [
    # Ruta para registrar nuevos usuarios
    path('registro/', views.registrar_usuario, name='registro'),

    # Ruta para iniciar sesión usando la vista genérica de Django, con nuestra plantilla personalizada
   path('login/', views.login_view, name='login'),

    # Ruta principal (home) del sitio
    path('', views.home, name='home'),

    # Ruta para cerrar sesión (usamos nuestra vista personalizada)
    path('logout/', views.logout_view, name='logout'),

    #Verificacion de correo
    
    path('verificar-correo/<str:token>/', views.verificar_correo, name='verificar_correo'),
    path('verificar-correo-registro/<str:token>/', views.verificar_correo_registro, name='verificar_correo_registro'),
    path('reenviar-verificacion-registro/', views.reenviar_verificacion_registro, name='reenviar_verificacion_registro'),
    path('crear-empleado/', views.crear_empleado, name='crear_empleado'),
    path('panel-gerente/', views.panel_gerente, name='panel_gerente'),
    path('ver-empleados/', views.ver_empleados, name='ver_empleados'),

    # URLs para recuperación de contraseña
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='usuarios/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='usuarios/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='usuarios/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='usuarios/password_reset_complete.html'), name='password_reset_complete'),
    

]
