# Generated by Django 4.2 on 2024-12-20 09:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=3, max_digits=10)),
                ('record_date', models.DateField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='courses.course')),
                ('recorder', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'exams',
            },
        ),
    ]