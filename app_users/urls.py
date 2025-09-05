from django.urls import path
from allauth.account.views import LoginView
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(template_name='account/login.html'), name='login'),
    path('dashboard/',view=views.dashboard,name='dashboard'),
    path('profile/',view=views.profile, name='profile'),
    path("search-users/", views.search_user, name="search_user"),  
    path("dashboard/<str:username>/", views.dashboard_view, name="dashboard"),
    path("dashboard/", views.dashboard, name="my_dashboard"),  # ของตัวเอง
    path("dashboard/<str:username>/", views.dashboard, name="dashboard"),  # ของคนอื่น
    path("create-post/", views.create_post, name="create_post"),  # หน้าโพสต์ใหม่
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
]
