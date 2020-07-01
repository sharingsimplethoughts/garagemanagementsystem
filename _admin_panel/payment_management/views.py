from django.shortcuts import render
from django.views.generic import TemplateView
import pytz
import csv
from django.http import HttpResponse
#FOR EXPORTING TABLE DATA
# import django_tables2 as tables
# from django_tables2.export.views import ExportMixin

# from _serviceprovider_panel.extra.models import MaintainCacheFlag
from django.core.cache import cache

from _serviceprovider_panel.payments.models import *
# from .tables import *
# Create your views here.
# ExportMixin, tables.SingleTableView
class PaymentListView(TemplateView):
    def get(self,request,*args,**kwargs):
        # table_class = MyTable
        # model = PaymentDetail
        # flag=''
        paymentlist=''
        cache_key='pm1'
        cache_time=86400
        # paymentlist=cache.get(cache_key)         #Uncomment this line to start memcached again
        # if paymentlist:
        #     flag=MaintainCacheFlag.objects.filter(model_name='PaymentDetail').first()
        #     if flag.is_changed:
        #         paymentlist=None
        if not paymentlist:
            print('-----------------no cache found OR cache has been reset-----------------')
            paymentlist=PaymentDetail.objects.all().order_by('-date_of_purchase')
            for p in paymentlist:
                p.date_of_purchase=str(p.date_of_purchase.strftime("%Y-%m-%d %H:%M:%S")).replace(',','-')
            template_name = 'payment_management/user_payment_list.html'
            cache.set(cache_key,paymentlist,cache_time)
            # if flag:
            #     flag.is_changed=False
            #     flag.save()
        return render(request,'payment_management/user_payment_list.html',{'paymentlist':paymentlist})

class PaymentDateWiseListView(TemplateView):
    def get(self, request, *args, **kwargs):
        w1=request.GET.get('startdate')
        w2=request.GET.get('enddate')
        w1=w1.split('/')
        w2=w2.split('/')
        start_date = datetime(int(w1[2]), int(w1[0]), int(w1[1]), 0, 0, 0, 0, pytz.timezone('Asia/Dubai'))
        end_date = datetime(int(w2[2]), int(w2[0]), int(w2[1]), 23, 59, 59, 999999, pytz.timezone('Asia/Dubai'))

        print(start_date)
        print(end_date)

        paymentlist = PaymentDetail.objects.filter(date_of_purchase__range=(start_date,end_date)).order_by('-date_of_purchase')
        for p in paymentlist:
            p.date_of_purchase=str(p.date_of_purchase.strftime("%Y-%m-%d %H:%M:%S")).replace(',','-')
        return render(request,'payment_management/user_payment_list.html',{'paymentlist':paymentlist})

# class TableView(ExportMixin, tables.SingleTableView):
#     table_class = MyTable
#     model = PaymentDetail
#     template_name = 'payment_management/user_payment_list.html'

# def exportToCSV(request):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="report.csv"'
#
#     queryset=PaymentDetail.objects.all()
#     writer = csv.writer(response)
#     field_names=['Sr. No.','SP. Name','Purchase Date','Status','Price','Subscribed Plan','Payment Mode']
#     writer.writerow(field_names)
#     counter=0
#     for q in queryset:
#         counter+=1
#         row=[counter,q.serv_provider.first_name,q.date_of_purchase,q.status,q.price,q.subscription_plan.plan_name,q.payment_mode]
#         writer.writerow(row)
#
#     return response
