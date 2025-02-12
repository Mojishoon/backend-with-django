# Generated by Django 4.2 on 2024-12-25 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseprices', '0002_alter_courseprice_private_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseprice',
            name='private_price',
            field=models.DecimalField(decimal_places=3, max_digits=10),
        ),
        migrations.AlterField(
            model_name='courseprice',
            name='public_price',
            field=models.DecimalField(decimal_places=3, max_digits=10),
        ),
    ]
