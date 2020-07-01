from rest_framework.views import (APIView,)
from rest_framework.generics import (CreateAPIView,ListAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView,)
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
from django.db.models import Q
from datetime import datetime

from dateutil.relativedelta import relativedelta
# from django.utils.timezone import utc
# from django.utils.timezone import Asia/Dubai
# import pytz
# from django.utils import timezone
# timezone.activate(pytz.timezone('Asia/Dubai'))
from datetime import date
import string
import random
#
from .serializers import *
from _serviceprovider_panel.offer.models import *
from _serviceprovider_panel.saccounts.models import *
from _serviceprovider_panel.payments.models import *

import logging
logger = logging.getLogger('accounts')

#..

class CreateOfferView(CreateAPIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    def post(self,request,*args,**kwargs):
        logger.debug('Create offer post called')
        logger.debug(request.data)
        ruser=request.user.ruser
        # garage=Garage.objects.filter(user=ruser).first()
        serializer=CreateOfferSerializer(data=request.data,context={'request':request,'ruser':ruser,})#'garage':garage
        if serializer.is_valid():
            serializer.save()
            data=serializer.data
            return Response({
                'message':'Offer added successfully',
                'success':'True',
                'data':data,
            },status=HTTP_200_OK,)
        else:
            return Response({
                'message':'data save failed',
                'success':'False',
                'data':serializer.errors,
            },status=HTTP_400_BAD_REQUEST,)

class GarageWiseOfferListView(ListAPIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    serializer_class=GarageWiseOfferListSerializer

    def get(self,request,*args,**kwargs):
        logger.debug('Garage wise offer list get called')
        logger.debug(request.data)
        ruser=self.request.user.ruser
        garage=Garage.objects.filter(user=ruser).first()
        queryset=Offer.objects.filter(garage=garage)
        if ruser.language_pref=='2':
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
            'message':'Data retrieved successfully',
            'success':'True',
            'data':data,
        },status=HTTP_200_OK,)

class ActiveOfferListView(ListAPIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    serializer_class=GarageWiseOfferListSerializer

    def get(self,request,*args,**kwargs):
        logger.debug('all offer list get called')
        logger.debug(request.data)
        # ruser=self.request.user.ruser
        # garage=Garage.objects.filter(user=ruser).first()
        user=request.user
        ruser=RegisteredUser.objects.filter(user=user).first()
        city=ruser.city
        print('-------------------------------')
        print(city)
        garagelist=Garage.objects.filter(city=city)
        print(garagelist)
        # now = datetime.utcnow().replace(tzinfo=utc) #THIS LINE NEEDS TO CHANGE
        now = datetime.now()
        queryset=Offer.objects.filter(garage__in=garagelist,end_date__gte=now).order_by('-start_date')
        if ruser.language_pref=='2':
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
            'message':'data retrieved successfully',
            'success':'True',
            'data':data,
        },status=HTTP_200_OK,)

class OfferDetailView(RetrieveAPIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)

    def get(self,request,*args,**kwargs):
        logger.debug('Offer detail get called')
        logger.debug(request.data)
        user=request.user
        ruser=RegisteredUser.objects.filter(user=user).first()
        pk=self.kwargs['pk']
        queryset=Offer.objects.filter(id=pk).first()
        if ruser.language_pref=='2':
            serializer=Ar_OfferDetailSerializer(queryset,context={'request':request,})
        else:
            serializer=OfferDetailSerializer(queryset,context={'request':request,})
        data=serializer.data
        return Response({
            'message':'data retrieved successfully',
            'success':'True',
            'data':data,
        },status=HTTP_200_OK,)

