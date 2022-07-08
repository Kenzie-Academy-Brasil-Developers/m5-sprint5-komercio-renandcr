from django.contrib.auth.models import AbstractUser   
from accounts.utils import  CustomUserManager
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_seller = models.BooleanField()
    username = models.CharField(max_length=50, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "is_seller"]
    objects = CustomUserManager()

    def __repr__(self) -> str:
        return f"model:User - email:{self.email} - id:{self.id}"