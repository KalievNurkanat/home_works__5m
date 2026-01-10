from rest_framework.generics import CreateAPIView
from users.serializers import (UserRegisterSerializer,
                                UserAuthSerializer,
                                  ConfirmCodeSerializer,
                                    CustomJWTSerilizer)
from rest_framework.response import Response
from users.models import CustomUser, ConfirmCode
from rest_framework.authtoken.models import Token
import random
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView
# Create your views here.

class CustomJWTView(TokenObtainPairView):
    serializer_class = CustomJWTSerilizer

class RegisterView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer
    def perform_create(self, serializer):
        user = serializer.save()
        user.save()
        code = str(random.randint(100000, 999999))

        ConfirmCode.objects.create(
                user=user,
                code=code
            )


class UserAuthView(CreateAPIView):
    serializer_class = UserAuthSerializer
    def post(self, request):
        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key})


class ConfirmCodeView(CreateAPIView):
    serializer_class = ConfirmCodeSerializer
    def post(self, request):
        serializer = ConfirmCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data["code"]
        users = serializer.validated_data["user_id"]
        
        try:
            conf = ConfirmCode.objects.get(code=code, user_id=users)
        except ConfirmCode.DoesNotExist:
            raise ValidationError("Invalid password or user not found")
        
        user = conf.user
        user.is_active = True
        user.save()

        return Response(data={"message":"user confirmed"}, status=200)



