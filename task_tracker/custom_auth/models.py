from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    username = models.CharField(max_length=1, blank=True)
    email = models.EmailField(('E-mail'), unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. \
                                 Up to 15 digits allowed.")
    phone = models.CharField(verbose_name='Номер телефона', max_length=15, validators=[phone_regex])
    first_name = models.CharField(verbose_name='Имя', max_length=30)
    last_name = models.CharField(verbose_name='Фамилия', max_length=30)
    age = models.PositiveIntegerField(verbose_name='Возвраст', blank=True, null=True)
    region = models.CharField(verbose_name='Регион', max_length=30, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
