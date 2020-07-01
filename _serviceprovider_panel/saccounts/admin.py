from django.contrib import admin


from .models import *
# Register your models here.
admin.site.register(ServiceType)
admin.site.register(ServiceSubType)
admin.site.register(Garage)
admin.site.register(WeeklySchedule)
admin.site.register(UserReview)
admin.site.register(CategoryManager)
admin.site.register(SubCategoryManager)
admin.site.register(CustomerComplaint)
admin.site.register(TempGarageImage)
admin.site.register(VehicleModle)
admin.site.register(VehicleModleManager)
