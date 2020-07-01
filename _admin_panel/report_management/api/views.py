from rest_framework.views import (APIView,)
from rest_framework.generics import (ListAPIView,RetrieveAPIView,)
from rest_framework.permissions import (IsAuthenticated,)
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.authentication import  JSONWebTokenAuthentication
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models import Count
from django.db.models import Sum
from rest_framework import status
from rest_framework.status import (
                                        HTTP_200_OK,
                                    	HTTP_400_BAD_REQUEST,
                                    	HTTP_204_NO_CONTENT,
                                    	HTTP_201_CREATED,
                                    	HTTP_500_INTERNAL_SERVER_ERROR,
                                    )

# from .pagination import *
from _serviceprovider_panel.payments.models import *
from _user_panel.uaccounts.models import *
from .serializers import *

import logging
logger = logging.getLogger('accounts')




class DisplayView(APIView):
    def get(self, request, *args, **kwargs):
        id=kwargs['pk']
        selection=kwargs['selection']
        result=''
        if id=='f1':
            pass
        elif id=='f2':
            if selection=='Datewise':
                result = RegisteredUser.objects.filter(Q(user_type=1)|Q(has_dual_account=True)).extra(select={'period': 'date( created_on )'}).values('period').annotate(available=Count('created_on'))
            elif selection=='Weekly':
                result = RegisteredUser.objects.filter(Q(user_type=1)|Q(has_dual_account=True)).extra(select={'period': 'week( created_on )'}).values('period').annotate(available=Count('created_on'))
            elif selection=='Monthly':
                result = RegisteredUser.objects.filter(Q(user_type=1)|Q(has_dual_account=True)).extra(select={'period': 'month( created_on )'}).values('period').annotate(available=Count('created_on'))
        elif id=='f3':
            if selection=='Datewise':
                result = RegisteredUser.objects.filter(Q(user_type=2)|Q(has_dual_account=True)).extra(select={'period': 'date( created_on )'}).values('period').annotate(available=Count('created_on'))
            elif selection=='Weekly':
                result = RegisteredUser.objects.filter(Q(user_type=2)|Q(has_dual_account=True)).extra(select={'period': 'week( created_on )'}).values('period').annotate(available=Count('created_on'))
            elif selection=='Monthly':
                result = RegisteredUser.objects.filter(Q(user_type=2)|Q(has_dual_account=True)).extra(select={'period': 'month( created_on )'}).values('period').annotate(available=Count('created_on'))
        elif id=='f4':
            if selection=='Datewise':
                result=PaymentDetail.objects.filter(status='Completed').extra(select={'period': 'date( date_of_purchase )'}).values('period').annotate(available=Sum('price'))
            elif selection=='Weekly':
                result=PaymentDetail.objects.filter(status='Completed').extra(select={'period': 'week( date_of_purchase )'}).values('period').annotate(available=Sum('price'))
            elif selection=='Monthly':
                result=PaymentDetail.objects.filter(status='Completed').extra(select={'period': 'month( date_of_purchase )'}).values('period').annotate(available=Sum('price'))

        labels=[]
        default_items=[]
        print(result)
        for r in result:
            labels.append(str(r['period']))
            default_items.append(r['available'])

        print(default_items)
        data = {
                "labels": labels,
                "default": default_items,
        }
        return Response(data)
