from rest_framework import serializers
from rest_framework.exceptions import APIException
# from ffmpy import FFmpeg
#..
from datetime import datetime
from dateutil.relativedelta import relativedelta
from _serviceprovider_panel.offer.models import *
from _user_panel.uaccounts.models import FavoriteOffer
from django.db.models import Q
from _user_panel.translation import translate_text_ar

offer_detail_url=serializers.HyperlinkedIdentityField(view_name='spp_offer:spp_offer_detail',lookup_field='pk')
offer_update_url=serializers.HyperlinkedIdentityField(view_name='spp_offer:spp_offer_update',lookup_field='pk')
offer_delete_url=serializers.HyperlinkedIdentityField(view_name='spp_offer:spp_offer_delete',lookup_field='pk')

plan_detail_url=serializers.HyperlinkedIdentityField(view_name='spp_offer:spp_sub_plan_detail', lookup_field='pk')
subscribe_url=serializers.HyperlinkedIdentityField(view_name='spp_offer:spp_subscribe', lookup_field='pk')

make_fav_offer_url=serializers.HyperlinkedIdentityField(view_name='up_accounts:user_fav_off',lookup_field='pk')
remove_fav_offer_url=serializers.HyperlinkedIdentityField(view_name='up_accounts:user_remove_fav_off',lookup_field='pk')

class APIException400(APIException):
    satus_code=400

