from django.shortcuts import render

# Create your views here.
def custom_login(request):
    return render(request, 'account/loging.html')