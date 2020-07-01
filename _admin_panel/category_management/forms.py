from django import forms
from django.contrib.auth.models import User

from _serviceprovider_panel.saccounts.models import *
from _user_panel.translation import translate_text_ar
# from accounts.models import *

class CreateCategoryForm(forms.Form):
    def clean(self):
        type=self.data['catname']
        type_ar=self.data['catname_ar']
        if not type or type=="":
            raise forms.ValidationError('Please provide category name')
        if not type_ar or type_ar=="":
            tdata=[]
            tdata.append(type)
            tres=translate_text_ar(tdata)
            type_ar=tres[0].text
            
        st_obj=ServiceType.objects.filter(type=type).first()
        if st_obj:
            raise forms.ValidationError('This category already exists')
        st_obj_ar=ServiceType.objects.filter(type=type_ar).first()
        if st_obj_ar:
            raise forms.ValidationError('This arabic category already exists')

class EditCategoryForm(forms.Form):
    def clean(self):
        cid=self.data['catid']
        type=self.data['catname']
        type_ar=self.data['catname_ar']
        if not type or type=="":
            raise forms.ValidationError('Please provide category name')
        if not type_ar or type_ar=="":
            tdata=[]
            tdata.append(type)
            tres=translate_text_ar(tdata)
            type_ar=tres[0].text
        print(cid)
        st_obj=ServiceType.objects.filter(type=type).exclude(id=cid).first()
        if st_obj:
            raise forms.ValidationError('This category already exists')
        st_obj_ar=ServiceType.objects.filter(type=type_ar).exclude(id=cid).first()
        if st_obj_ar:
            raise forms.ValidationError('This arabic category already exists')

class CreateSubCategoryForm(forms.Form):
    def clean(self):
        type=self.data['sty']
        subtype=self.data['catname']
        # type_ar=self.data['sty_ar']
        subtype_ar=self.data['catname_ar']

        if not subtype or subtype=="":
            raise forms.ValidationError('Please provide subcategory name')
        if not subtype_ar or subtype_ar=="":
            tdata=[]
            tdata.append(subtype)
            tres=translate_text_ar(tdata)
            subtype_ar=tres[0].text
        if not type or type=="":
            raise forms.ValidationError('Please select category')
        if type:
            st_obj=ServiceType.objects.filter(type=type).first()
            sst_obj=ServiceSubType.objects.filter(type=st_obj,subtype=subtype).first()
            if sst_obj:
                raise forms.ValidationError('This subcategory under this category already exists')
        
class EditSubCategoryForm(forms.Form):
    def clean(self):
        cid=self.data['catid']
        type=self.data['sty']
        subtype=self.data['catname']
        # type_ar=self.data['sty_ar']
        subtype_ar=self.data['catname_ar']

        if not subtype or subtype=="":
            raise forms.ValidationError('Please provide subcategory name')
        if not subtype_ar or subtype_ar=="":
            tdata=[]
            tdata.append(subtype)
            tres=translate_text_ar(tdata)
            subtype_ar=tres[0].text
        if not type or type=="":
            raise forms.ValidationError('Please select category')
        if type:
            st_obj=ServiceType.objects.filter(type=type).first()
            sst_obj=ServiceSubType.objects.filter(type=st_obj,subtype=subtype).exclude(id=cid).first()
            if sst_obj:
                raise forms.ValidationError('This subcategory under this category already exists')

class CreateCarModelForm(forms.Form):
    def clean(self):
        type=self.data['catname']
        type_ar=self.data['catname_ar']
        if not type or type=="":
            raise forms.ValidationError('Please provide model name')
        if not type_ar or type_ar=="":
            tdata=[]
            tdata.append(type)
            tres=translate_text_ar(tdata)
            type_ar=tres[0].text
        st_obj=VehicleModle.objects.filter(model_name=type).first()
        if st_obj:
            raise forms.ValidationError('This model already exists')
        st_obj_ar=VehicleModle.objects.filter(model_name_ar=type_ar).first()
        if st_obj_ar:
            raise forms.ValidationError('This model already exists in arabic')

class EditCarModelForm(forms.Form):
    def clean(self):
        type=self.data['catname']
        type_ar=self.data['catname_ar']
        is_edit = self.data['myhiddenfield']
        if not type or type=="":
            raise forms.ValidationError('Please provide model name')
        if not type_ar or type_ar=="":
            tdata=[]
            tdata.append(type)
            tres=translate_text_ar(tdata)
            type_ar=tres[0].text
        st = VehicleModle.objects.filter(id=is_edit).first()
        if not st:
            raise forms.ValidationError('This model id does not exists')
