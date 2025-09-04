from django.db import models
from django.contrib.auth.models import User



class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(blank=True)  # ข้อความ optional
    image = models.ImageField(upload_to="post_images/", blank=True, null=True)  # รูป optional
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:30]}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default="", blank=True)
    address = models.TextField(default="", blank=True)
    phone = models.CharField(max_length=15, default="", blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', default='default.png')
    favorite_genres = models.CharField(max_length=255, default="", blank=True)  # แนวอนิเมะที่ชอบ

    def __str__(self):
        return self.user.username