class CreateOfferSerializer(serializers.Serializer):
    garage=serializers.CharField(allow_blank=True,)
    image1=serializers.ImageField(required=False,)
    image2=serializers.ImageField(required=False,)
    image3=serializers.ImageField(required=False,)
    image4=serializers.ImageField(required=False,)
    video1=serializers.FileField(required=False,)
    video1_thumbnail=serializers.ImageField(required=False,)
    video2=serializers.FileField(required=False,)
    video2_thumbnail=serializers.ImageField(required=False,)
    title=serializers.CharField(allow_blank=True,)
    description=serializers.CharField(allow_blank=True,)
    coupon=serializers.CharField(allow_blank=True,)
    advertisment_license_number=serializers.CharField(allow_blank=True)
    start_date=serializers.CharField(allow_blank=True,)
    end_date=serializers.CharField(allow_blank=True,)

    class Meta:
        model=Offer
        fields=('garage','image1','image2','image3','image4','video1','video1_thumbnail',
        'video2','video2_thumbnail','title','description','coupon','advertisment_license_number',
        'start_date','end_date')

    def validate(self,data):
        garage=data['garage']
        title=data['title']
        description=data['description']
        coupon=data['coupon']
        advertisment_license_number=data['advertisment_license_number']
        start_date=data['start_date']
        end_date=data['end_date']

        if not garage or garage=="":
            raise APIException400({
                'messgae':'Garage name can not be blank',
                'success':'False',
            })
        else:
            ruser=self.context['ruser']
            garage_obj=Garage.objects.filter(user=ruser,name=garage).first()
            if not garage_obj:
                raise APIException400({
                    'messgae':'Garage name is not correct for this service provider.',
                    'success':'False',
                })
        if not title or title=='':
            raise APIException400({
                'messgae':'Title can not be blank',
                'success':'False',
            })
        if not description or description=='':
            raise APIException400({
                'messgae':'Description can not be blank',
                'success':'False',
            })
        if not coupon or coupon=='':
            raise APIException400({
                'messgae':'Coupon can not be blank',
                'success':'False',
            })
        if not advertisment_license_number or advertisment_license_number=='':
            raise APIException400({
                'messgae':'advertisment_license_number can not be blank',
                'success':'False',
            })
        if not start_date or start_date=='':
            raise APIException400({
                'messgae':'Start_date can not be blank',
                'success':'False',
            })
        if not end_date or end_date=='':
            raise APIException400({
                'messgae':'End_date can not be blank',
                'success':'False',
            })

        d=start_date.split('-')
        start_date = datetime(int(d[0]), int(d[1]), int(d[2]))#, 0, 0, 0, 0, pytz.timezone('Asia/Dubai'))
        # start_date=start_date.date()
        e=end_date.split('-')
        end_date = datetime(int(e[0]), int(e[1]), int(e[2]))#, 0, 0, 0, 0, pytz.timezone('Asia/Dubai'))
        # end_date=end_date.date()
        # d1 = datetime.datetime(2018, 5, 3)
        if start_date>end_date:
            raise APIException({
                'message':'Start date can not be grater than end date',
                'success':'False',
            })


        return data

    def create(self,validated_data,*args,**kwargs):
        request=self.context['request']
        # garage=self.context['garage']
        ruser=self.context['ruser']
        garage=validated_data['garage']
        image1=request.FILES.get('image1')
        image2=request.FILES.get('image2')
        image3=request.FILES.get('image3')
        image4=request.FILES.get('image4')
        video1=request.FILES.get('video1')
        video1_thumbnail=request.FILES.get('video1_thumbnail')
        video2=request.FILES.get('video2')
        video2_thumbnail=request.FILES.get('video2_thumbnail')
        title=validated_data['title']
        description=validated_data['description']
        coupon=validated_data['coupon']
        advertisment_license_number=validated_data['advertisment_license_number']
        start_date=validated_data['start_date']
        end_date=validated_data['end_date']

        garage_obj=Garage.objects.filter((Q(user=ruser) & Q(name=garage))|(Q(user=ruser) & Q(ar_name=garage))).first()
        usub=UserSubscription.objects.filter(ruser=ruser).first()
        #88888888888888888888888888888888888888888888888888888888888888888888888
        if usub:
            expires_on=usub.created_on+relativedelta(months=usub.plan.valid_for)
            days1=expires_on.date()-usub.created_on.date()
            # days=usub.plan.valid_for*30
            delta=datetime.now().date()-usub.created_on.date()
            if delta.days>days1.days:
                raise APIException400({
                    'message':'Sorry..!! Your subscription plan expired. To create new offers you must subscrib to a plan.',
                    'success':'False',
                })

        # usub.plan.valid_for

        #     pil_image2 = VideoStream(video2).get_frame_at_sec(5).image()

        #----------------Arabic Conversion--------------------------------
        tdata=[]
        tdata.append(title)
        tdata.append(description)
        tdata.append(advertisment_license_number)
        tres=translate_text_ar(tdata)

        offer=Offer(
            garage=garage_obj,
            image1=image1,
            image2=image2,
            image3=image3,
            image4=image4,
            video1=video1,
            video1_thumbnail=video1_thumbnail,
            video2=video2,
            video2_thumbnail=video2_thumbnail,
            title=title,
            description=description,
            coupon=coupon,
            advertisment_license_number=advertisment_license_number,
            start_date=start_date,
            end_date=end_date,
            ar_title=tres[0].text,
            ar_description=tres[1].text,
            ar_advertisment_license_number=tres[2].text,
        )
        offer.save()

#TRIED VIDEO THUMBNAIL
        # ff1=''
        # ff2=''
        # if offer.video1:
        #     ff1 = FFmpeg(inputs={offer.video1.url: None}, outputs={"output1.png": ['-ss', '00:00:4', '-vframes', '1']})
        # #     pil_image1 = VideoStream(video1).get_frame_at_sec(5).image()
        # if offer.video2:
        #     ff2 = FFmpeg(inputs={offer.video2.url: None}, outputs={"output2.png": ['-ss', '00:00:4', '-vframes', '1']})
        #
        # offer.video1_thumbnail=ff1
        # offer.video2_thumbnail=ff2
        # offer.save()

        validated_data['garage']=garage
        validated_data['image1']=offer.image1
        validated_data['image2']=offer.image2
        validated_data['image3']=offer.image3
        validated_data['image4']=offer.image4
        validated_data['video1']=offer.video1
        validated_data['video1_thumbnail']=offer.video1_thumbnail
        validated_data['video2']=offer.video2
        validated_data['video2_thumbnail']=offer.video2_thumbnail

        return validated_data

