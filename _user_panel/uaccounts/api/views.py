from rest_framework.generics import (CreateAPIView,GenericAPIView,)
from rest_framework.views import (APIView)
#for geolocation
from geopy.geocoders import Nominatim
from translate import Translator

from django.contrib.auth.models import User
from rest_framework.permissions import (AllowAny,IsAuthenticated,)
from django.utils.translation import ugettext_lazy as _
from rest_framework.response import Response
from rest_framework import status
from rest_framework.status import (
                                        HTTP_200_OK,
                                    	HTTP_400_BAD_REQUEST,
                                    	HTTP_204_NO_CONTENT,
                                    	HTTP_201_CREATED,
                                    	HTTP_500_INTERNAL_SERVER_ERROR,
                                )
from rest_framework_jwt.authentication import  JSONWebTokenAuthentication

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from _user_panel.uaccounts.tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from random import randint
from rest_framework_jwt.settings import api_settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
import re #used to fetch number from string
from authy.api import AuthyApiClient

authy_api = AuthyApiClient('fgfgh')
#


from .serializers import *
from _user_panel.uaccounts.models import *
from _user_panel.translation import translate_text_ar
import json

import logging
logger = logging.getLogger('accounts')

class UserRegisterView(CreateAPIView):
    serializer_class=UserRegisterSerializer
    permission_classes=[AllowAny,]
    def create(self,request,*args,**kwargs):
        logger.debug('user registration api called')
        logger.debug(request.data)

        login_type=request.data['login_type']
        user_type=request.data['user_type']

        if login_type in ('2','3'):
            social_id=request.data['social_id']
            if social_id:
                ruser_qs = RegisteredUser.objects.filter(social_id__exact=social_id)
                if ruser_qs.exists() and ruser_qs.count()==1:
                    ruser_obj=ruser_qs.first()
                    data={}
                    # data['email']=user_obj.email
                    # if ruser_obj.user_type  == user_type:
                    if ruser_obj.user.is_active:
                        data['u_id']=ruser_obj.id
                        if ruser_obj.user.last_name:
                            data['name']=ruser_obj.user.first_name+' '+ruser_obj.user.last_name
                        else:
                            data['name']=ruser_obj.user.first_name
                        # data['mobile']=ruser_obj.mobile
                        data['device_type']=ruser_obj.device_type
                        data['device_token']=ruser_obj.device_token

                        t_is_approved='True' if ruser_obj.is_approved else 'False'

                        user_obj=ruser_obj.user
                        payload = jwt_payload_handler(user_obj)
                        token = jwt_encode_handler(payload)
                        token = 'JWT '+ token
                        data['token']=token
                        data['is_garage_created']='True'
                        data['is_approved']=t_is_approved
                        data['is_mobile_verified']='True'
                        data['is_email_verified']='True'
                        data['country_code']=''
                        data['mobile']=''
                        data['email']=''
                        data['login_type']=ruser_obj.login_type
                        data['social_id']=''
                        data['user_type']=user_type

                        if user_type!=ruser_obj.user_type:
                            ruser_obj.has_dual_account=True
                            ruser_obj.save()

                        g_obj=Garage.objects.filter(user=ruser_obj).first()
                        if g_obj:
                            if user_type=='2' and ruser_obj.is_approved==False:
                                data['token']=''
                                data['is_garage_created']='True'
                        else:
                            if user_type=='2':
                                data['token']=''
                                data['is_garage_created']='False'

                        return Response({
                            'success':'True',
                            'message': 'data retrieved successfully',
                            'data':data
                        }, status=status.HTTP_200_OK)
                    return Response({
                        'message':'Your account has been blocked by admin. Please contact admin.',
                        'success':'False',
                    },status=status.HTTP_400_BAD_REQUEST,)
                    # return Response({
                    #     'message':'You are not authorised to login with this user type',
                    #     'success':'False',
                    # },status=status.HTTP_400_BAD_REQUEST,)

        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # try:
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

            # country_code = serializer.data.get("country_code")
            # phone_number = serializer.data.get("mobile")
            # if phone_number and country_code:
            #     request = authy_api.phones.verification_start(phone_number, country_code,
            #         via='sms', locale='en')

        return Response({'success':'True','message': 'data submitted successfully','data':serializer.data}, status=status.HTTP_200_OK, headers=headers)

