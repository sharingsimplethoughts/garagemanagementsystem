from django.shortcuts import render
from django.views.generic import TemplateView
import csv
from django.http import HttpResponse
from django.db.models import Q
from django.db.models import Count
from django.db.models import Sum
# Create your views here.
from _serviceprovider_panel.payments.models import *
from _user_panel.uaccounts.models import *

class AllReportsView(TemplateView):
    def get(self,request,*args,**kwargs):
        tot_user=RegisteredUser.objects.filter(Q(user_type=1)|Q(has_dual_account=True)).count()
        tot_sp=RegisteredUser.objects.filter(Q(user_type=2)|Q(has_dual_account=True)).count()
        tot_rev_gen=PaymentDetail.objects.filter(status='Completed').aggregate(Sum('price'))
        return render(request,'report_management/report_list.html',{'tuser':tot_user,'tsp':tot_sp,'trev':tot_rev_gen['price__sum']})

class DownloadCSVView(TemplateView):
    def get(self,request,*args,**kwargs):
        id=kwargs['pk']
        selection=request.GET['selection'+str(id)]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="report.csv"'

        if id=='f1':
            if selection=="Datewise":
                pass
            elif selection=="Weekly":
                pass
            elif selection=="Monthly":
                pass
        elif id=='f2':
            if selection=="Datewise":
                queryset=RegisteredUser.objects.filter(Q(user_type=1)|Q(has_dual_account=True)).extra(select={'period': 'date( created_on )'}).values('period').annotate(available=Count('created_on'))
            elif selection=="Weekly":
                queryset=RegisteredUser.objects.filter(Q(user_type=1)|Q(has_dual_account=True)).extra(select={'period': 'week( created_on )'}).values('period').annotate(available=Count('created_on'))
            elif selection=="Monthly":
                queryset=RegisteredUser.objects.filter(Q(user_type=1)|Q(has_dual_account=True)).extra(select={'period': 'month( created_on )'}).values('period').annotate(available=Count('created_on'))

        elif id=='f3':
            if selection=="Datewise":
                queryset=RegisteredUser.objects.filter(Q(user_type=2)|Q(has_dual_account=True)).extra(select={'period': 'date( created_on )'}).values('period').annotate(available=Count('created_on'))
            elif selection=="Weekly":
                queryset=RegisteredUser.objects.filter(Q(user_type=2)|Q(has_dual_account=True)).extra(select={'period': 'week( created_on )'}).values('period').annotate(available=Count('created_on'))
            elif selection=="Monthly":
                queryset=RegisteredUser.objects.filter(Q(user_type=2)|Q(has_dual_account=True)).extra(select={'period': 'month( created_on )'}).values('period').annotate(available=Count('created_on'))
        elif id=='f4':
            if selection=='Datewise':
                queryset=PaymentDetail.objects.filter(status='Completed').extra(select={'period': 'date( date_of_purchase )'}).values('period').annotate(available=Sum('price'))
            elif selection=='Weekly':
                queryset=PaymentDetail.objects.filter(status='Completed').extra(select={'period': 'week( date_of_purchase )'}).values('period').annotate(available=Sum('price'))
            elif selection=='Monthly':
                queryset=PaymentDetail.objects.filter(status='Completed').extra(select={'period': 'month( date_of_purchase )'}).values('period').annotate(available=Sum('price'))

        # queryset=RegisteredUser.objects.all()
        print(queryset)
        writer = csv.writer(response)
        field_names=['Sr. No.','period','available']
        writer.writerow(field_names)
        counter=0
        for q in queryset:
            print(q)
            counter+=1
            row=[counter,q['period'],q['available']]
            writer.writerow(row)
        #
        return response
