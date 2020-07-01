"""Garage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url,include
from django.conf import settings
from django.conf.urls.static import static
from _user_panel.uaccounts.views import activate
# from django.conf.urls.i18n import i18n_patterns
# from django.utils.translation import ugettext_lazy as _

urlpatterns = [
    # path('i18n/',include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    #Email varification
    url('^', include('django.contrib.auth.urls')),
    #User Panel
    path('user/',include('_user_panel.uaccounts.api.urls',namespace='up_accounts')),
    path('user/detail/',include('_user_panel.ugarage.api.urls',namespace='up_garage')),
    path('user/search/',include('_user_panel.search.api.urls',namespace='up_search')),

    #Email Activation
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',activate, name='activate'),
    #Service Provider Panel
    path('serviceprovider/',include('_serviceprovider_panel.saccounts.api.urls',namespace='spp_accounts')),
    path('serviceprovider/offer/',include('_serviceprovider_panel.offer.api.urls',namespace='spp_offer')),
    path('serviceprovider/extra/',include('_serviceprovider_panel.extra.api.urls',namespace='spp_extra')),
    path('serviceprovider/payments/',include('_serviceprovider_panel.payments.api.urls',namespace='spp_payments')),

    #Admin Panel
    path('garage_admin/',include('_admin_panel.aaccounts.urls', namespace='ap_accounts')),
    path('user_management/',include('_admin_panel.user_management.urls', namespace='ap_user_mgmt')),
    path('category_management/',include('_admin_panel.category_management.urls', namespace='ap_cat_mgmt')),
    path('settings_management/',include('_admin_panel.settings_management.urls', namespace='ap_set_mgmt')),
    path('notification_management/',include('_admin_panel.notification_management.urls', namespace='ap_not_mgmt')),
    path('subscription_plan_management/',include('_admin_panel.subscription_plan_management.urls', namespace='ap_splan_mgmt')),
    path('payment_management/',include('_admin_panel.payment_management.urls', namespace='ap_payment_mgmt')),
    path('complaint_management/',include('_admin_panel.complaint_management.urls', namespace='ap_comp_mgmt')),
    path('report_management/',include('_admin_panel.report_management.urls', namespace='ap_report_mgmt')),

    #Admin Panel Different APIs
    path('ap_um_api/', include('_admin_panel.user_management.api.urls', namespace='ap_um_api')),
    path('ap_cm_api/', include('_admin_panel.category_management.api.urls', namespace='ap_cm_api')),
    path('ap_setm_api/', include('_admin_panel.settings_management.api.urls', namespace='ap_setm_api')),
    path('ap_notm_api/', include('_admin_panel.notification_management.api.urls', namespace='ap_notm_api')),
    path('ap_splanm_api/', include('_admin_panel.subscription_plan_management.api.urls', namespace='ap_splanm_api')),
    path('ap_com_api/', include('_admin_panel.complaint_management.api.urls', namespace='ap_com_api')),
    path('ap_report_api/', include('_admin_panel.report_management.api.urls', namespace='ap_report_api')),
    # url(r'^silk', include('silk.urls', namespace='silk'))
    # url(r'^i18n/', include('django.conf.urls.i18n')),

]


# urlpatterns += i18n_patterns(
# urlpatterns += i18n_patterns('',
#     #Admin Panel
#     path(_('garage_admin/'),include('_admin_panel.aaccounts.urls')),
#     path(_('user_management/'),include('_admin_panel.user_management.urls')),
#     path(_('category_management/'),include('_admin_panel.category_management.urls')),
#     path(_('settings_management/'),include('_admin_panel.settings_management.urls')),
#     path(_('notification_management/'),include('_admin_panel.notification_management.urls')),
#     path(_('subscription_plan_management/'),include('_admin_panel.subscription_plan_management.urls')),
#     path(_('payment_management/'),include('_admin_panel.payment_management.urls')),
#     path(_('complaint_management/'),include('_admin_panel.complaint_management.urls')),
#     path(_('report_management/'),include('_admin_panel.report_management.urls')),

#     #Admin Panel Different APIs
#     path(_('ap_um_api/'), include('_admin_panel.user_management.api.urls')),
#     path(_('ap_cm_api/'), include('_admin_panel.category_management.api.urls')),
#     path(_('ap_setm_api/'), include('_admin_panel.settings_management.api.urls')),
#     path(_('ap_notm_api/'), include('_admin_panel.notification_management.api.urls')),
#     path(_('ap_splanm_api/'), include('_admin_panel.subscription_plan_management.api.urls')),
#     path(_('ap_com_api/'), include('_admin_panel.complaint_management.api.urls')),
#     path(_('ap_report_api/'), include('_admin_panel.report_management.api.urls')),
# )

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
