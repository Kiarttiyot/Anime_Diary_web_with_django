from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from app_users.forms import UserProfileForm,ExtendedProfileForm
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect, render

@login_required
def dashboard(request: HttpRequest):
    return render(request,"account/dashboard.html")

def search_user(request):
    q = request.GET.get("q")
    if q:
        try:
            user_obj = User.objects.get(username=q)
            return redirect("dashboard", username=user_obj.username)
        except User.DoesNotExist:
            # ส่ง error message กลับไปหน้า home (หรือหน้าเดิม)
            return render(request, "appgenral/home.html", {"error": "User not found"})
    return redirect("home")  # ถ้าไม่ได้พิมพ์อะไรเลย

def dashboard_view(request, username):
    # เอา user ที่เราต้องการแสดง ไม่ใช่ request.user
    user_profile = get_object_or_404(User, username=username)
    return render(request, "account/dashboard.html", {"user_profile": user_profile})

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