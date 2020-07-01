from django.urls import path

from .views import *

app_name='ap_splan_mgmt'

urlpatterns=[
    path('list/',SubscriptionPlanListView.as_view(),name='apspm_list'),
    path('list/dt/',SubscriptionPlanDateWiseListView.as_view(),name='apspm_date_wise_list'),
    path('add/',AddNewSubscriptionView.as_view(),name='apspm_add'),
    path('edit/<int:pk>',EditSubscriptionView.as_view(),name='apspm_edit'),
]
