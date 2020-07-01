from django.urls import path

from .views import *

app_name='ap_notm_api'

urlpatterns=[
    # path('settings_list/',SettingsManagementListView.as_view(),name='apsetm_set_list'),
    # # path('view/<str:id>',SettingsManagementDisplayView.as_view(),name='apsetm_display'),
    # path('edit/<str:id>',SettingsManagementEditView.as_view(),name='apsetm_edit'),
    # path('add/',SettingsManagementAddView.as_view(),name='apsetm_add'),

]
