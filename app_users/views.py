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
from .models import Post, Like

@login_required
def dashboard(request: HttpRequest):
    return render(request,"account/dashboard.html")

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
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=profile_user, is_archived=False).order_by('-created_at') 
    return render(request, "account/dashboard.html", {"user_profile": profile_user,"posts": posts})

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

    form = None
    if profile_user == request.user:  # เฉพาะของตัวเอง
        if request.method == "POST":
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.user = request.user
                new_post.save()
                return redirect("my_dashboard")  # กลับมาหน้า dashboard ตัวเอง
        else:
            form = PostForm()
    for post in posts:
        post.is_liked = post.likes.filter(user=request.user).exists()

    return render(request, "account/dashboard.html", {
        "profile_user": profile_user,
        "posts": posts,
        "form": form,
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
            

    return redirect('post_detail', pk=post.pk)
    
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
