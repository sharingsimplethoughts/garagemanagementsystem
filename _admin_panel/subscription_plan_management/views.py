from django.shortcuts import render
from django.views.generic import TemplateView
from datetime import datetime
import pytz
from django.db.models import Q

from _serviceprovider_panel.offer.models import *
from _user_panel.translation import translate_text_ar
from .forms import *

class SubscriptionPlanListView(TemplateView):
    def get(self,request,*args,**kwargs):
        sublist=SubscriptionPlan.objects.all()
        return render(request,'subscription_plan_management/user_subscription_list.html',{'sublist':sublist})

class SubscriptionPlanDateWiseListView(TemplateView):
    def get(self, request, *args, **kwargs):
        w1=request.GET.get('startdate')
        w2=request.GET.get('enddate')
        w1=w1.split('/')
        w2=w2.split('/')
        start_date = datetime(int(w1[2]), int(w1[0]), int(w1[1]), 0, 0, 0, 0, pytz.timezone('Asia/Dubai'))
        end_date = datetime(int(w2[2]), int(w2[0]), int(w2[1]), 23, 59, 59, 999999, pytz.timezone('Asia/Dubai'))

        print(start_date)
        print(end_date)

        sublist = SubscriptionPlan.objects.filter(created_on__range=(start_date,end_date))

        return render(request,'subscription_plan_management/user_subscription_list.html',{'sublist':sublist})

class AddNewSubscriptionView(TemplateView):
    def get(self,request,*args,**kwargs):
        return render(request,'subscription_plan_management/add_new_subscription.html')
    def post(self,request,*args,**kwargs):
        msg=''
        form=CheckAddNewSubPlanForm(data=request.POST or None)
        pname=request.POST['pname']
        pname=pname.strip()
        pdesc=request.POST['pdesc']
        pdesc=pdesc.strip()
        price=request.POST['price']
        valid_for=request.POST['valid_for']
        pname_ar=request.POST['pname_ar']
        pname_ar=pname_ar.strip()
        pdesc_ar=request.POST['pdesc_ar']
        pdesc_ar=pdesc_ar.strip()
        
        if not pname_ar or pname_ar=="":
            tdata=[]
            tdata.append(pname)
            tres=translate_text_ar(tdata)
            pname_ar=tres[0].text
        if not pdesc_ar or pdesc_ar=="":
            tdata=[]
            tdata.append(pdesc)
            tres=translate_text_ar(tdata)
            pdesc_ar=tres[0].text

        # pwrapper=request.POST.getlist('p')
        # for p in pwrapper:
        #     pass

        if form.is_valid():
            sp=SubscriptionPlan(
                plan_name=pname,
                plan_name_ar=pname_ar,
                plan_desc=pdesc,
                plan_desc_ar=pdesc_ar,
                price=price,
                valid_for=valid_for,
            )
            sp.save()
            msg='Plan saved successfully'
            return render(request,'subscription_plan_management/add_new_subscription.html',{'form':form,'msg':msg})
        context={}
        context['pname']=pname
        context['pname_ar']=pname_ar
        context['pdesc']=pdesc
        context['pdesc_ar']=pdesc_ar
        context['price']=price
        context['valid_for']=valid_for
        return render(request,'subscription_plan_management/add_new_subscription.html',{'context':context,'form':form})

class EditSubscriptionView(TemplateView):
    def get(self,request,*args,**kwargs):
        id=self.kwargs['pk']
        sp=SubscriptionPlan.objects.filter(id=id).first()
        return render(request,'subscription_plan_management/subscription_plan_edit.html',{'context':sp})

    def post(self,request,*args,**kwargs):
        id=self.kwargs['pk']
        msg=''
        form=CheckAddNewSubPlanForm(data=request.POST or None)
        pname=request.POST['pname']
        pname=pname.strip()
        pdesc=request.POST['pdesc']
        pdesc=pdesc.strip()
        pname_ar=request.POST['pname_ar']
        pname_ar=pname_ar.strip()
        pdesc_ar=request.POST['pdesc_ar']
        pdesc_ar=pdesc_ar.strip()
        price=request.POST['price']
        valid_for=request.POST['valid_for']

        if not pname_ar or pname_ar=="":
            tdata=[]
            tdata.append(pname)
            tres=translate_text_ar(tdata)
            pname_ar=tres[0].text
        if not pdesc_ar or pdesc_ar=="":
            tdata=[]
            tdata.append(pdesc)
            tres=translate_text_ar(tdata)
            pdesc_ar=tres[0].text

        if form.is_valid():
            sp=SubscriptionPlan.objects.filter(id=id).first()
            sp.plan_name=pname
            sp.plan_name_ar=pname_ar
            sp.plan_desc=pdesc
            sp.plan_desc_ar=pdesc_ar
            sp.price=price
            sp.valid_for=valid_for
            sp.save()            
            msg='Plan saved successfully'
            return render(request,'subscription_plan_management/subscription_plan_edit.html',{'context':sp,'form':form,'msg':msg})
        context={}
        context['plan_name']=pname
        context['plan_desc']=pdesc
        context['plan_name_ar']=pname_ar
        context['plan_desc_ar']=pdesc_ar
        context['price']=price
        context['valid_for']=valid_for
        return render(request,'subscription_plan_management/subscription_plan_edit.html',{'context':context,'form':form})
