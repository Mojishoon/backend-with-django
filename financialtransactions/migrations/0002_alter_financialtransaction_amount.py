# Generated by Django 4.2 on 2024-12-21 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financialtransactions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financialtransaction',
            name='amount',
            field=models.DecimalField(decimal_places=3, max_digits=20),
        ),
    ]