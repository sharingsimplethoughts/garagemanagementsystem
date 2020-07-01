from django.views.generic import TemplateView
from rest_framework.views import (APIView,)
from rest_framework.generics import (ListAPIView,RetrieveAPIView,)
from rest_framework.permissions import (IsAuthenticated,)
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.authentication import  JSONWebTokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.status import (
                                        HTTP_200_OK,
                                    	HTTP_400_BAD_REQUEST,
                                    	HTTP_204_NO_CONTENT,
                                    	HTTP_201_CREATED,
                                    	HTTP_500_INTERNAL_SERVER_ERROR,
                                    )
# from django.core.cache import cache


from rest_framework_jwt.settings import api_settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

#..

import logging
logger = logging.getLogger('accounts')

from _user_panel.uaccounts.models import *
from _serviceprovider_panel.saccounts.models import *
from .serializers import *
from _user_panel.uaccounts.api.serializers import UserProfileUpdateSerializer
from _user_panel.ugarage.api.serializers import GarageReviewSerializer,Ar_GarageReviewSerializer

class ServiceProviderProfileCreateView(APIView):
    # permission_classes=(IsAuthenticated,)
    # authentication_classes=(JSONWebTokenAuthentication,)
    def post(self,request,*args,**kwargs):
        logger.debug('service provider profile post called')
        logger.debug(request.data)
        data=request.data
        id=self.kwargs['pk']
        # user=User.objects.filter(id=id).first()
        ruser=RegisteredUser.objects.filter(id=id).first()
        g_obj=Garage.objects.filter(user=ruser).first()
        if g_obj:
            return Response({
                'success':'False',
                'message':'You have already created a garage earlier.',
            },status=HTTP_400_BAD_REQUEST)

        data_garage=data['garage_detail']
        data_category=data['category_detail']
        data_subcategory=data['subcategory_detail']
        data_vehicle_model=data['vehicle_model_detail']
        data_schedule=data['schedule_detail']

        serializer2=CreateGarage(data=data_garage, context={'request':request,'ruser':ruser})

        if serializer2.is_valid():
            serializer2.save()
            data2=serializer2.data
            garage_id=data2['id']

            garage=Garage.objects.filter(id=garage_id).first()
            serializer3=CreateCategory(data=data_category,many=True, context={'request':request,'garage':garage})
            serializer4=CreateSubCategory(data=data_subcategory,many=True, context={'request':request,'garage':garage})
            serializer6=CreateVehicleModel(data=data_vehicle_model,many=True, context={'request':request,'garage':garage})
            serializer5=CreateSchedule(data=data_schedule,many=True, context={'request':request,'garage':garage})

            if serializer3.is_valid():
                if serializer4.is_valid():
                    if serializer6.is_valid():
                        if serializer5.is_valid():

                            serializer3.save()
                            serializer4.save()
                            serializer6.save()
                            serializer5.save()

                            data3=serializer3.data
                            data4=serializer4.data
                            data5=serializer5.data

                            # data={}
                            # payload = jwt_payload_handler(ruser.user)
                            # token = jwt_encode_handler(payload)
                            # token = 'JWT '+token
                            # data['token'] = token

                            return Response({
                                'success':'True',
                                'message':'Data updated successfully.',
                                # 'data':data,
                            },status=HTTP_200_OK)
                        else:
                            logger.debug(serializer5.errors)
                            return Response({
                                'message':'Some problems',
                                'success':'False',
                                'data':serializer5.errors,
                            },status=HTTP_400_BAD_REQUEST,)
                    else:
                        logger.debug(serializer6.errors)
                        return Response({
                            'message':'Some problems',
                            'success':'False',
                            'data':serializer6.errors,
                        },status=HTTP_400_BAD_REQUEST,)
                else:
                    logger.debug(serializer4.errors)
                    return Response({
                        'message':'Some problems',
                        'success':'False',
                        'data':serializer4.errors,
                    },status=HTTP_400_BAD_REQUEST,)
            else:
                logger.debug(serializer3.errors)
                return Response({
                    'message':'Some problems',
                    'success':'False',
                    'data':serializer3.errors,
                },status=HTTP_400_BAD_REQUEST,)
        else:
            logger.debug(serializer2.errors)
            return Response({
                'message':'Some problems',
                'success':'False',
                'data':serializer2.errors,
            },status=HTTP_400_BAD_REQUEST,)

