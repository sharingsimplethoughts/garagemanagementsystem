from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from rest_framework.exceptions import APIException
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from rest_framework.response import Response

from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from _user_panel.uaccounts.models import *
from _serviceprovider_panel.saccounts.models import CustomerComplaint
from .password_reset_form import MyPasswordResetForm
from _user_panel.translation import translate_text_ar
from rest_framework.status import (
                                        HTTP_200_OK,
                                    	HTTP_400_BAD_REQUEST,
                                    	HTTP_204_NO_CONTENT,
                                    	HTTP_201_CREATED,
                                    	HTTP_500_INTERNAL_SERVER_ERROR,
                                )

import logging
logger = logging.getLogger('accounts')

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class APIException400(APIException):
    status_code = 400
class APIException401(APIException):
    status_code = 401

'''
Common APIS for all-----
'''

class UserRegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(allow_blank=True)
    # garage_name = serializers.CharField(allow_blank=True)
    country_code=serializers.CharField(allow_blank=True)
    mobile = serializers.CharField(allow_blank=True)
    email = serializers.CharField(allow_blank=True, style={'input_type':'email'})
    password = serializers.CharField(allow_blank=True,write_only=True,style={'input_type':'password'})

    login_type = serializers.CharField(allow_blank=True)
    social_id = serializers.CharField(allow_blank=True)

    device_type = serializers.CharField(allow_blank=True)

    user_type = serializers.CharField(allow_blank=True)

    message = serializers.CharField(allow_blank=True, read_only=True)
    success = serializers.CharField(allow_blank=True, read_only=True)
    token = serializers.CharField(allow_blank=True,read_only=True)
    u_id = serializers.CharField(allow_blank=True, read_only=True)
    created_on = serializers.CharField(allow_blank=True, read_only=True)
    is_garage_created = serializers.CharField(read_only=True)
    is_approved = serializers.CharField(read_only=True)
    is_mobile_verified = serializers.CharField(read_only=True)
    is_email_verified = serializers.CharField(read_only=True)

    class Meta:
        model=RegisteredUser
        # 'garage_name',
        fields=['name', 'country_code', 'mobile', 'email', 'password', 'login_type', 'social_id',
        'device_type', 'device_token', 'user_type', 'message', 'success', 'token', 'u_id', 'created_on',
        'is_garage_created','is_approved','is_mobile_verified','is_email_verified']

    def validate(self, data):
        name=data['name']
        # garage_name=data['garage_name']
        country_code=data['country_code']
        mob=data['mobile']
        email=data['email']
        password=data['password']
        login_type=data['login_type']
        social_id=data['social_id']
        device_type=data['device_type']
        device_token=data['device_token']
        user_type=data['user_type']

        if not login_type or login_type=='':
            raise APIException400({
                'success':'False',
                'message':'Please provide login type',
            })
        if login_type not in ('1','2','3'):
            raise APIException400({
                'success':'False',
                'message':'Please provide a valid login type',
            })
        if login_type in ('2','3'):
            if not social_id or social_id=="" :
                raise APIException400({
                    'success':'False',
                    'message':'Please provide social id'
                })

        if login_type in ('2','3'):
            ruser_qs = RegisteredUser.objects.filter(social_id__exact=social_id)
            if ruser_qs.exists() and ruser_qs.count()==1:
                ruser_obj=ruser_qs.first()

                user_obj=ruser_obj.user
                payload = jwt_payload_handler(user_obj)
                token = jwt_encode_handler(payload)
                token = 'JWT '+ token

                # data['email']=user_obj.email
                data['token']=token
                if ruser_obj.user.last_name:
                    data['name']=ruser_obj.user.first_name+' '+ruser_obj.user.last_name
                else:
                    data['name']=ruser_obj.user.first_name
                # data['mobile']=ruser_obj.mobile
                data['device_type']=ruser_obj.device_type
                data['device_token']=ruser_obj.device_token

                # return Response({
                #     'message':'You are logged in successfully',
                #     'success':'True',
                #     'data':data,
                # })
                raise APIException400({
                    'success':'True',
                    'message':'Social id already exists',
                    'data':data,
                })

        if not name or name=='':
            raise APIException400({
                'success':"False",
                'message':'Name can not be blank',
                })

        if login_type in ('2','3'):
            print('aaaaa')
            if social_id:
                print('hello')
                if (not country_code or country_code=="") and mob:
                    raise APIException400({
                        'success':"False",
                        'message':'please provide country code',
                        })
                if (not mob or mob=="") and country_code:
                    raise APIException400({
                        'success':"False",
                        'message':'please provide mobile',
                        })
                if mob and country_code:
                    ruo=RegisteredUser.objects.filter(mobile__iexact=mob,country_code__iexact=country_code).first()
                    if ruo:
                        raise APIException400({
                            'success':"False",
                            'message':'user with this mobile is already exists',
                            })
                else:
                    country_code='+971'
                    mob=social_id
                if email:
                    print('ccc')
                    user_t=User.objects.filter(email__iexact=email).first()
                    if user_t:
                        raise APIException400({
                            'success':"False",
                            'message':'This email is already registered',
                            })
                    else:
                        password='C123M@45'
                else:
                    print('bbbbb')
                    email=social_id+'@xyz63.com'
                    password='12345678'

        if not country_code or country_code=='':
            raise APIException400({
                'success':'False',
                'message':'country code is required',
            })
        if not mob or mob=='':
            raise APIException400({
                'success':'False',
                'message':'mobile is required',
            })
        if not email or email=='':
            raise APIException400({
                'success':'False',
                'message':'email is required',
            })
        if not password or password=='':
            raise APIException400({
                'success':'False',
                'message':'password is required',
            })
    

    
        if not device_type or device_type=='':
            raise APIException400({
                'success':'False',
                'message':'device_type is required',
            })
        if not user_type or user_type=='':
            raise APIException({
                'success':'False',
                'message':'user_type is required',
            })
        # if user_type == '2' and login_type == '1':
        #     if not garage_name or garage_name=="":
        #         raise APIException({
        #             'success':'False',
        #             'message':'garage_name is required',
        #         })
        # email validation
        allowedDomains = [
        "aol.com", "att.net", "comcast.net", "facebook.com", "gmail.com", "gmx.com", "googlemail.com",
        "google.com", "hotmail.com", "hotmail.co.uk", "mac.com", "me.com", "mail.com", "msn.com",
        "live.com", "sbcglobal.net", "verizon.net", "yahoo.com", "yahoo.co.uk",
        "email.com", "games.com" , "gmx.net", "hush.com", "hushmail.com", "icloud.com", "inbox.com",
        "lavabit.com", "love.com" , "outlook.com", "pobox.com", "rocketmail.com",
        "safe-mail.net", "wow.com", "ygm.com" , "ymail.com", "zoho.com", "fastmail.fm",
        "yandex.com","iname.com","xyz63.com"
        ]
        if '@' not in email:
            raise APIException400({
                'success':'False',
                'message':'Please provide a valid email',
            })
        else:
            if not email.split('@')[1] or email.split('@')[1]=="":
                raise APIException400({
                    'success':'False',
                    'message':'Please provide a valid email',
                })
            else:
                temp=email.split('@')[1]
                if '.' in temp:
                    if (not temp.split('.')[0] or temp.split('.')[0]=="") or (not temp.split('.')[1] or temp.split('.')[1]==""):
                        raise APIException400({
                            'success':'False',
                            'message':'Please provide a valid email',
                        })
                else:
                    raise APIException400({
                        'success':'False',
                        'message':'Please provide a valid email',
                    })
            domain = email.split('@')[1]
            # if domain not in allowedDomains:
            #     raise APIException400({
            #         'success':'False',
            #         'message':'Please provide a valid email',
            #     })
            user_qs = RegisteredUser.objects.filter(user__email__iexact=email)
            if user_qs.exists():
                raise APIException400({
                    'success':'False',
                    'message':'User with this email is already registered. Please login to continue.',
                })
        # mobile validation
        if login_type=='1':
            if mob.isdigit():
                user_qs=RegisteredUser.objects.filter(mobile__iexact=mob)
                if user_qs.exists():
                    raise APIException400({
                        'success':'False',
                        'message':'This mobile number already exists. Please login to continue.',
                    })
            else:
                raise APIException400({
                    'success':'False',
                    'message':'Please provide a valid number only',
                })
            if len(password)<8:
                raise APIException400({
                    'success':"False",
                    'message':'Password must be at least 8 characters',
                })
            count=0
            for x in password:
                if x in ('a','b','c','d','e','f','g','h','i','j','k',
                        'l','m','n','o','p','q','r','s','t','u','v','w',
                        'x','y','z','A','B','C','D','E','F','G','H','I',
                        'J','K','L','M','N','O','P','Q','R','S','T','U',
                        'V','W','X','Y','Z'):
                    count=count+1
            if count<2:
                raise APIException400({
                    'success':'False',
                    'message':'Password must contain atleast 2 alphabets',
                })


        # device type varification
        if device_type not in ['1','2','3']:
            raise APIException400({
                'success':'False',
                'message':'Please enter correct format of device_type',
            })
        if user_type not in ['1','2']:
            raise APIException400({
                'success':'False',
                'message':'Please enter correct format of user_type',
            })
        # if user_type == '2' and login_type == '1':
        #     g=Garage.objects.filter(name__iexact=(garage_name)).first()
        #     if g:
        #         raise APIException({
        #             'success':'False',
        #             'message':'Garage with this name already exists',
        #         })

        data['email']=email
        data['mobile']=mob
        data['country_code']=country_code
        data['password']=password
        return data

    def create(self, validated_data):
        social_id = ''

        name = validated_data['name']
        email = validated_data['email']
        password = validated_data['password']
        user_type = validated_data['user_type']
        login_type = validated_data['login_type']
        mobile = validated_data['mobile']
        # garage_name = validated_data['garage_name']

        # is_active=True
        # if user_type=='2':
        #     is_active=False

        # is_approved=True
        # if user_type=='2':
        is_approved=False


        first_name=name.split(' ')[0]
        last_name=' '.join(name.split(' ')[1:])

        user_obj = User(
            username = email.split('@')[0]+mobile,
            email = email,
            first_name=first_name,
            last_name=last_name,
            # is_active=is_active,
        )
        user_obj.set_password(password)
        user_obj.save()

        country_code = validated_data['country_code']
        mobile = validated_data['mobile']
        device_type = validated_data['device_type']
        device_token = validated_data['device_token']

        # if login_type in ('2','3'):
        #     if social_id:
        #         country_code='+971'
        #         mobile=social_id

        login_type = validated_data['login_type']
        if login_type in ('2','3'):
            social_id = validated_data['social_id']

        if social_id:
            ruser_obj = RegisteredUser(
                first_name=first_name,
                last_name=last_name,
                country_code=country_code,
                mobile=mobile,
                email=email,
                login_type = login_type,
                social_id = social_id,
                device_type = device_type,
                device_token = device_token,
                user_type = user_type,
                user = user_obj,
                is_email_verified=True,
                is_mobile_verified=True,
                is_approved=is_approved,
            )
        else:
            ruser_obj = RegisteredUser(
                first_name=first_name,
                last_name=last_name,
                country_code=country_code,
                mobile=mobile,
                email=email,
                login_type = login_type,
                social_id = social_id,
                device_type = device_type,
                device_token = device_token,
                user_type = user_type,
                user = user_obj,
                is_approved=is_approved,
            )

        ruser_obj.save()

        #-----------Arabic Save()----------------------------
        tdata=[]
        
        tdata.append(first_name)
        tdata.append(last_name)
        # tdata.append(about)
        tdata.append(mobile)
        tdata.append(country_code)
        # tdata.append(zipcode)
        # tdata.append(street)
        # tdata.append(area)
        # tdata.append(city)
        # tdata.append(country)

        tres = translate_text_ar(tdata)

        ruser_obj.ar_first_name=first_name
        ruser_obj.ar_last_name=last_name
        ruser_obj.ar_mobile=mobile
        ruser_obj.ar_country_code=country_code

        # ruser_obj.ar_first_name=tres[0].text
        # ruser_obj.ar_last_name=tres[1].text
        # ruser_obj.ar_about=tres[2].text
        # ruser_obj.ar_mobile=tres[2].text
        # ruser_obj.ar_country_code=tres[3].text
        # ruser_obj.ar_zipcode=tres[5].text
        # ruser_obj.ar_street=tres[6].text
        # ruser_obj.ar_area=tres[7].text
        # ruser_obj.ar_city=tres[8].text
        # ruser_obj.ar_country=tres[9].text
        ruser_obj.save()
        #------------------------------------------------------------


        # if user_type=='2' and login_type=='1':
        #     garage_obj=Garage(
        #         name=garage_name,
        #         user=ruser_obj,
        #     )
        #     garage_obj.save()
        validated_data['token']=''
        if login_type in ('2','3') and user_type=='1':
            payload = jwt_payload_handler(user_obj)
            token = jwt_encode_handler(payload)
            token = 'JWT '+token
            validated_data['token'] = token

        g_obj=Garage.objects.filter(user=ruser_obj).first()
        if g_obj:
            validated_data['is_garage_created']='True'
        else:
            validated_data['is_garage_created']='False'

        t_is_approved='True' if ruser_obj.is_approved else 'False'
        validated_data['is_approved']=t_is_approved

        if ruser_obj.is_mobile_verified:
            validated_data['is_mobile_verified']='True'
        else:
            validated_data['is_mobile_verified']='False'
        if ruser_obj.is_email_verified:
            validated_data['is_email_verified']='True'
        else:
            validated_data['is_email_verified']='False'

        validated_data['u_id'] = ruser_obj.id
        validated_data['created'] = ruser_obj.created_on

        return validated_data
