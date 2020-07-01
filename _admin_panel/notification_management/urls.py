from django.urls import path

from .views import *

app_name='ap_not_mgmt'

urlpatterns=[
    path('send_notification/',NotificationManagementCreateView.as_view(),name='apnotm_new_notification'),
    # path('add_user/',NotificationManagementUserListView.as_view(),name='apnotm_add_user_list'),
    path('send_notification/<int:role>/',NotificationManagementUserTypeWiseListView.as_view(),name='apnotm_add_user_list_type_wise'),
    path('send_notification/<int:role>/dt/',NotificationManagementUserDateWiseListView.as_view(),name='apnotm_add_user_list_date_wise'),
    # # path('view/<str:id>',SettingsManagementDisplayView.as_view(),name='apsetm_display'),
    # path('edit/<str:id>',SettingsManagementEditView.as_view(),name='apsetm_edit'),
    # path('add/',SettingsManagementAddView.as_view(),name='apsetm_add'),

]
