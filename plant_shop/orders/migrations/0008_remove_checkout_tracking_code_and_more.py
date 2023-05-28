# Generated by Django 4.1.5 on 2023-05-28 06:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_alter_deliveryinformation_city_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkout',
            name='tracking_code',
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 28, 7, 44, 23, 526440, tzinfo=datetime.timezone.utc)),
        ),
    ]
