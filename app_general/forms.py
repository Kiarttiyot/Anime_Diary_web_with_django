from django import forms
from app_myanimes.models import myanime
from .models import  Subscription
class AnimeMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.title


class SubscriptionForms(forms.Form):
    name = forms.CharField(max_length=60, required=True, label='ชื่อ-นามสกุล')
    email = forms.EmailField(max_length=60,required=True,label='email')
    anime = AnimeMultipleChoiceField(
        queryset=myanime.objects.order_by('-status'),
        required = True,
        label = 'อนิเมะที่สนใจ',
        widget = forms.CheckboxSelectMultiple
        )
    accepted = forms.BooleanField(required=True,label='ข้อความยาวๆๆที่รู้ว่าลอกควายอ่านสำเร็จว้ายๆ')
    
class SubscriptionClassForms(forms.ModelForm):
    anime = AnimeMultipleChoiceField(
        queryset=myanime.objects.order_by('-status'),
        required = True,
        label = 'อนิเมะที่สนใจ',
        widget = forms.CheckboxSelectMultiple
        )
    accepted = forms.BooleanField(required=True,label='ข้อความยาวๆๆที่รู้ว่าหลอกควายอ่านสำเร็จว้ายๆ')
    class Meta:
        model = Subscription
        fields = ['name','email','anime','accepted']
        labels = {
            'name': 'ชื่อ-นามสกุล',
            'email': 'email',
            'anime':'อนิเมะที่สนใจ'
        }
        