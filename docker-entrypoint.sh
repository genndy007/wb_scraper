#!/bin/sh
python ./src/manage.py migrate

exec "$@"