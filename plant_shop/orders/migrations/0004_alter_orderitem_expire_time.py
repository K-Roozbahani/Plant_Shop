# Generated by Django 4.1.5 on 2023-03-22 05:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_orderitem_expire_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 22, 6, 8, 53, 164351, tzinfo=datetime.timezone.utc)),
        ),
    ]