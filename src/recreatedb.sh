DB_NAME=wb_app

dropdb $DB_NAME -U postgres
createdb $DB_NAME -O postgres -U postgres

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

find `SCRIPT_DIR` -path "*/migrations/*.py" -not -name "__init__.py" -delete
python `SCRIPT_DIR`/manage.py makemigrations
python `SCRIPT_DIR`/manage.py migrate