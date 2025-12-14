from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.registration_api_view),
    path("authenticate/", views.authorization_api_view),
    path("<int:id>/", views.delete_user),
    path("confirm/", views.confirmation_api_view)
]