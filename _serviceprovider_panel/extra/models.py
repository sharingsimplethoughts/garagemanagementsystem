from django.db import models
from datetime import datetime
from django.utils.timezone import now

from _user_panel.uaccounts.models import RegisteredUser
# Create your models here.
class AboutUs(models.Model):
    title=models.CharField(max_length=100,default='')
    title_ar=models.CharField(max_length=200,default='')
    content=models.TextField()
    content_ar=models.TextField(default='')
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'About Us-'+str(self.id)

class TermsAndCondition(models.Model):
    title=models.CharField(max_length=100,default='')
    title_ar=models.CharField(max_length=100,default='')
    content=models.TextField()
    content_ar=models.TextField(default='')
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Terms and Condition-'+str(self.id)

class Help(models.Model):
    title=models.CharField(max_length=100,default='')
    title_ar=models.CharField(max_length=100,default='')
    content=models.TextField()
    content_ar=models.TextField(default='')
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Help-'+str(self.id)

class Legal(models.Model):
    title=models.CharField(max_length=100,default='')
    title_ar=models.CharField(max_length=100,default='')
    content=models.TextField()
    content_ar=models.TextField(default='')
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Legal-'+str(self.id)

class PrivacyPolicy(models.Model):
    title=models.CharField(max_length=100,default='')
    title_ar=models.CharField(max_length=100,default='')
    content=models.TextField()
    content_ar=models.TextField(default='')
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'PrivacyPolicy-'+str(self.id)

class Faq(models.Model):
    title=models.CharField(max_length=500)
    title_ar=models.CharField(max_length=500,default='')
    content=models.TextField()
    content_ar=models.TextField(default='')
    created_on=models.DateTimeField(default=datetime.now)

    def __str__(self):
        return 'Faq-'+str(self.title)

class Notification(models.Model):
    title=models.CharField(max_length=300,)
    title_ar=models.CharField(max_length=300,default='')
    description=models.TextField()
    description_ar=models.TextField(default='')
    user=models.ManyToManyField(RegisteredUser, related_name='runot', through='UserNotification')
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class UserNotification(models.Model):
    notification=models.ForeignKey(Notification,on_delete=models.CASCADE,related_name='unot')
    user=models.ForeignKey(RegisteredUser,on_delete=models.CASCADE,related_name='unuser')
    class Meta:
        unique_together=('notification','user')

    def __str__(self):
        return str(self.id)

class NewOptions(models.Model):
    title=models.CharField(max_length=50,blank=True)
    title_ar=models.CharField(max_length=50,blank=True,default='')
    content=models.TextField()
    content_ar=models.TextField(default='')
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

class MaintainCacheFlag(models.Model):
    model_name=models.CharField(max_length=100,unique=True,null=True,blank=True)
    is_changed=models.BooleanField(default=False)

    def __str__(self):
        return self.model_name+str(self.is_changed)
