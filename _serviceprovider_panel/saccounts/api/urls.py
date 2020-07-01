from django.urls import path

from .views import *

app_name='spp_accounts'

urlpatterns=[
    path('profile/create/<int:pk>',ServiceProviderProfileCreateView.as_view(),name='sp_profile_create'),
    path('profile/update/',ServiceProviderProfileUpdateView.as_view(),name='sp_profile_update'),
    path('service_type/<int:uid>',ServiceTypeListView.as_view(),name='sp_service_type'),
    path('service_subtype/<int:pk>/<int:uid>',ServiceSubTypeListView.as_view(),name='sp_service_subtype'),
    path('vehicle_model_list/<int:uid>',VehicleModelListView.as_view(),name='sp_vehicle_model'),
    path('garage/list/',ServiceProviderGarageListView.as_view(),name='sp_garage_list'),
    path('garage/review/<int:pk>',GarageReviewListView.as_view(),name='sp_garage_review'),
    path('subcatlist/',SubCatListBasedOnCat.as_view(),name='sp_subcatlist'),
    path('upload_image/<int:pk>',UploadImageView.as_view(),name='sp_upload_image'),
]
