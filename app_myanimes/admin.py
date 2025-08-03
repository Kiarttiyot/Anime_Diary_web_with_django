from django.contrib import admin
from app_myanimes.models import myanime
# Register your models here.

class myanimeAdmin(admin.ModelAdmin):
    list_display = ['title','story','score','status','Date_post']
    search_fields = ['title']
    list_filter = ['status']
admin.site.register(myanime,myanimeAdmin)