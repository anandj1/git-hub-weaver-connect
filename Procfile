web: python manage.py collectstatic --noinput --settings=projectdir.railway && DJANGO_SETTINGS_MODULE=projectdir.railway gunicorn --bind 0.0.0.0:$PORT projectdir.wsgi:application
