'''Сериализаторы моделей User'''
from rest_framework import serializers

from recipes.models import Recipe
from .models import User, Subscription

class UserSerializer(serializers.ModelSerializer):
    '''Отображение списка пользователей'''
    #id = serializers.ReadOnlyField
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        '''Метамодель'''
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')
        #read_only_fields = '__all__'

    def get_is_subscribed(self, obj):
        '''Функция првоерки подписки на автора'''
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(user=request.user, author=obj).exists()

class UserRegistrationSerializer(serializers.ModelSerializer):
    '''Сериализатор модели User для регистрации пользователя'''
    class Meta:
        '''Метамодель'''
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class RecipesSerializer:
    '''Сериализатор рецептов для Мои подписки'''
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
        model = Recipe
        fields = ('id', 'name', 'image', 'coocking_time')
        read_only_fields = '__all__'

class SubscriptionSerializer:
    '''Сериализатор мои подписки'''
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
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed',
                  'recipes', 'recipes_count')
        #read_only_fields = '__all__'

    def get_is_subscribed(self, obj):
        '''Проверка пописки на автора'''
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(user=obj.user, author=obj.author).exists()


    def get_recipe(self, obj):
        pass


    def get_recipes_count(self, obj):
        '''Функция подсчета количесвта рецептов'''
        return Recipe.objects.filter(author=obj.author).count()
