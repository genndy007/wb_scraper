# Generated by Django 4.0.4 on 2022-05-03 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='user_id',
            field=models.PositiveIntegerField(),
        ),
    ]