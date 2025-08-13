from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse


@login_required
def dashboard(request: HttpRequest):
    return render(request,"account/dashboard.html")