class UserLoginSerializer(serializers.ModelSerializer):
    name=serializers.CharField(read_only=True)
    email=serializers.CharField(allow_blank=True)
    profile_image=serializers.ImageField(required=False)
    password = serializers.CharField(allow_blank=True,write_only=True,label='Password',style={'input_type':'password'})
    device_type  = serializers.CharField(allow_blank=True)
    device_token = serializers.CharField(allow_blank=True)
    user_type = serializers.CharField(allow_blank=True)

    is_email_verified=serializers.CharField(allow_blank=True,read_only=True)
    is_mobile_verified=serializers.CharField(allow_blank=True,read_only=True)
    country_code=serializers.CharField(read_only=True)
    mobile=serializers.CharField(allow_blank=True,read_only=True)
    token = serializers.CharField(allow_blank=True,read_only=True)
    message = serializers.CharField(allow_blank=True, read_only=True)
    success = serializers.CharField(allow_blank=True, read_only=True)

    is_garage_created = serializers.CharField(read_only=True)
    is_approved = serializers.CharField(read_only=True)
    u_id = serializers.CharField(read_only=True)
    login_type = serializers.CharField(read_only=True)
    garage_name = serializers.CharField(read_only=True)
    garage_id = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ('u_id','name','profile_image','country_code','mobile','email','password','device_type','device_token','user_type','is_email_verified',
        'is_mobile_verified','token','message','success','is_garage_created','is_approved','login_type','garage_name','garage_id')

    # def to_representation(self,instance):
    #     data=super().to_representation(instance)
    #     if not data['profile_image'] or data['profile_image']=='':
    #         data['profile_image']=""
    #     return data

    def validate(self,data):
        email = data['email']
        password = data['password']
        device_token = data['device_token']
        device_type = data['device_type']
        user_type = data['user_type']

        if not email or email=='':
            raise APIException400({
                'success':'False',
                'message':'email is required',
            })

        if not password or password=='':
            raise APIException400({
                'success':'False',
                'message':'password is required',
            })

        if not device_type or device_type=='':
            raise APIException400({
                'success':'False',
                'message':'device_type is required',
            })
        if not user_type or user_type=='':
            raise APIException400({
                'success':'False',
                'message':'user_type is required',
            })

        if not email or not password:
            raise APIException400({
                'success':'False',
                'message':'email and password is required',
            })

        # email validation
        # user=User.objects.filter(username__iexact=email.split('@')[0])
        user=User.objects.filter(email__iexact=email)
        user_obj=''
        if user.exists() and user.count()==1:
            user_obj=user.first()
            # ruser_o=RegisteredUser.objects.filter(user=user_obj).first()
            # if ruser_o.user_type=='1' and ruser_o.is_mobile_verified==False:
            #     raise APIException400({
            #         'success':'False',
            #         'message':'This mobile is not verified',
            #         'is_email_verified':ruser_o.is_email_verified,
            #         'is_mobile_verified':ruser_o.is_mobile_verified,
            #         'country_code':
            #     })
            # if ruser_o.user_type=='2' and ruser_o.is_email_verified==False and ruser_o.is_mobile_verified==False:
            #     raise APIException400({
            #         'success':'False',
            #         'message':'Verification for this account is pending. Please verify either mobile or email.',
            #         'is_email_verified':ruser_o.is_email_verified,
            #         'is_mobile_verified':ruser_o.is_mobile_verified,
            #     })
        else:
            raise APIException400({
                'success':'False',
                'message':'This email is not registered',
            })

        # password Validation
        if len(password)<8:
            raise APIException400({
                'success':"false",
                'message':'Password must be at least 8 characters',
            })

        # device type varification
        if device_type not in ['1','2','3']:
            raise APIException400({
                'success':'False',
                'message':'Please enter correct format of device_type',
            })
        if user_type not in ['1','2']:
            raise APIException400({
                'success':'False',
                'message':'Please enter correct format of user_type',
            })

        if user_obj:
            # uobj = user_obj.user
            if not user_obj.check_password(password):
                raise APIException401({
                    'success':'False',
                    'message':'Invalid credentials',
                })

            # if not ruser_o.is_approved:
            #     raise APIException400({
            #         'success':'False',
            #         'message':'Your request has been sent to the admin for verification. You will receive a confirmation email once its done.',
            #     })
            if user_obj.ruser.user_type != user_type:
                user_obj.ruser.has_dual_account=True
                user_obj.ruser.save()
                # raise APIException400({
                #     'success':'False',
                #     'message':'You are not authorised to login with this user type',
                # })

        ruser = RegisteredUser.objects.filter(user__id=user_obj.id)
        ruser = ruser.first()

        ruser.device_type = device_type
        ruser.device_token = device_token
        ruser.save()

        if not user_obj.is_active:
            raise APIException400({
                'success':'False',
                'message':'Your account has been blocked by admin. Please contact admin.',
            })

        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        token = 'JWT '+token
        data['token']=token

        if user_type=='1' and ruser.is_mobile_verified==False:
            data['token']=''
        if user_type=='2'  and ruser.is_email_verified==False and ruser.is_mobile_verified==False:
            data['token']=''
        if user_type=='2' and ruser.is_approved==False:
            data['token']=''

        data['u_id']=ruser.id
        data['name']=user_obj.first_name
        if user_obj.last_name:
            data['name']=user_obj.first_name+' '+user_obj.last_name
        # data['mobile']=ruser.mobile
        data['profile_image']=""
        if ruser.profile_image:
            data['profile_image']=ruser.profile_image
        data['country_code']=ruser.country_code
        data['mobile']=ruser.mobile

        g_obj=Garage.objects.filter(user=ruser).first()
        data['is_garage_created']=False
        if g_obj:
            data['is_garage_created']=True
        # else:
        #     data['token']=''
        data['is_approved']=ruser.is_approved
        data['is_email_verified']=ruser.is_email_verified
        data['is_mobile_verified']=ruser.is_mobile_verified
        data['login_type']=ruser.login_type

        data['garage_name']=""
        data['garage_id']=""
        print(ruser.user_type)
        if ruser.user_type=="2" or ruser.has_dual_account==True:
            garage=Garage.objects.filter(user=ruser).first()
            if garage:
                data['garage_id']=garage.id
                if garage.name:
                    data['garage_name']=garage.name

        return data

