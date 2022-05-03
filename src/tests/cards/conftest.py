import pytest
import datetime

from .common import URL_PREFIX
from cards.models import Card, Record


@pytest.fixture(autouse=True)
def cards_in_db(auth_client):
    Card.objects.create(
        user_id=1,
        articul=14714897,
        brand='Reebok',
        goods_name='Shoes',
        price_without_discount=1000,
        price_with_discount=800,
        supplier='Reebok',
    )
    Card.objects.create(
        user_id=1,
        articul=14714898,
        brand='Adidas',
        goods_name='Shoes',
        price_without_discount=1000,
        price_with_discount=800,
        supplier='Adidas',
    )


@pytest.fixture()
def records_in_db(auth_client):
    Record.objects.create(
        articul=14714897,
        price_without_discount=1000,
        price_with_discount=800,
        supplier='Reebok',
    )
    Record.objects.create(
        articul=14714897,
        price_without_discount=1000,
        price_with_discount=800,
        supplier='Reebok',
    )
