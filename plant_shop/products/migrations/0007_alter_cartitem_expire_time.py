# Generated by Django 4.1.5 on 2023-02-06 15:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_cart_cartitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 7, 15, 48, 45, 424317, tzinfo=datetime.timezone.utc), verbose_name='expire_time'),
        ),
    ]
