from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
import random
from .models import ConfirmCode

class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ["id", "username", "password", "confirmation_code"]

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username already exists")
        return username   

class UserAuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    password = serializers.CharField()

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValidationError("username doesn't exists")
        return username

class ConfirmCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)
