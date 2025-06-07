from .settings import *
import os

# Production settings
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY', '3ogf9n1&zvyaetvw#(tq9*pz#0@_=7r_p0o2e4a!mpa*50()8q')

# Database for Railway
DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': os.environ.get('MYSQL_DATABASE'),
        'USER': os.environ.get('MYSQL_USER'),
        'PASSWORD': os.environ.get('MYSQL_PASSWORD'),
        'HOST': os.environ.get('MYSQL_HOST'),
        'PORT': os.environ.get('MYSQL_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Allowed hosts
ALLOWED_HOSTS = ['*']  # Railway will provide the domain
