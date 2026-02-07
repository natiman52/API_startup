from django.shortcuts import render
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import permission_classes,authentication_classes,api_view
from phonenumber_field.phonenumber import PhoneNumber
from .models import OTP,PasswordResetToken
from rest_framework.response import Response
from django.utils import timezone
from .serializer import CustomPasswordResetSerializer,PasswordRestTokenSeriailzer,ChangePasswordSerailzer
from rest_framework.generics import GenericAPIView
from .utils import verify_phone_util
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:3000/auth/callback/google"
    client_class = OAuth2Client
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class PasswordResetView(GenericAPIView):
    serializer_class = CustomPasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return_status = serializer.save()
        if(render.get("status") == "error"):
            return Response(
                return_status,
                status=401,
            )
        else:
            return Response(
                return_status,
                status=200,
            )
class PasswordResetOTPVerify(GenericAPIView):
    serializer_class = PasswordRestTokenSeriailzer
    permission_classes = (AllowAny,)
    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return_status = serializer.save()
        if(render.get("status") == "error"):
            return Response(
                return_status,
                status=401,
            )
        else:
            return Response(
                return_status,
                status=200,
            )
class ChangePasswordView(GenericAPIView):
    def post(self,request,*args,**kwargs):
        objs = ChangePasswordSerailzer(data=request.data)
        if(objs.is_valid()):
            token = objs.cleaned_data.get('token')
            password = objs.cleaned_data.get('password')
            token = PasswordResetToken.objects.filter(code=token)
            if(token.exists()):
                user = token.first().otp.user
                user.set_password(password)
                return Response({'status':"success","message":"password has been changed changed"})
            else:
                return Response({'status':"error","message":"token does not much"})
        else:
            return Response({'status':"error","message":"the given credential don't meet standards"})

                
# will add more data when needed
class CompleteSignup(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,*args,**kwargs):
        user =request.user
        data = request.data
        if(data.get("phone")):
            phone_number = PhoneNumber.from_string(data.get("phone"),"ET")
            if(phone_number.is_valid()):
                otp_obj,created = OTP.objects.get_or_create(user=user)
                print(otp_obj.code)
                # do some code sending
                user.phone_number = data.get("phone")
                user.save()
                return Response({"status":"success","message":""},status=200)
            else:
                return Response({"status":"failed","message":"phone number not valid"},status=401)
        return Response({"status":"failed","message":"phone number is empty"},status=401)
        
class VerifyCode(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,*args,**kwargs):
        user = request.user
        otp_obj = OTP.objects.filter(user=user)
        def callback():
            user.is_phone_verified = True
            user.save()
            otp_obj.first().delete()
            return Response({"status":"success","message":"Account Verified"},status=200)
        verify_phone_util(request,otp_obj,callback)