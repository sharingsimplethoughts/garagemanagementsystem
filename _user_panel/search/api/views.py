from django.db.models import Q
from rest_framework.filters import (SearchFilter,OrderingFilter,)
from rest_framework.generics import (CreateAPIView,GenericAPIView,ListAPIView,)
from rest_framework.views import (APIView)
from django.views.generic import TemplateView

from django.contrib.auth.models import User
from rest_framework.permissions import (AllowAny,IsAuthenticated,)
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

from datetime import datetime
from django.utils.timezone import utc
from datetime import date

from .serializers import *
from _user_panel.ugarage.api.serializers import GarageListSerializer,ServiceTypeListSerializer,Ar_GarageListSerializer,Ar_ServiceTypeListSerializer
from _serviceprovider_panel.offer.api.serializers import *
from _serviceprovider_panel.saccounts.models import *
from _serviceprovider_panel.offer.models import *

import logging
logger = logging.getLogger('accounts')


class HomeSearchView(ListAPIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    serializer_class=GarageListSerializer
    filter_backends=(SearchFilter,OrderingFilter,)
    search_fields=['slug1','slug2','state','city','country','service_type','service_subtype',]

    def get_queryset(self,request,*args,**kwargs):
        user=request.user
        ruser=RegisteredUser.objects.filter(user=user).first()
        city=ruser.city
        queryset_list=Garage.objects.filter(city=city)## find most popular garages here
        query=self.request.GET.get('q',None)

        print('----------------')
        print(query)
        st=ServiceType.objects.filter(Q(slug__icontains=query)|Q(slug_ar__icontains=query))
        sst=ServiceSubType.objects.filter(Q(slug__icontains=query)|Q(slug_ar__icontains=query))
        vmt=VehicleModle.objects.filter(Q(slug__icontains=query)|Q(slug_ar__icontains=query))
        if query:
            queryset_list=queryset_list.filter(
                Q(name__icontains=query)|
                Q(location__icontains=query)|
                Q(state__icontains=query)|
                Q(city__icontains=query)|
                Q(country__icontains=query)|
                Q(service_type__in=(st))|
                Q(service_subtype__in=(sst))|
                Q(vehicle_model__in=(vmt))
            ).distinct()
        return queryset_list
    def list(self,request,*args,**kwargs):
        logger.debug('home search list called')
        logger.debug(self.request.data)
        qs=self.get_queryset(request)
        user=request.user
        ruser=RegisteredUser.objects.filter(user=user).first()
        if ruser.language_pref=='2':
            data=Ar_GarageListSerializer(qs,many=True,context={'request':self.request}).data
        else:
            data=GarageListSerializer(qs,many=True,context={'request':self.request}).data
        for obj in data:
            if obj['is_favorite']=='True':
                obj['make_fav_garage_url']=''
            else:
                obj['remove_fav_garage_url']=''
        return Response({
            'message':'data retrieved successfully',
            'success':'True',
            'data':data,
        },status=HTTP_200_OK,)

class PopularGarageListCumSearchView(ListAPIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    serializer_class=GarageListSerializer
    filter_backends=(SearchFilter,OrderingFilter,)
    search_fields=['slug1','slug2','state','city','country','service_type','service_subtype',]

    def get_queryset(self,request,*args,**kwargs):
        user=request.user
        ruser=RegisteredUser.objects.filter(user=user).first()
        city=ruser.city
        # queryset_list=Garage.objects.filter(city=city,garage_rating__gte=0).order_by('-garage_rating')## find most popular garages here
        queryset_list=Garage.objects.filter(city=city).order_by('-garage_rating')
        query=self.request.GET.get('q',None)

        print('----------------')
        print(query)
        st=ServiceType.objects.filter(Q(slug__icontains=query)|Q(slug_ar__icontains=query))
        sst=ServiceSubType.objects.filter(Q(slug__icontains=query)|Q(slug_ar__icontains=query))
        vmt=VehicleModle.objects.filter(Q(slug__icontains=query)|Q(slug_ar__icontains=query))
        if query:
            queryset_list=queryset_list.filter(
                Q(name__icontains=query)|
                Q(location__icontains=query)|
                Q(state__icontains=query)|
                Q(city__icontains=query)|
                Q(country__icontains=query)|
                Q(service_type__in=(st))|
                Q(service_subtype__in=(sst))|
                Q(vehicle_model__in=(vmt))
            ).distinct()
        return queryset_list
    def list(self,request,*args,**kwargs):
        logger.debug('home search list called')
        logger.debug(self.request.data)
        qs=self.get_queryset(request)
        user=request.user
        ruser=RegisteredUser.objects.filter(user=user).first()
        if ruser.language_pref=='2':
            data=Ar_GarageListSerializer(qs,many=True,context={'request':self.request}).data
        else:
            data=GarageListSerializer(qs,many=True,context={'request':self.request}).data
        for obj in data:
            if obj['is_favorite']=='True':
                obj['make_fav_garage_url']=''
            else:
                obj['remove_fav_garage_url']=''
        return Response({
            'message':'data retrieved successfully',
            'success':'True',
            'data':data,
        },status=HTTP_200_OK,)

class HomeSpecificSearchView(ListAPIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    serializer_class=GarageListSerializer
    filter_backends=(SearchFilter,OrderingFilter,)
    search_fields=['slug1','slug2','state','city','country','service_type','service_subtype',]

    def get_queryset(self,*args,**kwargs):
        id=self.kwargs['pk']
        sstype=ServiceSubType.objects.filter(id=id).first()
        queryset_list=Garage.objects.filter(service_subtype=sstype) ## find most popular garages here
        query=self.request.GET.get('q',None)

        print('----------------')
        print(query)
        st=ServiceType.objects.filter(Q(slug__icontains=query)|Q(slug_ar__icontains=query))
        sst=ServiceSubType.objects.filter(Q(slug__icontains=query)|Q(slug_ar__icontains=query))
        vmt=VehicleModle.objects.filter(Q(slug__icontains=query)|Q(slug_ar__icontains=query))
        if query:
            queryset_list=queryset_list.filter(
                Q(name__icontains=query)|
                Q(location__icontains=query)|
                Q(state__icontains=query)|
                Q(city__icontains=query)|
                Q(country__icontains=query)|
                Q(service_type__in=(st))|
                Q(service_subtype__in=(sst))|
                Q(vehicle_model__in=(vmt))
            ).distinct()
        return queryset_list
    def list(self,*args,**kwargs):
        logger.debug('home search list called')
        logger.debug(self.request.data)
        qs=self.get_queryset()
        user=self.request.user
        ruser=RegisteredUser.objects.filter(user=user).first()
        if ruser.language_pref:
            data=Ar_GarageListSerializer(qs,many=True,context={'request':self.request}).data
        else:
            data=GarageListSerializer(qs,many=True,context={'request':self.request}).data
        for obj in data:
            if obj['is_favorite']=='True':
                obj['make_fav_garage_url']=''
            else:
                obj['remove_fav_garage_url']=''
        return Response({
            'message':'data retrieved successfully',
            'success':'True',
            'data':data,
        },status=HTTP_200_OK,)

class PopularGarageSearchView(ListAPIView):
    permisstion_class=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    serializer_class=GarageListSerializer
    filter_backends=(SearchFilter,OrderingFilter,)

    def get_queryset(self,request,*args,**kwargs):
        user=request.user
        ruser=RegisteredUser.objects.filter(user=user).first()
        city=ruser.city
        # queryset=Garage.objects.filter(city=city,garage_rating__gte=0)[:10]
        queryset=Garage.objects.filter(city=city).order_by('-garage_rating')
        return queryset

    def list(self,request,*args,**kwargs):
        logger.debug('popular garage search list called')
        logger.debug(self.request.data)
        qs=self.get_queryset(request)
        user=request.user
        ruser=RegisteredUser.objects.filter(user=user).first()
        if ruser.language_pref=='2':
            data=Ar_GarageListSerializer(qs,many=True,context={'request':self.request}).data
        else:
            data=GarageListSerializer(qs,many=True,context={'request':self.request}).data
        for obj in data:
            if obj['is_favorite']=='True':
                obj['make_fav_garage_url']=''
            else:
                obj['remove_fav_garage_url']=''
        return Response({
            'message':'data retrieved successfully',
            'success':'True',
            'data':data,
        },status=HTTP_200_OK,)

class PopularCategorySearchView(ListAPIView):
    permisstion_class=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    serializer_class=ServiceTypeListSerializer
    filter_backends=(SearchFilter,OrderingFilter,)

    def get_queryset(self,*args,**kwargs):
        # Employer.objects.values('id').annotate(jobtitle_count=Count('jobtitle')).order_by('-jobtitle_count')[:5]
        e = ServiceSubType.objects.values('type').distinct()
        queryset=ServiceType.objects.filter(id__in=e).order_by('-category_rating')[:10]
        return queryset

    def list(self,request,*args,**kwargs):
        logger.debug('popular category search list called')
        logger.debug(self.request.data)
        qs=self.get_queryset()
        ruser=request.user.ruser
        if ruser.language_pref=='2':
            data=Ar_ServiceTypeListSerializer(qs,many=True,context={'request':self.request}).data
        else:
            data=ServiceTypeListSerializer(qs,many=True,context={'request':self.request}).data

        return Response({
            'message':'data retrieved successfully',
            'success':'True',
            'data':data,
        },status=HTTP_200_OK,)

class OfferSearchView(ListAPIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    serializer_class=GarageWiseOfferListSerializer
    filter_backends=(SearchFilter,OrderingFilter,)
    # search_fields=['slug1','slug2','state','city','country','service_type','service_subtype',]

    def get_queryset(self,*args,**kwargs):
        # now = datetime.utcnow().replace(tzinfo=utc)
        now = datetime.now()
        queryset_list=Offer.objects.filter(end_date__gte=now)

        query=self.request.GET.get('q',None)

        print('----------------')
        print(query)

        if query:
            queryset_list=queryset_list.filter(
                Q(title__icontains=query)|
                Q(description__icontains=query)|
                Q(coupon__icontains=query)
            ).distinct()
        return queryset_list
    def list(self,*args,**kwargs):
        logger.debug('home offer search list called')
        logger.debug(self.request.data)
        qs=self.get_queryset()
        user=self.request.user
        ruser=RegisteredUser.objects.filter(user=user).first()
        if ruser.language_pref=='2':
            data=Ar_GarageWiseOfferListSerializer(qs,many=True,context={'request':self.request}).data
        else:
            data=GarageWiseOfferListSerializer(qs,many=True,context={'request':self.request}).data
        if data:
            return Response({
                'message':'data retrieved successfully',
                'success':'True',
                'data':data,
            },status=HTTP_200_OK,)
        return Response({
            'message':'No result found matching your selection',
            'success':'False',
        },status=HTTP_400_BAD_REQUEST,)

class ServiceProviderOfferSearchView(ListAPIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    serializer_class=GarageWiseOfferListSerializer
    filter_backends=(SearchFilter,OrderingFilter,)
    # search_fields=['slug1','slug2','state','city','country','service_type','service_subtype',]

    def get_queryset(self,request,*args,**kwargs):
        user=request.user
        ruser=RegisteredUser.objects.filter(user=user).first()
        garagelist=Garage.objects.filter(user=ruser)
        # now = datetime.utcnow().replace(tzinfo=utc)
        queryset_list=Offer.objects.filter(garage__in=garagelist)#end_date__lte=now

        query=self.request.GET.get('q',None)

        print('----------------')
        print(query)

        if query:
            queryset_list=queryset_list.filter(
                Q(title__icontains=query)|
                Q(description__icontains=query)|
                Q(coupon__icontains=query)
            ).distinct()
        return queryset_list
    def list(self,request,*args,**kwargs):
        logger.debug('home offer search list called')
        logger.debug(self.request.data)
        qs=self.get_queryset(request)
        user=request.user
        ruser=RegisteredUser.objects.filter(user=user).first()
        if ruser.language_pref=='2':
            data=Ar_GarageWiseOfferListSerializer(qs,many=True,context={'request':self.request}).data
        else:
            data=GarageWiseOfferListSerializer(qs,many=True,context={'request':self.request}).data
        return Response({
            'message':'data retrieved successfully',
            'success':'True',
            'data':data,
        },status=HTTP_200_OK,)
