from django.urls import path

from .views import *

app_name='ap_setm_api'

urlpatterns=[
    path('deleteoption/<int:pk>',DeleteOptionsView.as_view(),name='setm_delete'),
    path('displayoption/<str:pk>',DisplayOptionsView.as_view(),name='setm_display'),
]
