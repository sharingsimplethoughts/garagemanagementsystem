from django.db import models

from _user_panel.uaccounts.models import *
from _serviceprovider_panel.offer.models import *
from django.core.cache import cache
# Create your models here.

payment_status_choices=(('Completed','1'),('Declined','2'),('Cancelled','3'),('Pending','4'))
payment_mode=(('Credit Card','1'),('Debit Card','2'),('Netbanking','3'),('Paypal','4'),('Terl','5'))

class PaymentDetail(models.Model):
    serv_provider=models.ForeignKey(RegisteredUser,on_delete=models.SET_NULL,related_name='sp_pay',null=True)
    date_of_purchase=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=10,choices=payment_status_choices)
    price=models.DecimalField(max_digits=10,decimal_places=2,default='0.00',)
    subscription_plan=models.ForeignKey(SubscriptionPlan,on_delete=models.SET_NULL,related_name='splan_pay',null=True)
    payment_mode=models.CharField(max_length=10,choices=payment_mode)
    is_deleted=models.BooleanField(default=False)
#---------------------------------Arabic Field------------------------------------
    ar_status=models.CharField(max_length=10,choices=payment_status_choices,default='')
    ar_price=models.DecimalField(max_digits=10,decimal_places=2,default='0.00')
#---------------------------------------------------------------------------------
    def __str__(self):
        return self.serv_provider.first_name+'-'+self.status+'-'+self.subscription_plan.plan_name
    def save(self,*args,**kwargs):
        pm1=cache.get('pm1')
        if pm1:
            cache.delete('pm1')
        super(PaymentDetail,self).save(*args,**kwargs)
    def delete(self,*args,**kwargs):
        pm1=cache.get('pm1')
        if pm1:
            cache.delete('pm1')
        super(PaymentDetail,self).delete(*args,**kwargs)

class TelrDetail(models.Model):
    ivp_method=models.CharField(max_length=10,blank=True)
    ivp_store=models.PositiveIntegerField()
    ivp_authkey=models.CharField(max_length=50,blank=True)
    ivp_cart=models.CharField(max_length=20,blank=True)
    ivp_test=models.PositiveIntegerField()
    ivp_amount=models.DecimalField(max_digits=10,decimal_places=2,default='0.00',)
    ivp_currency=models.CharField(max_length=5,blank=True)
    ivp_desc=models.CharField(max_length=100,blank=True)
    return_auth=models.CharField(max_length=300,blank=True)
    return_can=models.CharField(max_length=300,blank=True)
    return_decl=models.CharField(max_length=300,blank=True)
    ivp_trantype=models.CharField(max_length=10,blank=True)
    bill_custref=models.PositiveIntegerField()
    status=models.CharField(max_length=20,blank=True,default='get api got hit')
    telr_ref=models.CharField(max_length=300,blank=True)
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.bill_custref)
