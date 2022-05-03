import pytest
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .common import URL_PREFIX

# user_id=1,
#         articul=14714897,
#         brand='Reebok',
#         goods_name='Shoes',
#         price_without_discount=1000,
#         price_with_discount=800,
#         supplier='Reebok',


@pytest.mark.django_db
def test_all_cards_get(auth_client):
    response = auth_client.get(f'{URL_PREFIX}/')
    data = response.data
    item = data[0]

    assert type(data) is list
    assert type(item['user_id']) is int
    assert type(item['articul']) is int
    assert type(item['brand']) is str
    assert type(item['goods_name']) is str
    assert type(item['price_without_discount']) is int
    assert type(item['price_with_discount']) is int
    assert type(item['supplier']) is str

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_all_cards_get_no_auth(client):
    response = client.get(f'{URL_PREFIX}/')
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_card_create(auth_client):
    response = auth_client.post(f'{URL_PREFIX}/', dict(
        articul=14714897
    ))
    data = response.data

    assert 'id' in data
    assert type(data.get('id')) is int
    assert type(data['user_id']) is int
    assert type(data['articul']) is int
    assert type(data['brand']) is str
    assert type(data['goods_name']) is str
    assert type(data['price_without_discount']) is int
    assert type(data['price_with_discount']) is int
    assert type(data['supplier']) is str

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_card_create_invalid_articul(auth_client):
    response = auth_client.post(f'{URL_PREFIX}/')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data.get('message') == 'Need articul field'

    response = auth_client.post(f'{URL_PREFIX}/', dict(
        articul='kdmvkmdvks'
    ))
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data.get('message') == 'Articul must be a number'

    response = auth_client.post(f'{URL_PREFIX}/', dict(
        articul=1236726137868
    ))
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data.get('message') == 'Non-existing articul'


@pytest.mark.django_db
def test_card_create_no_auth(client):
    response = client.post(f'{URL_PREFIX}/', dict(
        articul=14714897
    ))
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_all_cards_delete(auth_client):
    response = auth_client.delete(f'{URL_PREFIX}/')

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data.get('message') == 'All cards deleted'

    response = auth_client.get(f'{URL_PREFIX}/')
    assert response.data == []


@pytest.mark.django_db
def test_all_cards_delete_no_auth(client):
    response = client.delete(f'{URL_PREFIX}/')
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_single_card_delete(auth_client):
    response = auth_client.post(f'{URL_PREFIX}/', dict(
        articul=14714897
    ))

    response = auth_client.get(f'{URL_PREFIX}/')
    num_before = len(response.data)
    card_id = response.data[0]['id']

    response = auth_client.delete(f'{URL_PREFIX}/{card_id}/')

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert '1' in response.data.get('message')

    response = auth_client.get(f'{URL_PREFIX}/')
    assert len(response.data) == num_before - 1


@pytest.mark.django_db
def test_update_info(auth_client):
    response = auth_client.get(f'{URL_PREFIX}/update/')

    assert response.status_code == status.HTTP_200_OK
    assert response.data.get('message') == 'Task for updating is sent'


@pytest.mark.django_db
def test_cards_stats(auth_client, records_in_db):
    response = auth_client.post(f'{URL_PREFIX}/', dict(
        articul=14714897
    ))
    response = auth_client.get(f'{URL_PREFIX}/')
    card_id = response.data[0]['id']

    response = auth_client.get(f'{URL_PREFIX}/{card_id}/stats/')
    assert response.status_code == status.HTTP_200_OK
    assert type(response.data.get('articul')) is int
    assert type(response.data.get('stats')) is list
