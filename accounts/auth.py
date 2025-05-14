from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from.models import *

class CustomUserBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        # If password is not correct, return None.
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()

        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

class PoliceInchargeBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        print("PoliceInchargeBackend called")
        print(email)
        print(password)
        try:
            user = police_incharge.objects.get(email=email)
            print(user.password)
            print("email found")
        except:
            return None

        # if user.check_password(password): 
        #     return user

        if user.password == password:
            print("right password")
            print(user)
            return user
        

        # If password is not correct, return None.
        print("wrong pass")

    def get_user(self, user_id):
        try:
            return police_incharge.objects.get(pk=user_id)
        except police_incharge.DoesNotExist:
            return None
        
class PoliceBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        print("PoliceBackend called")
        print(email)
        print(password)
        try:
            user = police_officer.objects.get(email=email)
            print(user.password)
            print("email found")
        except:
            return None

        # if user.check_password(password): 
        #     return user

        if user.password == password:
            print("right password")
            print(user)
            return user
        

        # If password is not correct, return None.
        print("wrong pass")

    def get_user(self, user_id):
        try:
            return police_officer.objects.get(pk=user_id)
        except police_officer.DoesNotExist:
            return None
