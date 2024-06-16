# Generated by Django 4.2.2 on 2024-06-16 09:36

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_attempt_at', models.DateTimeField(auto_now_add=True, verbose_name='Последняя попытка')),
                ('status', models.BooleanField(default=False, verbose_name='Статус')),
                ('server_response', models.CharField(blank=True, null=True, verbose_name='Ответ сервера')),
            ],
            options={
                'verbose_name': 'Попытка',
                'verbose_name_plural': 'Попытки',
                'ordering': ('last_attempt_at',),
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Ф.И.О.')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Почта')),
                ('phone', models.CharField(blank=True, max_length=35, null=True, verbose_name='Номер телефона')),
                ('comment', models.CharField(blank=True, max_length=100, null=True, verbose_name='Комментарий')),
            ],
            options={
                'verbose_name': 'Получатель',
                'verbose_name_plural': 'Получатели',
                'ordering': ('email',),
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.CharField(max_length=100, verbose_name='Тема')),
                ('text', models.TextField(verbose_name='Текст')),
            ],
            options={
                'verbose_name': 'Письмо',
                'verbose_name_plural': 'Письма',
                'ordering': ('theme',),
            },
        ),
        migrations.CreateModel(
            name='Sending',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent_at', models.DateTimeField(blank=True, null=True, verbose_name='Когда и во сколько отправлено')),
                ('period', models.CharField(choices=[('Day', 'Раз в день'), ('Week', 'Раз в неделю'), ('Month', 'Раз в месяц')], default='Раз в день', max_length=30, verbose_name='Периодичность отправки')),
                ('status', models.CharField(choices=[('Created', 'Создано'), ('Executing', 'Запущено'), ('Finished', 'Завершено')], default='Создано', max_length=30, verbose_name='Статус рассылки')),
                ('start_at', models.DateTimeField(default=datetime.datetime(2024, 6, 16, 9, 36, 1, 572926, tzinfo=datetime.timezone.utc), verbose_name='Дата старта')),
                ('finish_at', models.DateTimeField(default=datetime.datetime(2024, 7, 16, 9, 36, 1, 572926, tzinfo=datetime.timezone.utc), verbose_name='Дата завершения')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активно')),
                ('clients', models.ManyToManyField(blank=True, null=True, to='main.client', verbose_name='Пользователи')),
                ('message', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.message', verbose_name='Письмо')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
                'ordering': ('sent_at',),
                'permissions': [('set_active', 'Can deactivate sending')],
            },
        ),
    ]
