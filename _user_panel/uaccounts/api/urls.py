from django.urls import path

from .views import *

app_name='up_accounts'

urlpatterns=[
    path('register/',UserRegisterView.as_view(),name='register'),
    path('login/',UserLoginAPIView.as_view(),name='login'),
    path('password/reset/', PasswordResetView.as_view(),name='reset_password_email'),
    path('otp/send/', OTPSendAPIView.as_view(),name="otpsend"),
    path('otp/verify/', OTPVerifyAPIView.as_view(),name="otpverify"),
    path('email_verification/',EmailVerificationView.as_view(),name='emailverify'),
    path('forgotpass/changepassword/',ChangePasswordAfterSignInAPIView.as_view(),name='change_pass_after_verification'),
    path('profile/changepassword/',ChangePasswordAfterSignInAPIView.as_view(),name='change_pass_by_profile'),
    path('location/',FindLocationView.as_view(),name='find_location'),
    path('change_location/',ChangeLocationView.as_view(),name='change_location'),

    path('profile/',UserProfileView.as_view(),name='user_profile'),
    path('profile/edit/',UserProfileView.as_view(),name='user_profile_edit'),

    path('language_pref/',UserLanguagePrefView.as_view(),name='user_language_pref'),

    path('make_favorite/<int:pk>',MakeFavoriteGarageView.as_view(),name='user_fav_gar'),
    path('remove_favorite/<int:pk>',RemoveFavoriteGarageView.as_view(),name='user_remove_fav_gar'),
    path('favorite_garages/',UserFavoriteGarageListView.as_view(),name='user_fav_gar_list'),
    path('complaint/',CustomerComplaintView.as_view(),name='user_complaint'),

    path('verification/',SPVerificationView.as_view(),name='verification'),
    path('email/otp/verification/',EmailOTPVerificationView.as_view(),name='email_otp_verification'),

    path('delete/',DeleteUserView.as_view(),name='user_delete'),

    path('make_favorite_offer/<int:pk>',MakeFavoriteOfferView.as_view(),name='user_fav_off'),
    path('remove_favorite_offer/<int:pk>',RemoveFavoriteOfferView.as_view(),name='user_remove_fav_off'),
    path('favorite_offers/',UserFavoriteOfferListView.as_view(),name='user_fav_off_list'),

    path('check_arabic/',CheckArabicView.as_view(),name='check_arabic_view'),

]
