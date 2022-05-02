import pytest
from rest_framework import status
from .common import URL_PREFIX



@pytest.mark.django_db
def test_register_user(client, user_data):
    response = client.post(f'{URL_PREFIX}/register/', user_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert 'id' in response.data
    assert response.data['email'] == user_data['email']
    assert response.data['login'] == user_data['login']


@pytest.mark.django_db
def test_login_user(reg_client, user_data):
    response = reg_client.post(f'{URL_PREFIX}/login/', dict(
        login=user_data['login'],
        password=user_data['password']
    ))

    assert response.status_code == status.HTTP_200_OK
    assert reg_client.cookies.get('jwt') is not None
    assert response.data['message'] == 'logged in'


@pytest.mark.django_db
def test_login_user_fail(reg_client, user_data):
    response = reg_client.post(f'{URL_PREFIX}/login/', dict())
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = reg_client.post(f'{URL_PREFIX}/login/', dict(
        login='not-right-login',
        password='not-right-password'
    ))
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = reg_client.post(f'{URL_PREFIX}/login/', dict(
        login=user_data['login'],
        password='not-right-password'
    ))
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_user_me_view(auth_client, user_data):
    response = auth_client.get(f'{URL_PREFIX}/me/')

    assert response.status_code == status.HTTP_200_OK
    assert 'id' in response.data
    assert response.data['email'] == user_data['email']
    assert response.data['login'] == user_data['login']


@pytest.mark.django_db
def test_logout_user(auth_client):
    response = auth_client.post(f'{URL_PREFIX}/logout/')

    assert response.status_code == status.HTTP_200_OK
    assert auth_client.cookies.get('jwt').coded_value == '""'
    assert response.data['message'] == 'logged out'



