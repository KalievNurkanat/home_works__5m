from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
import random
from users.models import *
from django.contrib.auth import authenticate


class UserBaseSerializer(serializers.Serializer):
    phone_number = serializers.IntegerField(min_value=3, max_value=10)
    email = serializers.EmailField()
    password = serializers.CharField()


class AuthValidateSerializer(UserBaseSerializer):
    pass



class UserRegisterSerializer(UserBaseSerializer):
    def validate_username(self, username):
        if CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username already exists")
        return username 
    
    def validate_email(self, email):
        try:
            CustomUser.objects.get(email=email)
        except:
            return email
        raise ValidationError('CustomUser уже существует!')


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

    


