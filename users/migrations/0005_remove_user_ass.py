# Generated by Django 4.2 on 2024-12-25 07:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_ass'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='ass',
        ),
    ]
