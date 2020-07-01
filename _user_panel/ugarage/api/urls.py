from django.urls import path

from .views import *

app_name="up_garage"

urlpatterns=[
    path('category/',ServiceTypeListView.as_view(),name='up_category'),
    path('category/<int:pk>',ServiceSubTypeListView.as_view(),name='up_subcategory'),
    path('category/subcategory/<int:pk>',GarageListView.as_view(),name='up_garage'),
    path('category/subcategory/garage/<int:pk>',GarageDetailView.as_view(),name='up_garage_detail'),
    path('category/subcategory/garage/offer/<int:pk>',GarageOfferDetailView.as_view(),name='up_offer_detail'),
    path('category/subcategory/garage_review/<int:pk>',UserReviewView.as_view(),name='up_review'),
]
