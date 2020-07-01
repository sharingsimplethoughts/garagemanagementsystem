from celery import shared_task

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from dateutil.relativedelta import relativedelta
from _user_panel.uaccounts.models import *
from _serviceprovider_panel.extra.models import *
from _serviceprovider_panel.offer.models import *
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from pyfcm import FCMNotification

push_service_sp = FCMNotification(api_key="api_key1")
push_service_us = FCMNotification(api_key="api_key2")

@periodic_task(run_every=10.0)
def every_ten_seconds():
    # push_service=push_service_sp
    # registration_id="dy345XNxwp0:APA91bEvY9srCBaOLfUpdq3Am1d8scDl5krR_wD-tJg7KzrBu673F3rTKLDYg6bfY1Ui-fT69RE7x6MsNBWrhCoW-FGHZxNZ3BWV-_uG8FC190ewXttqjEymYQ7Km66TeT41mKdWHD0I"
    # message_title="garage Subscription Plan"
    # message_body='HELLO..!! FROM garage'
    # result=push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
    # print(result)
    print("This runs in every 10 seconds")

@periodic_task(run_every=crontab(hour=7, minute=30, day_of_week="sun,mon,tue,wed,thu,fri,sat"))
def every_day_morning():
    # user_qs=User.objects.filter(is_active=True)
    # ruser_qs=RegisteredUser.objects.filter(is_approved=True,user__in=user_qs)
    # usersub_qs=UserSubscription.objects.filter(ruser__in=ruser_qs)
    usersub_qs=UserSubscription.objects.filter(ruser__is_approved=True,ruser__user__is_active=True)
    for s in usersub_qs:
        if s.ruser.user_type=='2' or s.ruser.has_dual_account==True:
            timespan=datetime.now().date()-s.created_on.date()
            expires_on=s.created_on+relativedelta(months=s.plan.valid_for)
            validity=expires_on.date()-usub.created_on.date()
            # validity=s.plan.valid_for*30
            if (validity.days-timespan.days)<6:
                push_service = push_service_sp
                registration_id=s.ruser.device_token
                message_title="garage Subscription Plan"
                message_body='Please subscribe to a new plan to continue with offer creation for your garage. Your current plan expiry date: '+str(s.expires_on.date())+'. If already subscribed then please ignore this.'
                result=push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
                print(result)
                n=Notification(
                    title=message_title,
                    description=message_body,
                )
                n.save()
                un=UserNotification(
                    notification=n,
                    user=s.ruser,
                )
                un.save()
    print("This runs every Monday morning at 7:30a.m.")

@shared_task(track_started=True)
def create_and_send_notification(current_site,qs,nottitle,notdesc,nottitle_ar,notdesc_ar):
    print('hiiii')
    for item in qs:
        print(item)
        ruser=RegisteredUser.objects.filter(id=item).first()
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
        # current_site = get_current_site(request)
        if (ruser.language_pref=='1') or nottitle_ar=='' or notdesc_ar=='':
            subject = n.title
            message = render_to_string('notification_email.html', {
                'user': ruser.user,
                'domain': current_site,
                'not_desc':n.description,
            })
        elif ruser.language_pref=='2':
            subject = n.title_ar
            message = render_to_string('notification_email.html', {
                'user': ruser.user,
                'domain': current_site,
                'not_desc':n.description_ar,
            })

        plain_message = strip_tags(message)
        email = EmailMultiAlternatives(
                    subject, plain_message, 'garage <webmaster@localhost>', to=[uemail]
        )
        email.attach_alternative(message, "text/html")
        email.send()
    print('end')
    return 'success..!!'
