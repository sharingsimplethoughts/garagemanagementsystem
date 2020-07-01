from django.urls import path

from .views import *

app_name='spp_offer'

urlpatterns=[
    path('create/',CreateOfferView.as_view(),name='spp_creare'),
    path('offers/',GarageWiseOfferListView.as_view(),name='spp_offers'),
    path('active_offers/',ActiveOfferListView.as_view(),name='spp_active_offers'),
    path('offers/<int:pk>',OfferDetailView.as_view(),name='spp_offer_detail'),
    path('update/<int:pk>',OfferUpdateView.as_view(),name='spp_offer_update'),
    path('delete/<int:pk>',OfferDeleteView.as_view(),name='spp_offer_delete'),
    path('sub_plan_list/',SubPlanListView.as_view(),name='spp_sub_plan_list'),
    path('sub_plan_list/<int:pk>',SubPlanDetailSerializer.as_view(),name='spp_sub_plan_detail'),

    path('sub_plan_list/<int:pk>/subscribe/',SubscribePlanView.as_view(),name='spp_subscribe'),
    path('update_telr_ref/',UpdateTelrDetailView.as_view(),name='spp_up_telr_ref'),

    path('coupon_code/',CouponCodeView.as_view(),name='spp_coupon_code'),
    path('top_offer_images/',TopTenOfferImageView.as_view(),name='spp_top_offer_images'),

    path('subscribed_plan_detail/',SPSubscribedPlanDetail.as_view(),name='spp_subs_plan_detail'),
]
