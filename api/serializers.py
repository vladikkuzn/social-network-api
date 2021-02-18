from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(_class, user):
        token = super(CustomTokenObtainPairSerializer, _class).get_token(user)
        token['username'] = user.username
        return token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_conf = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password_conf', 'email')
    
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
