# Generated by Django 4.1.5 on 2023-06-02 08:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_alter_cartitem_expire_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 3, 8, 10, 3, 707476, tzinfo=datetime.timezone.utc), verbose_name='expire time'),
        ),
    ]