class ServiceProviderProfileUpdateView(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    def get(self,request,*args,**kwargs):
        logger.debug('service provider profile get called')
        logger.debug(request.data)
        user=request.user
        ruser=RegisteredUser.objects.filter(user=user).first()
        queryset=Garage.objects.filter(user=ruser)
        if ruser.language_pref=='2':
            serializer=Ar_ServiceProviderProfileSerializer(queryset,many=True,context={'request':request})
        else:
            serializer=ServiceProviderProfileSerializer(queryset,many=True,context={'request':request})
        data=serializer.data
        return Response({
            'message':'data retrieved successfully',
            'success':'True',
            'data':data,
        },status=HTTP_200_OK,)

    def post(self,request,*args,**kwargs):
        logger.debug('service provider profile post called')
        logger.debug(request.data)
        data=request.data
        ruser=RegisteredUser.objects.filter(user=request.user).first()
        garage_id=data['garage_detail']['id']
        garage=Garage.objects.filter(id=garage_id).first()
        WeeklySchedule.objects.filter(garage=garage).delete()

        data_owner=data['owner_profile']
        data_garage=data['garage_detail']
        data_category=data['category_detail']
        data_subcategory=data['subcategory_detail']
        data_vehicle_model=data['vehicle_model_detail']
        data_schedule=data['schedule_detail']

        # print(data_owner)
        # print(data_garage)
        # print(data_category)
        # print(data_subcategory)
        # print(data_schedule)

        serializer1=UpdateOwner(data=data_owner, context={'request':request,'ruser':ruser})
        serializer2=UpdateGarage(data=data_garage, context={'request':request,'garage':garage})
        serializer3=UpdateCategory(data=data_category,many=True, context={'request':request,'garage':garage})
        serializer4=UpdateSubCategory(data=data_subcategory,many=True, context={'request':request,'garage':garage})
        serializer6=UpdateVehicleModel(data=data_vehicle_model,many=True, context={'request':request,'garage':garage})
        print(data_schedule)
        
        serializer5=UpdateSchedule(data=data_schedule,many=True, context={'request':request,'garage':garage})

        if serializer1.is_valid():
            if serializer2.is_valid():
                if serializer3.is_valid():
                    if serializer4.is_valid():
                        if serializer6.is_valid():
                            if serializer5.is_valid():

                                country_code=data_owner['country_code']
                                mobile=data_owner['mobile']
                                email=data_owner['email']
                                garage_country_code=data_garage['country_code']
                                garage_contact_num=data_garage['contact_num']
                                imp1,imp2,imp3,imp4,imp5='0','0','0','0','0'

                                if country_code != ruser.country_code:
                                    imp1='1'
                                if mobile != ruser.mobile:
                                    imp2='1'
                                if email != ruser.email:
                                    imp3='1'
                                if garage_contact_num != garage.contact_num:
                                    imp4='1'
                                if garage_country_code != garage.country_code:
                                    imp5='1'

                                serializer1.save()
                                serializer2.save()
                                serializer3.save()
                                serializer4.save()
                                serializer6.save()
                                serializer5.save()

                                data1=serializer1.data
                                data2=serializer2.data
                                data3=serializer3.data
                                data4=serializer4.data
                                data6=serializer6.data
                                data5=serializer5.data

                                # print(data1)
                                # print(data2)
                                # print(data3)
                                # print(data4)
                                # print(data5)

                                # data=data5.copy()
                                # data.update(data2)
                                # data.update(data3[0])
                                # data.update(data4)
                                # data.append(data1)

                                # if ((imp1=='1' and imp2=='1') or imp1=='1' or imp2=='1') and imp3=='1':
                                #     ruser.is_mobile_verified=False
                                #     ruser.is_email_verified=False
                                #     ruser.save()
                                #     return Response({
                                #         'success':'True',
                                #         'message':'Data updated succefully. owner mobile and email needs varification.',
                                #         # 'data':data,
                                #     },status=HTTP_200_OK)
                                # elif (imp1=='1' and imp2=='1') or imp1=='1' or imp2=='1':
                                #     ruser.is_mobile_verified=False
                                #     ruser.save()
                                #     return Response({
                                #         'success':'True',
                                #         'message':'Data updated succefully. owner mobile needs varification.',
                                #         # 'data':data,
                                #     },status=HTTP_200_OK)
                                # elif imp3=='1':
                                #     ruser.is_email_verified=False
                                #     ruser.save()
                                #     return Response({
                                #         'success':'True',
                                #         'message':'Data updated succefully. owner email needs varification.',
                                #         # 'data':data,
                                #     },status=HTTP_200_OK)
                                # if (imp4=='1' and imp5=='1') or imp4=='1' or imp5=='1':
                                #     return Response({
                                #         'success':'True',
                                #         'message':'Data updated succefully. garage contact number needs varification.',
                                #         # 'data':data,
                                #     },status=HTTP_200_OK)
                                # else:
                                    # tempdata={}
                                    # if ruser.last_name:
                                    #     tempdata['name']=ruser.first_name+' '+ruser.last_name
                                    # else:
                                    #     tempdata['name']=ruser.first_name
                                    # tempdata['image']=ruser.profile_image
                                    # tempdata['garage_name']=garage.name
                                    # tempdata['country_code']=ruser.country_code
                                    # tempdata['mobile']=ruser.mobile
                                    # tempdata['email']=ruser.email
                                return Response({
                                    'success':'True',
                                    'message':'Data updated successfully.',
                                    # 'data':tempdata,
                                },status=HTTP_200_OK)
                            else:
                                return Response({
                                    'message':'Some problems',
                                    'success':'False',
                                    'data':serializer5.errors,
                                },status=HTTP_400_BAD_REQUEST,)
                        else:
                            return Response({
                                'message':'Some problems',
                                'success':'False',
                                'data':serializer6.errors,
                            },status=HTTP_400_BAD_REQUEST,)
                    else:
                        return Response({
                            'message':'Some problems',
                            'success':'False',
                            'data':serializer4.errors,
                        },status=HTTP_400_BAD_REQUEST,)
                else:
                    return Response({
                        'message':'Some problems',
                        'success':'False',
                        'data':serializer3.errors,
                    },status=HTTP_400_BAD_REQUEST,)
            else:
                return Response({
                    'message':'Some problems',
                    'success':'False',
                    'data':serializer2.errors,
                },status=HTTP_400_BAD_REQUEST,)

        # serializer=ServiceProviderProfileUpdateSerializer(data=data, context={'request':request,'garage':garage})
        # if serializer.is_valid():
        #     # serializer.save()
        #     data=serializer.data
        #     return Response({
        #         'message':'Some problems',
        #         'success':'False',
        #         'data':serializer.errors,
        #     },status=HTTP_400_BAD_REQUEST,)

        else:
            return Response({
                'message':'Some problems',
                'success':'False',
                'data':serializer1.errors,
            },status=HTTP_400_BAD_REQUEST,)

class ServiceTypeListView(ListAPIView):
    # permission_classes=(IsAuthenticated,)
    # authentication_classes=(JSONWebTokenAuthentication,)
    def get(self,request,*args,**kwargs):
        logger.debug('service type list get called')
        logger.debug(request.data)
        
        u_id = self.kwargs['uid']
        ruser=RegisteredUser.objects.filter(id=u_id).first()
        e = ServiceSubType.objects.values('type').distinct()
        queryset=ServiceType.objects.filter(id__in=e)
        print(ruser.language_pref)
        if ruser.language_pref=='2':
            serializer=Ar_ServiceTypeListSerializer(queryset,many=True,context={'request':request,})
        else:
            serializer=ServiceTypeListSerializer(queryset,many=True,context={'request':request,})
        data=serializer.data
        return Response({
            'message':'data retrieved successfully',
            'success':'True',
            'data':data,
        },status=HTTP_200_OK)

class ServiceSubTypeListView(ListAPIView):
    # permission_classes=(IsAuthenticated,)
    # authentication_classes=(JSONWebTokenAuthentication,)
    def get(self,request,*args,**kwargs):
        logger.debug('service subtype get called')
        logger.debug(request.data)
        pk=self.kwargs['pk']
        u_id=self.kwargs['uid']
        ruser=RegisteredUser.objects.filter(id=u_id).first()
        queryset=ServiceSubType.objects.filter(type__id=pk)
        print(queryset)
        if ruser.language_pref=='2':
            serializer=Ar_ServiceSubTypeSerializer(queryset,many=True,context={'request':request})
        else:
            serializer=ServiceSubTypeSerializer(queryset,many=True,context={'request':request})
        data=serializer.data
        return Response({
            'message':'data retrieved successfully',
            'success':'True',
            'data':data,
        },status=HTTP_200_OK,)

class VehicleModelListView(ListAPIView):
    def get(self,request,*args,**kwargs):
        logger.debug('vehicle list get called')
        logger.debug(request.data)
        u_id=self.kwargs['uid']
        ruser=RegisteredUser.objects.filter(id=u_id).first()
        queryset=VehicleModle.objects.all()
        if ruser.language_pref=='2':
            serializer=Ar_VehicleModelListSerializer(queryset,many=True,context={'request':request,})
        else:
            serializer=VehicleModelListSerializer(queryset,many=True,context={'request':request,})
        data=serializer.data
        return Response({
            'message':'data retrieved successfully',
            'success':'True',
            'data':data,
        },status=HTTP_200_OK)

class ServiceProviderGarageListView(ListAPIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    serializer_class=ServiceProviderGarageListSerializer
    def get_queryset(self,*args,**kwargs):
        user=self.request.user.ruser
        queryset=Garage.objects.filter(user=user)
        return queryset
    def list(self,request,*args,**kwargs):
        # cache_key = 'um3' # needs to be unique
        # cache_time =600 # time in seconds for cache to be valid
        # t1=datetime.now()
        # data = cache.get(cache_key)
        # print(datetime.now()-t1)
        # if not data:
            # print('no cache.......................')
            # t1=datetime.now()
        qs=self.get_queryset()
        user=request.user
        ruser=RegisteredUser.objects.filter(user=user).first()
        if ruser.language_pref=='2':
            data=Ar_ServiceProviderGarageListSerializer(qs,many=True,context={'request':request}).data
        else:
            data=ServiceProviderGarageListSerializer(qs,many=True,context={'request':request}).data
            # print(datetime.now()-t1)
            # cache.set(cache_key, data, cache_time)
        return Response({
            'message':'data retrieved successfully',
            'success':'True',
            'data':data,
        },status=HTTP_200_OK,)

class GarageReviewListView(ListAPIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    def get_queryset(self,*args,**kwargs):
        id=self.kwargs['pk']
        queryset=UserReview.objects.filter(garage__id=id)
        return queryset
    def list(self,request,*args,**kwargs):
        qs=self.get_queryset()
        user=request.user
        ruser=RegisteredUser.objects.filter(user=user).first()
        if ruser.language_pref=='2':
            data=Ar_GarageReviewSerializer(qs,many=True,context={'request':request}).data
        else:
            data=GarageReviewSerializer(qs,many=True,context={'request':request}).data
        return Response({
            'message':'data retrieved successfully',
            'success':'True',
            'data':data,
        },status=HTTP_200_OK,)

class SubCatListBasedOnCat(APIView):
    def post(self,request,*args,**kwargs):
        catlist=request.data['catlist']
        u_id=request.data['uid']
        ruser=RegisteredUser.objects.filter(id=u_id).first()
        print(catlist)
        cl=[]
        catlist=catlist.split(',')
        for s in catlist:
            cl.append(s)

        q1=ServiceType.objects.filter(Q(type__in=cl)|Q(type_ar__in=cl))
        print(q1)
        # for q in q1:
        queryset=ServiceSubType.objects.filter(type__in=q1)
        if ruser.language_pref=='2':
            serializer=Ar_ServiceSubTypeSerializer(queryset,many=True)
        else:
            serializer=ServiceSubTypeSerializer(queryset,many=True)
        
        data=serializer.data
        return Response({
            'message':'list retrieved successfully',
            'success':'False',
            'data':data
        },status=HTTP_200_OK,)

class UploadImageView(APIView):
    def post(self,request,*args,**kwargs):
        image=request.FILES.get('image')
        id=self.kwargs['pk']
        if image:
            ruser=RegisteredUser.objects.filter(id=id).first()
            tgi=TempGarageImage(
                user=ruser,
                image=image,
            )
            tgi.save()
            data={}
            data['image']='http://ip:8000'+tgi.image.url
            data['user_id']=tgi.user.id
            return Response({
                'message':'Data submitted successfully',
                'success':'True',
                'data':data,
            },status=HTTP_200_OK,)
        return Response({
            'message':'Please provide image',
            'success':'True',
        },status=HTTP_200_OK,)