class ChangePasswordAfterSignInSerializer(serializers.Serializer):
    oldPassword = serializers.CharField(allow_blank=True,required=True)
    newPassword = serializers.CharField(allow_blank=True,required=True)
    confPassword = serializers.CharField(allow_blank=True,required=True)

    def validate_oldPassword(self, password):
        if not password or password=='':
            raise APIException400({
                'success':'False',
                'message':'Old password is required'
            })
        if len(password) < 8:
            raise APIException400({
                'success':"False",
                'message':'Old password must be at least 8 characters',
            })
        return password
    def validate_newPassword(self, password):
        if not password or password=='':
            raise APIException400({
                'success':'False',
                'message':'New password is required'
            })
        if len(password) < 8:
            raise APIException400({
                'success':"False",
                'message':'New password must be at least 8 characters',
            })
        return password
    def validate_confPassword(self, password):
        if not password or password=='':
            raise APIException400({
                'success':'False',
                'message':'Confirm password is required',
            })
        if len(password) < 8:
            raise APIException400({
                'success':"False",
                'message':'Confirm password must be at least 8 characters',
            })
        return password
class ChangePasswordAfterVerificationSerializer(serializers.Serializer):
    newPassword = serializers.CharField(allow_blank=True,required=True)
    confPassword = serializers.CharField(allow_blank=True,required=True)

    def validate_newPassword(self, password):
        if not password or password=='':
            raise APIException400({
                'success':'False',
                'message':'New password is required'
            })
        if len(password) < 8:
            raise APIException400({
                'success':"false",
                'message':'New password must be at least 8 characters',
            })
        return password
    def validate_confPassword(self, password):
        if not password or password=='':
            raise APIException400({
                'success':'False',
                'message':'Confirm password is required',
            })
        if len(password) < 8:
            raise APIException400({
                'success':"false",
                'message':'Confirm password must be at least 8 characters',
            })
        return password
