from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    online = models.BooleanField(default=False)


class PhoneNumber(models.Model):
    book_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    phone_number1 = models.CharField(max_length=50)
    phone_number2 = models.CharField(max_length=50)


admin.site.register(PhoneNumber)
