from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.conf import settings


from scrape.utils import get_all_good_info
from auth.auth import is_jwt_authenticated

from .models import Card, Record
from .serializers import CardSerializer, RecordSerializer
from main.celery import celery_app

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


class UpdateInfoView(APIView):
    def get(self, request):
        celery_app.send_task('cards.tasks.get_and_update_good_info')
        return Response(status=status.HTTP_200_OK)


class CardStatsView(APIView):
    def get(self, request, pk):
        payload = is_jwt_authenticated(request, settings.SECRET_KEY)
        user_id = payload['id']
        user_card = Card.objects.filter(id=pk).first()

        if not user_card:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not user_card.id == user_id:
            print('Its not your card')
            return Response('Its not your card', status.HTTP_403_FORBIDDEN)

        records = Record.objects.filter(articul=user_card.articul)

        response = {
            'articul': user_card.articul,
            'stats': [],
        }
        for record in records:
            response['stats'].append({
                'record_date': record.record_date,
                'price_without_discount': record.price_without_discount,
                'price_with_discount': record.price_with_discount,
            })

        return Response(response)