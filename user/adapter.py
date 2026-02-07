from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.hashers import make_password
import secrets
from .models import OTP
class CustomAccountAdapter(DefaultAccountAdapter):
    def send_confirmation_mail(self, request, emailconfirmation, signup):
        user = emailconfirmation.email_address.user
        # If the user has a phone number, send SMS instead of Email
        if hasattr(user, 'phone_number') and user.phone_number:
            otp_obj,created = OTP.objects.get_or_create(user=user)
            code = otp_obj.code # Or your own logic
            self.send_verification_code_sms(user, str(user.phone_number), code)
        else:
            # Fallback to default email behavior if no phone
            super().send_confirmation_mail(request, emailconfirmation, signup)
    def send_verification_code_sms(self, user, phone, code, **kwargs):
        # Integration logic for Twilio/Vonage
        print(f"Sending SMS to {phone}: Your code is {code}")


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def is_auto_signup_allowed(self, request, sociallogin):
        return True
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        
        extra_data = sociallogin.account.extra_data
        if sociallogin.account.provider == "google":
            picture = extra_data.get("picture")
            if picture:
                user.photo = picture
        if not user.username:
            user.username = generate_unique_username([
                sociallogin.account.extra_data.get('name'),
                sociallogin.account.extra_data.get('email'),
                'user'
            ])
        password = secrets.token_urlsafe(16)
        user.password = make_password(password)
        user.save()
        
        return user