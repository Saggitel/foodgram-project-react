'''Модели Users'''
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F, Q


class User(AbstractUser):
    '''Модель пользовтеля и его роли'''
    USER = 'user'
    ADMIN = 'admin'
    GUEST = 'guest'
    ROLE_USER = [
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор'),
        (GUEST, 'Гость'),
    ]


    '''Модель пользователя'''
    username = models.CharField(max_length=150, unique=True, verbose_name='Имя пользователя')
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    email = models.EmailField(max_length=150, unique=True, verbose_name='Адресс электроной почты')
    password = models.CharField(max_length=150, verbose_name='Пароль')
    role = models.CharField(max_length=15, choices=ROLE_USER,
                            default=USER, verbose_name='Пользовательская роль')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        '''Метамодель'''
        constraints = [
                models.UniqueConstraint(fields=['email', 'username'],
                                    name='unique_user')
            ]
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def admin(self):
        '''Проверка роли пользовтеля,
           является ли он админом'''
        return self.role == self.ADMIN

    def __str__(self):
        return f'{self.username}'


class Subscription(models.Model):
    """Модель подписка на автора"""
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='subscriber',
        on_delete=models.CASCADE,
        help_text='Подписчик')
    author = models.ForeignKey(
        User,
        verbose_name='Подписка',
        related_name='subscribed',
        on_delete=models.CASCADE,
        help_text='Подписаться на автора')

    class Meta:
        '''Метамодель'''
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'),
            models.CheckConstraint(
                check=~Q(user=F('author')),
                name='no_self_subscription')]

    def __str__(self):
        return f'{self.user.username} подписан на {self.author.username}'