class GarageWiseOfferListSerializer(serializers.ModelSerializer):
    offer_detail_url=offer_detail_url
    make_fav_offer_url=make_fav_offer_url
    remove_fav_offer_url=remove_fav_offer_url
    is_favorite=serializers.SerializerMethodField()
    garage_name=serializers.SerializerMethodField()
    class Meta:
        model=Offer
        fields=('id','offer_detail_url','garage','garage_name','image1','image2',
        'image3','image4','video1','video1_thumbnail','video2','video2_thumbnail',
        'title','description','coupon','start_date','end_date','make_fav_offer_url',
        'remove_fav_offer_url','is_favorite')
    def get_garage_name(self,instance):
        return instance.garage.name
    def get_is_favorite(self,instance):
        user=self.context['request'].user.ruser
        if FavoriteOffer.objects.filter(offer=instance,user=user):
            return 'True'
        else:
            return 'False'
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['image1']:
            data['image1'] = ""
        if not data['image2']:
            data['image2'] = ""
        if not data['image3']:
            data['image3'] = ""
        if not data['image4']:
            data['image4'] = ""
        if not data['video1']:
            data['video1'] = ""
        if not data['video2']:
            data['video2'] = ""
        return data
class Ar_GarageWiseOfferListSerializer(serializers.ModelSerializer):
    offer_detail_url=offer_detail_url
    make_fav_offer_url=make_fav_offer_url
    remove_fav_offer_url=remove_fav_offer_url
    is_favorite=serializers.SerializerMethodField()
    garage_name=serializers.SerializerMethodField()
    title=serializers.SerializerMethodField()
    description=serializers.SerializerMethodField()
    # coupon=serializers.SerializerMethodField()

    class Meta:
        model=Offer
        fields=('id','offer_detail_url','garage','garage_name','image1','image2',
        'image3','image4','video1','video1_thumbnail','video2','video2_thumbnail',
        'title','description','coupon','start_date','end_date','make_fav_offer_url',
        'remove_fav_offer_url','is_favorite')
    def get_garage_name(self,instance):
        return instance.garage.ar_name
    def get_is_favorite(self,instance):
        user=self.context['request'].user.ruser
        if FavoriteOffer.objects.filter(offer=instance,user=user):
            return 'True'
        else:
            return 'False'
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['image1']:
            data['image1'] = ""
        if not data['image2']:
            data['image2'] = ""
        if not data['image3']:
            data['image3'] = ""
        if not data['image4']:
            data['image4'] = ""
        if not data['video1']:
            data['video1'] = ""
        if not data['video2']:
            data['video2'] = ""
        return data
    
    def get_title(self,instance):
        return instance.ar_title
    def get_description(self,instance):
        return instance.ar_description

class OfferDetailSerializer(serializers.ModelSerializer):
    offer_update_url=offer_update_url
    offer_delete_url=offer_delete_url
    garage_name=serializers.SerializerMethodField()

    class Meta:
        model=Offer
        fields=('offer_update_url','offer_delete_url','garage','garage_name','image1','image2',
        'image3','image4','video1','video1_thumbnail','video2','video2_thumbnail',
        'title','description','coupon','start_date','end_date','advertisment_license_number')
    def get_garage_name(self,instance):
        return instance.garage.name
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['image1']:
            data['image1'] = ""
        if not data['image2']:
            data['image2'] = ""
        if not data['image3']:
            data['image3'] = ""
        if not data['image4']:
            data['image4'] = ""
        if not data['video1']:
            data['video1'] = ""
        if not data['video2']:
            data['video2'] = ""
        return data
class Ar_OfferDetailSerializer(serializers.ModelSerializer):
    offer_update_url=offer_update_url
    offer_delete_url=offer_delete_url
    garage_name=serializers.SerializerMethodField()
    title=serializers.SerializerMethodField()
    description=serializers.SerializerMethodField()
    advertisment_license_number=serializers.SerializerMethodField()
    class Meta:
        model=Offer
        fields=('offer_update_url','offer_delete_url','garage','garage_name','image1','image2',
        'image3','image4','video1','video1_thumbnail','video2','video2_thumbnail',
        'title','description','coupon','start_date','end_date','advertisment_license_number')
    def get_garage_name(self,instance):
        return instance.garage.ar_name
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['image1']:
            data['image1'] = ""
        if not data['image2']:
            data['image2'] = ""
        if not data['image3']:
            data['image3'] = ""
        if not data['image4']:
            data['image4'] = ""
        if not data['video1']:
            data['video1'] = ""
        if not data['video2']:
            data['video2'] = ""
        return data
    def get_title(self,instance):
        return instance.ar_title
    def get_description(self,instance):
        return instance.ar_description
    def get_advertisment_license_number(self,instance):
        # return instance.ar_advertisment_license_number
        return instance.advertisment_license_number

