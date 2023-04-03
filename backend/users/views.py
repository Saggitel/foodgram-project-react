'''Вьюctns модели Users'''
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Subscription, User
from .serializers import (PasswordSerializer, SubscriptionSerializer,
                          UserRegistrationSerializer, UserSerializer)


class UserViewSet(DjoserUserViewSet):
    '''Вьюсет модели User'''
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return UserSerializer
        return UserRegistrationSerializer

    @action(methods=['post', 'delete'],
            detail=True,
            permission_classes=(IsAuthenticated,),
            url_path='subscribe',)
    def subscribe(self, request, id=None):
        '''Метод для создания Подписки на автора, удаления Подписки на атвора'''
        if request.method == 'POST':
            serializer = SubscriptionSerializer(
                data=request.data, context={
                    'pk': id, 'user': self.request.user
                }
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(
                author_id=id,
                user=self.request.user
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            user = self.request.user
            author = get_object_or_404(User, pk=id)
            subscription = Subscription.objects.filter(
                user=user, author=author
            )
            if subscription.exists():
                subscription.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {'Вы не были подписаны на этого пользователя'},
                    status=status.HTTP_400_BAD_REQUEST)

class APIChangePassword(APIView):
    '''Метод для смены пароля пользователя'''
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        '''Переопределен метод Post'''
        serializer = PasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=request.user.username
        )
        if check_password(
                serializer.validated_data['current_password'], user.password
        ):
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

class SubscriptionViewSet(viewsets.ReadOnlyModelViewSet):
    '''Метод для подписки'''
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    serializer_class = SubscriptionSerializer

    def ger_queryset(self):
        '''Переопределен метод queryset'''
        user = self.request.user
        queryset = Subscription.objects.filter(user=user)
        return queryset
