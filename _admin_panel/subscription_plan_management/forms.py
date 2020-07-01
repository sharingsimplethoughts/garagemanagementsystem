from django import forms
from datetime import date
from datetime import datetime
from django.contrib.auth.models import User

from _serviceprovider_panel.saccounts.models import *
from _user_panel.translation import translate_text_ar

class CheckAddNewSubPlanForm(forms.Form):
    def clean(self):
        pname=self.data['pname']
        pdesc=self.data['pdesc']
        price=self.data['price']
        valid_for=self.data['valid_for']
        pname_ar=self.data['pname_ar']
        pdesc_ar=self.data['pdesc_ar']
        
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


        if not pname or pname == "":
            raise forms.ValidationError('Please provide plan name')
        if not pdesc or pdesc == "":
            raise forms.ValidationError('Please provide plan description')
        if not price or price == "":
            raise forms.ValidationError('Please provide price')
        if not pname_ar or pname_ar == "":
            raise forms.ValidationError('Please provide plan name in Arabic')
        if not pdesc_ar or pdesc_ar == "":
            raise forms.ValidationError('Please provide plan description in Arabic')
        


        price=price.split('.')
        if len(price) >2:
            raise forms.ValidationError('Please provide a valid price')
        pr=''
        for i in price:
            pr=pr+i
        if not pr.isdigit():
            raise forms.ValidationError('Please provide a valid price')
        if len(pr)>10:
            raise forms.ValidationError('Price is too high. Total 10 digits are possible including decimal.')
        if len(price)==2:
            if len(price[1])>2:
                raise forms.ValidationError('Please provide a valid price')

        


