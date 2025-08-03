from datetime import datetime
from django.shortcuts import render
from .models import myanime
# Create your views here.

def myanimes(request):
    all_myanimes = myanime.objects.order_by('-status')
    context = {'myanimes':all_myanimes}
    return render(request, 'app_myanimes/myanimes.html',context)

def anime(request,myanime_id):
    one_anime = None
    try:
        one_anime = myanime.objects.get(id=myanime_id)
    except:
        print("ไม่มีอะไร")
    context = {'anime': one_anime}
    return render(request, 'app_myanimes/myanime.html', context)
