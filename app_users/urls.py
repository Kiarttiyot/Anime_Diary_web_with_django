from django.urls import path,include
from . import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path("",include("django.contrib.auth.urls")),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('register/',view=views.register,name="register"),
    
]
