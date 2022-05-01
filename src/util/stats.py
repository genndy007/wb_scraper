from datetime import timedelta, datetime
from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError
from rest_framework import status

from cards.models import Record


def validate_url_query_params(params: dict):
    try:
        start_date = params.get('start')
        end_date = params.get('end')
        interval = int(params.get('interval', 1))

        if start_date is not None:
            check_start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if end_date is not None:
            check_end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except:
        raise ValidationError(detail='Query params: start, end: YYYY-MM-DD; interval: int', code=status.HTTP_400_BAD_REQUEST)

    return start_date, end_date, interval


def filter_records(records: QuerySet[Record], start_date=None, end_date=None):
    if start_date:
        records = records.filter(record_date__gte=start_date)
    if end_date:
        records = records.filter(record_date__lte=end_date)

    return records.order_by('record_date')


def set_time_values(records: QuerySet[Record], interval: int):
    time_first = records.first().record_date
    time_last = records.last().record_date
    time_interval = timedelta(hours=interval)
    time_to_check = time_first.replace(minute=0, second=0, microsecond=0)

    return time_to_check, time_last, time_interval


def get_stats_list(records: QuerySet[Record], time_to_check, time_last, time_interval) -> list:
    stats = []
    current_record = records.filter(record_date__gte=time_to_check).first()
    while time_to_check < time_last and current_record:
        stats.append({
            'time_to_check': time_to_check,
            'price_without_discount': current_record.price_without_discount,
            'price_with_discount': current_record.price_with_discount,
            'supplier': current_record.supplier,
        })
        time_to_check += time_interval
        current_record = records.filter(record_date__gte=time_to_check).first()

    return stats
