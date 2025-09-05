from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('about/',views.about,name='about'),
    path('subscription/',views.subscription,name='subscription'),
    path('about_us/', views.about_us, name='about_us'),
]
