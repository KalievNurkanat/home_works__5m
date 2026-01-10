from django.urls import path
from users.views import RegisterView, UserAuthView, ConfirmCodeView, CustomJWTView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView
)
from users.google_oauth import GoogleLoginAPIView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("authenticate/", UserAuthView.as_view()),
    path("confirm/", ConfirmCodeView.as_view()),
    path('jwt/', CustomJWTView.as_view(), name='token_obtain_pair'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('google-login/', GoogleLoginAPIView.as_view()),
]

