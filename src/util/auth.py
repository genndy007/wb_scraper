from rest_framework.exceptions import AuthenticationFailed
import jwt


def is_jwt_authenticated(request, secret_key):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('You need to authenticate first - login')

    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256', ])
    except:
        raise AuthenticationFailed('You need to authenticate first - login')

    return payload
