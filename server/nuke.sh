#!/bin/bash

python manage.py reset_db
python manage.py migrate --noinput
python manage.py createsuperuser --noinput # recreate the superuser to login to the admin panel