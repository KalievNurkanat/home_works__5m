from django.urls import path
from users.views import RegisterView, UserAuthView, ConfirmCodeView, CustomJWTView
from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenVerifyView
)
from users.google_oauth import GoogleLoginAPIView
from users.redis_code import GenerateConfirmaitonCode, CheckConfirmationCode

urlpatterns = [
    path("generate_code/", GenerateConfirmaitonCode.as_view()),
    path("check_generated_code/", CheckConfirmationCode.as_view()),
    path("register/", RegisterView.as_view()),
    path("authenticate/", UserAuthView.as_view()),
    path("confirm/", ConfirmCodeView.as_view()),
    path('jwt/', CustomJWTView.as_view(), name='token_obtain_pair'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('google-login/', GoogleLoginAPIView.as_view()),
]

