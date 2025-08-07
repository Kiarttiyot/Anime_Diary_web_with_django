from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def authentication_error(self, request, provider_id, error=None, exception=None, extra_context=None):
        return redirect('/')
