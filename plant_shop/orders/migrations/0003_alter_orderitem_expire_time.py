# Generated by Django 4.1.5 on 2023-03-20 06:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_is_open_alter_orderitem_expire_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 20, 7, 14, 10, 905117, tzinfo=datetime.timezone.utc)),
        ),
    ]
