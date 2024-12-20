# Generated by Django 4.2 on 2024-12-19 13:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('presentations', '0001_initial'),
        ('surveycategories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PresentationSurvey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.DecimalField(decimal_places=2, max_digits=4, null=True)),
                ('record_date', models.DateField()),
                ('presentation', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='presentations.presentation')),
                ('recorder', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('survey_category', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='surveycategories.surveycategory')),
            ],
            options={
                'db_table': 'presentation_surveys',
            },
        ),
    ]