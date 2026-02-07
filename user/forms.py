from allauth.account.forms import SignupForm
from phonenumber_field.formfields import PhoneNumberField
class CustomSignupForm(SignupForm):
    phone_number = PhoneNumberField()
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    def save(self, request):
        user = super().save(request)
        return user