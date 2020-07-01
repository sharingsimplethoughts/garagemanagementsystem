from django.urls import path

from .views import *

app_name='ap_report_mgmt'

urlpatterns=[
    path('report_list/',AllReportsView.as_view(),name='aprm_list'),
    # path('download_csv/<str:pk>/<str:selection>',DownloadCSVView.as_view(),name='aprm_download_csv'),
    path('download_csv/<str:pk>',DownloadCSVView.as_view(),name='aprm_download_csv'),
]
