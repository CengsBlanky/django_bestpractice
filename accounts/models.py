import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager

# Create your models here.


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(
        "电话号码", max_length=25, null=False, blank=False, unique=True
    )
    gender = models.CharField(
        "性别", max_length=1, choices=(("M", "男"), ("F", "女")), default="M"
    )

    objects = CustomUserManager()  # pyright: ignore[reportAssignmentType]

    USERNAME_FIELD = "phone"

    REQUIRED_FIELDS = [
        "username",
        "gender",
    ]

    def get_username(self):
        return self.username

    def __str__(self):
        return self.username
