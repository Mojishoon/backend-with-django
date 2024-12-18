# Generated by Django 4.2 on 2024-12-18 23:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('classrooms', '0002_alter_classroom_lesson_group'),
        ('presentations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PresentationSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('is_cancelled', models.BooleanField(default=False)),
                ('is_extra', models.BooleanField(default=False)),
                ('record_date', models.DateField()),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='classrooms.classroom')),
                ('presentation', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='presentations.presentation')),
                ('recorder', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'presentation_sessions',
            },
        ),
    ]
