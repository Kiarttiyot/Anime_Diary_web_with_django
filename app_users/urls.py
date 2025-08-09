from django.urls import path
from allauth.account.views import LoginView

urlpatterns = [
    path('login/', LoginView.as_view(template_name='account/loging.html'), name='account_login'),
   
    
]