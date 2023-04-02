"""Сериализаторы для моделей"""
from rest_framework import serializers

from recipes.models import Tag, Ingredient, IngredientRecipe

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
        