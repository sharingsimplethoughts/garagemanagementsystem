from rest_framework import serializers

from _serviceprovider_panel.extra.models import *

class AboutUsSerializer2(serializers.ModelSerializer):
    class Meta:
        model=AboutUs
        fields='__all__'

class TermsAndConditionSerializer2(serializers.ModelSerializer):
    class Meta:
        model=TermsAndCondition
        fields='__all__'

class HelpSerializer2(serializers.ModelSerializer):
    class Meta:
        model=Help
        fields='__all__'

class LegalSerializer2(serializers.ModelSerializer):
    class Meta:
        model=Legal
        fields='__all__'

class PrivacyPolicySerializer2(serializers.ModelSerializer):
    class Meta:
        model=PrivacyPolicy
        fields='__all__'

class FaqSerializer2(serializers.ModelSerializer):
    class Meta:
        model=Faq
        fields='__all__'

class NewOptionsSerializer2(serializers.ModelSerializer):
    class Meta:
        model=NewOptions
        fields='__all__'
