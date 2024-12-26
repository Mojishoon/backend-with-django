# Generated by Django 4.2 on 2024-12-25 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseprices', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseprice',
            name='private_price',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='courseprice',
            name='public_price',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=10),
        ),
    ]
