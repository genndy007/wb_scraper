from main.celery import celery_app
from celery import group

from util.scrape import get_all_good_info
from .models import Card, Record


@celery_app.task
def write_record_to_db(articul):
    good_info = get_all_good_info(str(articul))
    print(good_info)

    if not good_info:
        return

    for key in 'goods_name', 'brand':
        good_info.pop(key)

    Record.objects.create(**good_info)


@celery_app.task
def get_and_update_good_info():
    all_articuls = list(Card.objects.values_list('articul', flat=True))

    g = group(write_record_to_db.s(articul) for articul in all_articuls)
    g.apply_async()
