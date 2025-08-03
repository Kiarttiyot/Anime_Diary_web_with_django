from django.db import models

# Create your models here.

class myanime(models.Model):
    title = models.CharField(max_length=60)
    story = models.TextField(null=True,blank=True)
    score = models.IntegerField()
    status = models.BooleanField(null=True)
    Date_post = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '{} (id={})'.format(self.title,self.id)
    

    
    