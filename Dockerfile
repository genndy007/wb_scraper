# syntax=docker/dockerfile:1
FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /code
COPY poetry.lock pyproject.toml /code/
RUN pip install poetry
RUN poetry install --no-dev

COPY src /code/src
COPY .env.prod /code/.env
COPY docker-entrypoint.sh /code/docker-entrypoint.sh


CMD [ "python", "./src/manage.py", "runserver", "0.0.0.0:8001" ]