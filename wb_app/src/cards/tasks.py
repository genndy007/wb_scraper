from main.celery import celery_app

from .models import Record, Card

@celery_app.task
def get_and_update_good_info():
    print(f'Retrieving data for ')


