# Archivo de configuración principal de Django para el proyecto DinnerGo

from pathlib import Path  # Librería para manejar rutas del sistema

# Construye la ruta base del proyecto (carpeta raíz)
BASE_DIR = Path(__file__).resolve().parent.parent


# CONFIGURACIONES BÁSICAS PARA DESARROLLO

# Clave secreta para seguridad (NO compartir en producción)
SECRET_KEY = 'django-insecure-ilgty49)is*arh+@($)=lvivz(rfv!_s@qikmi(0t5weo=&=4r'

# Modo de depuración activado (muestra errores detallados en el navegador)
DEBUG = True

# Lista de dominios/hosts permitidos para acceder a la web
ALLOWED_HOSTS = []  # Vacío durante desarrollo local


# APLICACIONES INSTALADAS EN EL PROYECTO

INSTALLED_APPS = [
    'django.contrib.admin',             # Panel de administración
    'django.contrib.auth',              # Sistema de autenticación
    'django.contrib.contenttypes',      # Manejo de modelos relacionados
    'django.contrib.sessions',          # Manejo de sesiones de usuario
    'django.contrib.messages',          # Sistema de mensajes
    'django.contrib.staticfiles',       # Archivos estáticos como CSS/JS
    'django.contrib.humanize',          # Filtros para mostrar datos de forma más legible (ej: 1,000 en vez de 1000)
    'reservas',                         # App para gestionar reservas
    'usuarios',                         # App para registro/login y perfiles de usuario
]


# MIDDLEWARE: Funciones que se ejecutan entre el navegador y el servidor

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',              # Seguridad general
    'django.contrib.sessions.middleware.SessionMiddleware',       # Manejo de sesiones
    'django.middleware.common.CommonMiddleware',                  # Middleware común de Django
    'django.middleware.csrf.CsrfViewMiddleware',                  # Protección contra ataques CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',    # Autenticación de usuarios
    'django.contrib.messages.middleware.MessageMiddleware',       # Sistema de mensajes flash
    'django.middleware.clickjacking.XFrameOptionsMiddleware',     # Protección contra clickjacking
    'django.middleware.locale.LocaleMiddleware',                  #
]


# Rutas principales del proyecto
ROOT_URLCONF = 'DinnerGo.urls'


# CONFIGURACIÓN DE PLANTILLAS HTML

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Motor de plantillas de Django
        'DIRS': [BASE_DIR / 'templates'],                              # Ruta a la carpeta de plantillas HTML
        'APP_DIRS': True,                                              # Activa búsqueda automática de plantillas en las apps
        'OPTIONS': {
            'context_processors': [                                    # Variables disponibles en todas las plantillas
                'django.template.context_processors.request',          
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Configuración del servidor WSGI (permite ejecutar el proyecto en servidores como Apache o Gunicorn)
WSGI_APPLICATION = 'DinnerGo.wsgi.application'


# BASE DE DATOS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',     # Motor de base de datos (SQLite por defecto)
        'NAME': BASE_DIR / 'db.sqlite3',            # Ruta al archivo de la base de datos
    }
}


# VALIDACIONES DE CONTRASEÑAS

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # Evita contraseñas parecidas al nombre o correo
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',            # Mínimo de caracteres
        'OPTIONS': {
            'min_length': 4  # Cambiado para que la contraseña sea al menos de 4 caracteres
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',           # Evita contraseñas comunes (ej: 123456)
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',          # Evita contraseñas solo numéricas
    },
]


# INTERNACIONALIZACIÓN Y ZONA HORARIA

LANGUAGE_CODE = 'es-co'  # Idioma por defecto del proyecto (puedes cambiarlo a 'es' si quieres en español)

TIME_ZONE = 'America/Bogota'  # Zona horaria (puedes poner 'America/Bogota' si estás en Colombia)

USE_I18N = True          # Activa traducción de textos

USE_TZ = True            # Usa zonas horarias con reconocimiento automático


# ARCHIVOS ESTÁTICOS (CSS, JS, imágenes)

import os  # Librería del sistema operativo para rutas

BASE_DIR = Path (__file__).resolve().parent.parent  # Se vuelve a definir BASE_DIR por seguridad

STATIC_URL = '/static/'  # URL base para acceder a los archivos estáticos

STATICFILES_DIRS = [     # Ruta de las carpetas donde buscará los archivos estáticos (en desarrollo)
    BASE_DIR / "static",
]


# TIPO DE CLAVE PRIMARIA POR DEFECTO PARA LOS MODELOS
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# REDIRECCIONES DESPUÉS DE LOGIN Y LOGOUT
LOGIN_REDIRECT_URL = '/'    # A dónde se redirige después de iniciar sesión
LOGOUT_REDIRECT_URL = '/'   # A dónde se redirige después de cerrar sesión


# AUTENTICACIONES PERSONALIZADAS
AUTHENTICATION_BACKENDS = [
    'usuarios.backends.AutenticacionPorNombreOCorreo',  # Permite iniciar sesión con nombre o correo
    'django.contrib.auth.backends.ModelBackend',         # Autenticación clásica de Django
]


# CONFIGURACIÓN DE ARCHIVOS MULTIMEDIA (imágenes de platos)

MEDIA_URL = '/media/'  # URL base para acceder a archivos multimedia

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Carpeta donde se guardan los archivos subidos por el usuario


# CONFIGURACIÓN DE CORREO ELECTRÓNICO
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'dinnergosa@gmail.com'
EMAIL_HOST_PASSWORD = 'rdvl rpjg xzqv kcte'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


LOGIN_URL = '/login/'


# Código secreto para registrar Gerentes
CODIGO_GERENTE = "DG-Admin2025"
