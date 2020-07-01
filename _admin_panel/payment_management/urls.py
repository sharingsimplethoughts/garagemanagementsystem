from django.urls import path

from .views import *

app_name='ap_payment_mgmt'

urlpatterns=[
    path('list/',PaymentListView.as_view(),name='appm_list'),
    path('list/dt/',PaymentDateWiseListView.as_view(),name='appm_date_wise_list'),
    # path('export_csv/',TableView.as_view(),name='appm_export_csv'),
    # path('export_csv/',exportToCSV,name='appm_export_csv'),
]
