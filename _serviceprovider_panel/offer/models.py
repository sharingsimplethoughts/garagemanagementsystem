from django.db import models
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
# Create your models here.
from _serviceprovider_panel.saccounts.models import *

class Offer(models.Model):
    garage=models.ForeignKey(Garage,on_delete=models.CASCADE,related_name='ogarage')
    image1=models.ImageField(upload_to='serviceprovider/offer/image',blank=True,null=True)
    image2=models.ImageField(upload_to='serviceprovider/offer/image',blank=True,null=True)
    image3=models.ImageField(upload_to='serviceprovider/offer/image',blank=True,null=True)
    image4=models.ImageField(upload_to='serviceprovider/offer/image',blank=True,null=True)
    video1=models.FileField(upload_to='serviceprovider/offer/video',blank=True,null=True)
    video1_thumbnail=models.ImageField(upload_to='serviceprovider/offer/video/thumbnail',blank=True,null=True,default='')
    video2=models.FileField(upload_to='serviceprovider/offer/video',blank=True,null=True)
    video2_thumbnail=models.ImageField(upload_to='serviceprovider/offer/video/thumbnail',blank=True,null=True,default='')
    title=models.CharField(max_length=100,)
    description=models.TextField()
    coupon=models.CharField(max_length=10,)
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()
    advertisment_license_number=models.CharField(max_length=100, blank=True,default='')
    expiry_date=models.DateTimeField(default=datetime.now)
    # is_active=models.BooleanField(default=True)
#---------------------------------Arabic Field--------------------------------------------
    ar_title=models.CharField(max_length=100,default='')
    ar_description=models.TextField(default='')
    ar_coupon=models.CharField(max_length=10,default='')
    ar_advertisment_license_number=models.CharField(max_length=100, blank=True,default='')
#------------------------------------------------------------------------------------------
    def is_active(self):
        if end_date>datetime.now():
            return False
        return True

    def __str__(self):
        return self.title

class SubscriptionPlan(models.Model):
    plan_name=models.CharField(max_length=100,)
    plan_desc=models.CharField(max_length=800,) #FOR ADDING THIS FIELD NEEDS TO CHANGE AND LINK TO SubscriptionPlanKeyFeatures
    price=models.DecimalField(max_digits=10,decimal_places=2,default='0.00',)
    # price_ar=models.CharField(max_length=10,default='')
    # validity_from=models.DateField(auto_now_add=False,)
    # validity_to=models.DateField(auto_now_add=False,)
    valid_for=models.PositiveIntegerField(default=0)
    # valid_for_ar=models.CharField(max_length=10,default='')
    created_on=models.DateTimeField(auto_now_add=True,)

#------------------------Arabic Field-------------------------------------
    plan_name_ar=models.CharField(max_length=200,default='')
    plan_desc_ar=models.CharField(max_length=1000,default='')
    ar_price=models.DecimalField(max_digits=10,decimal_places=2,default='0.00',)
    ar_valid_for=models.PositiveIntegerField(default=0)
#-------------------------------------------------------------------------

    def __str__(self):
        return self.plan_name

class SubscriptionPlanKeyFeatures(models.Model):
    plan=models.ForeignKey(SubscriptionPlan,on_delete=models.CASCADE,name='spkf_plan')
    key_feature=models.CharField(max_length=200)
#------------------------------Arabic Field-----------------------------------
    key_feature_ar=models.CharField(max_length=400,default='')
#-----------------------------------------------------------------------------
    def __str__(self):
        return self.plan.plan_name

class UserSubscription(models.Model):
    plan=models.ForeignKey(SubscriptionPlan,on_delete=models.CASCADE,related_name='us_plan')
    ruser=models.ForeignKey(RegisteredUser,on_delete=models.CASCADE,related_name='us_ruser')
    created_on=models.DateTimeField(auto_now_add=True,)
    expires_on=models.DateTimeField()

    def __str__(self):
        return self.plan.plan_name+'-'+self.ruser.first_name

    def save(self,*args,**kwargs):
        # self.expires_on=datetime.now()+timedelta(days=self.plan.valid_for*30)
        self.expires_on=datetime.now()+relativedelta(months=self.plan.valid_for)
        super(UserSubscription, self).save(*args, **kwargs)
