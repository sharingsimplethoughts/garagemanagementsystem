from django.urls import path

from .views import *

app_name='ap_cm_api'

urlpatterns=[
    path('delete/<str:pk>',APCMDeleteView.as_view(),name='cmdelete'),
    path('getcat/',APCMCategoryListView.as_view(),name='cmgetcat'),
    path('delete_car_model/<str:pk>',APCMDeleteCarModelView.as_view(),name='cmdeletecarmodel'),
]