class OfferUpdateSerializer(serializers.ModelSerializer):
    garage=serializers.CharField(read_only=True)
    image1=serializers.ImageField(required=False,)
    image2=serializers.ImageField(required=False,)
    image3=serializers.ImageField(required=False,)
    image4=serializers.ImageField(required=False,)
    video1=serializers.FileField(required=False,)
    video1_thumbnail=serializers.ImageField(required=False,)
    video2=serializers.FileField(required=False,)
    video2_thumbnail=serializers.ImageField(required=False,)
    title=serializers.CharField(allow_blank=True,)
    description=serializers.CharField(allow_blank=True,)
    coupon=serializers.CharField(allow_blank=True,)
    advertisment_license_number=serializers.CharField(allow_blank=True)
    start_date=serializers.CharField(allow_blank=True,)
    end_date=serializers.CharField(allow_blank=True,)

    class Meta:
        model=Offer
        fields=('garage','image1','image2','image3','image4','video1',
        'video1_thumbnail','video2','video2_thumbnail',
        'title','description','coupon','advertisment_license_number','start_date','end_date')

    def validate(self,data):
        title=data['title']
        description=data['description']
        coupon=data['coupon']
        advertisment_license_number=data['advertisment_license_number']
        start_date=data['start_date']
        end_date=data['end_date']

        if not title or title=='':
            raise APIException400({
                'messgae':'title can not be blank',
                'success':'False',
            })
        if not description or description=='':
            raise APIException400({
                'messgae':'description can not be blank',
                'success':'False',
            })
        if not coupon or coupon=='':
            raise APIException400({
                'messgae':'coupon can not be blank',
                'success':'False',
            })
        if not advertisment_license_number or advertisment_license_number=='':
            raise APIException400({
                'messgae':'advertisment_license_number can not be blank',
                'success':'False',
            })
        if not start_date or start_date=='':
            raise APIException400({
                'messgae':'start_date can not be blank',
                'success':'False',
            })
        if not end_date or end_date=='':
            raise APIException400({
                'messgae':'end_date can not be blank',
                'success':'False',
            })

        return data

    def create(self,validated_data,*args,**kwargs):
        request=self.context['request']
        offer=self.context['offer']

        image1=request.FILES.get('image1')
        image2=request.FILES.get('image2')
        image3=request.FILES.get('image3')
        image4=request.FILES.get('image4')
        video1=request.FILES.get('video1')
        video1_thumbnail=request.FILES.get('video1_thumbnail')
        video2=request.FILES.get('video2')
        video2_thumbnail=request.FILES.get('video2_thumbnail')
        title=validated_data['title']
        description=validated_data['description']
        coupon=validated_data['coupon']
        advertisment_license_number=validated_data['advertisment_license_number']
        start_date=validated_data['start_date']
        end_date=validated_data['end_date']

        #------------------Arabic Conversion-------------------------------
        tdata=[]
        tdata.append(title)
        tdata.append(description)
        tdata.append(advertisment_license_number)
        tres=translate_text_ar(tdata)
        #------------------------------------------------

        if image1:
            offer.image1=image1
        if image2:
            offer.image2=image2
        if image3:
            offer.image3=image3
        if image4:
            offer.image4=image4
        if video1:
            offer.video1=video1
        if video2:
            offer.video2=video2
        if video1_thumbnail:
            offer.video1_thumbnail=video1_thumbnail
        if video2_thumbnail:
            offer.video2_thumbnail=video2_thumbnail
        offer.title=title
        offer.description=description
        offer.coupon=coupon
        offer.advertisment_license_number=advertisment_license_number
        offer.start_date=start_date
        offer.end_date=end_date
        offer.ar_title=tres[0].text
        offer.ar_description=tres[1].text
        offer.ar_advertisment_license_number=tres[2].text
        offer.save()

        validated_data['garage']=offer.garage
        validated_data['image1']=offer.image1
        validated_data['image2']=offer.image2
        validated_data['image3']=offer.image3
        validated_data['image4']=offer.image4
        validated_data['video1']=offer.video1
        validated_data['video1_thumbnail']=offer.video1_thumbnail
        validated_data['video2']=offer.video2
        validated_data['video2_thumbnail']=offer.video2_thumbnail

        return validated_data

