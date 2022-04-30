from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.conf import settings


from scrape.utils import get_all_good_info
from auth.auth import is_jwt_authenticated

from .models import Card
from .serializers import CardSerializer, RecordSerializer

# Create your views here.

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
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        payload = is_jwt_authenticated(request, settings.SECRET_KEY)
        user_id = payload['id']

        user_cards = Card.objects.filter(user_id=user_id)
        for card in user_cards:
            card.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class SingleCardView(APIView):
    def delete(self, request, pk):
        payload = is_jwt_authenticated(request, settings.SECRET_KEY)
        user_id = payload['id']

        user_card = Card.objects.filter(user_id=user_id).filter(id=pk)
        user_card.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


# class UpdateInfoView(APIView):
#     def get(self, request):
#         all_articuls = list(Card.objects.values_list('articul', flat=True))
#         print(all_articuls)
#
#
#         for articul in all_articuls:
#             good_info = get_all_good_info(str(articul))
#
#             for key in 'goods_name', 'brand':
#                 good_info.pop(key)
#
#             serializer = RecordSerializer(data=good_info)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#
#
#
#
#         return Response(status=status.HTTP_200_OK)



