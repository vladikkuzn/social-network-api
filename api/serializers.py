from rest_framework import serializers
from .models import User, Post, Like
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email', 
            'password'
        )


class PostListSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Post
        fields = (
            'id', 
            'title', 
            'text', 
            'likes', 
            'created', 
            'created_by'
        )
        read_only_fields = (
            'created', 
            'created_by'
        )

    @property
    def request(self):
        return self._context['request']

    def create(self, data):
        data.update({
            'created_by': self.request.user,
            'changed_by': self.request.user,
        })
        return super().create(data)

    def update(self, instance, data):
        data.update({
            'changed_by': self.request.user
        })
        return super().update(instance, data)


class PostSerializer(PostListSerializer):
    likes = serializers.StringRelatedField(
        many=True, 
        read_only=True
    )


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'
        read_only_fields = (
            'changed_datetime',
            'changed_by',
            'created_datetime',
            'created_by'
        )


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(_class, user):
        token = super(CustomTokenObtainPairSerializer, _class).get_token(user)
        token['username'] = user.username
        return token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password]
    )
    password_conf = serializers.CharField(
        write_only=True, 
        required=True
    )

    class Meta:
        model = User
        fields = (
            'username', 
            'password', 
            'password_conf', 
            'email'
        )
    
    def validate(self, kwarg):
        if kwarg['password'] != kwarg['password_conf']:
            raise serializers.ValidationError()
        return kwarg

    def create(self, data):
        user = User.objects.create(
            username = data['username'],
            email = data['email']
        )
        user.set_password(data['password'])
        user.save()
        return user


class ActivitySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = (
            'username',
            'last_login',
            'last_request'
        )
