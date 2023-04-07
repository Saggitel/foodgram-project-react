'''Сервисный слой'''
from datetime import date

from django.db.models import Sum
from django.http import HttpResponse
from recipes.models import IngredientRecipe


def shopping_cart(self, request, author):
    """Функция скачивание списка продуктов для выбранных рецептов"""
    sum_ingredients_in_recipes = IngredientRecipe.objects.filter(
        recipe__shopping_cart__author=author
    ).values(
        'ingredient__name', 'ingredient__measurement_unit'
    ).annotate(
        amounts=Sum('amount', distinct=True)).order_by('amounts')
    today = date.today().strftime("%d-%m-%Y")
    shoppings = f'Список покупок на: {today}\n\n'
    for ingredient in sum_ingredients_in_recipes:
        shoppings += (
            f'{ingredient["ingredient__name"]} - '
            f'{ingredient["amounts"]} '
            f'{ingredient["ingredient__measurement_unit"]}\n'
        )
    shoppings += '\n\nFoodgram (2022)'
    filename = 'shopping_cart.txt'
    response = HttpResponse(shopping_cart, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response
