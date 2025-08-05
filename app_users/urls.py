from django.urls import path,include
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path("",include("django.contrib.auth.urls")),
     path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    
]
