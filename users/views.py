from rest_framework.generics import *
from users.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import *
from rest_framework import status
# Create your views here.


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


class UserAuthView(APIView):
    def post(self, request):
        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key})


class ConfirmCodeView(APIView):
    def post(self, request):
        serializer = ConfirmCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data["code"]
        
        try:
            conf = ConfirmCode.objects.get(code=code)
        except ConfirmCode.DoesNotExist:
            raise ValidationError("Invalid password or user not found")
        
        user = conf.user
        user.is_active = True
        user.save()

        return Response(data={"message":"user confirmed"}, status=200)



