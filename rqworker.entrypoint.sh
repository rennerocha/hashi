#!/bin/sh

printenv | grep -v "no_proxy" >> /etc/environment

python manage.py rqworker default
