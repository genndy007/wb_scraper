from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status


from util.scrape import get_all_good_info
from users.auth import authenticate_jwt
from util.stats import set_time_values, get_stats_list, filter_records, validate_url_query_params
from .models import Card, Record
from .serializers import CardSerializer
from main.celery import celery_app


class AllCardsView(APIView):
    def get(self, request):
        payload = authenticate_jwt(request)
        user_id = payload.get('id')
        user_cards = Card.objects.filter(user_id=user_id)

        data = []
        for card in user_cards:
            serializer = CardSerializer(card)
            data.append(serializer.data)

        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        payload = authenticate_jwt(request)
        user_id = payload.get('id')

        articul = request.data.get('articul')
        if not articul:
            raise ValidationError(dict(message='Need articul field'))

        if not articul.isdigit():
            raise ValidationError(dict(message='Articul must be a number'))

        good_info = get_all_good_info(articul)

        if not good_info:
            raise ValidationError(dict(message='Non-existing articul'))

        data = {
            'user_id': user_id,
            **good_info,
        }
        serializer = CardSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        payload = authenticate_jwt(request)
        user_id = payload['id']

        user_cards = Card.objects.filter(user_id=user_id)
        for card in user_cards:
            card.delete()

        return Response(dict(message='All cards deleted'), status=status.HTTP_204_NO_CONTENT)


class SingleCardView(APIView):
    def delete(self, request, pk):
        payload = authenticate_jwt(request)
        user_id = payload['id']

        user_card = Card.objects.filter(user_id=user_id).filter(id=pk)
        user_card.delete()

        return Response(dict(message=f'Card with id {pk} deleted'), status=status.HTTP_204_NO_CONTENT)


class UpdateInfoView(APIView):
    def get(self, request):
        celery_app.send_task('cards.tasks.get_and_update_good_info')
        return Response(dict(message='Task for updating is sent'), status=status.HTTP_200_OK)


class CardStatsView(APIView):
    def get(self, request, pk):
        payload = authenticate_jwt(request)
        user_id = payload['id']
        user_card = Card.objects.filter(id=pk).first()

        if not user_card:
            return Response(dict(message=f'Card with id {pk} not found'), status=status.HTTP_404_NOT_FOUND)

        if not user_card.user_id == user_id:
            return Response(dict(message=f'It is not your card'), status.HTTP_403_FORBIDDEN)

        records = Record.objects.filter(articul=user_card.articul)
        start_date, end_date, interval = validate_url_query_params(self.request.query_params)

        records = filter_records(records, start_date, end_date)
        time_to_check, time_last, time_interval = set_time_values(records, interval)
        stats = get_stats_list(records, time_to_check, time_last, time_interval)

        return Response(dict(
            articul=user_card.articul,
            stats=stats,
        ), status=status.HTTP_200_OK)
