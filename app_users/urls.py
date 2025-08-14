from django.urls import path
from allauth.account.views import LoginView
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(template_name='account/login.html'), name='login'),
    path('dashboard/',view=views.dashboard,name='dashboard'),
]