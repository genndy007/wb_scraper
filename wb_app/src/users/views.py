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
            'message': 'logged in'
        }

        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('You need to authenticate first - /login')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256', ])
        except:
            raise AuthenticationFailed('You need to authenticate first - /login')

        user_id = payload['id']
        user = User.objects.filter(id=user_id).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'logged out'
        }

        return response
