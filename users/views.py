from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from .models import ConfirmCode
# Create your views here.

@api_view(["POST"])
def registration_api_view(request):
    registrate = UserRegisterSerializer(data=request.data)
    registrate.is_valid(raise_exception=True)

    username = registrate.validated_data["username"]
    password = registrate.validated_data["password"]

    user = User.objects.create_user(
        username=username, password=password,
        is_active=False
    )
      
    code = str(random.randint(100000, 999999))
    ConfirmCode.objects.create(user=user, code=code)

    # optionally return code for testing
    return Response(
        {"message": "User created", "confirmation_code": code},
        status=status.HTTP_201_CREATED
    )


@api_view(["POST"])
def authorization_api_view(request):
    authentication = UserAuthSerializer(data=request.data)
    authentication.is_valid(raise_exception=True)

    username = authentication.validated_data["username"]
    password = authentication.validated_data["password"]

    user = authenticate(username=username, password=password)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response(data={"key":token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(["DELETE"])
def delete_user(request, id):
    user = User.objects.get(id=id)

    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def confirmation_api_view(request):
    confirm_code = ConfirmCodeSerializer(data=request.data)
    confirm_code.is_valid(raise_exception=True)

    code = confirm_code.validated_data["code"]

    try:
        confirm = ConfirmCode.objects.get(code=code)
    except ConfirmCode.DoesNotExist:
        return Response({"error": "Неверный код"}, status=400)

    user = confirm.user
    user.is_active = True
    user.save()


    return Response({"message": "Аккаунт подтверждён"}, status=status.HTTP_202_ACCEPTED)

