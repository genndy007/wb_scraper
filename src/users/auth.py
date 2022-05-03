import datetime
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
import jwt

from users.models import User


def validate_login_password(login: str, password: str):
    if not login or not password:
        raise AuthenticationFailed('Insufficient credentials, need login and password')

    user = User.objects.filter(login=login).first()
    if user is None:
        raise AuthenticationFailed('User not found')

    if not user.check_password(password):
        raise AuthenticationFailed('Incorrect password')

    return user


def generate_jwt_token(user) -> str:
    time_now = datetime.datetime.utcnow()
    payload = {
        'id': user.id,
        'exp': time_now + datetime.timedelta(minutes=60),
        'iat': time_now,
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


def authenticate_jwt(request):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('You need to authenticate first - login')

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256', ])
    except:
        raise AuthenticationFailed('You need to authenticate first - login')

    return payload



