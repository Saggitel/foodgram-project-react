'''Сериализаторы моделей User'''
from recipes.models import Recipe
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
import api.serializers

from .models import Subscription, User


class UserSerializer(serializers.ModelSerializer):
    '''Отображение списка пользователей'''
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        '''Метамодель'''
        model = User
        fields = ('email', 'id', 'username', 
                  'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        '''Функция првоерки подписки на автора'''
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(user=request.user, 
                                           author=obj).exists()


class UserRegistrationSerializer(serializers.ModelSerializer):
    '''Сериализатор модели User для регистрации пользователя'''
    class Meta:
        '''Метамодель'''
        model = User
        fields = ('email', 'id', 'username', 'first_name', 
                  'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class SubscriptionSerializer(serializers.ModelSerializer):
    '''Сериализатор модели Subscription'''
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        '''Метамодель'''
        model = Subscription
        fields = ('email', 'id', 'username', 'first_name', 
                  'last_name', 'is_subscribed',
                  'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        '''Проверка подписки на автора'''
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(user=obj.user, 
                                           author=obj.author).exists()

    def get_recipes(self, obj):
        '''Функция вывода рецепта в подписки'''
        recipes = Recipe.objects.filter(author=obj.author)
        return api.serializers.RecipeMiniSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        '''Функция подсчета количесвта рецептов'''
        return Recipe.objects.filter(author=obj.author).count()

    def validate(self, data):
        '''Функция валидации'''
        author = self.context.get('author')
        user = self.context.get('request')
        if Subscription.objects.filter(
                author=author,
                user=user).exists():
            raise ValidationError(
                detail='Вы уже подписаны на этого пользователя!',
                code=status.HTTP_400_BAD_REQUEST)
        return super().validate(data)


class PasswordSerializer(serializers.ModelSerializer):
    """Сериализатор модели User для смены пароля"""
    current_password = serializers.CharField(max_length=150, required=True)
    new_password = serializers.CharField(max_length=150, required=True)

    class Meta:
        '''Метаккласс'''
        model = User
        fields = ('current_password', 'new_password')
