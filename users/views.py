from rest_framework.generics import *
from users.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import *
from rest_framework.authtoken.models import Token
from rest_framework import status
# Create your views here.


class RegisterView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = CustomUser.objects.create_user(
                email=email,
                password=password,
                is_active=False
            )

            # Create a random 6-digit code
        code = ''.join(random.choices(string.digits, k=6))

        confirmation_code = ConfirmationCode.objects.create(
                user=user,
                code=code
            )

        return Response(
            status=status.HTTP_201_CREATED,
            data={
                'user_id': user.id,
                'confirmation_code': code
            }
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
        
        try:
            conf = ConfirmCode.objects.get(code=code)
        except ConfirmCode.DoesNotExist:
            raise ValidationError("Invalid password or user not found")
        
        user = conf.user
        user.is_active = True
        user.save()

        return Response(data={"message":"user confirmed"}, status=200)



