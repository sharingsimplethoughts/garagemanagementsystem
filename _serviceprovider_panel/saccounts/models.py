from django.db import models
from django.utils.text import slugify
# import pytz
# from datetime import datetime
from django.utils import timezone
from datetime import datetime
from django.core.cache import cache

from _user_panel.uaccounts.models import RegisteredUser

# Create your models here.
days_choices=(('1','sat'),('2','sun'),('3','mon'),('4','tue'),('5','wed'),('6','thur'),('7','fri'))
complaint_choices=(('Open','1'),('Closed','2'),('Processing','3'))

# default=timezone.now
def slugify(str):
    str = str.replace(" ", "-")
    str = str.replace(",", "-")
    str = str.replace("(", "-")
    str = str.replace(")", "")
    str = str.replace("؟", "")
    return str

class ServiceType(models.Model):
    type=models.CharField(max_length=100)
    icon=models.ImageField(upload_to='serviceprovider/service_type',blank=True,null=True,default='serviceprovider/service_type/def_cat.png')
    slug = models.SlugField(max_length=100,default='')
    created_on = models.DateTimeField(auto_now_add=True)
    # created_on = models.DateTimeField(default=timezone.now)
    category_rating = models.PositiveIntegerField(default=0)
    #-----------------Arabic Field------------------------------------
    type_ar=models.CharField(max_length=200, default='')
    slug_ar = models.SlugField(max_length=200,default='')
    #-----------------------------------------------------------------
    def __str__(self):
        return self.type

    def save(self, *args, **kwargs):
        self.slug = slugify(self.type)
        self.slug_ar = slugify(self.type_ar)
        super(ServiceType, self).save(*args, **kwargs)

class ServiceSubType(models.Model):
    subtype=models.CharField(max_length=100,)
    type=models.ForeignKey(ServiceType,on_delete=models.CASCADE)
    icon=models.ImageField(upload_to='serviceprovider/service_subtype',blank=True,null=True,default='serviceprovider/service_subtype/def_subcat.png')
    slug = models.SlugField(max_length=100,default='')
    created_on = models.DateTimeField(auto_now_add=True)
    subcategory_rating = models.PositiveIntegerField(default=0)
    # created_on = models.DateTimeField(default=timezone.now)
    #-----------------Arabic Field------------------------------------
    subtype_ar=models.CharField(max_length=200, default='')
    slug_ar = models.SlugField(max_length=200,default='')
    #-----------------------------------------------------------------
    def __str__(self):
        return self.subtype

    def save(self, *args, **kwargs):
        self.slug = slugify(self.subtype)
        self.slug_ar = slugify(self.subtype_ar)
        super(ServiceSubType, self).save(*args, **kwargs)

class VehicleModle(models.Model):
    model_name=models.CharField(max_length=100)
    icon=models.ImageField(upload_to='serviceprovider/service_type',blank=True,null=True)
    slug=models.SlugField(max_length=100,unique=True,default='')
    created_on = models.DateTimeField(auto_now_add=True)
    # created_on = models.DateTimeField(default=timezone.now)
    model_rating = models.PositiveIntegerField(default=0)
#-----------------Arabic Field------------------------------------
    model_name_ar=models.CharField(max_length=200,default='')
    slug_ar=models.SlugField(max_length=100,default='')
#------------------------------------------------------------------
    def __str__(self):
        return self.model_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.model_name)
        self.slug_ar = slugify(self.model_name_ar)
        super(VehicleModle, self).save(*args, **kwargs)

class Garage(models.Model):
    name=models.CharField(max_length=100,)
    store_image1=models.ImageField(upload_to='serviceprovider/garage', blank=True,null=True)
    store_image2=models.ImageField(upload_to='serviceprovider/garage', blank=True,null=True)
    store_image3=models.ImageField(upload_to='serviceprovider/garage', blank=True,null=True)
    contact_person=models.CharField(max_length=70)

    lat=models.CharField(max_length=20,)
    lon=models.CharField(max_length=20,)
    location=models.CharField(max_length=500,)
    state=models.CharField(max_length=20,)
    city=models.CharField(max_length=20,)
    country=models.CharField(max_length=20,)
    country_code=models.CharField(max_length=10)
    contact_num=models.CharField(max_length=15,)

    tax_registration_num=models.CharField(max_length=50,blank=True,null=True)
    tax_registration_date=models.DateTimeField(blank=True,null=True)

    created_on=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)

    is_owner=models.BooleanField(default=True)
    user=models.ForeignKey(RegisteredUser,on_delete=models.CASCADE,related_name='guser')
    service_type=models.ManyToManyField(ServiceType,related_name='gst', through='CategoryManager')
    service_subtype=models.ManyToManyField(ServiceSubType,related_name='gsst', through='SubCategoryManager')
    vehicle_model=models.ManyToManyField(VehicleModle,related_name='gvm', through='VehicleModleManager')
    garage_rating=models.PositiveIntegerField(default=0,)

    slug1 = models.SlugField(max_length=100,default='')
    slug2 = models.SlugField(max_length=500,default='')

