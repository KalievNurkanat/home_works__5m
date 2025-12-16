from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view()),
    path("authenticate/", views.UserAuthView.as_view()),
    path("confirm/", views.ConfirmCodeView.as_view())
]