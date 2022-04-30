# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY wb_app /app/
RUN pip install -r requirements.txt
RUN python ./src/manage.py migrate

CMD [ "python", "./src/manage.py", "runserver", "0.0.0.0:8000" ]