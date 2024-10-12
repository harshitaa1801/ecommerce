from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class PhoneNumberAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(profile__phone_number=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        return None
