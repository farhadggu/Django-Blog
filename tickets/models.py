from django.db import models
from django.conf import settings
from home.models import TimeStamp


class Ticket(TimeStamp):
    CHOICES = (
        ('author', 'نویسندگی'),
        ('contact', 'تماس با ما'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='کاربر')
    choice = models.CharField(max_length=7, choices=CHOICES, verbose_name='موضوع')
    body = models.TextField(null=True, blank=True, verbose_name='متن')

    class Meta:
        verbose_name = 'تیکت کاربر'
        verbose_name_plural = 'تیکت کاربران'

    def __str__(self):
        return self.user.username

    

class AdminTicket(TimeStamp):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='admin_ticket', verbose_name='تیکت')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='کاربر')
    body = models.TextField(null=True, blank=True, verbose_name='متن')

    class Meta:
        verbose_name = 'پاسخ تیکت ادمین'
        verbose_name_plural = 'پاسخ های تیکت ادمین'

    def __str__(self):
        return self.user.username
