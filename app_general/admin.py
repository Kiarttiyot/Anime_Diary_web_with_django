from django.contrib import admin
from app_general.models import Subscription
# Register your models here.


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['name','email','status','registered']
    search_fields = ['name','email']
    list_filter = ['status']
    def __str__(self):
        return '{} (id={})'.format(self.title,self.id)
admin.site.register(Subscription,SubscriptionAdmin)