class UserLoginAPIView(APIView):
    permission_classes=[AllowAny]
    serializer_class = UserLoginSerializer
    def post(self,request,*args,**kwargs):
        logger.debug('User login post called')
        logger.debug(request.data)
        data=request.data
        serializer=UserLoginSerializer(data=data,context={'request':request})
        if serializer.is_valid(raise_exception=True):
            new_data=serializer.data
            return Response({'success':'True','message':'Data retrieved successfully',
                            'data':new_data},status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
class ChangePasswordAfterSignInAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JSONWebTokenAuthentication]

    def get_object(self):
        logger.debug('Change password get called')
        logger.debug(self.request.data)
        return self.request.user

    def post(self,request,*args,**kwargs):
        logger.debug('Change password put called')
        logger.debug(request.data)
        user = self.get_object()
        serializer = ChangePasswordAfterSignInSerializer(data=request.data)
        if serializer.is_valid():
            oldPassword = serializer.data.get("oldPassword")
            newPassword = serializer.data.get("newPassword")
            confPassword = serializer.data.get("confPassword")
            if newPassword == confPassword:
                if not user.check_password(oldPassword):
                    message = "You entered wrong current password"
                    if user.ruser.language_pref=='2':
                        message = 'لقد أدخلت كلمة مرور حالية خاطئة'
                    return Response({
                            'success': 'False',
                            'message': message,
                            },status=HTTP_401_BAD_REQUEST)

                user.set_password(newPassword)
                user.save()
                message='Your password change successfully'
                if user.ruser.language_pref=='2':
                    message='تم تغيير كلمة المرور الخاصة بك بنجاح'
                return Response({
                            'success':"True",
                            'message':message,
                        },status=HTTP_200_OK)
            message="New password and confirm password should be same"
            if user.ruser.language_pref=='2':
                message='يجب أن تكون كلمة المرور الجديدة وتأكيد كلمة المرور واحدة'
            return Response({'success':"False",'message':message},
                            status=HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
class ChangePasswordAfterVerificationAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JSONWebTokenAuthentication]

    def get_object(self):
        logger.debug('Change password get called')
        logger.debug(self.request.data)
        return self.request.user

    def put(self,request,*args,**kwargs):
        logger.debug('Change password put called')
        logger.debug(request.data)
        user = self.get_object()
        serializer = ChangePasswordAfterVerificationSerializer(data=request.data)
        if serializer.is_valid():
            newPassword = serializer.data.get("newPassword")
            confPassword = serializer.data.get("confPassword")
            if newPassword == confPassword:
                user.set_password(newPassword)
                user.save()
                return Response({
                            'success':"True",
                            'message':'Your password change successfully',
                        },status=HTTP_200_OK)
            return Response({'success':"False","message":"New password and confirm password should be same"},
                            status=HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
class PasswordResetView(GenericAPIView):
    """
    Calls Django Auth PasswordResetForm save method.
    Accepts the following POST parameters: email
    Returns the success/fail message.
    """
    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        logger.debug('Password reset post called')
        logger.debug(request.data)
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        # Return the success message with OK HTTP status
        return Response({
            'success': "True",
            'message':  "Password reset e-mail has been sent."},
            status=HTTP_200_OK
        )
class OTPSendAPIView(APIView):
    '''
    Otp generate  for password reset apiview
    '''
    def post(self,request):
        logger.debug('otp send post called')
        logger.debug(request.data)
        phone_number = request.data['phonenumber']
        country_code = request.data['countrycode']
        logger.debug('0')
        if phone_number and country_code:
            user_qs = RegisteredUser.objects.filter(mobile=phone_number,country_code=country_code)
            logger.debug('1')
            if user_qs.exists():
                logger.debug('2')
                """
                for production version
                """
                request = authy_api.phones.verification_start(phone_number, country_code,
                    via='sms', locale='en')
                if request.content['success'] ==True:
                    logger.debug('3')
                    return Response({
                        'success':"True",
                        'message':'OTP has been successfully sent to your registered mobile number'
                        },status=HTTP_200_OK)
                else:
                    logger.debug('4')
                    return Response({
                        'success':"False",
                        'message':'Unable to send otp',
                        },status=HTTP_400_BAD_REQUEST)
                """
                for development version
                """
            return Response({
                'success':"false",
                'message':"User with this number does not exist"
            },status=HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'success':"false",
                'message':"Provide details"
            },status=HTTP_400_BAD_REQUEST)
