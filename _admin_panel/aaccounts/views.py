from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login ,logout
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy,reverse
from django.contrib.auth import views as auth_views
from datetime import datetime

from .forms import *
from _user_panel.uaccounts.api.password_reset_form import MyPasswordResetForm

# Create your views here.
class AdminHomeView(LoginRequiredMixin,TemplateView):
    login_url='ap_accounts:alogin'
    # template_name='home/index.html'index
    def get(self, request, *args, **kwargs):
        anot = AllNotifications.objects.all().order_by('-created_on')[:7]
        return render(request, 'home/index.html',{'anot':anot})

class AllNotificationsView(TemplateView):
    def get(self,request,*args,**kwargs):
        anot = AllNotifications.objects.all().order_by('-created_on')
        # for a in anot:
        #     b = datetime.now().replace(microsecond=0)
        #     c = a.created_on.replace(microsecond=0)
        #     diff = b - c
        #     print(diff)
        #     #Need to check--------
            
        return render(request, 'home/notification.html',{'anot':anot})


class AdminLoginView(TemplateView):
    def get(self, request, *args, **kwargs):
        form = LoginForm
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('ap_accounts:ahome'))
        return render(request, 'aaccounts/login.html', {'form':form})

    def post(self,request,*args,**kwargs):
        form = LoginForm(data=request.POST or None)
        print(form.errors)
        if form.is_valid():
            em=request.POST['email']
            user_qs= User.objects.get(email=em, is_active=True, is_staff=True, is_superuser=True)
            if not request.POST.getlist('rememberChkBox'):
                request.session.set_expiry(0)
            login(request,user_qs,backend='django.contrib.auth.backends.ModelBackend')
            response = HttpResponseRedirect(reverse('ap_accounts:ahome'))
            # response.set_cookie['role_admin']
            response.set_cookie(key='id', value=1)
            return response
        return render(request,'aaccounts/login.html', {'form':form})

class AdminLogoutView(LoginRequiredMixin, TemplateView):
    login_url='ap_accounts:alogin'
    def get(self, request):
        logout(request)
        response = HttpResponseRedirect(reverse('ap_accounts:ahome'))
        response.delete_cookie(key='id')
        return response

class ResetPasswordView(auth_views.PasswordResetView):
    form_class = MyPasswordResetForm

class ChangePasswordView(LoginRequiredMixin,TemplateView):
    login_url='ap_accounts:alogin'
    def get(self,request):
        form = ChangePasswordForm(user=request.user)
        return render(request, 'aaccounts/change_password.html',{'form': form})

    def post(self,request):
        user = request.user
        form = ChangePasswordForm(request.POST or None, user=request.user)

        if form.is_valid():
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            return HttpResponseRedirect(reverse('ap_accounts:alogin'))
        return render(request, 'aaccounts/change_password.html',{'form': form})

class AdminProfileView(LoginRequiredMixin, TemplateView):
    login_url='ap_accounts:alogin'
    def get(self, request, *args, **kwargs):
        form=AdminProfileEditForm
        print(request.user)
        context={}
        context['email']=request.user.email
        ruser=RegisteredUser.objects.filter(user=request.user).first()
        if ruser:
            if ruser.last_name:
                context['name']=ruser.first_name+' '+ruser.last_name
            else:
                context['name']=ruser.first_name
            context['mobile']=ruser.mobile
            context['profile_image']=ruser.profile_image
            context['background_image']=ruser.background_image
            context['about']=ruser.about

        return render(request,'aaccounts/admin_profile.html',context)

class AdminProfileEditView(LoginRequiredMixin, TemplateView):
    login_url='ap_accounts:alogin'
    def get(self,request,*args,**kwargs):
        print('inside get')
        form=AdminProfileEditForm
        user=request.user
        context={
            'form':form,
            'email':user.email,
        }
        ruser=RegisteredUser.objects.filter(user=user).first()
        if ruser:
            if ruser.first_name:
                context['first_name']=ruser.first_name
            if ruser.last_name:
                context['last_name']=ruser.last_name

            context['mobile']=ruser.mobile
            context['profile_image']=ruser.profile_image
            context['background_image']=ruser.background_image
            context['about']=ruser.about
        return render(request,'aaccounts/admin_profile_change.html',context)

    def post(self,request,*args,**kwargs):
        print('inside post')
        user=request.user
        form=AdminProfileEditForm(data=request.POST or None, user=request.user)
        if form.is_valid():
            print('inside post valid form')
            try:
                ruser=RegisteredUser.objects.filter(user=user).first()
            except:
                ruser=None

            first_name=request.POST['firstname']
            last_name=request.POST['lastname']
            email=request.POST['email']
            mobile=request.POST['phonenumber']
            profile_image=request.FILES.get('profileimg')
            background_image=request.FILES.get('coverimg')
            about=request.POST['about']

            user.email=email
            user.first_name=first_name
            user.last_name=last_name
            user.save()

            if ruser:
                ruser.first_name=first_name
                ruser.last_name=last_name
                ruser.country_code='+971'
                ruser.mobile=mobile
                ruser.email=email
                if profile_image:
                    ruser.profile_image=profile_image
                if background_image:
                    ruser.background_image=background_image
                ruser.about=about
                ruser.user=user
                ruser.save()
            else:
                country_code='+971'
                RegisteredUser.objects.create(
                    first_name=first_name,last_name=last_name,
                    country_code=country_code,mobile=mobile,email=email,
                    profile_image=profile_image,background_image=background_image,
                    about=about,user=user,
                )
            return HttpResponseRedirect(reverse('ap_accounts:aprofile'))

        print(form.errors)
        return render(request,'aaccounts/admin_profile_change.html',{'form':form})
