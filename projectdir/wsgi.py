"""
WSGI config for projectdir project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Set the default settings module for Railway deployment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectdir.railway')

application = get_wsgi_application()
