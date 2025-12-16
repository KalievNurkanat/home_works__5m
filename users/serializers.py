from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
import random
from .models import ConfirmCode
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password"]

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username already exists")
        return username 

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User.objects.create_user(
            username=validated_data["username"],
            password=password, is_active = False
        )  
        user.save()

        code = str(random.randint(100000, 999999))
        ConfirmCode.objects.create(code=code, user=user)

        return user

class UserAuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data["username"],
            password=data["password"]
        )

        if user is None:
            raise serializers.ValidationError("Неверный логин или пароль")

        if not user.is_active:
            raise serializers.ValidationError("Аккаунт не активирован")

        data["user"] = user
        return data

class ConfirmCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)
    user_id = serializers.IntegerField()

    


