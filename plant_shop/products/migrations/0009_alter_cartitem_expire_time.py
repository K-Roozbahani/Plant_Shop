# Generated by Django 4.1.5 on 2023-02-06 15:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_alter_cartitem_expire_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 7, 15, 50, 1, 264970, tzinfo=datetime.timezone.utc), verbose_name='expire time'),
        ),
    ]
