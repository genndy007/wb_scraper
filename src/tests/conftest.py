import pytest
from rest_framework.test import APIClient
from users.models import User


@pytest.fixture
def user_data():
    return {
        'email': 'a@a.com',
        'login': 'a',
        'password': 'a',
    }

@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(user_data):
    instance = User(email=user_data['email'], login=user_data['login'])
    instance.set_password(user_data['password'])
    instance.save()



@pytest.fixture
def auth_client(client, user_data):
    client.post('/users/login', dict(login=user_data['login'],
                                     password=user_data['password']))
    return client
