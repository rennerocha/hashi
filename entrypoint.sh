#!/bin/sh

printenv | grep -v "no_proxy" >> /etc/environment

python manage.py collectstatic --noinput
python manage.py migrate
python manage.py rqworker default &

gunicorn --workers=2 --bind=0.0.0.0:8182 hashi.wsgi:application
