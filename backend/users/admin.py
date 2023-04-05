'''Админ-зоны для разных моделей'''
from django.contrib import admin

from .models import Subscription, User


class UserAdmin(admin.ModelAdmin):
    '''Пользователь'''
    list_display = ('id', 'username', 'first_name',
                    'last_name', 'email', 'role', 'admin')
    search_fields = ('username', 'email')
    list_filter = ('username', 'email',)
    empty_value_display = '-пусто-'

class SubscriptionAdmin(admin.ModelAdmin):
    '''Подписки'''
    list_display = ('user', 'author')
    list_filter = ('author',)
    search_fields = ('user',)


admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
