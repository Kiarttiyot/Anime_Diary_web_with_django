from django.contrib.auth import login
from django.shortcuts import render
from app_users.forms import RegisterForm
from django.http import HttpResponse, HttpResponseRedirect
from app_users.forms import RegisterForm
from django.urls import reverse
# Create your views here.


def register(request):
    # POST
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return HttpResponseRedirect(reverse("home"))
    else:
        form = RegisterForm()        
            
    #GET
    context = {'form':form}
    return render(request,'app_users/register.html',context)