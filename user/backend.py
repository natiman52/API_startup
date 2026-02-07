from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from phonenumber_field.phonenumber import to_python
from django.conf import settings
User = get_user_model()

class PhoneOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None,email=None, **kwargs):
        try:
            phone_number = username or ""

            phone_obj = to_python(phone_number)
            if not (phone_obj and phone_obj.is_valid()):
                default_region = getattr(settings, 'PHONENUMBER_DEFAULT_REGION', 'ET')
                phone_obj = to_python(phone_number, region=default_region)
            if phone_obj and phone_obj.is_valid():
                 phone_number = phone_obj.as_e164
            user = User.objects.get(Q(username=username) | Q(phone_number=phone_number) | Q(email=email))
        except User.DoesNotExist:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user