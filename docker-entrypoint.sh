#!/bin/sh
python ./src/manage.py makemigrations
python ./src/manage.py migrate

exec "$@"