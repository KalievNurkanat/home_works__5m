from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from users.managers import CustomUserManager
# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField()
    email = models.EmailField(unique=True)
    phone_number = models.IntegerField()
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number"]

    def __str__(self) -> str:
        return self.email or ""
    
    
class ConfirmCode(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)


    def __str__(self):
        return f"{self.user}: {self.code}"
    
