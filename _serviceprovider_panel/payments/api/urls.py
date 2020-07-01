from django.urls import path

from .views import *

app_name='spp_payments'

urlpatterns=[
    path('success/<int:pk>/<int:rid>',PaymentSuccessView.as_view(),name='spp_pay_success'),
    path('decline/<int:pk>/<int:rid>',PaymentDeclineView.as_view(),name='spp_pay_decline'),
    path('cancel/<int:pk>/<int:rid>',PaymentCancelView.as_view(),name='spp_pay_cancel'),
]
