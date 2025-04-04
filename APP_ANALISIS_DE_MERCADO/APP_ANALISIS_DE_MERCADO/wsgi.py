"""
WSGI config for APP_ANALISIS_DE_MERCADO project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'APP_ANALISIS_DE_MERCADO.settings')

application = get_wsgi_application()
