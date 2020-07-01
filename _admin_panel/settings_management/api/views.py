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
from _serviceprovider_panel.extra.models import *
from .serializers import *

import logging
logger = logging.getLogger('accounts')

class DisplayOptionsView(ListAPIView):
    def get_serializer(self,*args,**kwargs):
        id=self.kwargs['pk']
        if id == 'f1':
            serializer_class=AboutUsSerializer2
        elif id=='f2':
            serializer_class=TermsAndConditionSerializer2
        elif id=='f3':
            serializer_class=FaqSerializer2
        elif id=='f4':
            serializer_class=HelpSerializer2
        elif id=='f5':
            serializer_class=PrivacyPolicySerializer2
        elif id=='f6':
            serializer_class=LegalSerializer2
        else:
            serializer_class=NewOptionsSerializer2
        print(serializer_class)
        return serializer_class(*args,**kwargs)

    def get_queryset(self,*args,**kwargs):
        id=self.kwargs['pk']
        print(id)
        if id=='f1':
            queryset=AboutUs.objects.all()
        elif id=='f2':
            queryset=TermsAndCondition.objects.all()
        elif id=='f3':
            queryset=Faq.objects.all()
        elif id=='f4':
            queryset=Help.objects.all()
        elif id=='f5':
            queryset=PrivacyPolicy.objects.all()
        elif id=='f6':
            queryset=Legal.objects.all()
        else:
            queryset=NewOptions.objects.filter(id=id)
        print('hi')
        return queryset

class DeleteOptionsView(APIView):
    def post(self,request,*args,**kwargs):
        id=self.kwargs['pk']
        newopt=NewOptions.objects.filter(id=id).first()
        newopt.delete()
        return Response({
            'message':'Deleted Successfully',
        },status=HTTP_200_OK,)
