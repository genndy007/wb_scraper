from rest_framework import serializers
from .models import Card, Record

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'user_id', 'articul', 'brand', 'goods_name', 'price_without_discount', 'price_with_discount', 'supplier']