class OfferUpdateView(UpdateAPIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    def post(self,request,*args,**kwargs):
        logger.debug('Create offer post called')
        logger.debug(request.data)
        pk=self.kwargs['pk']
        offer=Offer.objects.filter(id=pk).first()
        serializer=OfferUpdateSerializer(data=request.data,context={'request':request,'offer':offer})
        if serializer.is_valid():
            serializer.save()
            data=serializer.data
            return Response({
                'message':'Offer updated successfully',
                'success':'True',
                'data':data,
            },status=HTTP_200_OK,)
        else:
            return Response({
                'message':'data save failed',
                'success':'False',
                'data':serializer.errors,
            },status=HTTP_400_BAD_REQUEST,)

class OfferDeleteView(DestroyAPIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)

    def get(self,request,*args,**kwargs):
        logger.debug('Create offer post called')
        logger.debug(request.data)
        pk=self.kwargs['pk']
        Offer.objects.filter(id=pk).delete()
        return Response({
            'message':'Offer deleted successfully',
            'success':'True',
        },status=HTTP_200_OK,)

class SubPlanListView(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    def get(self,request,*args,**kwargs):
        logger.debug('Subscription plan list get called')
        logger.debug(request.data)
        # queryset=SubscriptionPlan.objects.filter(validity_to__gte=date.today())
        queryset=SubscriptionPlan.objects.filter(~Q(plan_name='Free Plan'))
        ruser=request.user.ruser
        if ruser.language_pref=='2':
            serializer=Ar_SubPlanListSerializer(queryset,many=True,context={'request':request})
        else:
            serializer=SubPlanListSerializer(queryset,many=True,context={'request':request})

        data=serializer.data

        return Response({
            'message':'data retrieved successfully',
            'success':'True',
            'data':data,
        },status=HTTP_200_OK,)

class SubPlanDetailSerializer(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    def get(self,request,*args,**kwargs):
        id=self.kwargs['pk']
        ruser=request.user.ruser
        queryset=SubscriptionPlan.objects.filter(id=id).first()
        if queryset:
            if ruser.language_pref=='2':
                serializer=Ar_SubPlanDetailSerializer1(queryset, context={'request':request})
            else:
                serializer=SubPlanDetailSerializer1(queryset, context={'request':request})

            return Response({
                'message':'Data retrieved successfully',
                'success':'True',
                'data':serializer.data,
            },status=HTTP_200_OK,)
        return Response({
            'message':'This plan does not exists',
            'success':'False',
        },status=HTTP_400_BAD_REQUEST,)

class SubscribePlanView(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    def get(self,request,*args,**kwargs):
        user=request.user
        ruser=RegisteredUser.objects.filter(user=user).first()
        garage=Garage.objects.filter(user=ruser).first()
        id=self.kwargs['pk']
        sub=SubscriptionPlan.objects.filter(id=id).first()
        ivp_cart=id_generator(size=10)
        while 1:
            td=TelrDetail.objects.filter(ivp_cart=ivp_cart).first()
            if not td:
                break;
            ivp_cart=id_generator(size=10)

        data={
            'ivp_method':'create',
            'ivp_store':21361,#garage.id,
            'ivp_authkey':'nK9Fw^LRWRR@3Pzd',
            'ivp_cart':ivp_cart,
            'ivp_test':'0',
            'ivp_amount':sub.price,
            'ivp_currency':'AED',
            'ivp_desc':'Plan Subscription',
            'return_auth':'http://ip:8000/serviceprovider/payments/success/'+str(id)+'/'+str(ruser.id),
            'return_can':'http://ip:8000/serviceprovider/payments/cancel/'+str(id)+'/'+str(ruser.id),
            'return_decl':'http://ip:8000/serviceprovider/payments/decline/'+str(id)+'/'+str(ruser.id),
            'ivp_trantype':'auth',
            'bill_custref':ruser.id,
        }
        td_obj=TelrDetail(
            ivp_method='create',
            ivp_store=garage.id,
            ivp_cart=ivp_cart,
            ivp_test='0',
            ivp_amount=sub.price,
            ivp_currency='AED',
            ivp_desc='Plan Subscription',
            return_auth='http://ip:8000/serviceprovider/payments/success/'+str(id)+'/'+str(ruser.id),
            return_can='http://ip:8000/serviceprovider/payments/cancel/'+str(id)+'/'+str(ruser.id),
            return_decl='http://ip:8000/serviceprovider/payments/decline/'+str(id)+'/'+str(ruser.id),
            ivp_trantype='auth',
            bill_custref=ruser.id,
        )
        td_obj.save()

        return Response({
            'message':'Data retrieved successfully',
            'success':'True',
            'data':data,
        },status=HTTP_200_OK,)

class UpdateTelrDetailView(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    def post(self,request,*args,**kwargs):
        telr_ref=request.data['telr_ref']
        user=request.user
        ruser=RegisteredUser.objects.filter(user=user).first()
        td=TelrDetail.objects.filter(bill_custref=ruser.id).order_by('-id').first()
        td.telr_ref=telr_ref
        td.save()
        return Response({
            'message':'Data saved successfully',
            'success':'True',
        },status=HTTP_200_OK,)

def id_generator(size=4, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class CouponCodeView(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    def get(self,request,*args,**kwargs):
        coupon=''
        advertisment_license_number=''
        while True:
            coupon=id_generator()
            off=Offer.objects.filter(coupon=coupon).first()
            if not off:
                break
        while True:
            advertisment_license_number=id_generator(size=10)
            off=Offer.objects.filter(advertisment_license_number=advertisment_license_number).first()
            if not off:
                break
        data={
            'coupon':coupon,
            'advertisment_license_number':advertisment_license_number,
        }
        return Response({
            'message':'Data retrieved successfully',
            'success':'True',
            'data':data,
        },status=HTTP_200_OK,)

class TopTenOfferImageView(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    serializer_class=GarageWiseOfferListSerializer

    def get(self,request,*args,**kwargs):
        logger.debug('top 10 offer images list get called')
        logger.debug(request.data)
        user=request.user
        ruser=RegisteredUser.objects.filter(user=user).first()
        # ruser=self.request.user.ruser
        # garage=Garage.objects.filter(user=ruser).first()
        # user=request.user
        # ruser=RegisteredUser.objects.filter(user=user).first()
        # city=ruser.city
        # garagelist=Garage.objects.filter(city=city)

        # now = datetime.utcnow().replace(tzinfo=utc) #THIS LINE NEEDS TO CHANGE
        now = datetime.now()
        queryset=Offer.objects.filter(end_date__gte=now).order_by('-start_date')[:10]
        if ruser.language_pref=='2':
            serializer=Ar_GarageWiseOfferListSerializer(queryset,many=True,context={'request':request})
        else:
            serializer=GarageWiseOfferListSerializer(queryset,many=True,context={'request':request})
        data=serializer.data

        return Response({
            'message':'data retrieved successfully',
            'success':'True',
            'data':data,
        },status=HTTP_200_OK,)

class SPSubscribedPlanDetail(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    def get(self,request,*args,**kwargs):
        user=request.user
        ruser=RegisteredUser.objects.filter(user=user).first()
        us=UserSubscription.objects.filter(ruser=ruser).first()
        if us:
            if ruser.language_pref=='2':
                serializer=Ar_SubPlanDetailSerializer1(us.plan,context={'request':request})
            else:
                serializer=SubPlanDetailSerializer1(us.plan,context={'request':request})
            data=serializer.data
            data['subscribed_on']=us.created_on
            data['plan_expiring_on']=us.created_on+relativedelta(months=us.plan.valid_for)
            exclude=['created_on','subscribe_url']
            data={x:data[x]for x in data if x not in exclude}
            return Response({
                'message':'Data retrieved successfully',
                'success':'True',
                'data':data,
            },status=HTTP_200_OK,)
        else:
            return Response({
                'message':'Sorry..!! You have not subscribed to any plan.',
                'success':'False',
            },status=HTTP_400_BAD_REQUEST,)
