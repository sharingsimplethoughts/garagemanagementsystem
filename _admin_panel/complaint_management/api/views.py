from rest_framework.views import (APIView,)
from rest_framework.permissions import (IsAuthenticated,)
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.authentication import  JSONWebTokenAuthentication
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.status import (
                                        HTTP_200_OK,
                                    	HTTP_400_BAD_REQUEST,
                                    	HTTP_204_NO_CONTENT,
                                    	HTTP_201_CREATED,
                                    	HTTP_500_INTERNAL_SERVER_ERROR,
                                    )

# from .pagination import *
from _serviceprovider_panel.saccounts.models import *
from .serializers import *
# from _serviceprovider_panel.extra.models import MaintainCacheFlag

import logging
logger = logging.getLogger('accounts')


class APCMDeleteView(APIView):
    def post(self,*args,**kwargs):
        comp_id = self.kwargs['pk']
        comp=''
        try:
            comp=CustomerComplaint.objects.filter(id=comp_id).first()
        except:
            return Response({
                    'message':'No complaint to delete'
                    },status=HTTP_400_BAD_REQUEST)
        if comp:
            comp.delete()
            # obj = MaintainCacheFlag.objects.filter(model_name='CustomerComplaint').first()
            # obj.is_changed=True
            # obj.save()
            # print(obj.is_changed)
            return Response({
                        'message':'Deleted successfully'
                        },status=HTTP_200_OK)
        return Response({
                    'message':'Something went wrong'
                    },status=HTTP_500_INTERNAL_SERVER_ERROR)
