# Generated by Django 4.2.2 on 2024-06-22 13:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sending',
            name='finish_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 22, 13, 21, 59, 780871, tzinfo=datetime.timezone.utc), verbose_name='Дата завершения'),
        ),
        migrations.AlterField(
            model_name='sending',
            name='start_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 22, 13, 21, 59, 780871, tzinfo=datetime.timezone.utc), verbose_name='Дата старта'),
        ),
    ]