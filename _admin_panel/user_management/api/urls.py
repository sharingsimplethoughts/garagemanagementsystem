from django.urls import path

from .views import *

app_name='ap_um_api'

urlpatterns=[
    path('block/<int:pk>',APUMBlockView.as_view(),name='umblock'),
    path('unblock/<int:pk>',APUMUnblockView.as_view(),name='umunblock'),
    path('delete/<int:pk>',APUMDeleteView.as_view(),name='umdelete'),
    path('approve/<int:pk>',APUMApproveView.as_view(),name='umapprove'),
]
