from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager
# Create your models here.

class MyManager(UserManager):
    def create_user(self,username,email,password=None,**extra_fields):
        if not username:
            raise ValueError("The username must be set")
        user=self.model(username=username,email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,username,email,password=None,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        return self.create_user(username,email,password,**extra_fields)
class MyUser(AbstractUser):
    photo = models.URLField(null=True,blank=True)
    objects=MyManager()
    USERNAME_FIELD = "username"