#-------------------Arabic Field------------------------------------------------
    ar_name=models.CharField(max_length=100,default='')
    ar_contact_person=models.CharField(max_length=70,default='')
    ar_location=models.CharField(max_length=500,default='')
    ar_state=models.CharField(max_length=20,default='')
    ar_city=models.CharField(max_length=20,default='')
    ar_country=models.CharField(max_length=20,default='')
    ar_country_code=models.CharField(max_length=10,default='')
    ar_contact_num=models.CharField(max_length=15,default='')
    ar_tax_registration_num=models.CharField(max_length=50,blank=True,null=True,default='')
    ar_garage_rating=models.PositiveIntegerField(default=0,)
    ar_slug1 = models.SlugField(max_length=100,default='')
    ar_slug2 = models.SlugField(max_length=500,default='')
#--------------------------------------------------------------------------------

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug1 = slugify(self.name)
        self.slug2 = slugify(self.location)
        self.ar_slug1 = slugify(self.ar_name)
        self.ar_slug2 = slugify(self.ar_location)
        super(Garage, self).save(*args, **kwargs)

class CategoryManager(models.Model):
    garage=models.ForeignKey(Garage,on_delete=models.CASCADE,related_name='cm_garage')
    category=models.ForeignKey(ServiceType,on_delete=models.CASCADE,related_name='cm_category')
    class Meta:
        unique_together=('garage','category')
    def __str__(self):
        return str(self.garage)+' '+str(self.category)

class SubCategoryManager(models.Model):
    garage=models.ForeignKey(Garage,on_delete=models.CASCADE,related_name='scm_garage')
    subcategory=models.ForeignKey(ServiceSubType,on_delete=models.CASCADE,related_name='scm_subcategory')
    class Meta:
        unique_together=('garage','subcategory')
    def __str__(self):
        return str(self.garage)+' '+str(self.subcategory)

class VehicleModleManager(models.Model):
    garage=models.ForeignKey(Garage,on_delete=models.CASCADE,related_name='vmm_garage')
    vehicle_model=models.ForeignKey(VehicleModle,on_delete=models.CASCADE,related_name='vmm_model')
    class Meta:
        unique_together=('garage','vehicle_model')
    def __str__(self):
        return str(self.garage)+' '+str(self.vehicle_model)

class WeeklySchedule(models.Model):
    garage=models.ForeignKey(Garage,on_delete=models.CASCADE,related_name='wsgarage')
    day=models.CharField(max_length=10,choices=days_choices)
    start_time=models.CharField(max_length=10)
    end_time=models.CharField(max_length=10)
#------------------Arabic Field----------------------------------------------
    ar_day=models.CharField(max_length=10,choices=days_choices,default='')
    ar_start_time=models.CharField(max_length=10,default='')
    ar_end_time=models.CharField(max_length=10,default='')
#----------------------------------------------------------------------------

    def __str__(self):
        return self.garage.name

class UserReview(models.Model):
    garage=models.ForeignKey(Garage,on_delete=models.CASCADE,related_name='rvgarage')
    user=models.ForeignKey(RegisteredUser,on_delete=models.CASCADE,related_name='rvuser')
    review=models.CharField(max_length=200,)
    rating=models.PositiveIntegerField(default=0)
    created_on=models.DateTimeField(auto_now_add=True)
#------------------Arabic Field--------------------------------------
    ar_review=models.CharField(max_length=200,default='')
    ar_rating=models.PositiveIntegerField(default=0)
#--------------------------------------------------------------------
    def __str__(self):
        return self.review

class CustomerComplaint(models.Model):
    user=models.ForeignKey(RegisteredUser,on_delete=models.CASCADE,related_name='csuser')
    name=models.CharField(max_length=50,)
    email=models.CharField(max_length=80,)
    complaint=models.CharField(max_length=1000,)
    admin_message=models.CharField(max_length=1000,default='')
    admin_message_ar=models.CharField(max_length=1000,default='')
    created_on=models.DateTimeField(auto_now_add=True,)
    status=models.CharField(max_length=10,choices=complaint_choices,default='Open')
#----------------------Arabic Field----------------------------------------
    ar_name=models.CharField(max_length=50,default='')
    ar_email=models.CharField(max_length=80,default='')
    ar_complaint=models.CharField(max_length=1000,default='')
    ar_admin_message=models.CharField(max_length=1000,default='')
    admin_message_ar=models.CharField(max_length=1000,default='')
#----------------------------------------------------------------------------
    def __str__(self):
        return self.user.first_name
    def save(self, *args, **kwargs):
        cm1=cache.get('cm1')
        if cm1:
            cache.delete('cm1')
        super(CustomerComplaint,self).save(*args,**kwargs)
    def delete(self, *args, **kwargs):
        cm1=cache.get('cm1')
        if cm1:
            cache.delete('cm1')
        super(CustomerComplaint,self).delete(*args,**kwargs)

class TempGarageImage(models.Model):
    user=models.ForeignKey(RegisteredUser,on_delete=models.CASCADE,related_name='tgi_user')
    image=models.ImageField(upload_to='serviceprovider/temp', blank=True)
    def __str__(self):
        return self.user.first_name
