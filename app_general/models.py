from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Subscription(models.Model):
    STATUS = [
        ('unapproved', 'Unapproved'),
        ('Approved', 'Approved'),
        ('banned', 'Banned')
    ]
    name = models.CharField(max_length=60)
    email = models.EmailField(max_length=60,unique=True)
    status = models.CharField(max_length=15, choices=STATUS, default='unapproved')
    registered = models.DateTimeField(auto_now_add=True)
    anime = models.ManyToManyField('app_myanimes.myanime')
