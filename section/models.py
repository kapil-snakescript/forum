from django.db import models
from django.utils import timezone
from registration.models import User
# Create your models here.

class Section(models.Model):
    topic = models.CharField(max_length=50)
    title = models.CharField(max_length=30,unique=True)
    description = models.TextField(max_length=2000)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="creater",null=True,blank=True)
    update_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="last_updater",null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_on = models.DateTimeField(auto_now=True,null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_on = timezone.localtime(timezone.now())
        self.updated_on = timezone.localtime(timezone.now())
        return super(Section, self).save(*args, **kwargs)


class NewPost(models.Model):

    creator = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.TextField(max_length=2000)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_on = timezone.localtime(timezone.now())
        self.updated_on = timezone.localtime(timezone.now())
        return super(NewPost, self).save(*args, **kwargs)