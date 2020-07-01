from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(RegisteredUser)
admin.site.register(FavoriteGarage)
admin.site.register(FavoriteOffer)
admin.site.register(AllNotifications)
