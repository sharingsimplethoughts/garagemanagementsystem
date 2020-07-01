from django.urls import path

from .views import *

app_name='up_search'

urlpatterns=[
    path('list/',HomeSearchView.as_view(),name='up_search'),
    path('list/<int:pk>/',HomeSpecificSearchView.as_view(),name='up_specific_search'),
    path('popular/garage/search/',PopularGarageListCumSearchView.as_view(),name='up_popular_garage_list_cum_search'),
    path('popular/garage/',PopularGarageSearchView.as_view(),name='up_popular_garage'),
    path('popular/category/',PopularCategorySearchView.as_view(),name='up_popular_category'),
    path('offer/',OfferSearchView.as_view(),name='up_popular_offer'),
    path('sp_offer/',ServiceProviderOfferSearchView.as_view(),name='up_search_sp_offer'),
]
