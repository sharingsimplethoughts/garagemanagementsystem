from django.urls import path

from .views import *

app_name='ap_com_api'

urlpatterns=[
    path('delete/<int:pk>',APCMDeleteView.as_view(),name='cmdelete'),
]
