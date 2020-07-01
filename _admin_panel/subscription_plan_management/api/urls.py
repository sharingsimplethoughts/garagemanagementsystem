from django.urls import path

from .views import *

app_name='ap_splanm_api'

urlpatterns=[
    path('delete/<int:pk>',APSPMDeleteView.as_view(),name='spmdelete'),
]
