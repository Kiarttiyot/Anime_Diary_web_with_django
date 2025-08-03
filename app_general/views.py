from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http.response import HttpResponse
from app_myanimes.models import myanime
from .models import Subscription
from app_general.forms import SubscriptionForms,SubscriptionClassForms
# Create your views here.
def home(request):
    return render(request, 'app_general/home.html')
def about(request):
    return render(request,'app_general/about.html')
def subscription(request):
    if request.method == "POST":
        form = SubscriptionClassForms(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('subscription_thankyou'))      
    else:
        form = SubscriptionClassForms()
    context = {'form':form}
    return render(request,'app_general/subscription_form.html',context)
def subscription_thankyou(request):
    return render(request,'app_general/subscription_thankyou.html')