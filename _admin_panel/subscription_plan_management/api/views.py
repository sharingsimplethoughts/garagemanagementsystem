from rest_framework.views import (APIView,)
from rest_framework.generics import (ListAPIView,RetrieveAPIView,)
from rest_framework.permissions import (IsAuthenticated,)
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.authentication import  JSONWebTokenAuthentication
from rest_framework.response import Response
from django.contrib.auth.models import User
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
from _serviceprovider_panel.offer.models import *

import logging
logger = logging.getLogger('accounts')

class APSPMDeleteView(APIView):
    def post(self,request,*args,**kwargs):
        user_id = self.kwargs['pk']
        try:
            user=SubscriptionPlan.objects.filter(id=user_id).first()
        except:
            return Response({
                    'message':'No item to delete'
                    },status=HTTP_400_BAD_REQUEST)
        if user:
            user.delete()
            return Response({
                        'message':'Deleted successfully'
                        },status=HTTP_200_OK)