class PasswordResetSerializer(serializers.Serializer):

    """
    Serializer for requesting a password reset e-mail.
    """

    email = serializers.CharField(allow_blank=True)
    class Meta:
        model = User
        fields = [
            'email',
        ]

    password_reset_form_class = MyPasswordResetForm

    def validate_email(self, value):
        if not value or value=='':
            raise APIException400({
                'success':'False',
                'message':'Confirm password is required'
            })
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            # raise serializers.ValidationError(_('Error'))
            raise APIException400({
                'success':'False',
                'message':'This email id is not registered with any account.'
            })

        if not User.objects.filter(email=value).exists():
            # raise serializers.ValidationError(_('This e-mail address is not linked with any account'))
            raise APIException400({
                'success':'False',
                'message':'No user registered with this email'
            })
        user=User.objects.filter(email=value).first()
        ruser=RegisteredUser.objects.filter(user=user).first()
        if ruser.social_id:
            raise APIException400({
                'success':'False',
                'message':'You are registered with your social credentials. Password reset is not applicable here.'
            })

        return value

    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
        }
        self.reset_form.save(**opts)
class FindLocationSerializer(serializers.Serializer):
    lat=serializers.CharField(allow_blank=True,)
    lon=serializers.CharField(allow_blank=True,)
    city=serializers.CharField(allow_blank=True,)
    def validate(self,data,*args,**kwargs):
        lat=data['lat']
        lon=data['lon']
        if not lat or lat=='':
            raise APIException400({
                'message':'Please provide latitude',
                'success':'False',
            })
        if not lon or lon=='':
            raise APIException400({
                'message':'Please provide longitude'
            })
        return data

