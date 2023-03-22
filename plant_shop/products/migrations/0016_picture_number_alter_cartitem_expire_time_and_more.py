# Generated by Django 4.1.5 on 2023-03-22 06:30

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_product_priority_alter_cartitem_expire_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='number',
            field=models.PositiveIntegerField(default=1, verbose_name='number'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 23, 6, 29, 53, 804150, tzinfo=datetime.timezone.utc), verbose_name='expire time'),
        ),
        migrations.AlterField(
            model_name='picture',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pictures', to='products.product', verbose_name='product'),
        ),
        migrations.AlterUniqueTogether(
            name='picture',
            unique_together={('product', 'number')},
        ),
    ]