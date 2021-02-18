from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, Post
from .serializers import (
    CustomTokenObtainPairSerializer,
    RegisterSerializer,
    PostListSerializer,
    PostSerializer, 
    UserSerializer
)


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    
    def get_serializer_class(self):
        return PostListSerializer if self.action == 'list' else PostSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer



