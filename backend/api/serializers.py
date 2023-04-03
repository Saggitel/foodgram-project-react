"""Сериализаторы для моделей"""
from rest_framework import serializers

from recipes.models import (Tag, Ingredient, IngredientRecipe, Favorite, ShoppingList)

class IngredientSerializer(serializers.ModelSerializer):
    ''''Сериализатор модели Ingredient'''
    class Meta:
        '''Метамодель'''
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    ''''Сериализатор модели Tag'''
    class Meta:
        '''Метамодель'''
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = '__all__'

class IngredientRecipeSerializer(serializers.ModelSerializer):
    ''''Сериализатор модели IngredientRecipe'''
    id = serializers.ReadOnlyField(
        source = 'ingredient.id')
    name = serializers.ReadOnlyField(
        source = 'ingredient.name')
    measurment_unit = serializers.ReadOnlyField(
        source = 'source.measurement_unit')
    class Meta:
        '''Метамодель'''
        model = IngredientRecipe
        fields = ('id', 'name', 'amount', 'measurment_unit')
        read_only_fields = '__all__'

class ShoppingListSerializer(serializers.ModelSerializer):
    '''Сериализатор модели список покупок'''
    name = serializers.ReadOnlyField(
        source ='recipe.name',
        read_only=True)
    image = serializers.ImageField(
        source ='recipe.image',
        read_only=True)
    cocking_time = serializers.IntegerField(
        source ='recipe.cocking_time',
        read_only=True)
    id = serializers.PrimaryKeyRelatedField(
        source ='recipe',
        read_only=True)

    class Meta:
        '''Метамодель'''
        model = ShoppingList
        fields = ('id', 'name', 'image', 'cocking_time')

class FavoriteSerializer(serializers.ModelSerializer):
    '''Сериализатор модели список избранного'''
    name = serializers.ReadOnlyField(
        source ='recipe.name',
        read_only=True)
    image = serializers.ImageField(
        source ='recipe.image',
        read_only=True)
    cocking_time = serializers.IntegerField(
        source ='recipe.cocking_time',
        read_only=True)
    id = serializers.PrimaryKeyRelatedField(
        source ='recipe',
        read_only=True)

    class Meta:
        '''Метамодель'''
        model = Favorite
        fields = ('id', 'name', 'image', 'cocking_time')
