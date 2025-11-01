from django.shortcuts import render
from django.urls import reverse, NoReverseMatch
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from app_users.forms import UserProfileForm,ExtendedProfileForm
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect, render
from .models import Post, Comment
from .forms import PostForm, CommentForm
from app_users.models import Profile
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Post, Like,Follow
from django.views.decorators.http import require_POST
from django.contrib import messages
from urllib.parse import urlencode


@login_required
def dashboard(request: HttpRequest):
    return render(request,"account/dashboard.html")

@login_required
def dashboard(request: HttpRequest):
    return render(request,"account/dashboard.html")
@login_required
def search_user(request):
    q = request.GET.get("q")
    if q:
        try:
            user_obj = User.objects.get(username=q)
            base = reverse("user_dashboard_from_search", kwargs={"username": user_obj.username})
            return redirect(f"{base}?{urlencode({'q': q})}")
        except User.DoesNotExist:
            # กลับหน้า friend (not-found) ตามที่คุณตั้งไว้
            return render(request, "friend.html", {"error": "User not found"})
    return redirect("home")

def dashboard_view(request, username):
    # เอา user ที่เราต้องการแสดง ไม่ใช่ request.user
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=profile_user, is_archived=False).order_by('-created_at') 
    return render(request, "account/dashboard.html", {"profile_user": profile_user,"posts": posts})

@login_required
def profile(request:HttpRequest):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        extended_form = ExtendedProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid() and extended_form.is_valid():
            form.save()
            extended_form.save()
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        form = UserProfileForm(instance=request.user)
        extended_form = ExtendedProfileForm(instance=profile)
    context = {
        "form": form,
        "extended_form": extended_form
    }
    return render(request, "account/profile.html", context)

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("my_dashboard")
    else:
        form = PostForm()
    return render(request, "account/create_post.html", {"form": form})

@login_required
def dashboard(request, username=None):
    # ✅ ถ้าไม่มี username (เช่นเข้าผ่าน /users/dashboard/)
    if not username:
        username = request.user.username

    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=profile_user, is_archived=False).order_by('-created_at')

    followers_count = profile_user.followers.count()
    following_count = profile_user.following.count()
    form = None

    if profile_user == request.user:
        if request.method == "POST":
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.user = request.user
                new_post.save()
                return redirect("dashboard")
        else:
            form = PostForm()

    for post in posts:
        post.is_liked = post.likes.filter(user=request.user).exists()

    return render(request, "account/dashboard.html", {
        "profile_user": profile_user,
        "posts": posts,
        "form": form,
        "followers_count": followers_count,
        "following_count": following_count,
    })


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, "Your comment was added!")
    
    return redirect(request.META.get('HTTP_REFERER', '/'))
    
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "account/post_detail.html", {"post": post})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, user=request.user)  # ลบได้เฉพาะของตัวเอง
    post.delete()
    messages.success(request, "ลบโพสต์เรียบร้อยแล้ว")
    return redirect("my_dashboard")

@login_required
def post_archive(request, pk):
    post = get_object_or_404(Post, pk=pk, user=request.user)
    post.is_archived = True
    post.save()
    messages.info(request, "โพสต์ถูกจัดเก็บแล้ว")
    return  redirect("my_dashboard")

@login_required
def post_unarchive(request, pk):
    post = get_object_or_404(Post, pk=pk, user=request.user)
    post.is_archived = False
    post.save()
    messages.info(request, "ยกเลิกการเก็บโพสต์แล้ว")
    return redirect("archive_list")

@login_required
def archive_list(request):
    posts = Post.objects.filter(user=request.user, is_archived=True).order_by('-created_at')
    return render(request, "account/archive_list.html", {"posts": posts})


@login_required
@require_POST
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    like_obj = Like.objects.filter(post=post, user=user)
    if like_obj.exists():
        like_obj.delete()
        liked = False
    else:
        Like.objects.create(post=post, user=user)
        liked = True

    return JsonResponse({
        "liked": liked,
        "like_count": post.likes.count(),
    })

@login_required
def user_dashboard_from_search(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=profile_user, is_archived=False).order_by('-created_at')
    followers_count = profile_user.followers.count()
    following_count = profile_user.following.count()
    query = request.GET.get("q") or request.POST.get("q") or ""

    is_following = False
    if request.user.is_authenticated and request.user != profile_user:
        is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()

    # ✅ ใช้ path เต็มที่ตรงกับโฟลเดอร์จริง
    return render(request, "app_general/user_dashboard_from_search.html", {
        "profile_user": profile_user,
        "posts": posts,
        "followers_count": followers_count,
        "following_count": following_count,
        "is_following": is_following,
        "query": query,
    })


@require_POST
@login_required
def follow_toggle(request, username):
    target = get_object_or_404(User, username=username)

    if target == request.user:
        return JsonResponse({"error": "ไม่สามารถติดตามตัวเองได้"}, status=400)

    follow, created = Follow.objects.get_or_create(follower=request.user, following=target)

    if not created:
        # ถ้ามีอยู่แล้ว → เลิกติดตาม
        follow.delete()
        following = False
    else:
        following = True

    # ✅ ส่งข้อมูลใหม่กลับไป
    followers_count = Follow.objects.filter(following=target).count()
    following_count = Follow.objects.filter(follower=target).count()

    return JsonResponse({
        "is_following": following,
        "followers_count": followers_count,
        "following_count": following_count,
    })


@login_required
def follower_list(request, username):
    user = get_object_or_404(User, username=username)
    followers = []
    
    for follow_obj in user.followers.select_related('follower').all():
        follower_user = follow_obj.follower
        
        # *** FIX: กรอง User ที่ไม่มี username ออกไป ***
        if not follower_user.username:
            continue
            
        # FIX: คำนวณสถานะ is_following และส่งเป็น List of Dicts
        is_following_current_user = Follow.objects.filter(
            follower=request.user, 
            following=follower_user
        ).exists() if request.user.is_authenticated and request.user != follower_user else False
        
        followers.append({
            'user': follower_user,
            'is_following': is_following_current_user
        })
    
    return render(request, "account/follow_list.html", {
        "profile_user": user,
        "user_list": followers,
        "list_type": "ผู้ติดตาม"
    })

@login_required
def following_list(request, username):
    user = get_object_or_404(User, username=username)
    following = []

    for follow_obj in user.following.select_related('following').all():
        following_user = follow_obj.following
        
        # *** FIX: กรอง User ที่ไม่มี username ออกไป ***
        if not following_user.username:
            continue
            
        # FIX: คำนวณสถานะ is_following และส่งเป็น List of Dicts
        is_following_current_user = Follow.objects.filter(
            follower=request.user, 
            following=following_user
        ).exists() if request.user.is_authenticated and request.user != following_user else False
        
        following.append({
            'user': following_user,
            'is_following': is_following_current_user
        })

    return render(request, "account/follow_list.html", {
        "profile_user": user,
        "user_list": following,
        "list_type": "กำลังติดตาม"
    })
    
@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk, user=request.user)  # ✅ เจ้าของเท่านั้น

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "แก้ไขโพสต์เรียบร้อยแล้ว ✅")
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, "account/edit_post.html", {"form": form, "post": post})

