import os

# Directorio base del proyecto (ajustado para estar en la raíz)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Clave secreta (cámbiala por una única y segura en producción)
SECRET_KEY = 'django-insecure-tu_clave_secreta_aqui_usa_una_segura'  # Cambia esto en producción

# Modo debug
DEBUG = True

# Hosts permitidos
ALLOWED_HOSTS = []

# Directorio de las plantillas
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

# Directorio de los archivos estáticos
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# Configuración de las aplicaciones
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user_management.apps.UserManagementConfig',  # Especificamos la configuración de la app
    'project_tasks',
    'job_market',
    'ai_component',
    'external_integration',
]

# Middleware necesario
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuración de URLs
ROOT_URLCONF = 'urls'

# Configuración de las plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Configuración de WSGI
WSGI_APPLICATION = 'wsgi.application'

# Configuración de la base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'task_manager_db',
        'USER': 'postgres',
        'PASSWORD': '12345678',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Configuración de la autenticación
AUTH_USER_MODEL = 'user_management.User'

# Configuración de URLs de autenticación
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Configuración de archivos estáticos
# Configuración de archivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Nueva línea
# Configuración de idioma y zona horaria
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Configuración de campos automáticos
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'