from django.contrib.auth.backends import BaseBackend
from account_app.models import User

class EmailAuthBackend(BaseBackend):
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            print(user)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None