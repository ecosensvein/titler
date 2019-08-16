#!/bin/bash
python manage.py runserver 127.0.0.1:80 & celery -A titler worker -l info -B
