from rest_framework import serializers
from rest_framework.exceptions import APIException

from _serviceprovider_panel.extra.models import *

class APIException400(APIException):
    satus_code=400

class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model=AboutUs
        fields='__all__'
class Ar_AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model=AboutUs
        fields=('title_ar','content_ar','created_on')

class TermsAndConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model=TermsAndCondition
        fields='__all__'
class Ar_TermsAndConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model=TermsAndCondition
        fields=('title_ar','content_ar','created_on')

class HelpSerializer(serializers.ModelSerializer):
    class Meta:
        model=Help
        fields='__all__'
class Ar_HelpSerializer(serializers.ModelSerializer):
    class Meta:
        model=Help
        fields=('title_ar','content_ar','created_on')

class LegalSerializer(serializers.ModelSerializer):
    class Meta:
        model=Legal
        fields='__all__'
class LegalSerializer(serializers.ModelSerializer):
    class Meta:
        model=Legal
        fields=('title_ar','content_ar','created_on')

class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model=PrivacyPolicy
        fields='__all__'
class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model=PrivacyPolicy
        fields=('title_ar','content_ar','created_on')

class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model=Faq
        fields='__all__'
class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model=Faq
        fields=('title_ar','content_ar','created_on')

class NotificationSerializer(serializers.ModelSerializer):
    created_on=serializers.SerializerMethodField()
    class Meta:
        model=Notification
        fields=('title','description','created_on')
    def get_created_on(self,instance):
        created_on=instance.created_on
        created_on=created_on.strftime('%Y-%m-%d %H:%M:%S')
        print(created_on)
        return created_on
class Ar_NotificationSerializer(serializers.ModelSerializer):
    title=serializers.SerializerMethodField()
    description=serializers.SerializerMethodField()
    created_on=serializers.SerializerMethodField()
    class Meta:
        model=Notification
        fields=('title','description','created_on')
    def get_title(self,instance):
        return instance.title_ar
    def get_description(self,instance):
        return instance.description_ar
    def get_created_on(self,instance):
        created_on=instance.created_on
        created_on=created_on.strftime('%Y-%m-%d %H:%M:%S')
        print(created_on)
        return created_on
