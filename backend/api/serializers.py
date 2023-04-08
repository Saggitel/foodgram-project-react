"""Сериализаторы моделей Recipes"""
from django.shortcuts import get_object_or_404
from recipes.models import (Favourite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Tag)
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.serializers import UserSerializer

from .fields import Base64ImageField


class IngredientSerializer(serializers.ModelSerializer):
    ''''Сериализатор модели Ingredient'''
    class Meta:
        '''Метамодель'''
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = '__all__',


class TagSerializer(serializers.ModelSerializer):
    ''''Сериализатор модели Tag'''
    class Meta:
        '''Метамодель'''
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = '__all__',


class IngredientRecipeSerializer(serializers.ModelSerializer):
    ''''Сериализатор модели IngredientRecipe'''
    id = serializers.ReadOnlyField(
        source='ingredient.id')
    name = serializers.ReadOnlyField(
        source='ingredient.name')
    measurment_unit = serializers.ReadOnlyField(
        source='source.measurement_unit')

    class Meta:
        '''Метамодель'''
        model = IngredientRecipe
        fields = ('id', 'name', 'amount', 'measurment_unit')


class ShoppingCartSerializer(serializers.ModelSerializer):
    '''Сериализатор модели список покупок'''
    name = serializers.ReadOnlyField(
        source='recipe.name',
        read_only=True)
    image = Base64ImageField(
        source='recipe.image',
        read_only=True)
    cocking_time = serializers.IntegerField(
        source='recipe.cocking_time',
        read_only=True)
    id = serializers.PrimaryKeyRelatedField(
        source='recipe',
        read_only=True)

    class Meta:
        '''Метамодель'''
        model = ShoppingCart
        fields = ('id', 'name', 'image', 'cocking_time')


class FavouriteSerializer(serializers.ModelSerializer):
    '''Сериализатор модели список избранного'''
    name = serializers.ReadOnlyField(
        source='recipe.name',
        read_only=True)
    image = Base64ImageField(
        source='recipe.image',
        read_only=True)
    cocking_time = serializers.IntegerField(
        source='recipe.cocking_time',
        read_only=True)
    id = serializers.PrimaryKeyRelatedField(
        source='recipe',
        read_only=True)

    class Meta:
        '''Метамодель'''
        model = Favourite
        fields = ('id', 'name', 'image', 'cocking_time')


class RecipeListSerializer(serializers.ModelSerializer):
    '''Сериализатор Recipe: чтение данных'''
    author = UserSerializer()
    tags = TagSerializer(
        many=True,
        read_only=True)
    ingredients = IngredientRecipeSerializer(
        many=True,
        source='recipe_ingredients',
        read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        '''Метамодель'''
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        '''Проверка наличия рецепта в избранном'''
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Favourite.objects.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        '''Проверка наличия рецепта в списке покупок'''
        request = self.context.get('request')
        if not request.user.is_anonymous:
            return ShoppingCart.objects.filter(recipe=obj).exists()
        return False


class AddIngredientSerializer(serializers.ModelSerializer):
    '''Сериализатор поля ingredient модели Recipe: создание ингредиентов'''
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        '''Метамодель'''
        model = IngredientRecipe
        fields = ('id', 'amount')


class RecipeWriteSerializer(serializers.ModelSerializer):
    '''Сериализатор Recipe: запись, обновление, удаление'''
    ingredients = AddIngredientSerializer(
        many=True,
        write_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True)
    image = Base64ImageField()
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault())
    added = serializers.SerializerMethodField()

    class Meta:
        '''Метамодель'''
        model = Recipe
        fields = ('ingredients', 'tags', 'image',
                  'name', 'text', 'cooking_time', 'author', 'added')

    def get_added(self, obj):
        '''Проверка создан ли рецепт'''
        request = self.context.get('request')
        if not request.user.is_anonymous:
            Favourite.objects.filter(author=request.user, recipe=obj).exists()
        return False

    def validate_ingredients(self, value):
        '''Валидация данных ингредиентов'''
        ingredients = value
        if not ingredients:
            raise ValidationError(
                {'ingredients': 'Нужно выбрать ингредиент!'})
        ingredients_list = []
        for item in ingredients:
            ingredient = get_object_or_404(Ingredient, name=item['id'])
            if ingredient in ingredients_list:
                raise ValidationError(
                    {'ingredients': 'Ингридиенты повторяются!'})
            if int(item['amount']) <= 0:
                raise ValidationError(
                    {'amount': 'Количество должно быть больше 0!'})
            ingredients_list.append(ingredient)
        return value

    def validate_tags(self, value):
        '''Функция валидации данных тегов'''
        tags = value
        if not tags:
            raise ValidationError(
                {'tags': 'Нужно выбрать тег!'})
        if len(set(tags)) != len(tags):
            raise serializers.ValidationError(
                'Теги повторяются')
        return value

    def to_representation(self, instance):
        ingredients = super().to_representation(instance)
        ingredients['ingredients'] = IngredientRecipeSerializer(
            instance.recipe_ingredients.all(), many=True).data
        return ingredients

    def add_tags_ingredients(self, ingredients, tags, model):
        '''Функция записи тегов'''
        for ingredient in ingredients:
            IngredientRecipe.objects.update_or_create(
                recipe=model,
                ingredient=ingredient['id'],
                amount=ingredient['amount'])
        model.tags.set(tags)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = super().create(validated_data)
        self.add_tags_ingredients(ingredients, tags, recipe)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.ingredients.clear()
        self.add_tags_ingredients(ingredients, tags, instance)
        return super().update(instance, validated_data)


class RecipeMiniSerializer(serializers.ModelSerializer):
    '''Сериализатор вывода рецептом в SubscriptionSerializer'''
    class Meta:
        '''Метамодель'''
        model = Recipe
        fields = ('id', 'name', 'cooking_time', 'image',)
