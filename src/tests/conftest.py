import pytest
from rest_framework.test import APIClient
from users.models import User


"""User data for registering and validating"""


@pytest.fixture
def user_data():
    return {
        'email': 'a@a.com',
        'login': 'a',
        'password': 'a',
    }


"""Client NOT registered"""


@pytest.fixture
def client():
    return APIClient()


"""Client registered"""


@pytest.fixture
def reg_client(user_data):
    instance = User(email=user_data['email'], login=user_data['login'])
    instance.set_password(user_data['password'])
    instance.save()

    return APIClient()


"""Client registered and logged in"""


@pytest.fixture
def auth_client(reg_client, user_data):
    reg_client.post('/users/login/', dict(login=user_data['login'], password=user_data['password']))
    return reg_client