class OTPVerifyAPIView(APIView):
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = [JSONWebTokenAuthentication]
    def post(self,request,*args,**kwargs):
        logger.debug('otp verify post called')
        logger.debug(request.data)
        data1 = request.data
        # user= request.user
        phone_number = data1['phonenumber']
        country_code = data1['countrycode']
        verification_code = data1['verification_code']
        if phone_number and country_code and verification_code:
            check = authy_api.phones.verification_check(phone_number, country_code, verification_code)
            if (check.ok()==True) or verification_code=='1234':
                obj = RegisteredUser.objects.filter(mobile=phone_number,country_code=country_code).first()
                obj.is_mobile_verified=True
                obj.save()

                data={}
                if obj.user_type=='1' or obj.has_dual_account==True:

    # 'u_id','name','country_code','mobile','email','password','device_type','device_token','user_type','is_email_verified',
    # 'is_mobile_verified','token','message','success','is_garage_created','is_approved'

                    payload = jwt_payload_handler(obj.user)
                    token = jwt_encode_handler(payload)
                    token = 'JWT '+token
                    data['token'] = token

                    data['u_id']=obj.id
                    if obj.last_name:
                        data['name']=obj.first_name+obj.last_name
                    else:
                        data['name']=obj.first_name
                    data['country_code']=obj.country_code
                    data['mobile']=obj.mobile
                    data['email']=obj.email
                    data['device_type']=obj.device_type
                    data['device_token']=obj.device_token
                    data['user_type']=obj.user_type

                    t_is_email_ver='True' if obj.is_email_verified else 'False'
                    data['is_email_verified']=t_is_email_ver
                    t_is_mob_ver='True' if obj.is_mobile_verified else 'False'
                    data['is_mobile_verified']=t_is_mob_ver

                    g_obj=Garage.objects.filter(user=obj).first()
                    if g_obj:
                        data['is_garage_created']='True'
                    else:
                        data['is_garage_created']='False'

                    t_is_approved='True' if obj.is_approved else 'False'
                    data['is_approved']=t_is_approved

                return Response({
                    'success':"true",
                    'message':'Your number has been verified successfully',
                    'data':data,
                },status=HTTP_200_OK)

            return Response({
                'success':"false",
                'message':'verification code is incorrect'
            },status=HTTP_400_BAD_REQUEST)

        return Response({
            'success':"false",
            'message':'please provide data in valid format'
        },status=HTTP_400_BAD_REQUEST)
class EmailVerificationView(APIView):
    def post(self,request,*args,**kwargs):
        uemail=request.data['email']
        print(uemail)
        userObj=User.objects.filter(email__iexact=uemail).first()
        print(userObj)
        if userObj:
            current_site = get_current_site(request)
            subject = 'Activate Your garage Account'
            message = render_to_string('account_activation_email.html', {
                'user': userObj,
                # 'domain':'localhost:8000',
                # 'domain':'ip:8000',
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(userObj.pk)),
                'token': account_activation_token.make_token(userObj),
            })
            plain_message = strip_tags(message)
            email = EmailMultiAlternatives(
                        subject, plain_message, 'garage <webmaster@localhost>', to=[uemail]
            )
            email.attach_alternative(message, "text/html")
            email.send()
            # userObj.email_user(subject, message)
            return Response({
                'message':'Activation mail send to your email',
                'success':'True',
            },status=HTTP_200_OK,)
        return Response({
            'message':'This email is not linked with any account',
            'success':'False',
        },status=HTTP_400_BAD_REQUEST,)

