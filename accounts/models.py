from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_college = models.BooleanField(default=False)
    is_railway = models.BooleanField(default=False)