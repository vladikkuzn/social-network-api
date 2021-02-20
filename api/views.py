from django.shortcuts import render, get_object_or_404
from rest_framework import generics, viewsets, serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, Post, Like
from .serializers import (
    CustomTokenObtainPairSerializer,
    RegisterSerializer,
    PostListSerializer,
    PostSerializer, 
    UserSerializer,
    LikeSerializer,
    ActivitySerializer
)
from django.db.models import Count


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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_like(request, post_id):
    
    def post_liked_by(user):
        if Like.objects.filter(created_by=user, post__id=post_id).exists():
            return True
        return False

    if request.method == 'POST':
        serializer = LikeSerializer(data=request.data)
        user = request.user
        if serializer.is_valid() and not post_liked_by(user):
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_like(request, like_id):
    like = get_object_or_404(Like, id=like_id)
    if request.method == 'DELETE':
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def analytics(request):
    try:
        date_from = request.GET['date_from']
        date_to = request.GET['date_to']
    except:
        return Response("Provide right args", status=status.HTTP_400_BAD_REQUEST)

    analytics = Like.objects.filter(
        created__range=(date_from, date_to)
    ).extra(
        {'created': "date(created)"}
    ).values(
        'created'
    ).annotate(
        liked_count=Count('id')
    )
    return Response({'data': analytics})


class Activity(generics.RetrieveAPIView):
    serializer_class = ActivitySerializer
    queryset = User.objects.all()