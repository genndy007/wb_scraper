from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

import jwt
import datetime

from .serializers import UserSerializer
from .models import User


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        login = request.data.get('login', None)
        password = request.data.get('password', None)

        if not login or not password:
            raise AuthenticationFailed("Insufficient credentials, need login and password")

        user = User.objects.filter(login=login).first()
        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        time_now = datetime.datetime.utcnow()
        payload = {
            'id': user.id,
            'exp': time_now + datetime.timedelta(minutes=60),
            'iat': time_now,
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'success': 'logged in, jwt cookie set'
        }

        return response