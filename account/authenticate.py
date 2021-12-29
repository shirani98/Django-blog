from django.contrib.auth.backends import ModelBackend
from django.shortcuts import redirect
from .models import CustomUser

class EmailPhoneBackend():
    def authenticate(self, request, username= None, password=None, **kwargs):
        if username is None:
            raise ValueError("username is None")
        else:
            try:
                user = CustomUser.objects.get(phone=username)
                if user is None:
                    user = CustomUser.objects.get(email=username)
            except CustomUser.DoesNotExist:
                return None
            if user.check_password(password):
                return user
            
    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise ValueError("CustomUser.DoesNotExist")