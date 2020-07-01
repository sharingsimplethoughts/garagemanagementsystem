from django.urls import path

from .views import *

app_name='ap_report_api'

urlpatterns=[
    path('display/<str:pk>/<str:selection>',DisplayView.as_view(),name='aprm_display'),
]
