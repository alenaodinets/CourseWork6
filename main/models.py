from datetime import datetime, timedelta
import pytz
from django.db import models
from config import settings

period_choices = (("Day", "Раз в день"), ("Week", "Раз в неделю"), ("Month", "Раз в месяц"),)
status_choices = (("Created", "Создано"), ("Executing", "Запущено"), ("Finished", "Завершено"),)


# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name='Ф.И.О.')
    email = models.EmailField(unique=True, verbose_name='Почта')
    phone = models.CharField(max_length=35, verbose_name='Номер телефона', null=True, blank=True)
    comment = models.CharField(max_length=100, verbose_name='Комментарий', null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                              null=True, blank=True)

    def __str__(self):
        return f'{self.name} ({self.email})'

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'
        ordering = ('email',)


class Message(models.Model):
    theme = models.CharField(max_length=100, verbose_name='Тема')
    text = models.TextField(verbose_name='Текст')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                              null=True, blank=True)

    def __str__(self):
        return f'{self.theme}'

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'
        ordering = ('theme',)


class Sending(models.Model):
    sent_at = models.DateTimeField(verbose_name='Когда и во сколько отправлено', null=True, blank=True)
    period = models.CharField(max_length=30, choices=period_choices, default="Раз в день",
                              verbose_name='Периодичность отправки')
    status = models.CharField(max_length=30, choices=status_choices, default="Создано", verbose_name='Статус рассылки')
    message = models.ForeignKey("Message", on_delete=models.CASCADE, verbose_name='Письмо', null=True, blank=True)
    clients = models.ManyToManyField(Client, verbose_name='Пользователи', null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                              null=True, blank=True)
    start_at = models.DateTimeField(default=datetime.now(pytz.timezone(settings.TIME_ZONE)), verbose_name='Дата старта')
    finish_at = models.DateTimeField(default=datetime.now(pytz.timezone(settings.TIME_ZONE)) + timedelta(days=30),
                                     verbose_name='Дата завершения')
    is_active = models.BooleanField(default=True, verbose_name='Активно')

    def __str__(self):
        return f'{self.message}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ('sent_at',)
        permissions = [
            ("set_active", "Can deactivate sending")
        ]


class Attempt(models.Model):
    sending = models.ForeignKey("Sending", on_delete=models.CASCADE, verbose_name='Рассылка')
    last_attempt_at = models.DateTimeField(auto_now_add=True, verbose_name='Последняя попытка')
    status = models.BooleanField(default=False, verbose_name='Статус')
    server_response = models.CharField(verbose_name='Ответ сервера', null=True, blank=True)

    def __str__(self):
        answ = f'{self.sending} {self.last_attempt_at} '
        if self.status:
            answ += 'Попытка отправки успешна'
        else:
            answ += f'Ошибка: {self.server_response}'
        return answ

    class Meta:
        verbose_name = 'Попытка'
        verbose_name_plural = 'Попытки'
        ordering = ('last_attempt_at',)
