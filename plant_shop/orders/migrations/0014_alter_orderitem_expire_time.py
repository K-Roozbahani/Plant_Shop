# Generated by Django 4.1.5 on 2023-07-07 07:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_alter_deliveryinformation_phone_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 7, 8, 58, 3, 678722, tzinfo=datetime.timezone.utc)),
        ),
    ]
