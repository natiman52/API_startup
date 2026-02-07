from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from dj_rest_auth.serializers import LoginSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from .models import MyUser,OTP,PasswordResetToken
from rest_framework import serializers
class CustomUserDetailSerializer(UserDetailsSerializer):
    class Meta:
        fields = ["id","username","is_phone_verified","photo"]
        model = MyUser
class CustomLoginSerializer(LoginSerializer):
    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data) 
        return internal_value
class CustomRegisterSerializer(RegisterSerializer):
    phone_number = PhoneNumberField(required=True)
    def clean(self):
        cleaned_data = super().clean()
        print("cleaned data in serializer:", cleaned_data)
        return cleaned_data
    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['phone_number'] = self.validated_data.get('phone_number', '')
        return data

    def save(self, request):
        user = super().save(request)
        user.phone_number = self.cleaned_data.get('phone_number')
        user.save()
        return user

class CustomPasswordResetSerializer(serializers.Serializer):
    phone = PhoneNumberField(region="ET")
    def save(self,*args,**kwargs):
        user = MyUser.objects.filter(phone_number=self.cleaned_data.get("phone"))
        if(user.exists()):
            otp_obj,created = OTP.objects.get_or_create(user=user.first())
            print(otp_obj.code)
            #send otp code
            return {"status":"success","message":"otp sent"}
        else:
            return {"status":"error","message":"The account does not exist"}

class PasswordRestTokenSeriailzer(serializers.Serializer):
    code = serializers.CharField()
    def save(self,*args,**kwargs):
        otp_obj = OTP.objects.filter(code=self.cleaned_data.get("code"))
        if(otp_obj.exists()):
            otp_obj,created = PasswordResetToken.objects.get_or_create(otp=otp_obj.first())
            return {"status":"success","message":"Everything works","token":otp_obj.code}
        else:
            return {"status":"error","message":"otp could't be verified"}
class ChangePasswordSerailzer(serializers.Serializer):
    token = serializers.CharField(required=True)
    password =serializers.CharField(required=True)
    confirm_password =serializers.CharField(required=True)

    def validate(self,data):
        if(data.get("password") != data.get("confirm_password")):
            return serializers.ValidationError("Passwords dont match")
        return data