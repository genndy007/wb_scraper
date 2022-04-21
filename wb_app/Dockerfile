# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . /app/
RUN pip install -r requirements.txt

CMD [ "python", "./src/manage.py", "runserver", "0.0.0.0:8000" ]