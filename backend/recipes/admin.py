'''Админ-зоны для разных моделей'''
from django.contrib import admin

from .models import (Favourite, Ingredient, IngredientRecipe, Recipe,
                     ShoppingCart, Tag)


class IngredientsInline(admin.TabularInline):
    '''Интеграции добавления 3х ингрдиентов в рецепты.'''
    model = IngredientRecipe
    extra = 3


class FavouriteAdmin(admin.ModelAdmin):
    '''Избрынне рецепты'''
    list_display = ('author', 'recipe')
    list_filter = ('author',)
    search_fields = ('author',)


class ShoppingCartAdmin(admin.ModelAdmin):
    '''Список покупок'''
    list_display = ('author', 'recipe')
    list_filter = ('author',)
    search_fields = ('author',)


class IngredientRecipeAdmin(admin.ModelAdmin):
    '''Ингредиенты для рецептов'''
    list_display = ('id', 'recipe', 'ingredient', 'amount',)
    list_filter = ('recipe', 'ingredient')
    search_fields = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    '''Рецепты, количесвто рецептов в избранном'''
    list_display = ('id', 'author', 'name', 'pub_date', 'in_favourite',)
    search_fields = ('author', 'name', 'tags')
    list_filter = ('pub_date', 'author', 'name', 'tags')
    filter_horizontal = ('ingredients',)
    empty_value_display = '-пусто-'
    inlines = [IngredientsInline]

    def in_favourite(self, obj):
        '''Добавленные рецепты в избранное'''
        return obj.favourite.all().count()


class TagAdmin(admin.ModelAdmin):
    '''Теги'''
    list_display = ('id', 'name', 'slug', 'color')
    list_filter = ('name',)
    search_fields = ('name',)


class IngredientAdmin(admin.ModelAdmin):
    '''Ингредиенты'''
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
admin.site.register(Favourite, FavouriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
