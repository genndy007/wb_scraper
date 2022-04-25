from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from django.conf import settings
import jwt

from scrape.utils import get_all_good_info

from .models import Card

from .serializers import CardSerializer

# Create your views here.

def is_jwt_authenticated(request, secret_key):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('You need to authenticate first - login')

    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256', ])
    except:
        raise AuthenticationFailed('You need to authenticate first - login')

    return payload

class AllCardsView(APIView):
    def get(self, request):
        payload = is_jwt_authenticated(request, settings.SECRET_KEY)
        user_id = payload['id']
        user_cards = Card.objects.filter(user_id=user_id)

        res = []
        for card in user_cards:
            serializer = CardSerializer(card)
            res.append(serializer.data)


        return Response(res)

    def post(self, request):
        payload = is_jwt_authenticated(request, settings.SECRET_KEY)
        user_id = payload['id']

        articul = request.data.get('articul')
        if not articul:
            raise ValidationError('Need articul field')

        if not articul.isdigit():
            raise ValidationError('Articul must be a number')

        good_info = get_all_good_info(articul)

        if not good_info:
            raise ValidationError('Non-existing articul')

        data = {
            'user_id': user_id,
            **good_info,
        }
        serializer = CardSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

