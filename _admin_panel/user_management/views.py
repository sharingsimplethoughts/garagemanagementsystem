from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.cache import cache
import datetime
import pytz
from django.db.models import Q

from _user_panel.uaccounts.models import *
from _serviceprovider_panel.saccounts.models import *
# from _serviceprovider_panel.extra.models import MaintainCacheFlag
# Create your views here.


class UserManagementListView(TemplateView):
    def get(self,request,*args,**kwargs):
        # cache.clear()
        # flag=''
        users=''
        cache_key = 'um0'
        cache_time =86400
        # users = cache.get(cache_key)    #Uncomment this line to start memcached again
        # if users:
        #     flag=MaintainCacheFlag.objects.filter(model_name='RegisteredUser_um_0').first()
        #     if flag.is_changed:
        #         users=None

        if not users:
            print('------------------no cache found OR cache has been reset---------------------')
            users = RegisteredUser.objects.filter(user_type__in=(1,2)).order_by('-created_on')
            for u in users:
                if u.user_type == '2':
                    g_obj=Garage.objects.filter(user=u).first()
                    u.garage_name=''
                    if g_obj:
                        u.garage_name=g_obj.name

            cache.set(cache_key, users, cache_time)
                # if flag:
                #     flag.is_changed=False
                #     flag.save()
        return render(request,'user_management/user_list.html',{'users':users,'role':'0'})
    # template_name='user_management/user_list.html'
class UserManagementTypeWiseListView(TemplateView):
    def get(self,request,*args,**kwargs):
        users=''
        role=self.kwargs['role']
        # flag=''
        cache_key='um'+str(role)
        cache_time=86400
        # users=cache.get(cache_key)         #Uncomment this line to start memcached again
        # if users:
        #     flag=MaintainCacheFlag.objects.filter(model_name='RegisteredUser_um_'+str(role)).first()
        #     if flag.is_changed:
        #         users=None
        if not users:
            print('------------------no cache found OR cache has been reset---------------------')
            if role==3:
                users = RegisteredUser.objects.filter((Q(user_type=2) | Q(has_dual_account=True)) & Q(is_approved=False) & Q(user__is_active=True)).order_by('-created_on')
                for u in users:
                    if u.user_type == '2':
                        g_obj=Garage.objects.filter(user=u).first()
                        u.garage_name=''
                        if g_obj:
                            print(u.first_name)
                            u.garage_name=g_obj.name
                cache.set(cache_key, users, cache_time)
                # if flag:
                #     flag.is_changed=False
                #     flag.save()
                return render(request,'user_management/user_list.html',{'users':users,'role':role})
            users = RegisteredUser.objects.filter(Q(user_type=role) | Q(has_dual_account=True)).order_by('-created_on')
            for u in users:
                if u.user_type == '2':
                    g_obj=Garage.objects.filter(user=u).first()
                    u.garage_name=''
                    if g_obj:
                        print(u.first_name)
                        u.garage_name=g_obj.name
            cache.set(cache_key, users, cache_time)
            # if flag:
            #     flag.is_changed=False
            #     flag.save()
            return render(request,'user_management/user_list.html',{'users':users,'role':role})

        return render(request,'user_management/user_list.html',{'users':users,'role':role})

class UserManagementDateWiseListView(TemplateView):
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
            users  = RegisteredUser.objects.filter((Q(user_type=role) | Q(has_dual_account=True)) & Q(created_on__range=(start_date,end_date))).order_by('-created_on')
        else:
            users  = RegisteredUser.objects.filter(Q(user_type__in=(1,2)) & Q(created_on__range=(start_date,end_date))).order_by('-created_on')
        for u in users:
            if u.user_type == '2':
                g_obj=Garage.objects.filter(user=u).first()
                u.garage_name=''
                if g_obj:
                    print(u.first_name)
                    u.garage_name=g_obj.name

        return render(request,'user_management/user_list.html',{'users':users,'role':role})

class UserManagementServiceProviderDetailView(TemplateView):
    def get(self,request,*args,**kwargs):
        pk=self.kwargs['pk']
        role=self.kwargs['role']
        userdata=RegisteredUser.objects.filter(id=pk).first()
        garagedata=Garage.objects.filter(user=userdata).first()
        categorydata=CategoryManager.objects.filter(garage=garagedata)
        scheduledata=WeeklySchedule.objects.filter(garage=garagedata)
        # print(garagedata.country)
        return render(request,'user_management/userprofile.html',{'userdata':userdata,'garagedata':garagedata,
                                                                    'categorydata':categorydata,
                                                                    'scheduledata':scheduledata,
                                                                })
    # template_name='user_management/userprofile.html'
