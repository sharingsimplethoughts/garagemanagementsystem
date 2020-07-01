from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.cache import cache
# Create your views here.
from _serviceprovider_panel.saccounts.models import *
from _admin_panel.notification_management.tasks import create_and_send_notification
from django.contrib.sites.shortcuts import get_current_site
# from _serviceprovider_panel.extra.models import MaintainCacheFlag

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from _serviceprovider_panel.extra.models import *
from _user_panel.translation import translate_text_ar

class ComplaintListView(TemplateView):
    def get(self,request,*args,**kwargs):
        # flag1=''
        # flag2=''
        complaints=''
        cache_key = 'cm1' # needs to be unique
        cache_time =86400 # time in seconds for cache to be valid - 24hrs(86400secs)
        # t1=datetime.now()
        # complaints = cache.get(cache_key) # returns None if no key-value pair           #Uncomment this line to start memcached again
        # print(datetime.now()-t1)
        # if complaints:
        #     flag1=MaintainCacheFlag.objects.filter(model_name='CustomerComplaint').first()
        #     flag2=MaintainCacheFlag.objects.filter(model_name='RegisteredUser_cm').first()
        #     if flag1.is_changed or flag2.is_changed:
        #         complaints=None
        if not complaints:
            print('------------------no cache found OR cache has been reset---------------------')
            # t1=datetime.now()
            complaints=CustomerComplaint.objects.all().order_by('-created_on')
            # print(datetime.now()-t1)
            cache.set(cache_key, complaints, cache_time)
            # if flag1:
            #     flag1.is_changed=False
            #     flag1.save()
            # if flag2:
            #     flag2.is_changed=False
            #     flag2.save()
        return render(request,'complaint_management/complaint_list.html',{'complaints':complaints})

class ComplaintDateWiseListView(TemplateView):
    def get(self, request, *args, **kwargs):
        w1=request.GET.get('startdate')
        w2=request.GET.get('enddate')
        w1=w1.split('/')
        w2=w2.split('/')
        start_date = datetime(int(w1[2]), int(w1[0]), int(w1[1]), 0, 0, 0, 0, pytz.timezone('Asia/Dubai'))
        end_date = datetime(int(w2[2]), int(w2[0]), int(w2[1]), 23, 59, 59, 999999, pytz.timezone('Asia/Dubai'))

        print(start_date)
        print(end_date)

        complaints = CustomerComplaint.objects.filter(created_on__range=(start_date,end_date)).order_by('-created_on')

        return render(request,'complaint_management/complaint_list.html',{'complaints':complaints})

class ComplaintEditView(TemplateView):
    def get(self,request,*args,**kwargs):
        id=self.kwargs['pk']
        comp=CustomerComplaint.objects.filter(id=id).first()
        return render(request,'complaint_management/edit_complaint.html',{'comp':comp})
    def post(self,request,*args,**kwargs):
        id=self.kwargs['pk']
        comp=CustomerComplaint.objects.filter(id=id).first()
        ruser=comp.user
        status=request.POST['sty']
        comp_email=request.POST['comp_email']
        user_email=request.POST['user_email']
        reply_message=request.POST['reply_message']
        reply_message_ar=request.POST['reply_message_ar']

        if not reply_message_ar or reply_message_ar=="":
            tdata=[]
            tdata.append(reply_message)
            tres=translate_text_ar(tdata)
            reply_message_ar=tres[0].text

        comp.admin_message=reply_message
        comp.admin_message_ar=reply_message_ar
        comp.status=status
        comp.save()

        '''
        Send confirmation email
        '''
        uemail=comp_email
        current_site = get_current_site(request)
        if ruser.language_pref=='1' or reply_message_ar=="":
            subject = "Garage - Complaint status update"
            message = render_to_string('complaint_email.html', {
                # 'user': ruser.user,
                'domain': current_site.domain,
                'not_desc':"Your Garage complaint status has been updated by admin to "+status,
                'reply_message':reply_message,
            })
        if ruser.language_pref=='2':
            tdata=[]
            tdata.append(status)
            tres=translate_text_ar(tdata)
            status_ar=tres[0].text
            subject = "Garage"
            message = render_to_string('complaint_email.html', {
                # 'user': ruser.user,
                'domain': current_site.domain,
                'not_desc':"تم تحديث حالة شكوى Garage بواسطة المشرف إلى "+status_ar,
                'reply_message':reply_message_ar,
            })
        
        plain_message = strip_tags(message)
        email = EmailMultiAlternatives(
                    subject, plain_message, 'Garage <webmaster@localhost>', to=[uemail]
        )
        email.attach_alternative(message, "text/html")
        email.send()

        # save notification
        print(user_email)
        print(comp_email)
        ruser=RegisteredUser.objects.filter(email=user_email).first()
        if ruser:
            n=Notification(
                title="Garage complaint status change",
                description="Your garage complaint status has been changed by admin. An email has been sent to the email id from which the complaint was generated.",
                title_ar="تغيير حالة شكوى Garage",
                description_ar="تم تغيير حالة شكوى Garage بواسطة المشرف. تم إرسال بريد إلكتروني إلى معرف البريد الإلكتروني الذي تم إنشاء الشكوى منه."
            )
            n.save()
            un=UserNotification(
                notification=n,
                user=ruser,
            )
            un.save()

        messages=[]
        messages.append('Status updated succesfully. An email has been sent to the complaint email id.')
        return render(request,'complaint_management/edit_complaint.html',{'comp':comp,'messages':messages})