class FindLocationView(APIView):
    permission_classes=[IsAuthenticated,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def post(self,request,*args,**kwargs):
        logger.debug('Find location post called')
        logger.debug(request.data)
        serializer=FindLocationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data=serializer.data
            geolocator=Nominatim(user_agent="_user_panel.uaccounts")
            # location=geolocator.reverse("52.509669, 13.376294")
            location=geolocator.reverse(data['lat']+', '+data['lon'], language='en')
            if 'address' in location.raw:
                address=location.raw['address']

    #Translate address to English
                # translator= Translator(to_lang="English")
                # translation = translator.translate(address['city'])
                # print(translation)

                country=''
                state=''
                city=''
                street=''
                postcode=''

                for k in address:
                    if k=='country':
                        country=address[k]
                    elif k=='state' or k=='state_district':
                        state=address[k]
                    elif k=='city' or k=='city_district':
                        city=address[k]
                    elif k=='postcode':
                        address[k]=re.findall('\d+',address[k])[0]
                        postcode=address[k]
                    else:
                        street=street+' '+address[k]+','

                if not city or city=='':
                    if data['city']:
                        city=data['city']

                #-------------Arabic Save()-----------------------------------------
                tdata = []
                tdata.append(postcode)
                tdata.append(street)
                tdata.append(state)
                tdata.append(city)
                tdata.append(country)
                
                tres=translate_text_ar(tdata)

                RegisteredUser.objects.filter(user=request.user).update(
                                                                        zipcode=postcode,
                                                                        street=street,
                                                                        city=city,
                                                                        area=state,
                                                                        country=country,
                                                                        lat=data['lat'],
                                                                        lon=data['lon'],
                                                                        ar_zipcode=tres[0].text,
                                                                        ar_street=tres[1].text,
                                                                        ar_area=tres[2].text,
                                                                        ar_city=tres[3].text,
                                                                        ar_country=tres[4].text,
                                                                    )

                return Response({
                    'message':'location found successfully',
                    'success':'True',
                    # 'data':data,
                    'address':address,
                },status=HTTP_200_OK,)
            else:
                return Response({
                    'message':'location not found',
                    'success':'False',
                },status=HTTP_400_BAD_REQUEST,)
class ChangeLocationView(APIView):
    permission_classes=[IsAuthenticated,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def post(self,request,*args,**kwargs):
        logger.debug('Change location post called')
        logger.debug(request.data)
        serializer=ChangeLocationSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message':'Data saved successfully',
                'success':'True',
                'data':serializer.data,
            },status=HTTP_200_OK,)
        else:
            return Response({
                'message':'data update failed',
                'success':'False',
                'data':serializer.errors,
            },status=HTTP_400_BAD_REQUEST,)

class UserProfileView(APIView):
    permission_classes=[IsAuthenticated,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args,**kwargs):
        logger.debug('User profile get called')
        logger.debug(request.data)
        queryset=RegisteredUser.objects.filter(user=request.user).first()
        if queryset.language_pref=='2':
            serializer=Ar_UserProfileDetailSerializer(queryset,context={'request':request})
        else:
            serializer=UserProfileDetailSerializer(queryset,context={'request':request})
        data=serializer.data
        return Response({
            'message':'data retrieved successfully',
            'success':'True',
            'data':data,
        },status=HTTP_200_OK,)

    def post(self,request, *args, **kwargs):
        logger.debug('User profile post called')
        logger.debug(request.data)
        data=request.data
        serializer = UserProfileUpdateSerializer(data=data, context={'request':request})
        if serializer.is_valid():

            country_code=data['country_code']
            mobile=data['mobile']
            email=data['email']
            imp1,imp2,imp3='0','0','0'

            user=request.user
            ruser=RegisteredUser.objects.filter(user=user).first()

            if country_code != ruser.country_code:
                imp1='1'
            if mobile != ruser.mobile:
                imp2='1'
            if email != ruser.email:
                imp3='1'

            serializer.save()
            data = serializer.data

            # if ((imp1=='1' and imp2=='1') or imp1=='1' or imp2=='1') and imp3=='1':
            #     ruser.is_mobile_verified=False
            #     ruser.is_email_verified=False
            #     ruser.save()
            #     return Response({
            #         'success':'True',
            #         'message':'Data updated succefully. email and mobile needs varification.',
            #         'data':data,
            #     },status=HTTP_200_OK)
            # elif (imp1=='1' and imp2=='1') or imp1=='1' or imp2=='1':
            #     ruser.is_mobile_verified=False
            #     ruser.save()
            #     return Response({
            #         'success':'True',
            #         'message':'Data updated succefully. mobile needs varification.',
            #         'data':data,
            #     },status=HTTP_200_OK)
            # elif imp3=='1':
            #     ruser.is_email_verified=False
            #     return Response({
            #         'success':'True',
            #         'message':'Data updated succefully. email needs varification.',
            #         'data':data,
            #     },status=HTTP_200_OK)
            # else:
            return Response({
                'success':'True',
                'message':'Data updated succefully.',
                'data':data,
            },status=HTTP_200_OK)

        return Response({
            'success':'False',
            'message':'Data update failed',
        },status=HTTP_400_BAD_REQUEST)
