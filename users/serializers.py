from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.models import CustomUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomJWTSerilizer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["birthday"] = str(user.birthday)

        return token

class UserBaseSerializer(serializers.Serializer):
    username = serializers.CharField()
    phone_number = serializers.CharField(required=False, default="+996")
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    birthday = serializers.DateField()


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
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            phone_number=validated_data.get("phone_number"),
            username=validated_data.get("username"),
            birthday=validated_data.get("birthday"),
            is_active=False
        )

        return user
    

class UserAuthSerializer(serializers.Serializer):
    user = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            user=data["user"],
            email=data["email"],
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

    


