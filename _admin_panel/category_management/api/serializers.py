from rest_framework import serializers

from _serviceprovider_panel.saccounts.models import *

class APCMCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model=ServiceType
        fields='__all__'
