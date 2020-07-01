from django.shortcuts import render
from django.views.generic import TemplateView
from datetime import datetime
import pytz
from django.db.models import Q
# from django.core.exceptions import ValidationError
# from django import forms

# from _user_panel.uaccounts.models import *
from _serviceprovider_panel.saccounts.models import *
from _user_panel.translation import translate_text_ar
from .forms import *

# Create your views here.
class CategoryManagementListView(TemplateView):
    def get(self,request,*args,**kwargs):

        # subcatlist = ServiceSubType.objects.all()
        catlist = ServiceType.objects.all()
        for c in catlist:
            q2 = ServiceSubType.objects.filter(type=c)
            c.subcatlist=q2

        # return render(request,'category_management/cat_list.html',{'subcatlist':subcatlist,'catlist':catlist})
        return render(request,'category_management/cat_list.html',{'catlist':catlist})

class CategoryManagementDateWiseListView(TemplateView):
    def get(self, request, *args, **kwargs):
        w1=request.GET.get('startdate')
        w2=request.GET.get('enddate')
        w1=w1.split('/')
        w2=w2.split('/')
        start_date = datetime(int(w1[2]), int(w1[0]), int(w1[1]), 0, 0, 0, 0, pytz.timezone('Asia/Dubai'))#pytz.UTC)
        end_date = datetime(int(w2[2]), int(w2[0]), int(w2[1]), 23, 59, 59, 999999, pytz.timezone('Asia/Dubai'))#pytz.UTC)

        print(start_date)
        print(end_date)
        # subcatlist=ServiceSubType.objects.filter(created_on__range=(start_date,end_date))

        catlist = ServiceType.objects.filter(created_on__range=(start_date,end_date))
        for c in catlist:
            q2 = ServiceSubType.objects.filter(type=c)
            c.subcatlist=q2

        return render(request,'category_management/cat_list.html',{'catlist':catlist})

class CategoryManagementAddCategoryView(TemplateView):
    def get(self,request,*args,**kwargs):
        return render(request,'category_management/add_category.html')
    def post(self,request,*args,**kwargs):
        form = CreateCategoryForm(data=request.POST or None,)
        x=0
        if form.is_valid():
            type = request.POST['catname']
            type=type.strip()
            type_ar = request.POST['catname_ar']
            type_ar=type_ar.strip()
            if not type_ar or type_ar=="":
                tdata=[]
                tdata.append(type)
                tres=translate_text_ar(tdata)
                type_ar=tres[0].text

            icon = request.FILES.get('caticon')
            # print(icon.name)
            # print(icon.size)
            # print(icon.content_type)
            # print(icon.name.split('.')[-1])
            if icon:
                if icon.size>1024000:
                    x=1
                if icon.name.split('.')[-1].lower() not in ('png','jpg','jpeg'):
                    x=1
            if x==1:
                return render(request,'category_management/add_category.html',{'form':form,'x':x})
            if icon:
                st = ServiceType(
                    type=type,
                    type_ar=type_ar,
                    icon=icon,
                )
                st.save()
            else:
                st = ServiceType(
                    type=type,
                    type_ar=type_ar,
                )
                st.save()
            x=2
            return render(request,'category_management/add_category.html',{'form':form,'x':x})
        return render(request,'category_management/add_category.html',{'form':form})

