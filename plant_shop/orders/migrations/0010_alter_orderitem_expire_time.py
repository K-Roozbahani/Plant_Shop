# Generated by Django 4.1.5 on 2023-06-02 14:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_alter_orderitem_expire_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 2, 15, 0, 37, 585932, tzinfo=datetime.timezone.utc)),
        ),
    ]
