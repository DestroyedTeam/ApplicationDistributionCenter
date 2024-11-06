#!/bin/sh

# Apply database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start the Django application using gunicorn
gunicorn applicationdistributioncenter.wsgi:application --bind 0.0.0.0:8000