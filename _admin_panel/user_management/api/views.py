from rest_framework.views import (APIView,)
from rest_framework.generics import (ListAPIView,RetrieveAPIView,)
from rest_framework.permissions import (IsAuthenticated,)
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.authentication import  JSONWebTokenAuthentication
from rest_framework.response import Response
from django.contrib.auth.models import User

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives

# from django.db.models import Q
from rest_framework import status
from rest_framework.status import (
                                        HTTP_200_OK,
                                    	HTTP_400_BAD_REQUEST,
                                    	HTTP_204_NO_CONTENT,
                                    	HTTP_201_CREATED,
                                    	HTTP_500_INTERNAL_SERVER_ERROR,
                                    )

# from .pagination import *
# from services.models import *
from .serializers import *
from _user_panel.uaccounts.models import *
from _serviceprovider_panel.offer.models import *
# from _serviceprovider_panel.extra.models import MaintainCacheFlag

import logging
logger = logging.getLogger('accounts')

class APUMBlockView(APIView):
    def post(self,request,*args,**kwargs):
        user_id = self.kwargs['pk']
        try:
            user=User.objects.filter(id=user_id).first()
        except:
            return Response({
                    'message':'No user to block'
                    },status=HTTP_400_BAD_REQUEST)
        if user.is_active == True:
            user.is_active = False
            user.save()
            # obj, created = MaintainCacheFlag.objects.update_or_create(model_name='RegisteredUser',is_changed=True)
            # print(obj.is_changed)
            return Response({
                        'message':'Blocked successfully'
                        },status=HTTP_200_OK)
        else:
            return Response({
                        'message':'Already Blocked'
                        },status=HTTP_200_OK)

class APUMUnblockView(APIView):
    def post(self,request,*args,**kwargs):
        user_id = self.kwargs['pk']
        try:
            user=User.objects.filter(id=user_id).first()
        except:
            return Response({
                    'message':'No user to unblock'
                    },status=HTTP_400_BAD_REQUEST)
        if user.is_active == False:
            user.is_active = True
            user.save()

            # obj, created = MaintainCacheFlag.objects.update_or_create(model_name='RegisteredUser',is_changed=True)
            # print(obj.is_changed)
            return Response({
                        'message':'Unblocked successfully'
                        },status=HTTP_200_OK)
        else:
            return Response({
                        'message':'Already unblocked'
                        },status=HTTP_200_OK)

class APUMDeleteView(APIView):
    def post(self,request,*args,**kwargs):
        user_id = self.kwargs['pk']
        try:
            user=User.objects.filter(id=user_id).first()
        except:
            return Response({
                    'message':'No user to delete'
                    },status=HTTP_400_BAD_REQUEST)
        if user:
            user.delete()

            # obj, created = MaintainCacheFlag.objects.update_or_create(model_name='RegisteredUser',is_changed=True)
            # print(obj.is_changed)
            return Response({
                        'message':'Deleted successfully'
                        },status=HTTP_200_OK)

class APUMApproveView(APIView):
    def post(self,request,*args,**kwargs):
        user_id = self.kwargs['pk']
        try:
            user=User.objects.filter(id=user_id).first()
            ruser=RegisteredUser.objects.filter(user=user).first()
        except:
            return Response({
                    'message':'No user to approve'
                    },status=HTTP_400_BAD_REQUEST)
        if ruser.is_approved == False:
            ruser.is_approved = True
            ruser.save()
            subPlan=SubscriptionPlan.objects.filter(plan_name='Free Plan').first()
            usub_obj=UserSubscription.objects.filter(ruser=ruser).first()
            if not usub_obj:
                usub=UserSubscription(
                    plan=subPlan,
                    ruser=ruser,
                )
                usub.save()

            '''
            Send confirmation email
            '''
            uemail=user.email
            current_site = get_current_site(request)
            subject = 'Welcome to garage'
            message = render_to_string('admin_approval_email.html', {
                'user': user,
                # 'domain':'localhost:8000',
                # 'domain':'ip:8000',
                'domain': current_site.domain,
            })
            plain_message = strip_tags(message)
            email = EmailMultiAlternatives(
                        subject, plain_message, 'garage <webmaster@localhost>', to=[uemail]
            )
            email.attach_alternative(message, "text/html")
            email.send()

            # obj, created = MaintainCacheFlag.objects.update_or_create(model_name='RegisteredUser',is_changed=True)
            # print(obj.is_changed)
            return Response({
                        'message':'Approved successfully'
                        },status=HTTP_200_OK)
        else:
            return Response({
                        'message':'Already approved'
                        },status=HTTP_200_OK)
