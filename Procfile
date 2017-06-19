web: gunicorn daat.wsgi --workers $WEB_CONCURRENCY
worker: python manage.py celery worker --loglevel=info
