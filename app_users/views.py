from django.shortcuts import render
from django.urls import reverse
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
            return redirect("dashboard", username=user_obj.username)
        except User.DoesNotExist:
            # ส่ง error message กลับไปหน้า home (หรือหน้าเดิม)
            return render(request, "appgenral/home.html", {"error": "User not found"})
    return redirect("home")  # ถ้าไม่ได้พิมพ์อะไรเลย

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
    if username:
        profile_user = get_object_or_404(User, username=username)
    else:
        profile_user = request.user

    # ดึงโพสต์ของ user
    posts = Post.objects.filter(user=profile_user, is_archived=False).order_by('-created_at')

    # 1. ดึงจำนวนผู้ติดตามและกำลังติดตาม
    followers_count = profile_user.followers.count()
    following_count = profile_user.following.count()
    form = None
    if profile_user == request.user:  # เฉพาะของตัวเอง
        if request.method == "POST":
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.user = request.user
                new_post.save()
                return redirect("dashboard")  # กลับมาหน้า dashboard ตัวเอง
        else:
            form = PostForm()
    for post in posts:
        post.is_liked = post.likes.filter(user=request.user).exists()

    return render(request, "account/dashboard.html", {
        "profile_user": profile_user,
        "posts": posts,
        "form": form,
        # 2. ส่งค่าจำนวนผู้ติดตาม/กำลังติดตามไปยัง Template
        'followers_count': followers_count,
        'following_count': following_count,
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
def toggle_like(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        user = request.user

        liked = False
        like_obj = Like.objects.filter(post=post, user=user)

        if like_obj.exists():
            like_obj.delete()
        else:
            Like.objects.create(post=post, user=user)
            liked = True

        return JsonResponse({
            "liked": liked,
            "like_count": post.likes.count()
        })
    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def follow_toggle(request, username):
    target_user = get_object_or_404(User, username=username)

    if request.method != "POST":
        # เปิดด้วย GET ก็พากลับไปหน้าโปรไฟล์ของเค้าแทน
        return redirect('dashboard', username=target_user.username)

    rel, created = Follow.objects.get_or_create(
        follower=request.user,
        following=target_user
    )
    if not created:
        rel.delete()
        action = 'unfollowed'
        messages.info(request, f"คุณเลิกติดตาม {username} แล้ว")
    else:
        action = 'followed'
        messages.success(request, f"คุณเริ่มติดตาม {username} แล้ว")

    # ถ้าเป็น AJAX ให้ตอบ JSON เพื่ออัปเดตปุ่ม/ตัวเลขบนหน้า
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'ok': True,
            'action': action,
            'followers_count': target_user.followers.count()
        })

    # ไม่ใช่ AJAX → กลับหน้าที่มาก่อน, ถ้าไม่มี referer ให้ตกไปหน้าโปรไฟล์ของ target
    return redirect(request.META.get('HTTP_REFERER') or
                    reverse('dashboard', kwargs={'username': target_user.username}))

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