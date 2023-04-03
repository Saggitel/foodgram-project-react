from django.shortcuts import render
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework import status, viewsets

from .models import User, Subscription
from .serializers import UserSerializer, UserRegistrationSerializer

class UserViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return UserSerializer
        return UserRegistrationSerializer

    def subscription():
        
    
class APIChangePassword(APIView):
    pass

class SubscriptionViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes
    pagination_class
    serializer_class
    
    def ger_queryset(self):
        user = self.request.user
        queryset = Subscription.objects.filter(user=user)
        return queryset
