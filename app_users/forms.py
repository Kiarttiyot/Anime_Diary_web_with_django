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
        fields = ('address', 'phone', 'profile_image')
        widgets = {
            'profile_image': forms.FileInput(attrs={
                'id': 'id_profile_image',
                'accept': 'image/*',  # จำกัดให้เลือกแค่รูป
                'style': 'display:none;'  # ซ่อนแทนการบังคับด้วย JS
            }),
        }
        

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["name", "content", "image", "state", "score"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "ชื่อโพสต์"}),
            "content": forms.Textarea(attrs={"rows": 3, "placeholder": "เพิ่มคำบรรยาย..."}),
            "state": forms.Select(),
            "score": forms.NumberInput(attrs={"type": "hidden"}),
        }

    # บังคับให้ใส่รูป
    def clean_image(self):
        image = self.cleaned_data.get("image")
        if not image:
            raise forms.ValidationError("กรุณาใส่รูปภาพด้วยครับ")
        return image