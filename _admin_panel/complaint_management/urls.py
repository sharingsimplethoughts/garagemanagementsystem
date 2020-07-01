from django.urls import path

from .views import *

app_name='ap_comp_mgmt'

urlpatterns=[
    path('list/',ComplaintListView.as_view(),name='apcm_list'),
    path('list/dt/',ComplaintDateWiseListView.as_view(),name='apcm_date_wise_list'),
    path('edit/<int:pk>',ComplaintEditView.as_view(),name='apcm_edit'),
]