class CategoryManagementAddSubCategoryView(TemplateView):
    def get(self,request,*args,**kwargs):
        st=ServiceType.objects.all()
        return render(request,'category_management/add_subcategory.html',{'st':st})
    def post(self,request,*args,**kwargs):
        form = CreateSubCategoryForm(data=request.POST or None)
        st=ServiceType.objects.all()
        x=0
        if form.is_valid():
            subtype = request.POST['catname']
            subtype=subtype.strip()
            subtype_ar = request.POST['catname_ar']
            subtype_ar = subtype_ar.strip()
            if not subtype_ar or subtype_ar=="":
                tdata=[]
                tdata.append(subtype)
                tres=translate_text_ar(tdata)
                subtype_ar=tres[0].text

            icon = request.FILES.get('caticon')
            # print(icon.name)
            # print(icon.size)
            # print(icon.content_type)
            # print(icon.name.split('.')[-1])
            if icon:
                if icon.size>1024000:
                    x=1
                if icon.name.split('.')[-1].lower() not in ('png','jpg','jpeg'):
                    x=1
            if x==1:
                return render(request,'category_management/add_subcategory.html',{'st':st,'form':form,'x':x})

            type = request.POST['sty']
            if type:
                type=ServiceType.objects.filter(type__iexact=type).first()
            if icon:
                sst = ServiceSubType(
                    subtype=subtype,
                    subtype_ar=subtype_ar,
                    icon=icon,
                    type=type,
                )
                sst.save()
            else:
                sst = ServiceSubType(
                    subtype=subtype,
                    subtype_ar=subtype_ar,
                    type=type,
                )
                sst.save()
            x=2
            return render(request,'category_management/add_subcategory.html',{'st':st,'form':form,'x':x})
        return render(request,'category_management/add_subcategory.html',{'st':st,'form':form})

class CategoryManagementAddCarModelView(TemplateView):
    def get(self,request,*args,**kwargs):
        models=VehicleModle.objects.all()
        return render(request,'category_management/add_car_model.html',context={'models':models,'hidden_value':0})

    def post(self,request,*args,**kwargs):
        models=VehicleModle.objects.all()
        is_edit = request.POST['myhiddenfield']
        
        if not int(is_edit):
            form = CreateCarModelForm(data=request.POST or None,)
            x=0
            if form.is_valid():
                type = request.POST['catname']
                type=type.strip()
                type_ar = request.POST['catname_ar']
                type_ar=type_ar.strip()
                if not type_ar or type_ar=="":
                    tdata=[]
                    tdata.append(type)
                    tres=translate_text_ar(tdata)
                    type_ar=tres[0].text
                icon = request.FILES.get('caticon')
                # print(icon.name)
                # print(icon.size)
                # print(icon.content_type)
                # print(icon.name.split('.')[-1])
                if icon:
                    if icon.size>1024000:
                        x=1
                    if icon.name.split('.')[-1].lower() not in ('png','jpg','jpeg'):
                        x=1
                if x==1:
                    return render(request,'category_management/add_car_model.html',{'models':models,'form':form,'x':x, 'hidden_value':0})
                if icon:
                    st = VehicleModle(
                        model_name=type,
                        model_name_ar=type_ar,
                        icon=icon,
                    )
                    st.save()
                else:
                    st = VehicleModle(
                        model_name=type,
                        model_name_ar=type_ar,
                    )
                    st.save()
                x=2
                return render(request,'category_management/add_car_model.html',{'models':models,'form':form,'x':x, 'hidden_value':0})
            return render(request,'category_management/add_car_model.html',{'models':models,'form':form, 'hidden_value':0})
        else:
            form = EditCarModelForm(data=request.POST or None,)
            x=0
            if form.is_valid():
                type = request.POST['catname']
                type=type.strip()
                type_ar = request.POST['catname_ar']
                type_ar=type_ar.strip()
                if not type_ar or type_ar=="":
                    tdata=[]
                    tdata.append(type)
                    tres=translate_text_ar(tdata)
                    type_ar=tres[0].text
                icon = request.FILES.get('caticon')
                # print(icon.name)
                # print(icon.size)
                # print(icon.content_type)
                # print(icon.name.split('.')[-1])
                if icon:
                    if icon.size>1024000:
                        x=1
                    if icon.name.split('.')[-1].lower() not in ('png','jpg','jpeg'):
                        x=1
                if x==1:
                    return render(request,'category_management/add_car_model.html',{'models':models,'form':form,'x':x, 'hidden_value':is_edit})
                st = VehicleModle.objects.filter(id=is_edit).first()
                print(type)
                print(type_ar)
                if icon:
                    st.model_name=type
                    st.model_name_ar=type_ar
                    st.icon=icon
                    st.save()
                else:
                    st.model_name=type
                    st.model_name_ar=type_ar
                    st.save()
                x=9
                return render(request,'category_management/add_car_model.html',{'models':models,'form':form,'x':x, 'hidden_value':0})
            return render(request,'category_management/add_car_model.html',{'models':models,'form':form, 'hidden_value':is_edit})