class ChangeLocationSerializer(serializers.Serializer):
    country=serializers.CharField(allow_blank=True)
    city=serializers.CharField(allow_blank=True)
    def validate(self,data):
        country=data['country']
        city=data['city']
        if not country or country=='':
            raise APIException400({
                'message':'country is required',
                'success':'False',
            })
        if not city or city=='':
            raise APIException400({
                'message':'city is required',
                'success':'False',
            })
        return data
    def create(self, validated_data):
        country=validated_data['country']
        city=validated_data['city']
        user=self.context['request'].user
        ruser=RegisteredUser.objects.filter(user=user).first()
        ruser.country=country
        ruser.city=city
        ruser.save()
        #---------------Arabic Save()----------------------------
        tdata=[]
        tdata.append(country)
        tdata.append(city)
        tres=translate_text_ar(tdata)
        ruser.ar_country=tdata[0].text
        ruser.ar_city=tdata[1].text
        ruser.save()
        #--------------------------------------------------------
        return validated_data
'''
Profile for user------
'''
class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=RegisteredUser
        fields=['profile_image','first_name','last_name','country_code','mobile','email','is_mobile_verified','is_email_verified']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['profile_image']:
            data['profile_image'] = ""
        if not data['last_name']:
            data['last_name'] = ""
        if not data['country_code']:
            data['country_code'] = ""
        if data['is_mobile_verified']:
            data['is_mobile_verified']="True"
        else:
            data['is_mobile_verified']="False"
        if data['is_email_verified']:
            data['is_email_verified']="True"
        else:
            data['is_email_verified']="False"
        return data
