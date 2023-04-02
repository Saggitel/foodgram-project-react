'''Модель потзовтелей'''
from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    '''Модель пользователя'''
    username = models.CharField(max_length=150, unique=True, verbose_name='Имя пользователя')
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    email = models.CharField(max_length=150, unique=True, verbose_name='Адресс электроной почты')
    password = models.CharField(max_length=150, verbose_name='Пароль')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

class Meta:
    '''Метамодель'''
    verbose_name = 'Пользователь'
    verbose_name_plural = 'Пользователи'

def __str__(self):
    return f'{self.username}'
