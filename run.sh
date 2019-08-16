#!/bin/bash
python manage.py runserver 192.168.100.100:80 & celery -A titler worker -l info -B
