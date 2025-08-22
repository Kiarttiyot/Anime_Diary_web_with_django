from django.urls import path
from allauth.account.views import LoginView
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(template_name='account/login.html'), name='login'),
    path('dashboard/',view=views.dashboard,name='dashboard'),
    path('profile/',view=views.profile, name='profile'),
    path("search-users/", views.search_user, name="search_user"),  
    path("dashboard/<str:username>/", views.dashboard_view, name="dashboard"),
    path('mydashboard/',view=views.dashboard,name='mydashboard'),
]
