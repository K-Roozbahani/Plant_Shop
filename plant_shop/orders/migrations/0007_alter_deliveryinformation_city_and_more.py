# Generated by Django 4.1.5 on 2023-05-06 10:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_deliveryinformation_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryinformation',
            name='city',
            field=models.CharField(default='تهران', max_length=32, verbose_name='city'),
        ),
        migrations.AlterField(
            model_name='deliveryinformation',
            name='state',
            field=models.CharField(default='تهران', max_length=32, verbose_name='state'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 6, 11, 10, 53, 669362, tzinfo=datetime.timezone.utc)),
        ),
    ]
