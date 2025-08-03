from django.urls import path
from . import views

urlpatterns = [
    path('',views.myanimes,name='myanimes'),
    path('<int:myanime_id>',views.anime,name="anime")
    
]
