from rest_framework import serializers
from rest_framework.exceptions import APIException
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings
from django.conf import settings
# import os

from geopy.geocoders import Nominatim
import base64

from django.core import files
from io import BytesIO
import requests

# from django.contrib.sites.shortcuts import get_current_site.
# from django.contrib.sites.models import Site.

import logging
logger = logging.getLogger('accounts')

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

from _user_panel.uaccounts.models import *
from _serviceprovider_panel.saccounts.models import *
from _user_panel.uaccounts.api.serializers import UserProfileUpdateSerializer
from _user_panel.translation import translate_text_ar
from django.db.models import Q

# service_type_detail_url=serializers.HyperlinkedIdentityField(view_name='spp_accounts:sp_service_subtype',lookup_field='pk')
review_list_url=serializers.HyperlinkedIdentityField(view_name='spp_accounts:sp_garage_review',lookup_field='pk')

class APIException400(APIException):
    status_code = 400

'''
CATEGORY AND VMODEL GET-------
'''
class ServiceTypeListSerializer(serializers.ModelSerializer):
    # subtype_list_url=service_type_detail_url
    id=serializers.CharField()
    class Meta:
        model=ServiceType
        fields=('id','type','icon')#,'subtype_list_url')
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['icon']:
            data['icon'] = ""
        return data

class Ar_ServiceTypeListSerializer(serializers.ModelSerializer):
    # subtype_list_url=service_type_detail_url
    id=serializers.CharField()
    type=serializers.SerializerMethodField()
    class Meta:
        model=ServiceType
        fields=('id','type','icon')#,'subtype_list_url')
    def get_type(self,instance):
        if instance.type_ar:
            return instance.type_ar
        return ''
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['icon']:
            data['icon'] = ""
        return data

class VehicleModelListSerializer(serializers.ModelSerializer):
    class Meta:
        model=VehicleModle
        fields=('id','model_name','icon')
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['icon']:
            data['icon'] = ""
        return data

class Ar_VehicleModelListSerializer(serializers.ModelSerializer):
    model_name=serializers.SerializerMethodField()
    class Meta:
        model=VehicleModle
        fields=('id','model_name','icon')
    def get_model_name(self,instance):
        if instance.model_name_ar:
            return instance.model_name_ar
        return ''
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['icon']:
            data['icon'] = ""
        return data

'''
PROFILE CREATE---------
'''

