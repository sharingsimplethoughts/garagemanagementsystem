from django.shortcuts import render
from django.views.generic import TemplateView

from django.utils.html import strip_tags
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
# import datetime
import pytz
from datetime import datetime
from pyfcm import FCMNotification

# from fcm_django.models import FCMDevice

# from django.core.exceptions import ValidationError
# from django import forms

# from _user_panel.uaccounts.models import *
from _serviceprovider_panel.extra.models import *
from _user_panel.translation import translate_text_ar
from .forms import *
from .tasks import create_and_send_notification#, every_ten_seconds#, every_day_morning
# from _serviceprovider_panel.extra.models import MaintainCacheFlag
from django.core.cache import cache

class NotificationManagementCreateView(TemplateView):
    def get(self,request):
        flag=''
        users=''
        cache_key='nm1'
        cache_time=86400
        # users=cache.get(cache_key)         #Uncomment this line to start memcached again
        # if users:
        #     flag=MaintainCacheFlag.objects.filter(model_name='RegisteredUser_nm').first()
        #     if flag.is_changed:
        #         users=None
        if not users:
            print('-----------------no cache found OR cache has been reset-----------------')
            users = RegisteredUser.objects.filter(user_type__in=(1,2),user__is_active=True)
            cache.set(cache_key,users,cache_time)
            # if flag:
            #     flag.is_changed=False
            #     flag.save()
        return render(request,'notification_management/send_notification.html',{'users':users,'role':'0'})

    def post(self,request,*args,**kwargs):
        nottitle=request.POST['nottitle']
        notdesc=request.POST['notdesc']
        nottitle_ar=request.POST['nottitle_ar']
        notdesc_ar=request.POST['notdesc_ar']
        print('hello---------------------------')
        # if not nottitle_ar or nottitle_ar=="":
        #     tdata=[]
        #     tdata.append(nottitle)
        #     tres=translate_text_ar(tdata)
        #     nottitle_ar=tres[0].text
        # if not notdesc_ar or notdesc_ar=="":
        #     tdata=[]
        #     tdata.append(notdesc)
        #     tres=translate_text_ar(tdata)
        #     notdesc_ar=tres[0].text

        form = UnknownForm(request.POST)
        print('hello---------------------------')
        if form.is_valid():
            print('hello---------------------------')
            push_service= FCMNotification(api_key="api_key")
            #device token here
            registration_id="someregistrationid"
            message_title="garage Admin Message"
            message_body='garage - New mail sent by admin'
            result=push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

            qs=form.cleaned_data['select']
            qs=qs.values_list('id', flat=True)
            qs=list(qs)

            # uncomment this for celery and supervisor
            # current_site = get_current_site(request)
            # create_and_send_notification.delay(current_site.domain,qs,nottitle,notdesc,nottitle_ar,notdesc_ar)
            # every_ten_seconds()

            # print(task.get(timeout=100))
            for item in form.cleaned_data['select']:
                ruser=RegisteredUser.objects.filter(id=item.id).first()
                n=Notification(
                    title=nottitle,
                    description=notdesc,
                    title_ar=nottitle_ar,
                    description_ar=notdesc_ar,
                )
                n.save()
                un=UserNotification(
                    notification=n,
                    user=ruser,
                )
                un.save()

                '''
                Send confirmation email
                '''
                uemail=ruser.user.email
                current_site = get_current_site(request)
                subject = n.title
                message = render_to_string('notification_email.html', {
                    'user': ruser.user,
                    'domain': current_site.domain,
                    'not_desc':n.description,
                })
                plain_message = strip_tags(message)
                email = EmailMultiAlternatives(
                            subject, plain_message, 'garage <webmaster@localhost>', to=[uemail]
                )
                email.attach_alternative(message, "text/html")
                email.send()

                #FOR FIREBASE NOTIFICATION
                # device = FCMDevice.objects.filter(user=ruser.user).first()
                # device.send_message(title=nottitle, body=notdesc, data={"test": "test"})

            users = RegisteredUser.objects.filter(user_type__in=(1,2),user__is_active=True)
            return render(request,'notification_management/send_notification.html',{'users':users,'role':'0','message':'Notifications sent successfully.'})
        else:
            print('......')
            print(form.errors)

        users = RegisteredUser.objects.filter(user_type__in=(1,2),user__is_active=True)
        return render(request,'notification_management/send_notification.html',{'users':users,'role':'0','message':'Failed to sent notification.'})

# class NotificationManagementUserListView(TemplateView):
#     def get(self,request,*args,**kwargs):
#         users = RegisteredUser.objects.filter(user_type__in=(1,2),user__is_active=True)
#         return render(request,'notification_management/add_user.html',{'users':users,'role':'0'})

class NotificationManagementUserTypeWiseListView(TemplateView):
    def get(self,request,*args,**kwargs):
        role=self.kwargs['role']
        flag=''
        users=''
        cache_key='nm'+str(role)
        cache_time=86400
        # users=cache.get(cache_key)         #Uncomment this line to start memcached again
        # if users:
        #     flag=MaintainCacheFlag.objects.filter(model_name='RegisteredUser_nm').first()
        #     if flag.is_changed:
        #         users=None
        if not users:
            print('-----------------no cache found OR cache has been reset-----------------')
            users = RegisteredUser.objects.filter(user_type=role,user__is_active=True)
            cache.set(cache_key,users,cache_time)
            # if flag:
            #     flag.is_changed=False
            #     flag.save()
        return render(request,'notification_management/send_notification.html',{'users':users,'role':role})

class NotificationManagementUserDateWiseListView(TemplateView):
    def get(self, request, *args, **kwargs):
        role=self.kwargs['role']

        w1=request.GET.get('startdate')
        w2=request.GET.get('enddate')
        w1=w1.split('/')
        w2=w2.split('/')
        start_date = datetime(int(w1[2]), int(w1[0]), int(w1[1]), 0, 0, 0, 0, pytz.timezone('Asia/Dubai'))
        end_date = datetime(int(w2[2]), int(w2[0]), int(w2[1]), 23, 59, 59, 999999, pytz.timezone('Asia/Dubai'))

        print(start_date)
        print(end_date)
        if role in ('1','2'):
            users  = RegisteredUser.objects.filter(user_type=role,user__is_active=True,created_on__range=(start_date,end_date))
        else:
            users  = RegisteredUser.objects.filter(user_type__in=(1,2),user__is_active=True,created_on__range=(start_date,end_date))

        return render(request,'notification_management/send_notification.html',{'users':users,'role':role})
