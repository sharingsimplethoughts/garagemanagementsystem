import django_tables2 as tables
from _serviceprovider_panel.payments.models import *

class MyTable(tables.Table):
    class Meta:
        model=PaymentDetail
        export_formats = ['csv', 'xlsx']
