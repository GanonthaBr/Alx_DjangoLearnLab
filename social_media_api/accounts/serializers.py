from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id','username','email', 'followers','bio','profile_picture','following')
        read_only_fields = [
            'id','followers','following'
        ]
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

        # token, created = Token.objects.create(user=user)
        # get_user_model().objects.create_user

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        print(user)
        raise serializers.ValidationError("Invalid credentials")