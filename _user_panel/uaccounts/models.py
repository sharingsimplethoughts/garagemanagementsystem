from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache


# Create your models here.
gender_choices=(('1','Male'),('2','Female'))
login_type_choices=(('1','Normal'),('2','Facebook'),('3','Google'))
device_type_choices=(('1','Android'),('2','Ios'),('3','Web'))
user_type_choices=(('1','User'),('2','Service Provider'))
language_choices=(('1','English'),('2','Arabic'))


class RegisteredUser(models.Model):
    language_pref=models.CharField(max_length=10,choices=language_choices,default='English')
    first_name=models.CharField(max_length=70)
    last_name=models.CharField(max_length=70,blank=True,null=True)
    about=models.CharField(max_length=200,blank=True,null=True)

    profile_image=models.ImageField(upload_to='user/profile/profile',blank=True,null=True)
    background_image=models.ImageField(upload_to='user/profile/background',blank=True,null=True)

    country_code=models.CharField(max_length=5,blank=True,null=True)
    mobile=models.CharField(max_length=200)
    is_mobile_verified=models.BooleanField(default=False)

    email=models.CharField(max_length=200)
    is_email_verified=models.BooleanField(default=False)

    gender=models.CharField(max_length=15, choices=gender_choices,blank=True,null=True)
    
    lat=models.CharField(max_length=50,blank=True,null=True)
    lon=models.CharField(max_length=50,blank=True,null=True)
    zipcode=models.CharField(max_length=50,blank=True,null=True)
    street=models.CharField(max_length=200,blank=True,null=True)
    area=models.CharField(max_length=100,blank=True,null=True)
    city=models.CharField(max_length=50,blank=True,null=True)
    country=models.CharField(max_length=50,blank=True,null=True)

    login_type=models.CharField(max_length=10,choices=login_type_choices)
    social_id=models.CharField(max_length=200,blank=True,null=True)

    device_type=models.CharField(max_length=10,choices=device_type_choices)
    device_token=models.CharField(max_length=200,blank=True,null=True)

    created_on=models.DateTimeField(auto_now_add=True)
    is_approved=models.BooleanField(default=False)

    user_type=models.CharField(max_length=20,choices=user_type_choices)
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='ruser')

    has_dual_account=models.BooleanField(default=False)

    is_deleted=models.BooleanField(default=False)

    #--------------------------------Arabic Fields------------------------------------
    ar_first_name=models.CharField(max_length=100, default='')
    ar_last_name=models.CharField(max_length=100,default='',blank=True,null=True)
    ar_about=models.CharField(max_length=300,default='',blank=True,null=True)
    ar_mobile=models.CharField(max_length=200,default='',)
    ar_country_code=models.CharField(max_length=5,default='',blank=True,null=True)
    ar_zipcode=models.CharField(max_length=50,default='',blank=True,null=True)
    ar_street=models.CharField(max_length=200,default='',blank=True,null=True)
    ar_area=models.CharField(max_length=100,default='',blank=True,null=True)
    ar_city=models.CharField(max_length=50,default='',blank=True,null=True)
    ar_country=models.CharField(max_length=50,default='',blank=True,null=True)
    #--------------------------------------------------------------------------------

    def __str__(self):
        return self.first_name+'-'+self.mobile

    def save(self,*args,**kwargs):
        um0=cache.get('um0')
        um1=cache.get('um1')
        um2=cache.get('um2')
        um3=cache.get('um3')
        cm1=cache.get('cm1')
        nm1=cache.get('nm1')
        if um0:
            cache.delete('um0')
        if um1:
            cache.delete('um1')
        if um2:
            cache.delete('um2')
        if um3:
            cache.delete('um3')
        if cm1:
            cache.delete('cm1')
        if nm1:
            cache.delete('nm1')
        super(RegisteredUser,self).save(*args,**kwargs)

    def delete(self,*args,**kwargs):
        um0=cache.get('um0')
        um1=cache.get('um1')
        um2=cache.get('um2')
        um3=cache.get('um3')
        cm1=cache.get('cm1')
        nm1=cache.get('nm1')
        if um0:
            cache.delete('um0')
        if um1:
            cache.delete('um1')
        if um2:
            cache.delete('um2')
        if um3:
            cache.delete('um3')
        if cm1:
            cache.delete('cm1')
        if nm1:
            cache.delete('nm1')
        super(RegisteredUser,self).delete(*args,**kwargs)

class TemporaryOTP(models.Model):
    user=models.ForeignKey(RegisteredUser,on_delete=models.CASCADE,related_name='otpuser')
    otp=models.CharField(max_length=4)
    active=models.BooleanField(default=False)

    def __str__(self):
        return self.otp

from _serviceprovider_panel.saccounts.models import Garage

class FavoriteGarage(models.Model):
    user=models.ForeignKey(RegisteredUser,on_delete=models.CASCADE,related_name='fuser')
    garage=models.ForeignKey(Garage,on_delete=models.CASCADE,related_name='fgarage')

    def __str__(self):
        return self.user.first_name

from _serviceprovider_panel.offer.models import Offer
class FavoriteOffer(models.Model):
    user=models.ForeignKey(RegisteredUser,on_delete=models.CASCADE,related_name='fuser_offer')
    offer=models.ForeignKey(Offer,on_delete=models.CASCADE,related_name='foffer')

    def __str__(self):
        return self.user.first_name

class AllNotifications(models.Model):
    heading = models.CharField(max_length=100, default='')
    text = models.CharField(max_length=500,default='')
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text