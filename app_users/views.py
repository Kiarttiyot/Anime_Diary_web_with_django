from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from app_users.forms import UserProfileForm,ExtendedProfileForm

@login_required
def dashboard(request: HttpRequest):
    return render(request,"account/dashboard.html")

@login_required
def profile(request:HttpRequest):
    #POST
    if request.method == 'POST':
        form = UserProfileForm(request.POST,instance=request.user)
        extended_form = ExtendedProfileForm(request.POST)
        if form.is_valid() and extended_form.is_valid():
            form.save()
            profile = extended_form.save(commit=False)
            profile.user = request.user
            profile.save()
            return HttpResponseRedirect(reverse('profile'))
    else:
        form = UserProfileForm()
        extended_form = ExtendedProfileForm()
    #GET
    context = {
        "form":form,
        "extended_form":extended_form
        
    }
    return render(request,"account/profile.html",context)