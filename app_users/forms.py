# # app_users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app_users.models import Profile
from .models import Post

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name","last_name")
        
class ExtendedProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('address','phone','profile_image')
        

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content", "image"]
        widgets = {
            "content": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "เขียนอะไรสักหน่อย..."
            }),
        }