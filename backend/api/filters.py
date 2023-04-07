'''Фильтры для вьюсетов'''
from django_filters.rest_framework import FilterSet, filters
from recipes.models import Recipe, Tag
from rest_framework.filters import SearchFilter
from users.models import User


class IngredientSearchFilter(SearchFilter):
    ''''Филтр списка ингредиентов по имени'''
    search_param = 'name'

class RecipeFilter(FilterSet):
    ''''Фильтр списка рецептов'''
    author = filters.ModelChoiceFilter(
        queryset=User.objects.all())
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    is_in_shopping_cart = filters.NumberFilter(
        method='filter_is_in_shopping_lsit')
    is_favourited = filters.NumberFilter(
        method='filter_is_favourited')

    class Meta:
        '''Метакласс'''
        model = Recipe
        fields = ('tags', 'author', 'is_favourited', 'is_in_shopping_cart')

    def filter_is_favourited(self, queryset, name, value):
        '''Метод фильтрации по избранному'''
        if self.request.user.is_authenticated and value:
            return queryset.filter(favourite__author=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        '''Метод фильтрации по списку покупок'''
        if self.request.user.is_authenticated and value:
            return queryset.filter(shopping_cart__author=self.request.user)
        return queryset
