from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.http.response import HttpResponse
from app_myanimes.models import myanime
from .models import Subscription
from app_general.forms import SubscriptionForms,SubscriptionClassForms
from app_users.models import Post
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from app_users.models import Profile,Post,Follow
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.db.models import Prefetch
# Create your views here.
def home(request):
    all_posts = Post.objects.all().order_by('-created_at')
    context = { 'all_posts': all_posts}
    return render(request, 'app_general/home.html',context)
def about(request):
    return render(request,'app_general/about.html')

def about_us(request):
    return render(request, 'app_general/about_us.html')


def friend(request):
    query = ""
    if request.method == "POST":
        query = (request.POST.get("name_friend") or "").strip()
        if query:
            try:
                # หา username แบบ case-insensitive
                profile = (
                    Profile.objects
                    .select_related("user")
                    .get(user__username__iexact=query)
                )
            except Profile.DoesNotExist:
                return render(request, "app_general/friend.html", {
                    "query": query,
                    "error": f'ไม่พบผู้ใช้ "{query}"',
                })

            profile_user = profile.user

            posts = (
                Post.objects
                .filter(user=profile_user)
                .select_related("user")
                .order_by("-created_at")
            )

            # นับ followers / following โดยอิงโมเดล Follow(follower, following)
            followers_count = Follow.objects.filter(following=profile_user).count()
            following_count = Follow.objects.filter(follower=profile_user).count()

            # ผู้ใช้ที่ล็อกอินอยู่ กำลังติดตาม profile_user อยู่ไหม?
            is_following = False
            if request.user.is_authenticated and request.user != profile_user:
                is_following = Follow.objects.filter(
                    follower=request.user,
                    following=profile_user
                ).exists()

            return render(request, "app_general/user_dashboard_from_search.html", {
                "profile_user": profile_user,
                "posts": posts,
                "query": query,
                "followers_count": followers_count,
                "following_count": following_count,
                "is_following": is_following,
            })

    # GET หรือยังไม่ได้ค้นหา → แค่แสดงฟอร์มค้นหา
    return render(request, "app_general/friend.html", {"query": query})