class CreateGarage(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    is_owner=serializers.CharField(max_length=1,allow_blank=True)
    name=serializers.CharField(max_length=50, allow_blank=True)
    store_image1=serializers.CharField(max_length=500, allow_blank=True)

    store_image2=serializers.CharField(max_length=500, allow_blank=True)
    store_image3=serializers.CharField(max_length=500, allow_blank=True)

    contact_person=serializers.CharField(max_length=70, allow_blank=True)
    lat=serializers.CharField(max_length=20, allow_blank=True)
    lon=serializers.CharField(max_length=20, allow_blank=True)
    location=serializers.CharField(max_length=500, allow_blank=True)
    state=serializers.CharField(max_length=20, allow_blank=True)
    city=serializers.CharField(max_length=20, allow_blank=True)
    country_code=serializers.CharField(max_length=10, allow_blank=True)
    contact_num=serializers.CharField(max_length=15, allow_blank=True)
    tax_registration_num=serializers.CharField(max_length=50, allow_blank=True)
    tax_registration_date=serializers.CharField(max_length=50, allow_blank=True)

    class Meta:
        model=Garage
        fields=('id','is_owner','name','store_image1','store_image2','store_image3','contact_person',
        'lat','lon','location','state','city','country_code','contact_num','tax_registration_num',
        'tax_registration_date')

    def validate(self,data):
        is_owner=data['is_owner']
        name=data['name']
        store_image1=data['store_image1']
        store_image2=data['store_image2']
        store_image3=data['store_image3']
        contact_person=data['contact_person']
        lat=data['lat']
        lon=data['lon']
        location=data['location']
        state=data['state']
        city=data['city']
        country_code=data['country_code']
        contact_num=data['contact_num']
        tax_registration_num=data['tax_registration_num']
        tax_registration_date=data['tax_registration_date']
        if not is_owner or is_owner=="":
            raise APIException400({
                'success':'False',
                'message':'is_owner is required',
            })
        if not name or name=='':
            raise APIException400({
                'success':'False',
                'message':'name is required',
            })
        # if not store_image1 or store_image1=='':
        #     raise APIException400({
        #         'success':'False',
        #         'message':'store name is required'
        #     })
        # if not store_image2 or store_image2=='':
        #     raise APIException400({
        #         'success':'False',
        #         'message':'store name is required'
        #     })
        # if not store_image3 or store_image3=='':
        #     raise APIException400({
        #         'success':'False',
        #         'message':'store name is required'
        #     })
        if not contact_person or contact_person=='':
            raise APIException400({
                'success':'False',
                'message':'contact person is required'
            })
        if not lat or lat=='':
            raise APIException400({
                'success':'False',
                'message':'lat is required'
            })
        if not lon or lon=='':
            raise APIException400({
                'success':'False',
                'message':'lon is required'
            })
        # if not location or location=='':
        #     raise APIException400({
        #         'success':'False',
        #         'message':'location is required'
        #     })
        if not state or state=='':
            raise APIException400({
                'success':'False',
                'message':'state is required'
            })
        if not city or city=='':
            raise APIException400({
                'success':'False',
                'message':'city is required'
            })
        if not country_code or country_code=='':
            raise APIException400({
                'success':'False',
                'message':'country code is required'
            })
        if not contact_num or contact_num=='':
            raise APIException400({
                'success':'False',
                'message':'contact number is required'
            })
        if is_owner not in ('0','1'):
            raise APIException400({
                'success':'False',
                'message':'is_owner value must be either 1 or 0'
            })
        # if not tax_registration_num or tax_registration_num=='':
        #     raise APIException400({
        #         'success':'False',
        #         'message':'tax registration number is required'
        #     })
        # if not tax_registration_date or tax_registration_date=='':
        #     raise APIException400({
        #         'success':'False',
        #         'message':'tax registration date is required'
        #     })
        return data

    def create(self,validated_data):
        user=self.context['ruser']
        is_owner=validated_data['is_owner']
        name=validated_data['name']
        store_image1=validated_data['store_image1']
        store_image2=validated_data['store_image2']
        store_image3=validated_data['store_image3']
        contact_person=validated_data['contact_person']
        lat=validated_data['lat']
        lon=validated_data['lon']
        location=validated_data['location']
        state=validated_data['state']
        city=validated_data['city']
        country_code=validated_data['country_code']
        contact_num=validated_data['contact_num']
        tax_registration_num=validated_data['tax_registration_num']
        tax_registration_date=validated_data['tax_registration_date']

    # Find location if location not provided manually
        if not location or location=="":
            geolocator=Nominatim(user_agent="_serviceprovider_panel.saccounts")
            # data['lat']+', '+data['lon']
            geolocation=geolocator.reverse(lat+', '+lon, language='en')
            if 'address' in geolocation.raw:
                address=geolocation.raw['address']
                for k in address:
                    location=location+address[k]+','
                location=location[:-1]

        is_owner = True if is_owner=='1' else False
        garage=''

        #------------- Arabic Conversion------------------------------
        tdata=[]
        tdata.append(name)
        tdata.append(contact_person)
        tdata.append(location)
        tdata.append(state)
        tdata.append(city)
        tdata.append(country_code)
        tdata.append(contact_num)
        tdata.append(tax_registration_num)
        tres=translate_text_ar(tdata)
        #--------------------------------------------------------------
        if not tax_registration_date or tax_registration_date=="":
            garage=Garage(
                is_owner=is_owner,
                name=name,
                # store_image1=filename1,
                # store_image2=filename2,
                # store_image3=filename3,
                contact_person=contact_person,
                lat=lat,
                lon=lon,
                location=location,
                state=state,
                city=city,
                country_code=country_code,
                contact_num=contact_num,
                tax_registration_num=tax_registration_num,
                user=user,
                ar_name=name,
                # ar_name=tres[0].text,
                ar_contact_person=tres[1].text,
                ar_location=tres[2].text,
                ar_state=tres[3].text,
                ar_city=tres[4].text,
                ar_country_code=tres[5].text,
                ar_contact_num=tres[6].text,
                ar_tax_registration_num=tres[7].text,
            )
        else:
            garage=Garage(
                is_owner=is_owner,
                name=name,
                # store_image1=filename1,
                # store_image2=filename2,
                # store_image3=filename3,
                contact_person=contact_person,
                lat=lat,
                lon=lon,
                location=location,
                state=state,
                city=city,
                country_code=country_code,
                contact_num=contact_num,
                tax_registration_num=tax_registration_num,
                tax_registration_date=tax_registration_date,
                user=user,
                ar_name=name,
                # ar_name=tres[0].text,
                ar_contact_person=tres[1].text,
                ar_location=tres[2].text,
                ar_state=tres[3].text,
                ar_city=tres[4].text,
                ar_country_code=tres[5].text,
                ar_contact_num=tres[6].text,
                ar_tax_registration_num=tres[7].text,
            )
        garage.save()

    # convert json string to image88888888888888888888888888888888888
        if store_image1:
            resp = requests.get(store_image1)
            if resp.status_code != requests.codes.ok:
                raise APIException400({
                    'message':'Image is invalid',
                    'success':'False',
                },status=HTTP_400_BAD_REQUEST,)
            fp = BytesIO()
            fp.write(resp.content)
            file_name = store_image1.split("/")[-1]  # There's probably a better way of doing this but this is just a quick example
            garage.store_image1.save(file_name, files.File(fp))

            # path='/'+store_image1.split('0/')[1]
            # print(path)
            # if os.path.isfile(path):
            #     print('file found')
            #     os.remove(path)
            # else:
            #     print('file not found')

            # imgdata = base64.b64decode(store_image1)
            # filename1 = 'garage1.jpg'
            # with open(filename, 'wb') as f:
            #     f.write(imgdata)
        if store_image2:
            resp = requests.get(store_image2)
            if resp.status_code != requests.codes.ok:
                raise APIException400({
                    'message':'Image is invalid',
                    'success':'False',
                },status=HTTP_400_BAD_REQUEST,)
            fp = BytesIO()
            fp.write(resp.content)
            file_name = store_image2.split("/")[-1]  # There's probably a better way of doing this but this is just a quick example
            garage.store_image2.save(file_name, files.File(fp))
            # imgdata = base64.b64decode(store_image2)
            # filename2 = 'garage2.jpg'
            # with open(filename, 'wb') as f:
            #     f.write(imgdata)
        if store_image3:
            resp = requests.get(store_image3)
            if resp.status_code != requests.codes.ok:
                raise APIException400({
                    'message':'Image is invalid',
                    'success':'False',
                },status=HTTP_400_BAD_REQUEST,)
            fp = BytesIO()
            fp.write(resp.content)
            file_name = store_image3.split("/")[-1]  # There's probably a better way of doing this but this is just a quick example
            garage.store_image3.save(file_name, files.File(fp))
            # imgdata = base64.b64decode(store_image3)
            # filename3 = 'garage3.jpg'
            # with open(filename, 'wb') as f:
            #     f.write(imgdata)

        validated_data['id']=garage.id
        validated_data['store_image1']=garage.store_image1
        validated_data['store_image2']=garage.store_image2
        validated_data['store_image3']=garage.store_image3
        validated_data['location']=garage.location

        return validated_data

class CreateSchedule(serializers.ModelSerializer):
    day=serializers.CharField(max_length=10, allow_blank=True)
    start_time=serializers.CharField(max_length=10, allow_blank=True)
    end_time=serializers.CharField(max_length=10, allow_blank=True)

    class Meta:
        model=WeeklySchedule
        fields=('day','start_time','end_time')

    def create(self,validated_data):
        garage=self.context['garage']

        day=validated_data['day']
        start_time=validated_data['start_time']
        end_time=validated_data['end_time']

        ws=WeeklySchedule(
            garage=garage,
            day=day,
            start_time=start_time,
            end_time=end_time,
        )
        ws.save()

        return validated_data

class CreateCategory(serializers.ModelSerializer):
    type=serializers.CharField(max_length=50, allow_blank=True)

    class Meta:
        model=Garage
        fields=('type',)

    def validate(self,data):
        type=data['type']
        if not type or type=='':
            raise APIException400({
                'success':'False',
                'message':'type is required'
            })
        return data

    def create(self,validated_data):
        garage=self.context['garage']
        type=validated_data['type']

        stype=ServiceType.objects.filter(Q(type__iexact=type)|Q(type_ar__iexact=type)).first()

        cm=CategoryManager(
            garage=garage,
            category=stype,
        )
        cm.save()

        return validated_data

class CreateVehicleModel(serializers.ModelSerializer):
    model_name=serializers.CharField(max_length=50, allow_blank=True)

    class Meta:
        model=Garage
        fields=('model_name',)

    def validate(self,data):
        vehicle_model=data['model_name']
        if not vehicle_model or vehicle_model=='':
            raise APIException400({
                'success':'False',
                'message':'model_name is required'
            })
        return data

    def create(self,validated_data):
        garage=self.context['garage']
        vehicle_model=validated_data['model_name']

        vmodel=VehicleModle.objects.filter(Q(model_name__iexact=vehicle_model)|Q(model_name_ar__iexact=vehicle_model)).first()

        vmm=VehicleModleManager(
            garage=garage,
            vehicle_model=vmodel,
        )
        vmm.save()

        return validated_data

class CreateSubCategory(serializers.ModelSerializer):
    subtype=serializers.CharField(max_length=50, allow_blank=True)

    class Meta:
        model=Garage
        fields=('subtype',)

    def validate(self,data):
        subtype=data['subtype']
        if not subtype or subtype=='':
            raise APIException400({
                'success':'False',
                'message':'subtype is required'
            })
        return data

    def create(self,validated_data):
        garage=self.context['garage']
        subtype=validated_data['subtype']

        sstype=ServiceSubType.objects.filter(Q(subtype__iexact=subtype)|Q(subtype_ar__iexact=subtype)).first()

        scm=SubCategoryManager(
            garage=garage,
            subcategory=sstype,
        )
        scm.save()

        return validated_data

'''
PROFIEL GET--------
'''

class ServiceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model=RegisteredUser
        fields=('id','profile_image','first_name','last_name','country_code','mobile','email','is_mobile_verified','is_email_verified')
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['profile_image']:
            data['profile_image'] = ""
        if not data['last_name']:
            data['last_name'] = ""
        if data['is_mobile_verified']:
            data['is_mobile_verified']="True"
        else:
            data['is_mobile_verified']="False"
        if data['is_email_verified']:
            data['is_email_verified']="True"
        else:
            data['is_email_verified']="False"
        return data
class Ar_ServiceProviderSerializer(serializers.ModelSerializer):
    first_name=serializers.SerializerMethodField()
    last_name=serializers.SerializerMethodField()
    country_code=serializers.SerializerMethodField()
    mobile=serializers.SerializerMethodField()

    class Meta:
        model=RegisteredUser
        fields=('id','profile_image','first_name','last_name','country_code','mobile','email','is_mobile_verified','is_email_verified')
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['profile_image']:
            data['profile_image'] = ""
        if not data['last_name']:
            data['last_name'] = ""
        if data['is_mobile_verified']:
            data['is_mobile_verified']="True"
        else:
            data['is_mobile_verified']="False"
        if data['is_email_verified']:
            data['is_email_verified']="True"
        else:
            data['is_email_verified']="False"
        return data
    def get_first_name(self,instance):
        return instance.ar_first_name
    def get_last_name(self,instance):
        if instance.ar_last_name:
            return instance.ar_last_name
    def get_country_code(self,instance):
        return instance.country_code
    def get_mobile(self,instance):
        return instance.mobile

class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=ServiceType
        fields=('type','icon')
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['icon']:
            data['icon'] = ""
        return data
class Ar_ServiceTypeSerializer(serializers.ModelSerializer):
    type=serializers.SerializerMethodField()
    class Meta:
        model=ServiceType
        fields=('type','icon')
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['icon']:
            data['icon'] = ""
        return data
    def get_type(self,instance):
        return instance.type_ar

class VehicleModleSerializer(serializers.ModelSerializer):
    class Meta:
        model=VehicleModle
        fields=('model_name','icon')
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['icon']:
            data['icon'] = ""
        return data
class Ar_VehicleModleSerializer(serializers.ModelSerializer):
    model_name=serializers.SerializerMethodField()
    class Meta:
        model=VehicleModle
        fields=('model_name','icon')
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['icon']:
            data['icon'] = ""
        return data
    def model_name(self,instance):
        return instance.model_name_ar

class ServiceSubTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=ServiceSubType
        fields=('subtype','icon')
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['icon']:
            data['icon'] = ""
        return data
class Ar_ServiceSubTypeSerializer(serializers.ModelSerializer):
    subtype=serializers.SerializerMethodField()
    class Meta:
        model=ServiceSubType
        fields=('subtype','icon')
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['icon']:
            data['icon'] = ""
        return data
    def get_subtype(self,instance):
        return instance.subtype_ar

class WeeklyScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model=WeeklySchedule
        fields=('day','start_time','end_time')

class GarageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Garage
        fields=('id','is_owner','name','store_image1','store_image2','store_image3','contact_person','lat',
        'lon','location','state','city','country_code','contact_num','tax_registration_num',
        'tax_registration_date')
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['store_image1']:
            data['store_image1'] = ""
        if not data['store_image2']:
            data['store_image2'] = ""
        if not data['store_image3']:
            data['store_image3'] = ""
        if not data['tax_registration_num']:
            data['tax_registration_num'] = ""
        if not data['tax_registration_date']:
            data['tax_registration_date'] = ""
        return data
class Ar_GarageSerializer(serializers.ModelSerializer):
    name=serializers.SerializerMethodField()
    contact_person=serializers.SerializerMethodField()
    location=serializers.SerializerMethodField()
    state=serializers.SerializerMethodField()
    city=serializers.SerializerMethodField()
    country_code=serializers.SerializerMethodField()
    contact_num=serializers.SerializerMethodField()
    tax_registration_num=serializers.SerializerMethodField()
    class Meta:
        model=Garage
        fields=('id','is_owner','name','store_image1','store_image2','store_image3','contact_person','lat',
        'lon','location','state','city','country_code','contact_num','tax_registration_num',
        'tax_registration_date')
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['store_image1']:
            data['store_image1'] = ""
        if not data['store_image2']:
            data['store_image2'] = ""
        if not data['store_image3']:
            data['store_image3'] = ""
        if not data['tax_registration_num']:
            data['tax_registration_num'] = ""
        if not data['tax_registration_date']:
            data['tax_registration_date'] = ""
        return data
    def get_name(self,instance):
        return instance.ar_name
    def get_contact_person(self,instance):
        return instance.ar_contact_person
    def get_location(self,instance):
        return instance.ar_location
    def get_state(self,instance):
        return instance.ar_state
    def get_city(self,instance):
        return instance.ar_city
    def get_country_code(self,instance):
        return instance.country_code
    def get_contact_num(self,instance):
        return instance.contact_num
    def get_tax_registration_num(self,instance):
        return instance.tax_registration_num

class ServiceProviderProfileSerializer(serializers.ModelSerializer):
    owner_profile=serializers.SerializerMethodField()
    garage_detail=serializers.SerializerMethodField()
    category_detail=serializers.SerializerMethodField()
    subcategory_detail=serializers.SerializerMethodField()
    vehicle_model_detail=serializers.SerializerMethodField()
    schedule_detail=serializers.SerializerMethodField()
    class Meta:
        model=Garage
        fields=('owner_profile','garage_detail','category_detail','subcategory_detail','vehicle_model_detail','schedule_detail')

    def get_owner_profile(self,garage):
        if garage is not None:
            instance=garage.user
            data=ServiceProviderSerializer(instance,context={'request':self.context['request']}).data
            return data
    def get_garage_detail(self,garage):
        if garage is not None:
            instance=garage
            data=GarageSerializer(instance,context={'request':self.context['request']}).data
            return data
    def get_category_detail(self,garage):
        if garage is not None:
            instance=garage.service_type
            data=ServiceTypeSerializer(instance,many=True,context={'request':self.context['request']}).data
            return data
    def get_subcategory_detail(self,garage):
        if garage is not None:
            instance=garage.service_subtype
            data=ServiceSubTypeSerializer(instance,many=True,context={'request':self.context['request']}).data
            return data
    def get_vehicle_model_detail(self,garage):
        if garage is not None:
            instance=garage.vehicle_model#************
            data=VehicleModleSerializer(instance,many=True,context={'request':self.context['request']}).data
            return data
    def get_schedule_detail(self,garage):
        if garage is not None:
            queryset=WeeklySchedule.objects.filter(garage=garage)
            data=WeeklyScheduleSerializer(queryset,many=True).data
            return data
class Ar_ServiceProviderProfileSerializer(serializers.ModelSerializer):
    owner_profile=serializers.SerializerMethodField()
    garage_detail=serializers.SerializerMethodField()
    category_detail=serializers.SerializerMethodField()
    subcategory_detail=serializers.SerializerMethodField()
    vehicle_model_detail=serializers.SerializerMethodField()
    schedule_detail=serializers.SerializerMethodField()
    class Meta:
        model=Garage
        fields=('owner_profile','garage_detail','category_detail','subcategory_detail','vehicle_model_detail','schedule_detail')

    def get_owner_profile(self,garage):
        if garage is not None:
            instance=garage.user
            data=Ar_ServiceProviderSerializer(instance,context={'request':self.context['request']}).data
            return data
    def get_garage_detail(self,garage):
        if garage is not None:
            instance=garage
            data=Ar_GarageSerializer(instance,context={'request':self.context['request']}).data
            return data
    def get_category_detail(self,garage):
        if garage is not None:
            instance=garage.service_type
            data=Ar_ServiceTypeSerializer(instance,many=True,context={'request':self.context['request']}).data
            return data
    def get_subcategory_detail(self,garage):
        if garage is not None:
            instance=garage.service_subtype
            data=Ar_ServiceSubTypeSerializer(instance,many=True,context={'request':self.context['request']}).data
            return data
    def get_vehicle_model_detail(self,garage):
        if garage is not None:
            instance=garage.vehicle_model#************
            data=Ar_VehicleModleSerializer(instance,many=True,context={'request':self.context['request']}).data
            return data
    def get_schedule_detail(self,garage):
        if garage is not None:
            queryset=WeeklySchedule.objects.filter(garage=garage)
            data=WeeklyScheduleSerializer(queryset,many=True).data
            return data

'''
UPDATE POST-------
'''

class UpdateOwner(serializers.ModelSerializer):
    profile_image = serializers.CharField(max_length=500, allow_blank=True)
    name = serializers.CharField(max_length=100, allow_blank=True)
    country_code = serializers.CharField(max_length=10, allow_blank=True)
    mobile = serializers.CharField(max_length=10, allow_blank=True)
    email = serializers.CharField(max_length=100, allow_blank=True)

    class Meta:
        model = RegisteredUser
        fields = ('profile_image','name','country_code','mobile','email')

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
            if domain not in allowedDomains:
                raise APIException400({
                    'success':'False',
                    'message':'Not a valid domain',
                })
        tempuser = self.context['request'].user
        tempruser = RegisteredUser.objects.filter(user=tempuser).first()

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        ruser = RegisteredUser.objects.filter(user=user).first()

        # pimage = self.context['request'].FILES.get('profile_image')
        pimage = validated_data['profile_image']
        first_name = validated_data['name'].split(' ')[0]
        last_name=' '.join(validated_data['name'].split(' ')[1:])
        country_code=validated_data['country_code']
        mobile=validated_data['mobile']
        email=validated_data['email']

        # convert json string to image
        # if pimage:
        #     imgdata = base64.b64decode(pimage)
        #     filename = 'garage_owner.jpg'
        #     with open(filename, 'wb') as f:
        #         f.write(imgdata)

        #-------------------Arabic Conversion-----------------------------------
        tdata=[]
        tdata.append(first_name)
        tdata.append(last_name)
        tdata.append(country_code)
        tdata.append(mobile)
        tres=translate_text_ar(tdata)

        user.username=email.split('@')[0]+mobile
        user.first_name=first_name
        user.last_name=last_name
        user.email=email
        user.save()

        ruser.first_name = first_name
        ruser.last_name = last_name
        # ruser.profile_image = filename
        ruser.country_code = country_code
        ruser.mobile = mobile
        ruser.email = email
        ruser.ar_first_name=first_name
        ruser.ar_last_name=last_name
        ruser.ar_country_code=country_code
        ruser.ar_mobile=mobile
        # ruser.ar_first_name=tres[0].text
        # ruser.ar_last_name=tres[1].text
        # ruser.ar_country_code=tres[2].text
        # ruser.ar_mobile=tres[3].text

        try:
            ruser.save()
        except:
            print('some db errors')

        if pimage:
            resp = requests.get(pimage)
            if resp.status_code != requests.codes.ok:
                raise APIException400({
                    'message':'Image is invalid',
                    'success':'False',
                },status=HTTP_400_BAD_REQUEST,)
            fp = BytesIO()
            fp.write(resp.content)
            file_name = pimage.split("/")[-1]  # There's probably a better way of doing this but this is just a quick example
            ruser.profile_image.save(file_name, files.File(fp))

        validated_data['profile_image'] = ruser.profile_image
        # validated_data['name'] = ruser.first_name+' '+ruser.last_name
        # validated_data['country_code'] = ruser.country_code
        # validated_data['mobile'] = ruser.mobile
        # validated_data['email'] = user.email

        return validated_data
class UpdateGarage(serializers.ModelSerializer):
    id=serializers.CharField(allow_blank=True)
    is_owner=serializers.CharField(max_length=1,allow_blank=True)
    name=serializers.CharField(max_length=50, allow_blank=True)
    store_image1=serializers.CharField(max_length=500, allow_blank=True)
    store_image2=serializers.CharField(max_length=500, allow_blank=True)
    store_image3=serializers.CharField(max_length=500, allow_blank=True)
    contact_person=serializers.CharField(max_length=70, allow_blank=True)
    lat=serializers.CharField(max_length=20, allow_blank=True)
    lon=serializers.CharField(max_length=20, allow_blank=True)
    location=serializers.CharField(max_length=500, allow_blank=True)
    state=serializers.CharField(max_length=20, allow_blank=True)
    city=serializers.CharField(max_length=20, allow_blank=True)
    country_code=serializers.CharField(max_length=10, allow_blank=True)
    contact_num=serializers.CharField(max_length=15, allow_blank=True)
    tax_registration_num=serializers.CharField(max_length=50, allow_blank=True)
    tax_registration_date=serializers.CharField(max_length=50, allow_blank=True)

    class Meta:
        model=Garage
        fields=('id','is_owner','name','store_image1','store_image2','store_image3','contact_person','lat',
        'lon','location','state','city','country_code','contact_num','tax_registration_num',
        'tax_registration_date')

    def validate(self,data):
        id=data['id']
        is_owner=data['is_owner']
        name=data['name']
        store_image1=data['store_image1']
        store_image2=data['store_image2']
        store_image3=data['store_image3']
        contact_person=data['contact_person']
        lat=data['lat']
        lon=data['lon']
        location=data['location']
        state=data['state']
        city=data['city']
        country_code=data['country_code']
        contact_num=data['contact_num']
        tax_registration_num=data['tax_registration_num']
        tax_registration_date=data['tax_registration_date']

        if not id or id=="":
            raise APIException400({
                'success':'False',
                'message':'id is required',
            })

        if not is_owner or is_owner=="":
            raise APIException400({
                'success':'False',
                'message':'is_owner is required',
            })
        if not name or name=='':
            raise APIException400({
                'success':'False',
                'message':'name is required',
            })
        # if not store_image1 or store_image1=='':
        #     raise APIException400({
        #         'success':'False',
        #         'message':'store name is required'
        #     })
        # if not store_image2 or store_image2=='':
        #     raise APIException400({
        #         'success':'False',
        #         'message':'store name is required'
        #     })
        # if not store_image3 or store_image3=='':
        #     raise APIException400({
        #         'success':'False',
        #         'message':'store name is required'
        #     })
        if not contact_person or contact_person=='':
            raise APIException400({
                'success':'False',
                'message':'contact person is required'
            })
        if not lat or lat=='':
            raise APIException400({
                'success':'False',
                'message':'lat is required'
            })
        if not lon or lon=='':
            raise APIException400({
                'success':'False',
                'message':'lon is required'
            })
        # if not location or location=='':
        #     raise APIException400({
        #         'success':'False',
        #         'message':'location is required'
        #     })
        if not state or state=='':
            raise APIException400({
                'success':'False',
                'message':'state is required'
            })
        if not city or city=='':
            raise APIException400({
                'success':'False',
                'message':'city is required'
            })
        if not country_code or country_code=='':
            raise APIException400({
                'success':'False',
                'message':'country code is required'
            })
        if not contact_num or contact_num=='':
            raise APIException400({
                'success':'False',
                'message':'contact number is required'
            })
        if is_owner not in ('0','1'):
            raise APIException400({
                'success':'False',
                'message':'is_owner value must be either 1 or 0'
            })
        # if not tax_registration_num or tax_registration_num=='':
        #     raise APIException400({
        #         'success':'False',
        #         'message':'tax registration number is required'
        #     })
        # if not tax_registration_date or tax_registration_date=='':
        #     raise APIException400({
        #         'success':'False',
        #         'message':'tax registration date is required'
        #     })
        return data

    def create(self,validated_data):
        garage = self.context['garage']

        id=validated_data['id']
        is_owner=validated_data['is_owner']
        name=validated_data['name']
        store_image1=validated_data['store_image1']
        store_image2=validated_data['store_image2']
        store_image3=validated_data['store_image3']
        contact_person=validated_data['contact_person']
        lat=validated_data['lat']
        lon=validated_data['lon']
        location=validated_data['location']
        state=validated_data['state']
        city=validated_data['city']
        country_code=validated_data['country_code']
        contact_num=validated_data['contact_num']
        tax_registration_num=validated_data['tax_registration_num']
        tax_registration_date=validated_data['tax_registration_date']

        # convert json string to image
        # if store_image1:
        #     imgdata = base64.b64decode(store_image1)
        #     filename1 = 'garage1.jpg'
        #     with open(filename, 'wb') as f:
        #         f.write(imgdata)
        # if store_image2:
        #     imgdata = base64.b64decode(store_image2)
        #     filename1 = 'garage1.jpg'
        #     with open(filename, 'wb') as f:
        #         f.write(imgdata)
        # if store_image3:
        #     imgdata = base64.b64decode(store_image3)
        #     filename1 = 'garage1.jpg'
        #     with open(filename, 'wb') as f:
        #         f.write(imgdata)
        # Find location if location not provided manually
        if not location or location=="":
            geolocator=Nominatim(user_agent="_serviceprovider_panel.saccounts")
            # data['lat']+', '+data['lon']
            geolocation=geolocator.reverse(lat+', '+lon, language='en')
            if 'address' in geolocation.raw:
                address=geolocation.raw['address']
                for k in address:
                    location=location+address[k]+','
                location=location[:-1]

        is_owner = True if is_owner=='1' else False

        #-----------Arabic Conversion----------------------------------
        tdata=[]
        tdata.append(name)
        tdata.append(contact_person)
        tdata.append(location)
        tdata.append(state)
        tdata.append(city)
        tdata.append(country_code)
        tdata.append(contact_num)
        tdata.append(tax_registration_num)
        tres=translate_text_ar(tdata)

        garage.is_owner=is_owner
        garage.name=name
        # if filename1:
            # garage.store_image1=filename1
        # if filename2:
            # garage.store_image2=filename2
        # if filename3:
            # garage.store_image3=filename3
        garage.contact_person=contact_person
        garage.lat=lat
        garage.lon=lon
        garage.location=location
        garage.state=state
        garage.city=city
        garage.country_code=country_code
        garage.contact_num=contact_num
        garage.tax_registration_num=tax_registration_num
        if garage.tax_registration_date:
            garage.tax_registration_date=tax_registration_date

        garage.ar_name=name
        # garage.ar_name=tres[0].text
        garage.ar_contact_person=tres[1].text
        garage.ar_location=tres[2].text
        garage.ar_state=tres[3].text
        garage.ar_city=tres[4].text
        garage.ar_country_code=tres[5].text
        garage.ar_contact_num=tres[6].text
        garage.ar_tax_registration_num=tres[7].text
        
        garage.save()

        if store_image1:
            resp = requests.get(store_image1)
            if resp.status_code != requests.codes.ok:
                raise APIException400({
                    'message':'Image is invalid',
                    'success':'False',
                },status=HTTP_400_BAD_REQUEST,)
            fp = BytesIO()
            fp.write(resp.content)
            file_name = store_image1.split("/")[-1]  # There's probably a better way of doing this but this is just a quick example
            garage.store_image1.save(file_name, files.File(fp))

        if store_image2:
            resp = requests.get(store_image2)
            if resp.status_code != requests.codes.ok:
                raise APIException400({
                    'message':'Image is invalid',
                    'success':'False',
                },status=HTTP_400_BAD_REQUEST,)
            fp = BytesIO()
            fp.write(resp.content)
            file_name = store_image2.split("/")[-1]  # There's probably a better way of doing this but this is just a quick example
            garage.store_image2.save(file_name, files.File(fp))

        if store_image3:
            resp = requests.get(store_image3)
            if resp.status_code != requests.codes.ok:
                raise APIException400({
                    'message':'Image is invalid',
                    'success':'False',
                },status=HTTP_400_BAD_REQUEST,)
            fp = BytesIO()
            fp.write(resp.content)
            file_name = store_image3.split("/")[-1]  # There's probably a better way of doing this but this is just a quick example
            garage.store_image3.save(file_name, files.File(fp))

        validated_data['store_image1']=garage.store_image1
        validated_data['store_image2']=garage.store_image2
        validated_data['store_image3']=garage.store_image3
        validated_data['location']=garage.location

        return validated_data
class UpdateCategory(serializers.ModelSerializer):
    type=serializers.CharField(max_length=50, allow_blank=True)

    class Meta:
        model=Garage
        fields=('type',)

    def validate(self,data):
        type=data['type']
        if not type or type=='':
            raise APIException400({
                'success':'False',
                'message':'type is required'
            })
        return data

    def create(self,validated_data):
        garage=self.context['garage']
        type=validated_data['type']

        stype=ServiceType.objects.filter(Q(type__iexact=type)|Q(type_ar__iexact=type)).first()
        cm=CategoryManager.objects.filter(garage=garage,category=stype).first()

        if cm:
            cm.category=stype
            cm.save()
        else:
            cm=CategoryManager(
                garage=garage,
                category=stype,
            )
            cm.save()

        return validated_data
class UpdateSubCategory(serializers.ModelSerializer):
    subtype=serializers.CharField(max_length=50, allow_blank=True)

    class Meta:
        model=Garage
        fields=('subtype',)

    def validate(self,data):
        subtype=data['subtype']
        if not subtype or subtype=='':
            raise APIException400({
                'success':'False',
                'message':'subtype is required'
            })
        return data

    def create(self,validated_data):
        garage=self.context['garage']
        subtype=validated_data['subtype']

        sstype=ServiceSubType.objects.filter(Q(subtype__iexact=subtype)|Q(subtype_ar__iexact=subtype)).first()
        scm=SubCategoryManager.objects.filter(garage=garage,subcategory=sstype).first()

        if scm:
            scm.subcategory=sstype
            scm.save()
        else:
            scm=SubCategoryManager(
                garage=garage,
                subcategory=sstype,
            )
            scm.save()


        return validated_data
class UpdateVehicleModel(serializers.ModelSerializer):
    model_name=serializers.CharField(max_length=50, allow_blank=True)

    class Meta:
        model=Garage
        fields=('model_name',)

    def validate(self,data):
        vehicle_model=data['model_name']
        if not vehicle_model or vehicle_model=='':
            raise APIException400({
                'success':'False',
                'message':'model_name is required'
            })
        return data

    def create(self,validated_data):
        garage=self.context['garage']
        vehicle_model=validated_data['model_name']

        vmodel=VehicleModle.objects.filter(Q(model_name__iexact=vehicle_model)|Q(model_name_ar__iexact=vehicle_model)).first()
        vmm=VehicleModleManager.objects.filter(garage=garage,vehicle_model=vmodel).first()

        if vmm:
            vmm.vehicle_model=vmodel
            vmm.save()
        else:
            vmm=VehicleModleManager(
                garage=garage,
                vehicle_model=vmodel,
            )
            vmm.save()

        return validated_data
class UpdateSchedule(serializers.ModelSerializer):
    day=serializers.CharField(max_length=10, allow_blank=True)
    start_time=serializers.CharField(max_length=10, allow_blank=True)
    end_time=serializers.CharField(max_length=10, allow_blank=True)

    class Meta:
        model=WeeklySchedule
        fields=('day','start_time','end_time')

    def create(self,validated_data):
        garage=self.context['garage']
        day=validated_data['day']
        start_time=validated_data['start_time']
        end_time=validated_data['end_time']
        
        ws=WeeklySchedule.objects.filter(garage=garage,day=day).first()


        print('---------')
        print(day)
        print(start_time)
        print(end_time)
        if ws:
            print('inside update')
            ws.day=day
            ws.start_time=start_time
            ws.end_time=end_time
            ws.save()
        else:
            print('inside create')
            w_obj=WeeklySchedule(
                garage=garage,
                day=day,
                start_time=start_time,
                end_time=end_time,
            )
            w_obj.save()

        return validated_data

# class ServiceProviderProfileUpdateSerializer(serializers.ModelSerializer):
#     owner_profile=serializers.SerializerMethodField()
#     garage_detail=serializers.SerializerMethodField()
#     category_detail=serializers.SerializerMethodField()
#     subcategory_detail=serializers.SerializerMethodField()
#     schedule_detail=serializers.SerializerMethodField()
#     class Meta:
#         model=Garage
#         fields=('owner_profile','garage_detail','category_detail','subcategory_detail','schedule_detail')
#
#     def get_owner_profile(self,data):
#         print(data)
#         request=self.context['request']
#         garage=self.context['garage']
#         data_owner=data['owner_profile']
#         data=data_owner
#         if data_owner is not None:
#             ruser=garage.user
#             serializer=UpdateOwner(data=data_owner, context={'request':request,'ruser':ruser})
#             if serializer.is_valid():
#                 serializer.save()
#                 data=serializer.data
#         return data
#     def get_garage_detail(self,data):
#         request=self.context['request']
#         garage=self.context['garage']
#         data_garage=data['data_garage']
#         data=data_garage
#         if data_garage is not None:
#             serializer=UpdateGarage(data=data_garage, context={'request':request,'garage':garage})
#             if serializer.is_valid():
#                 serializer.save()
#                 data=serializer.data
#         return data
#     def get_category_detail(self,data):
#         request=self.context['request']
#         garage=self.context['garage']
#         data_category=data['data_category']
#         data=data_category
#         if data_category is not None:
#             serializer=UpdateCategory(data=data_category, many=True, context={'request':request,'garage':garage})
#             if serializer.is_valid():
#                 serializer.save()
#                 data=serializer.data
#         return data
#     def get_subcategory_detail(self,data):
#         request=self.context['request']
#         garage=self.context['garage']
#         data_subcategory=data['data_subcategory']
#         data=data_subcategory
#         if data_subcategory is not None:
#             serializer=UpdateSubCategory(data=data_subcategory, many=True, context={'request':request,'garage':garage})
#             if serializer.is_valid():
#                 serializer.save()
#                 data=serializer.data
#         return data
#     def get_schedule_detail(self,data):
#         request=self.context['request']
#         garage=self.context['garage']
#         data_schedule=data['data_schedule']
#         data=data_schedule
#         if data_schedule is not None:
#             serializer=UpdateSchedule(data=data_subcategory, many=True, context={'request':request,'garage':garage})
#             if serializer.is_valid():
#                 serializer.save()
#                 data=serializer.data
#         return data

'''
GARAGE LIST FOR A SERVICE PROVIDER-------
'''

class ServiceProviderGarageListSerializer(serializers.ModelSerializer):
    review_list_url=review_list_url
    class Meta:
        model=Garage
        fields=('id','name','review_list_url')
class Ar_ServiceProviderGarageListSerializer(serializers.ModelSerializer):
    review_list_url=review_list_url
    name=serializers.SerializerMethodField()
    class Meta:
        model=Garage
        fields=('id','name','review_list_url')
    def get_name(self,instance):
        return instance.ar_name