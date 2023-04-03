'''Основные модели'''
from django.db import models
from django.core.validators import MinValueValidator
from users.models import User

class Tag(models.Model):
    '''Теги для рецептов'''
    name = models.CharField(
        verbose_name ='Название тега',
        max_length = 150, unique = True,
        help_text = 'Ввведите тег')
    ORANGE = 'fa6a02'
    GREEN = '09db4f'
    PURPLE = 'b813d1'
    COLOR_TAG = [
        (ORANGE, 'Оранжевый'),
        (GREEN, 'Зеленный'),
        (PURPLE, 'Фиолетовый')
    ]
    color = models.CharField(
        verbose_name='Цвет в HEX-коде',
        max_length=10, unique=True,
        default=GREEN,
        choices=COLOR_TAG,
        help_text='Выберите цвет')
    slag = models.SlugField(
        verbose_name ='Название слага',
        max_length = 150, unique = True,
        help_text = 'Укажите слаг')

    class Meta:
        '''Метамодель'''
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'{self.name}'

class Ingredient(models.Model):
    '''Ингридиент для рецепта'''
    name = models.CharField(
        verbose_name ='Название ингредиента',
        max_length = 150,
        db_index = True,
        help_text = 'Введите название ингредиента')
    measurement_unit = models.SlugField(
        verbose_name ='Единица измерения',
        max_length = 150,
        help_text = 'Укажите единицы измерения')

    class Meta:
        '''Метамодель'''
        ordering = ['id']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}'

class Recipe(models.Model):
    '''Рецепт'''
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        help_text='Автор рецепта')
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200,
        help_text='Введите название рецепта',
        db_index=True)
    image = models.ImageField(
        verbose_name='Картинка рецепта',
        upload_to='media/',
        help_text='Добавьте изображение рецепта')
    text = models.TextField(
        verbose_name='Описание рецепта',
        help_text='Опишите приготовление рецепта')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Ингредиент')
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Название тега',
        help_text='Выберите tag')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[MinValueValidator(1, 'Минимальное время приготовления')],
        help_text='Укажите время приготовления рецепта в минутах')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True)

class IngredientRecipe(models.Model):
    '''Модель связывающая игредиенты и рецепт'''
    recipe = models.ForeignKey(
        Recipe,
        related_name='recipe_ingredients',
        verbose_name='Название рецепта',
        on_delete=models.CASCADE,
        help_text='Выберите рецепт')
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
        help_text='Укажите ингредиенты')
    amount = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, 'Минимальное количество ингредиентов 1')],
        verbose_name='Количество',
        help_text='Укажите количество ингредиента')

    class Meta:
        '''Метамодель'''
        verbose_name = 'Cостав рецепта'
        verbose_name_plural = 'Состав рецепта'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredients')]

    def __str__(self):
        return f'{self.ingredient} {self.amount}'

class ShoppingList(models.Model):
    """Модель для списка покупок"""
    author = models.ForeignKey(
        User,
        related_name='shopping_list',
        on_delete=models.CASCADE,
        verbose_name='Пользователь')
    recipe = models.ForeignKey(
        Recipe,
        related_name='shopping_list',
        verbose_name='Рецепт приготовления',
        on_delete=models.CASCADE,
        help_text='Выберите рецепт приготовления')

    class Meta:
        '''Метамодель'''
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [models.UniqueConstraint(
            fields=['author', 'recipe'],
            name='unique_shopping_list')]

    def __str__(self):
        return f'{self.recipe}'


class Favorite(models.Model):
    """Избранные рецепты"""
    author = models.ForeignKey(
        User,
        related_name='favorite',
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта')
    recipe = models.ForeignKey(
        Recipe,
        related_name='favorite',
        on_delete=models.CASCADE,
        verbose_name='Рецепт')

    class Meta:
        '''Метамодель'''
        verbose_name = 'Избранные рецепты'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [models.UniqueConstraint(
            fields=['author', 'recipe'],
            name='unique_favorite')]

    def __str__(self):
        return f'{self.recipe}'

