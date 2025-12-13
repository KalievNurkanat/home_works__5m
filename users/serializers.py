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

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(
            username=validated_data["username"],
            is_active=False
        )
        user.set_password(password)
        user.save()

        code = str(random.randint(100000, 999999))
        ConfirmCode.objects.create(user=user, code=code)

        return user


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



