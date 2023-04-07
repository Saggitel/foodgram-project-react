'''Вьюсеты прложения Recipes'''
from api.paginations import ApiPagination
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Favourite, Ingredient, Recipe, ShoppingCart, Tag
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import User

from .filters import IngredientSearchFilter, RecipeFilter
from .permissions import IsOwnerOrAdminOrReadOnly
from .serializers import (FavouriteSerializer, IngredientSerializer,
                          RecipeListSerializer, RecipeWriteSerializer,
                          ShoppingCartSerializer, TagSerializer)
from .services import shopping_cart


class TagViewSet(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):
    '''Вьюсет модели Tag'''
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permissions_class = (AllowAny,)

class IngredientViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    '''Вьюсет модели Ingredient'''
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permissions_class = (AllowAny,)
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)

class RecipeViewSet(viewsets.ModelViewSet):
    '''Вьюсет рецепты'''
    queryset = Recipe.objects.all()
    permission_classes = (IsOwnerOrAdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    pagination_class = ApiPagination
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        '''Функция выболра сериализатора 
           в зависимости от метода запроса'''
        if self.request.method in SAFE_METHODS:
            return RecipeListSerializer
        return RecipeWriteSerializer

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favourite(self, request, *args, **kwargs):
        '''Функция получения, добавления и удаления рецепта из избранного'''
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))
        user = self.request.user
        if request.method == 'POST':
            serializer = FavouriteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(author=user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        Favourite.objects.get(recipe=recipe).delete()
        return Response('Рецепт успешно удалён из избранного.',
                        status=status.HTTP_204_NO_CONTENT)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, **kwargs):
        '''Функция получения, добавления и удаления рецепта из списка покупок'''
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))
        user = self.request.user
        if request.method == 'POST':
            serializer = ShoppingCartSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(author=user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if not ShoppingCart.objects.filter(author=user,
                                           recipe=recipe).exists():
            return Response({'errors': 'Объект не найден'},
                            status=status.HTTP_404_NOT_FOUND)
        ShoppingCart.objects.get(recipe=recipe).delete()
        return Response('Рецепт успешно удалён из списка покупок.',
                        status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,
            methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        '''Функция скачивания из покупок нексольких рецептов'''
        author = User.objects.get(id=self.request.user.pk)
        if author.shopping_cart.exists():
            return shopping_cart(self, request, author)
        return Response('Список покупок пуст.',
                        status=status.HTTP_404_NOT_FOUND)