class CategoryManagementEditCategoryView(TemplateView):
    def get(self,request,*args,**kwargs):
        id = self.kwargs['id']
        cat = ServiceType.objects.filter(id=id).first()
        return render(request,'category_management/edit_category.html',{'cat':cat})
    def post(self,request,*args, **kwargs):
        id = self.kwargs['id']
        cat = ServiceType.objects.filter(id=id).first()
        form = EditCategoryForm(data=request.POST or None,)
        x=0
        if form.is_valid():
            type = request.POST['catname']
            type=type.strip()
            type_ar = request.POST['catname_ar']
            print(type_ar)
            type_ar=type_ar.strip()
            if not type_ar or type_ar=="":
                tdata=[]
                tdata.append(type)
                tres=translate_text_ar(tdata)
                type_ar=tres[0].text

            icon = request.FILES.get('caticon')
            # print(icon.name)
            # print(icon.size)
            # print(icon.content_type)
            # print(icon.name.split('.')[-1])
            if icon:
                if icon.size>1024000:
                    x=1
                if icon.name.split('.')[-1].lower() not in ('png','jpg','jpeg'):
                    x=1
            if x==1:
                return render(request,'category_management/edit_category.html',{'form':form,'x':x})
            if icon:
                cat.type=type
                cat.type_ar=type_ar
                cat.icon=icon
                cat.save()
            else:
                cat.type=type
                cat.type_ar=type_ar
                cat.save()
            x=2
            return render(request,'category_management/edit_category.html',{'form':form,'x':x,'cat':cat})
        return render(request,'category_management/edit_category.html',{'form':form, 'cat':cat})

class CategoryManagementEditSubCategoryView(TemplateView):
    def get(self,request,*args,**kwargs):
        id = self.kwargs['id']
        st=ServiceType.objects.all()
        scat = ServiceSubType.objects.filter(id=id).first()
        return render(request,'category_management/edit_subcategory.html',{'st':st,'scat':scat})
    def post(self,request,*args, **kwargs):
        id = self.kwargs['id']
        scat = ServiceSubType.objects.filter(id=id).first()

        form = EditSubCategoryForm(data=request.POST or None)
        st=ServiceType.objects.all()
        x=0
        if form.is_valid():
            subtype = request.POST['catname']
            subtype=subtype.strip()
            subtype_ar = request.POST['catname_ar']
            subtype_ar = subtype_ar.strip()
            if not subtype_ar or subtype_ar=="":
                tdata=[]
                tdata.append(subtype)
                tres=translate_text_ar(tdata)
                subtype_ar=tres[0].text

            icon = request.FILES.get('caticon')
            # print(icon.name)
            # print(icon.size)
            # print(icon.content_type)
            # print(icon.name.split('.')[-1])
            if icon:
                if icon.size>1024000:
                    x=1
                if icon.name.split('.')[-1].lower() not in ('png','jpg','jpeg'):
                    x=1
            if x==1:
                return render(request,'category_management/edit_subcategory.html',{'st':st,'form':form,'x':x})

            type = request.POST['sty']
            if type:
                type=ServiceType.objects.filter(type__iexact=type).first()
            if icon:
                scat.subtype=subtype
                scat.subtype_ar=subtype_ar
                scat.icon=icon
                scat.type=type
                scat.save()
            else:
                scat.subtype=subtype
                scat.subtype_ar=subtype_ar
                scat.type=type
                scat.save()
            x=2
            return render(request,'category_management/edit_subcategory.html',{'st':st,'form':form,'x':x, 'scat':scat})
        
        return render(request,'category_management/edit_subcategory.html',{'st':st, 'scat':scat})