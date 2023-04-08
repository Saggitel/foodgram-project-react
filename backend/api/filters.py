'''Фильтры для вьюсетов'''
import django_filters
from django_filters.rest_framework import FilterSet, filters
from recipes.models import Recipe, Tag, ShoppingCart, Favourite
from rest_framework.filters import SearchFilter
from users.models import User

class IngredientSearchFilter(SearchFilter):
    ''''Филтр списка ингредиентов по имени'''
    search_param = 'name'

class RecipeFilter(FilterSet):
    ''''Фильтр списка рецептов'''
    tags = django_filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = django_filters.NumberFilter(method='get_is_favorited')
    is_in_shopping_cart = django_filters.NumberFilter(
        method='get_is_in_shopping_cart'
    )
    author = django_filters.CharFilter(field_name='author')

    class Meta:
        model = Recipe
        fields = [
            'tags', 'author'
        ]

    def get_is_favorited(self, queryset, name, value):
        if value == 1 and self.request.user.is_authenticated:
            favorites = list(
                Favourite.objects.filter(
                    author=self.request.user).values_list('recipe_id', flat=True)
            )
            fav_queryset = queryset.filter(id__in=favorites)
            return fav_queryset
        else:
            return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value == 1 and self.request.user.is_authenticated:
            shopping_cart = list(
                ShoppingCart.objects.filter(
                    author=self.request.user).values_list('recipe_id', flat=True)
            )
            sc_queryset = queryset.filter(id__in=shopping_cart)
            return sc_queryset
        else:
            return queryset