class Ar_UserProfileDetailSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    country_code = serializers.SerializerMethodField()
    mobile = serializers.SerializerMethodField()

    class Meta:
        model=RegisteredUser
        fields=['profile_image','first_name','last_name','country_code','mobile','email','is_mobile_verified','is_email_verified']
    def get_first_name(self,instance):
        return instance.ar_first_name
    def get_last_name(self,instance):
        return instance.ar_last_name
    def get_country_code(self,instance):
        return instance.country_code
    def get_mobile(self,instance):
        return instance.mobile
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['profile_image']:
            data['profile_image'] = ""
        if not data['last_name']:
            data['last_name'] = ""
        if not data['country_code']:
            data['country_code'] = ""
        if data['is_mobile_verified']:
            data['is_mobile_verified']="True"
        else:
            data['is_mobile_verified']="False"
        if data['is_email_verified']:
            data['is_email_verified']="True"
        else:
            data['is_email_verified']="False"
        return data
class UserProfileUpdateSerializer(serializers.Serializer):
    profile_image = serializers.ImageField(required=False)
    name = serializers.CharField(max_length=100, allow_blank=True)
    country_code = serializers.CharField(max_length=10, allow_blank=True)
    mobile = serializers.CharField(max_length=10, allow_blank=True)
    email = serializers.CharField(max_length=100, allow_blank=True)
    is_mobile_verified=serializers.CharField(read_only=True)
    is_email_verified=serializers.CharField(read_only=True)
    class Meta:
        model = 'RegisteredUser'
        fields = ('profile_image','name','country_code','mobile','email','is_mobile_verified','is_email_verified')

    def validate(self,data):
        country_code = data['country_code']
        mobile = data['mobile']
        email = data['email']

        if not country_code or country_code=='':
            raise APIException400({
                'success':'False',
                'message':'country_code is required'
            })
        if not mobile or mobile=='':
            raise APIException400({
                'success':'False',
                'message':'mobile is required'
            })
        if not email or email=='':
            raise APIException400({
                'success':'False',
                'message':'email is required'
            })
        if len(mobile)<8:
            raise APIException400({
                'success':'False',
                'message':'Not a valid mobile number'
            })

        allowedDomains = [
        "aol.com", "att.net", "comcast.net", "facebook.com", "gmail.com", "gmx.com", "googlemail.com",
        "google.com", "hotmail.com", "hotmail.co.uk", "mac.com", "me.com", "mail.com", "msn.com",
        "live.com", "sbcglobal.net", "verizon.net", "yahoo.com", "yahoo.co.uk",
        "email.com", "games.com" , "gmx.net", "hush.com", "hushmail.com", "icloud.com", "inbox.com",
        "lavabit.com", "love.com" , "outlook.com", "pobox.com", "rocketmail.com",
        "safe-mail.net", "wow.com", "ygm.com" , "ymail.com", "zoho.com", "fastmail.fm",
        "yandex.com","iname.com"
        ]

        if '@' not in email:
            raise APIException400({
                'success':'False',
                'message':'Email is not valid',
            })
        else:
            domain = email.split('@')[1]
            # if domain not in allowedDomains:
            #     raise APIException400({
            #         'success':'False',
            #         'message':'Not a valid domain',
            #     })
        tempuser = self.context['request'].user
        tempruser = RegisteredUser.objects.filter(user=tempuser).first()

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        ruser = RegisteredUser.objects.filter(user=user).first()

        pimage = self.context['request'].FILES.get('profile_image')
        first_name = validated_data['name'].split(' ')[0]
        last_name=' '.join(validated_data['name'].split(' ')[1:])
        country_code=validated_data['country_code']
        mobile=validated_data['mobile']
        email=validated_data['email']

        user.username=email.split('@')[0]+mobile
        user.first_name=first_name
        user.last_name=last_name
        user.email=email
        user.save()

        ruser.first_name = first_name
        ruser.last_name = last_name
        if pimage:
            ruser.profile_image = pimage
        ruser.country_code = country_code
        ruser.mobile = mobile
        ruser.email = email
        ruser.save()

        #---------------------Arabic save()-------------------------------
        tdata=[]
        tdata.append(first_name)
        tdata.append(last_name)
        
        tdata.append(country_code)
        tdata.append(mobile)

        tres = translate_text_ar(tdata)
        
        user.ar_first_name=first_name
        user.ar_last_name=last_name
        # user.ar_first_name=tres[0].text
        # user.ar_last_name=tres[1].text
        user.save()

        ruser.ar_country_code=country_code
        ruser.ar_mobile=mobile
        # ruser.ar_country_code=tdata[2]
        # ruser.ar_mobile=tdata[3]
        ruser.save()
        #-----------------------------------------------------------------

        validated_data['profile_image'] = ruser.profile_image
        if ruser.language_pref=='2':
            validated_data['name'] = ruser.ar_first_name+' '+ruser.ar_last_name
            validated_data['country_code'] = ruser.country_code
            validated_data['mobile'] = ruser.mobile
        else:
            validated_data['name'] = ruser.first_name+' '+ruser.last_name
            validated_data['country_code'] = ruser.country_code
            validated_data['mobile'] = ruser.mobile
        validated_data['email'] = user.email
        if ruser.is_mobile_verified:
            validated_data['is_mobile_verified']="True"
        else:
            validated_data['is_mobile_verified']="False"
        if ruser.is_email_verified:
            validated_data['is_email_verified']="True"
        else:
            validated_data['is_email_verified']="False"
        return validated_data
