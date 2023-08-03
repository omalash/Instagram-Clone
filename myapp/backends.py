from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Check if the provided identifier is an email
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            # If not an email, try to authenticate with the provided username
            user = User.objects.filter(username=username).first()

        if user is not None and user.check_password(password):
            return user
        return None