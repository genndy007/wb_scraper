dropdb wb_app -U postgres
createdb wb_app -O postgres -U postgres

find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
python manage.py makemigrations
python manage.py migrate