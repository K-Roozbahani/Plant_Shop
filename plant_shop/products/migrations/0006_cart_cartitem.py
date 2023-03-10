# Generated by Django 4.1.5 on 2023-02-06 09:18

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0005_alter_category_parent_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False, verbose_name='is active')),
                ('total_price', models.PositiveBigIntegerField(default=0, verbose_name='total price')),
                ('discount', models.PositiveBigIntegerField(default=0, verbose_name='discount')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'cart',
                'verbose_name_plural': 'carts',
                'db_table': 'cart',
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expire_time', models.DateTimeField(default=datetime.datetime(2023, 2, 7, 9, 18, 46, 771192, tzinfo=datetime.timezone.utc), verbose_name='expire_time')),
                ('count', models.PositiveSmallIntegerField(default=1, verbose_name='count')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='products.cart', verbose_name='cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='products.product', verbose_name='products')),
            ],
            options={
                'verbose_name': 'cart item',
                'verbose_name_plural': 'cart items',
                'db_table': 'cart_item',
            },
        ),
    ]
