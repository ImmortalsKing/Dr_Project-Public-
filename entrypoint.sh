#!/bin/bash

python manage.py migrate --noinput
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# اجرای Gunicorn
echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 Dr_Project.wsgi:application
