# Generated by Django 4.1.5 on 2023-02-03 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productattribute',
            name='sub_attribute',
            field=models.ManyToManyField(blank=True, related_name='parent_attribute', to='products.productattribute', verbose_name='sub_attribute'),
        ),
    ]