class SubPlanListSerializer(serializers.ModelSerializer):
    plan_detail_url=plan_detail_url
    subscribe_url=subscribe_url
    is_subscribed=serializers.SerializerMethodField()
    class Meta:
        model=SubscriptionPlan
        # fields=('plan_name','plan_desc','price','validity_from','validity_to','created_on','plan_detail_url')
        fields=('id','plan_name','plan_desc','price','valid_for','created_on','plan_detail_url','subscribe_url','is_subscribed')
    def get_is_subscribed(self,instance):
        user=self.context['request'].user
        ruser=RegisteredUser.objects.filter(user=user).first()
        usub=UserSubscription.objects.filter(ruser=ruser).first()

        if usub:
            if instance.id==usub.plan.id:
                return 'True'
        return 'False'

class Ar_SubPlanListSerializer(serializers.ModelSerializer):
    plan_name=serializers.SerializerMethodField()
    plan_desc=serializers.SerializerMethodField()
    plan_detail_url=plan_detail_url
    subscribe_url=subscribe_url
    is_subscribed=serializers.SerializerMethodField()
    class Meta:
        model=SubscriptionPlan
        # fields=('plan_name','plan_desc','price','validity_from','validity_to','created_on','plan_detail_url')
        fields=('id','plan_name','plan_desc','price','valid_for','created_on','plan_detail_url','subscribe_url','is_subscribed')
    def get_is_subscribed(self,instance):
        user=self.context['request'].user
        ruser=RegisteredUser.objects.filter(user=user).first()
        usub=UserSubscription.objects.filter(ruser=ruser).first()

        if usub:
            if instance.id==usub.plan.id:
                return 'True'
        return 'False'
    def get_plan_name(self,instance):
        return instance.plan_name_ar
    def get_plan_desc(self,instance):
        return instance.plan_desc_ar

class SubPlanDetailSerializer1(serializers.ModelSerializer):
    subscribe_url=subscribe_url
    class Meta:
        model=SubscriptionPlan
        # fields=('plan_name','plan_desc','price','validity_from','validity_to','created_on','subscribe_url')
        fields=('plan_name','plan_desc','price','valid_for','created_on','subscribe_url')

class Ar_SubPlanDetailSerializer1(serializers.ModelSerializer):
    plan_name=serializers.SerializerMethodField()
    plan_desc=serializers.SerializerMethodField()
    subscribe_url=subscribe_url
    class Meta:
        model=SubscriptionPlan
        fields=('plan_name','plan_desc','price','valid_for','created_on','subscribe_url')
    def get_plan_name(self,instance):
        return instance.plan_name_ar
    def get_plan_desc(self,instance):
        return instance.plan_desc_ar

class ChoosePaymentOptionSerializer(serializers.Serializer):
    choose_option = serializers.CharField()
    # redirect_url = redirect_url
    # class Meta:
    #     model=UserSubscription
    #     fields=

    def validate(self,data):
        choose_option=data['choose_option']
        if choose_option not in ('1','2','3','4'):
            raise APIException400({
                'messgae':'Please choose your payment option',
                'success':'False',
            })
    def create(self,validated_data):
        choose_option=validated_data['choose_option']
        if choose_option == '1':
            pass

# class TopTenOfferImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Offer
#         fields=('id','image1')
#
#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         if not data['image1']:
#             data['image1'] = ""
#         return data
