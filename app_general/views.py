from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http.response import HttpResponse
from app_myanimes.models import myanime
from .models import Subscription
from app_general.forms import SubscriptionForms,SubscriptionClassForms
from app_users.models import Post
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    all_posts = Post.objects.all().order_by('-created_at')
    context = { 'all_posts': all_posts}
    return render(request, 'app_general/home.html',context)
def about(request):
    return render(request,'app_general/about.html')

def about_us(request):
    return render(request, 'app_general/about_us.html')
