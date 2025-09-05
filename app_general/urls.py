from django.urls import path
from . import views
from app_users import views as user_views

urlpatterns = [
    path('', views.home,name='home'),
    path('about/',views.about,name='about'),
    path('about_us/', views.about_us, name='about_us'),
    path('add_comment/<int:post_id>/', user_views.add_comment, name='add_comment'),

]
