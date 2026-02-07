from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager
from phonenumber_field.modelfields import PhoneNumberField
from allauth.account.adapter import generate_user_code
from django.utils import timezone
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
    phone_number = PhoneNumberField(max_length=15, unique=True, null=True, blank=True)
    is_phone_verified = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    photo = models.URLField(null=True,blank=True)
    objects=MyManager()
    USERNAME_FIELD = "username" 

def expire_time():
    return  timezone.datetime.now() + timezone.timedelta(minutes=10)
class OTP(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    code =models.CharField(max_length=25,default=generate_user_code) 
    expire_date = models.DateTimeField(default=expire_time)

def generate_token():
    return generate_user_code(50)
class PasswordResetToken(models.Model):
    otp = models.ForeignKey(OTP,on_delete=models.CASCADE)
    code =models.CharField(max_length=200,default=generate_token) 
    expire_date = models.DateTimeField(default=expire_time)