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
# from django.utils.timezone import utc
# from django.utils.timezone import Asia/Dubai
# import pytz
# from django.utils import timezone
# timezone.activate(pytz.timezone('Asia/Dubai'))
from datetime import date
import string
import random

from .serializers import *
from _serviceprovider_panel.offer.models import *
from _serviceprovider_panel.saccounts.models import *
from _serviceprovider_panel.payments.models import *

import logging
logger = logging.getLogger('accounts')


class PaymentSuccessView(APIView):
    # permission_classes=(IsAuthenticated,)
    # authentication_classes=(JSONWebTokenAuthentication,)
    def post(self,request,*args,**kwargs):
        logger.debug('Create offer post called')
        logger.debug(request.data)
        id=self.kwargs['pk']
        rid=self.kwargs['rid']
        sub_plan=SubscriptionPlan.objects.filter(id=id).first()
        # user=request.user
        ruser=RegisteredUser.objects.filter(id=rid).first()
        usub=UserSubscription.objects.filter(ruser=ruser).first()
        if usub:
            usub.plan=sub_plan
            usub.created_on=datetime.now()
            usub.save()
        else:
            us=UserSubscription(
                plan=sub_plan,
                ruser=ruser,
            )
            us.save()
        pd=PaymentDetail(
            serv_provider=ruser,
            status='Completed',
            price=sub_plan.price,
            subscription_plan=sub_plan,
            payment_mode="Telr"
        )
        pd.save()
        td=TelrDetail.objects.filter(bill_custref=ruser.id).order_by('-id').first()
        td.status='Completed'
        td.save()

        return Response({
            'message':'Payment successfully..!! Your Plan is Active now.',
            'success':'True',
        },status=HTTP_200_OK,)

class PaymentDeclineView(APIView):
    # permission_classes=(IsAuthenticated,)
    # authentication_classes=(JSONWebTokenAuthentication,)
    def post(self,request,*args,**kwargs):
        logger.debug('Create offer post called')
        logger.debug(request.data)
        id=self.kwargs['pk']
        rid=self.kwargs['rid']
        sub_plan=SubscriptionPlan.objects.filter(id=id).first()
        # user=request.user
        ruser=RegisteredUser.objects.filter(id=rid).first()
        pd=PaymentDetail(
            serv_provider=ruser,
            status='Declined',
            price=sub_plan.price,
            subscription_plan=sub_plan,
            payment_mode="Telr"
        )
        pd.save()
        td=TelrDetail.objects.filter(bill_custref=ruser.id).order_by('-id').first()
        td.status='Declined'
        td.save()

        return Response({
            'message':'Payment declined.',
            'success':'False',
        },status=402,)

class PaymentCancelView(APIView):
    def post(self,request,*args,**kwargs):
        logger.debug('Create offer post called')
        logger.debug(request.data)
        id=self.kwargs['pk']
        rid=self.kwargs['rid']
        sub_plan=SubscriptionPlan.objects.filter(id=id).first()
        # user=request.user
        ruser=RegisteredUser.objects.filter(id=rid).first()
        pd=PaymentDetail(
            serv_provider=ruser,
            status='Cancelled',
            price=sub_plan.price,
            subscription_plan=sub_plan,
            payment_mode="Telr"
        )
        pd.save()
        td=TelrDetail.objects.filter(bill_custref=ruser.id).order_by('-id').first()
        td.status='Cancelled'
        td.save()

        return Response({
            'message':'Payment cancelled.',
            'success':'False',
        },status=HTTP_400_BAD_REQUEST,)
