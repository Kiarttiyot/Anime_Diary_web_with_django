# app_users/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    # คุณสามารถเพิ่ม field หรือแก้ไข widget ได้ตรงนี้
    username = forms.CharField(
        label='ชื่อผู้ใช้',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'กรอกชื่อผู้ใช้'})
    )
    password = forms.CharField(
        label='รหัสผ่าน',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'กรอกรหัสผ่าน'})
    )
