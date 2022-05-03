from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.auth import authenticate_jwt, validate_login_password, generate_jwt_token
from .serializers import UserSerializer
from .models import User


class RegisterView(APIView):
    def post(self, request):
        """Register a new user
        Args:
            request.data = {
                "email": email-str,
                "login": str,
                "password": str,
            }
        Returns:
            response.data = {
                "id": int,
                "email": email-str,
                "login": str,
            }
            response.status_code = 201
        Raises:
            ValidationError: request.data is insufficient
        """
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        """Login into account
        Args:
            request.data = {
                "login": str,
                "password": str,
            }
        Returns:
            response.data = {
                "message": str
            }
            response.status_code = 200
            cookie: jwt
        Raises:
            AuthenticationFailed: Insufficient credentials
        """
        login = request.data.get('login', None)
        password = request.data.get('password', None)
        user = validate_login_password(login, password)
        token = generate_jwt_token(user)

        response = Response(dict(message='logged in'), status=status.HTTP_200_OK)
        response.set_cookie(key='jwt', value=token, httponly=True)

        return response


class UserView(APIView):
    def get(self, request):
        """Check your account
        Args:
            request.COOKIES = {
                "jwt": str
            }
        Returns:
            response.data = {
                "id": int,
                "email": email-str,
                "login": str,
            }
        Raises:
            AuthenticationFailed: Insufficient credentials
        """
        payload = authenticate_jwt(request)
        user_id = payload.get('id')
        user = User.objects.filter(id=user_id).first()
        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    def post(self, request):
        """Log out, delete cookie
        Args:
            request.COOKIES = {
                "jwt": str
            }
        Returns:
            response.data = {
                "message": str
            }
            delete request.COOKIES['jwt']
        Raises:
            AuthenticationFailed: User is not authenticated
        """
        payload = authenticate_jwt(request)
        response = Response(dict(message='logged out'), status=status.HTTP_200_OK)
        response.delete_cookie('jwt')

        return response