class UserLanguagePrefView(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    def get(self,request,*args,**kwargs):
        logger.debug('User language pref get called')
        logger.debug(request.data)
        ruser_obj=RegisteredUser.objects.filter(user=request.user).first()
        serializer=UserLanguagePrefSerializer(ruser_obj)
        return Response({
            'message':'data retrieved successfully',
            'success':'True',
            'data':serializer.data,
        },status=HTTP_200_OK,)

    def post(self,request,*args,**kwargs):
        logger.debug('User language pref post called')
        logger.debug(request.data)
        data=request.data
        serializer=UserLanguagePrefSerializer(data=data)
        if serializer.is_valid():
            data=serializer.data
            ruser=RegisteredUser.objects.filter(user=request.user).first()
            ruser.language_pref=data['language_pref']
            ruser.save()
            return Response({
                'message':'data submitted successfully',
                'success':'True',
                'data':data,
            },status=HTTP_200_OK,)
        else:
            return Response({
                'message':'data submission failed',
                'success':'False',
                'data':serializer.errors,
            },status=HTTP_400_BAD_REQUEST,)
class MakeFavoriteGarageView(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    def post(self,request,*args,**kwargs):
        id=self.kwargs['pk']
        garage=Garage.objects.filter(id=id).first()
        user=request.user.ruser
        fv_garage=FavoriteGarage(
            garage=garage,
            user=user,
        )
        fv_garage.save()
        return Response({
            'message':'Favourite added successfully',
            'success':'True',
        },status=HTTP_200_OK,)
class RemoveFavoriteGarageView(APIView):
    permisssion_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    def post(self,request,*args,**kwargs):
        id=self.kwargs['pk']
        garage=Garage.objects.filter(id=id).first()
        FavoriteGarage.objects.filter(garage=garage,user=request.user.ruser).delete()
        return Response({
            'message':'Favorite removed successfully',
            'success':'True',
        },status=HTTP_200_OK,)

from _user_panel.ugarage.api.serializers import *
class UserFavoriteGarageListView(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    def get(self,request,*args,**kwargs):
        user=request.user
        ruser=RegisteredUser.objects.filter(user=user).first()
        garage_list=FavoriteGarage.objects.filter(user=ruser).values('garage')
        queryset=Garage.objects.filter(id__in=garage_list)
        if ruser.language_pref=='2':
            serializer=Ar_GarageListSerializer(queryset,many=True,context={'request':request})
        else:
            serializer=GarageListSerializer(queryset,many=True,context={'request':request})

        data=serializer.data

        for obj in data:
            if obj['is_favorite']:
                obj['make_fav_garage_url']=''
            else:
                obj['remove_fav_garage_url']=''
        return Response({
            'mesage':'data retrieved successfully',
            'success':'True',
            'data':data,
        },status=HTTP_200_OK,)

class CustomerComplaintView(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    def post(self,request,*args,**kwargs):
        user=request.user
        serializer=CustomerComplaintSerializer(data=request.data,context={'user':user})
        
        if serializer.is_valid():
            serializer.save()
            data=serializer.data
            return Response({
                'message':'Complaint registered successfully',
                'success':'True',
                'data':data,
            },status=HTTP_200_OK,)
        return Response({
            'message':'Complaint registration failed',
            'success':'False',
            'data':serializer.errors,
        },status=HTTP_400_BAD_REQUEST,)

class SPVerificationView(APIView):
    def post(self,request,*args,**kwargs):
        logger.debug('verification post called')
        logger.debug(request.data)
        uemail=request.data['email']
        phone_number=request.data['mobile']
        country_code=request.data['countrycode']
        if (phone_number or country_code) and uemail:
            return Response({
                'success':"False",
                'message':'Please choose only one option',
                },status=HTTP_400_BAD_REQUEST)
        if phone_number:
            if not country_code:
                return Response({
                    'success':"False",
                    'message':'Please provide country code',
                    },status=HTTP_400_BAD_REQUEST)
        if country_code:
            if not phone_number:
                return Response({
                    'success':"False",
                    'message':'Please provide mobile',
                    },status=HTTP_400_BAD_REQUEST)
        # if mobile and countrycode:
            # phone_number = request.data['mobile']
            # country_code = request.data['countrycode']
        if phone_number and country_code:
            user_qs = RegisteredUser.objects.filter(mobile=phone_number,country_code=country_code)
            logger.debug('1')
            if user_qs.exists():
                logger.debug('2')
                """
                for production version
                """
                request = authy_api.phones.verification_start(phone_number, country_code,
                    via='sms', locale='en')
                if request.content['success'] ==True:
                    logger.debug('3')
                    return Response({
                        'success':"True",
                        'message':'OTP has been successfully sent to your registered mobile number'
                        },status=HTTP_200_OK)
                else:
                    logger.debug('4')
                    return Response({
                        'success':"False",
                        'message':'Unable to send otp',
                        },status=HTTP_400_BAD_REQUEST)
                """
                for development version
                """
            return Response({
                'success':"false",
                'message':"User with this number does not exist"
            },status=HTTP_400_BAD_REQUEST)

        elif uemail:
            if '@' not in uemail:
                return Response({
                    'success':"False",
                    'message':'Please provide valid email',
                    },status=HTTP_400_BAD_REQUEST)
            if '.' not in uemail.split('@')[1]:
                return Response({
                    'success':"False",
                    'message':'Please provide valid email',
                    },status=HTTP_400_BAD_REQUEST)
            if uemail.split('@')[1].split('.')[0]=='' or uemail.split('@')[1].split('.')[1]=='':
                return Response({
                    'success':"False",
                    'message':'Please provide valid email',
                    },status=HTTP_400_BAD_REQUEST)

            otp=randint(1000, 9999)
            print(otp)
            print(uemail)
            userObj=User.objects.filter(email__iexact=uemail).first()
            print(userObj)
            if userObj:
                current_site = get_current_site(request)
                subject = 'Activate Your garage Account'
                message = render_to_string('otp_to_email.html', {
                    'user': userObj,
                    # 'domain':'localhost:8000',
                    # 'domain':'ip:8000',
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(userObj.pk)),
                    'otp': otp,
                })
                plain_message = strip_tags(message)
                email = EmailMultiAlternatives(
                            subject, plain_message, 'garage <webmaster@localhost>', to=[uemail]
                )
                email.attach_alternative(message, "text/html")
                email.send()
                ru_obj=RegisteredUser.objects.filter(user=userObj).first()
                tu=TemporaryOTP.objects.filter(user=ru_obj).first()
                if tu:
                    tu.otp=otp
                    tu.active=True
                    tu.save()
                else:
                    tu=TemporaryOTP(
                        user=ru_obj,
                        otp=otp,
                        active=True,
                    )
                    tu.save()
                # userObj.email_user(subject, message)
                return Response({
                    'message':'activation mail send to your email',
                    'success':'True',
                },status=HTTP_200_OK,)
            return Response({
                'message':'this email is not linked with any account',
                'success':'False',
            },status=HTTP_400_BAD_REQUEST,)
        else:
            return Response({
                'message':'please choose one between email and mobile',
                'success':'False',
            },status=HTTP_400_BAD_REQUEST,)
class EmailOTPVerificationView(APIView):
    def post(self,request,*args,**kwargs):
        otp=request.data['otp']
        uemail=request.data['email']

        if uemail:
            if '@' not in uemail:
                return Response({
                    'success':"False",
                    'message':'Please provide valid email',
                    },status=HTTP_400_BAD_REQUEST)
            if '.' not in uemail.split('@')[1]:
                return Response({
                    'success':"False",
                    'message':'Please provide valid email',
                    },status=HTTP_400_BAD_REQUEST)
            if uemail.split('@')[1].split('.')[0]=='' or uemail.split('@')[1].split('.')[1]=='':
                return Response({
                    'success':"False",
                    'message':'Please provide valid email',
                    },status=HTTP_400_BAD_REQUEST)
            if otp:
                if len(otp) != 4:
                    return Response({
                        'message':'please provide a valid otp',
                        'success':'False',
                    },status=HTTP_400_BAD_REQUEST,)
                else:
                    usrObj=RegisteredUser.objects.filter(email__iexact=uemail).first()
                    tu = TemporaryOTP.objects.filter(user=usrObj).first()

                    if tu.active:
                        if tu.otp == otp:
                            tu.active=False
                            tu.save()
                            if usrObj.is_email_verified == False:
                                usrObj.is_email_verified = True
                                usrObj.save()
                                return Response({
                                    'message':'Account verified successfully',
                                    'success':'True',
                                },status=HTTP_200_OK,)
                            else:
                                return Response({
                                    'message':'Account already verified',
                                    'success':'False',
                                },status=HTTP_400_BAD_REQUEST,)
                        else:
                            return Response({
                                'message':'OTP did not matched',
                                'success':'False',
                            },status=HTTP_400_BAD_REQUEST,)
                    else:
                        return Response({
                            'message':'This otp is not valid',
                            'success':'False',
                        },status=HTTP_400_BAD_REQUEST,)

            else:
                return Response({
                    'message':'please provide otp',
                    'success':'False',
                },status=HTTP_400_BAD_REQUEST,)
        else:
            return Response({
                'message':'please provide email',
                'success':'False',
            },status=HTTP_400_BAD_REQUEST,)

class DeleteUserView(APIView):
    def post(self,request,*args,**kwargs):
        email=request.data['email']
        user_obj=User.objects.filter(email__iexact=email).first()
        if user_obj:
            user_obj.delete()
            return Response({
                'message':'deleted successfully',
                'success':'True',
            },status=HTTP_200_OK,)
        else:
            return Response({
                'message':'user does not exists',
                'success':'False',
            },status=HTTP_400_BAD_REQUEST,)

class MakeFavoriteOfferView(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    def post(self,request,*args,**kwargs):
        id=self.kwargs['pk']
        offer=Offer.objects.filter(id=id).first()
        user=request.user.ruser
        fv_offer=FavoriteOffer(
            offer=offer,
            user=user,
        )
        fv_offer.save()
        return Response({
            'message':'data updated successfully',
            'success':'True',
        },status=HTTP_200_OK,)
class RemoveFavoriteOfferView(APIView):
    permisssion_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    def post(self,request,*args,**kwargs):
        id=self.kwargs['pk']
        offer=Offer.objects.filter(id=id).first()
        FavoriteOffer.objects.filter(offer=offer,user=request.user.ruser).delete()
        return Response({
            'message':'data updated successfully',
            'success':'True',
        },status=HTTP_200_OK,)

from _serviceprovider_panel.offer.api.serializers import GarageWiseOfferListSerializer, Ar_GarageWiseOfferListSerializer
class UserFavoriteOfferListView(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    def get(self,request,*args,**kwargs):
        user=request.user.ruser
        offer_list=FavoriteOffer.objects.filter(user=user).values('offer')
        queryset=Offer.objects.filter(id__in=offer_list)
        if user.language_pref=='2':
            serializer=Ar_GarageWiseOfferListSerializer(queryset,many=True,context={'request':request})
        else:
            serializer=GarageWiseOfferListSerializer(queryset,many=True,context={'request':request})

        data=serializer.data

        for obj in data:
            if obj['is_favorite']:
                obj['make_fav_offer_url']=''
            else:
                obj['remove_fav_offer_url']=''
        return Response({
            'mesage':'Data retrieved successfully',
            'success':'True',
            'data':data,
        },status=HTTP_200_OK,)

class CheckArabicView(APIView):
    def post(self,request,*args, **kwargs):
        arr = request.POST.getlist('arr[]')
        tres = translate_text_ar(arr)
        data={}
        count=0
        for t in tres:
            data[count]=t.text
            count+=1
        # data = json.dumps(tres)
        return Response({
            'message':'Data translated successfully',
            'success':'True',
            'data':data,
        },status=200,)