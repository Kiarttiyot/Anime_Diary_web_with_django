# # app_users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app_users.models import Profile
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name","last_name")
        
class ExtendedProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('address','phone')
