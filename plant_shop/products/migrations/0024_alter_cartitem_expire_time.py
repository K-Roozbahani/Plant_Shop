# Generated by Django 4.1.5 on 2023-07-07 07:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0023_alter_cartitem_expire_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 8, 7, 57, 57, 235765, tzinfo=datetime.timezone.utc), verbose_name='expire time'),
        ),
    ]