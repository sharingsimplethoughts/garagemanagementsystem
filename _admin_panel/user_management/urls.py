from django.urls import path
# from django.views.decorators.cache import cache_page

from .views import *

app_name='ap_user_mgmt'
# cache_page(60 * 15)(
urlpatterns=[
    path('user_list/',UserManagementListView.as_view(),name='apum_user_list'),
    path('user_list/<int:role>/',UserManagementTypeWiseListView.as_view(),name='apum_type_wise_user_list'),
    path('user_list/<int:role>/dt/',UserManagementDateWiseListView.as_view(),name='apum_date_wise_user_list'),
    path('user_list/detail/<int:pk>/<int:role>/',UserManagementServiceProviderDetailView.as_view(),name='apum_user_list'),
]
