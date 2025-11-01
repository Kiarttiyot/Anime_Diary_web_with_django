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
    path("post/<int:pk>/delete/", views.post_delete, name="post_delete"),
    path("archive/", views.archive_list, name="archive_list"),
    path("post/<int:pk>/archive/", views.post_archive, name="post_archive"),
    path("post/<int:pk>/unarchive/", views.post_unarchive, name="post_unarchive"),
    path('toggle-like/<int:post_id>/', views.toggle_like, name='toggle_like'),
    path('follow_toggle/<str:username>/', views.follow_toggle, name='follow_toggle'),
    path('<str:username>/followers/', views.follower_list, name='follower_list'),
    path('<str:username>/following/', views.following_list, name='following_list'),
    path("<str:username>/from-search/", views.user_dashboard_from_search, name="user_dashboard_from_search"),
    path("post/<int:pk>/edit/", views.edit_post, name="edit_post"),
    path("post/<int:post_id>/like/", views.toggle_like, name="toggle_like"),
]
