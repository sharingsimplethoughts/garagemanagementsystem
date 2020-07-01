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
from django.db.models import Q

import logging
logger = logging.getLogger('accounts')

from .serializers import *
from _serviceprovider_panel.offer.api.serializers import OfferDetailSerializer,Ar_OfferDetailSerializer

class ServiceTypeListView(ListAPIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)

    def get(self,request,*args,**kwargs):
        logger.debug('service type list get called')
        logger.debug(request.data)
        ruser=request.user.ruser
        # queryset=ServiceType.objects.all()
        e = ServiceSubType.objects.values('type').distinct()
        queryset=ServiceType.objects.filter(id__in=e)
        if ruser.language_pref=='2':
            serializer=Ar_ServiceTypeListSerializer(queryset,many=True,context={'request':request,})
        else:
            serializer=ServiceTypeListSerializer(queryset,many=True,context={'request':request,})
        data=serializer.data
        return Response({
            'message':'Data retrieved successfully',
            'success':'True',
            'data':data,
        },status=HTTP_200_OK)

class ServiceSubTypeListView(ListAPIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    def get(self,request,*args,**kwargs):
        logger.debug('service subtype get called')
        logger.debug(request.data)
        pk=self.kwargs['pk']
        ruser=request.user.ruser
        queryset=ServiceSubType.objects.filter(type__id=pk)
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

class GarageListView(ListAPIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    def get(self,request,*args,**kwargs):
        logger.debug('service subtype get called')
        logger.debug(request.data)
        pk=self.kwargs['pk']
        user=request.user
        ruser=RegisteredUser.objects.filter(user=user).first()
        # sst=ServiceSubType.objects.filter(id=pk).first()
        queryset=Garage.objects.filter(service_subtype__id=pk).distinct()
        if ruser.language_pref=='2':
            serializer=Ar_GarageListSerializer(queryset,many=True,context={'request':request})
        else:
            serializer=GarageListSerializer(queryset,many=True,context={'request':request})
        data=serializer.data
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

class GarageDetailView(RetrieveAPIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    def get(self,request,*args,**kwargs):
        pk=self.kwargs['pk']
        queryset=Garage.objects.filter(id=pk)
        user=request.user
        ruser = RegisteredUser.objects.filter(user=user).first()
        if ruser.language_pref=='2':
            serializer=Ar_GarageAllDetailSerializer(queryset,many=True,context={'request':request})
        else:
            serializer=GarageAllDetailSerializer(queryset,many=True,context={'request':request})
        data=serializer.data
        return Response({
            'message':'Data retrieved successfully',
            'success':'True',
            'data':data,
        },status=HTTP_200_OK,)

class GarageOfferDetailView(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    def get(self,request,*args,**kwargs):
        logger.debug('Offer detail get called')
        logger.debug(request.data)
        user=request.user
        ruser=RegisteredUser.objects.filter(user=user).first()
        pk=self.kwargs['pk']
        queryset=Offer.objects.filter(id=pk).first()
        if queryset:
            garage=queryset.garage.name
            if ruser.language_pref=='2':
                serializer=Ar_OfferDetailSerializer(queryset,context={'garage':garage,'request':request})
            else:
                serializer=OfferDetailSerializer(queryset,context={'garage':garage,'request':request})
            data=serializer.data
            return Response({
                'message':'data retrieved successfully',
                'success':'True',
                'data':data,
            },status=HTTP_200_OK,)
        return Response({
            'message':'Invalid offer id',
            'success':'False',
        },status=HTTP_400_BAD_REQUEST,)

class UserReviewView(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    def post(self,request,*args,**kwargs):
        id=self.kwargs['pk']
        user=request.user
        serializer=UserReviewSerializer(data=request.data,context={'request':request,'id':id})
        if serializer.is_valid():
            serializer.save()
            data=serializer.data
            return Response({
                'message':'Review submitted successfully',
                'success':'True',
                'data':data,
            },status=HTTP_200_OK,)
        return Response({
            'message':'failed to submit',
            'success':'False',
            'data':serializer.errors,
        },status=HTTP_200_OK,)