class UserLanguagePrefSerializer(serializers.ModelSerializer):
    language_pref=serializers.CharField(max_length=10,allow_blank=True)
    class Meta:
        model=RegisteredUser
        fields=('language_pref',)
    def validate(self,data):
        lang=data['language_pref']
        if not lang or lang=="":
            raise APIException400({
                'message':'please provide language pref',
                'success':'False'
            })
        return data

'''
Customer Complaint-----
'''
class CustomerComplaintSerializer(serializers.ModelSerializer):
    name=serializers.CharField(allow_blank=True,)
    email=serializers.CharField(allow_blank=True,)
    complaint=serializers.CharField(allow_blank=True,)
    class Meta:
        model=CustomerComplaint
        fields=('name','email','complaint')
    def validate(self,data):
        name=data['name']
        email=data['email']
        complaint=data['complaint']

        if not name or name=='':
            raise APIException400({
                'message':'name is required',
                'success':'False',
            })
        if not email or email=='':
            raise APIException400({
                'message':'email is required',
                'success':'False',
            })
        if not complaint or complaint=='':
            raise APIException400({
                'message':'complaint is required',
                'success':'False',
            })
        # email validation
        allowedDomains = [
        "aol.com", "att.net", "comcast.net", "facebook.com", "gmail.com", "gmx.com", "googlemail.com",
        "google.com", "hotmail.com", "hotmail.co.uk", "mac.com", "me.com", "mail.com", "msn.com",
        "live.com", "sbcglobal.net", "verizon.net", "yahoo.com", "yahoo.co.uk",
        "email.com", "games.com" , "gmx.net", "hush.com", "hushmail.com", "icloud.com", "inbox.com",
        "lavabit.com", "love.com" , "outlook.com", "pobox.com", "rocketmail.com",
        "safe-mail.net", "wow.com", "ygm.com" , "ymail.com", "zoho.com", "fastmail.fm",
        "yandex.com","iname.com"
        ]
        if '@' not in email:
            raise APIException400({
                'success':'False',
                'message':'Please provide a valid email',
            })
        else:
            domain = email.split('@')[1]
            # if domain not in allowedDomains:
            #     raise APIException400({
            #         'success':'False',
            #         'message':'un-identified domain name',
            #     })
        return data

    def create(self,validated_data):
        name=validated_data['name']
        email=validated_data['email']
        complaint=validated_data['complaint']

        user=self.context['user'].ruser
        tdata=[]
        tdata.append(name)
        tdata.append(email)
        tdata.append(complaint)
        tres=translate_text_ar(tdata)

        cc=CustomerComplaint(
            name=name,
            email=email,
            complaint=complaint,
            user=user,
            ar_name=name,
            ar_email=email,
            # ar_name=tres[0].text,
            # ar_email=tres[1].text,
            ar_complaint=tres[2].text,
        )
        cc.save()

        if user.language_pref=='2':
            validated_data['complaint']=cc.ar_complaint
        else:
            validated_data['complaint']=cc.complaint
        return validated_data
