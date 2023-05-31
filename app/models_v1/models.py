from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.db.models.base import Model
from django.utils import timezone


# Create your models here.
class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Admin(AbstractBaseUser, BaseModel):
    id = models.AutoField(auto_created=True, primary_key=True)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=50)
    is_mailauth_completed = models.BooleanField(default=0)
    is_master = models.BooleanField(default=0)
    is_enabled = models.BooleanField(default=1)
    config = models.JSONField(null=True)
    is_super = models.BooleanField(default=0)

    USERNAME_FIELD = "name"

    def __str__(self):
        return self.name

    class Meta:
        db_table = "admins"
        app_label = "api"
