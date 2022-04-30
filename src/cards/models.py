from django.db import models



# Create your models here.

class Card(models.Model):
    user_id = models.ForeignKey('users.User', on_delete=models.CASCADE)
    articul = models.PositiveBigIntegerField()
    brand = models.CharField(max_length=255)
    goods_name = models.CharField(max_length=255)
    price_without_discount = models.PositiveIntegerField()
    price_with_discount = models.PositiveIntegerField()
    supplier = models.CharField(max_length=255)

class Record(models.Model):
    articul = models.PositiveBigIntegerField()
    price_without_discount = models.PositiveIntegerField()
    price_with_discount = models.PositiveIntegerField()
    supplier = models.CharField(max_length=255)
    record_date = models.DateTimeField(auto_now_add=True)