from django.shortcuts import render
from django import forms
from django.core.exceptions import ValidationError

# Create your views here.
from allauth.account.forms import SignupForm, LoginForm
from allauth.account.utils import setup_user_email
from allauth.account.models import EmailAddress
from allauth.account.views import LoginView, SignupView

from allauth.account import views as allauth_views


from accounts.models import Profile

class CustomSignupForm(SignupForm):
    phone_number = forms.CharField(max_length=15, required=True, label="Phone Number")

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        # Check if phone number already exists
        if Profile.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("This phone number is already in use. Please use a different phone number.")

        return phone_number

    def save(self, request):
        user = super().save(request)
        
        # If the user has provided an email, set up email verification
        cleaned_data = super().clean()
        phone_number = self.cleaned_data.get('phone_number')
        print(phone_number)
        # profile = Profile.objects.filter(user=user).first()
        # print(profile)
        # print(profile.phone_number)
        # profile.phone_number=phone_number
        # profile.save()
        # print(profile.phone_number)
        # print(phone_number)
        Profile.objects.create(user=user, phone_number=phone_number)
        if user.email:
            setup_user_email(request, user)
            if not EmailAddress.objects.filter(user=user, email=user.email).exists():
                EmailAddress.objects.create(user=user, email=user.email, verified=False, primary=True)
        
        return user


class CustomLoginForm(LoginForm):
    phone_number = forms.CharField(max_length=15, required=False, label="Phone Number")
    print(phone_number)


    def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data.get("phone_number")

        # Add custom logic to authenticate using phone number if provided
        if phone_number:
            # Your logic to find and authenticate using phone number
            pass  # Implement custom authentication logic here

        return cleaned_data



def login_signup_view(request):

    print('login signup form')

    login_form = CustomLoginForm()  # Instantiate login form
    signup_form = CustomSignupForm()  # Instantiate signup form


    return render(request, 'accounts/login_signup.html', {
        'login_form': login_form,
        'signup_form': signup_form
    })




class CustomSignupView(SignupView):
    template_name = 'accounts/login_signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['open_signup'] = True  # Add variable to open signup form
        return context