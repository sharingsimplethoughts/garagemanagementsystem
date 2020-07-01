from django.urls import path

from .views import *

app_name='ap_cat_mgmt'

urlpatterns=[
    path('category_list/',CategoryManagementListView.as_view(),name='apcm_cat_list'),
    path('category_list/dt/',CategoryManagementDateWiseListView.as_view(),name='apcm_date_wise_cat_list'),
    path('add_category/',CategoryManagementAddCategoryView.as_view(),name='apcm_add_category'),
    path('add_sub_category/',CategoryManagementAddSubCategoryView.as_view(),name='apcm_add_sub_category'),
    path('add_car_model/',CategoryManagementAddCarModelView.as_view(),name='apcm_add_car_model'),
    path('edit_category/<int:id>',CategoryManagementEditCategoryView.as_view(),name='apcm_edit_category'),
    path('edit_sub_category/<int:id>',CategoryManagementEditSubCategoryView.as_view(),name='apcm_edit_sub_category'),
]
