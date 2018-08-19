# -*- coding: utf-8 -*-
import json


from django.shortcuts import render

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic.base import View
from .forms import LoginFrom,RegisterForms,ForgetForms,ModifypwdForms,UploadimageForm,Updatauser_infoForms
from django.contrib.auth.hashers import make_password
from .models import UserProfile,EmailVerifyRecord
from utils.email_send import send_register_email
from utils.if_login import LoginRequest
from operation.models import UserCourse
from .models import Banner
from courses.models import Course
from organization.models import CourseOrg


# Create your views here.


class CustomBanckend(ModelBackend):  #自定义authenicate的认证方法
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ActiveView(View):
    def get(self,request,active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:#如果不为空
            for records in all_records:
                email = records.email
                user = UserProfile.objects.get(email = email)
                user.is_active = True
                user.save()
        else:
            return render(request,'active_fail.html')
        return render(request,'login.html')


class RegisterView(View):
    def get(self,request):
        register_forms = RegisterForms()
        banner_courses = Course.objects.all().filter(isbanner=True)[:3]
        return render(request,'register.html',{
            'register_forms':register_forms,
            'banner_courses': banner_courses,
        })
    def post(self,request):
        register_forms = RegisterForms(request.POST)
        if register_forms.is_valid():
            email_1 = request.POST.get('email','')
            if UserProfile.objects.filter(email=email_1):
                return render(request,'register.html',{'msg':'用户名以存在'})
            pass_word = request.POST.get('password','')
            user_profile = UserProfile()
            user_profile.email = email_1
            user_profile.username = email_1
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            send_register_email(email_1,'register')
            return render(request, 'login.html', {})
        else:
            return render(request,'register.html',{'register_forms': register_forms})


class LogoutView(View):
    '''
    Y用户登出
    '''
    def get(self,request):
        logout(request)
        #页面重定向
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse('index'))



class LoginView(View):   #用类的方法来实现判断登录功能
    def get(self,request):  #重新定义get请求
        banner_courses = Course.objects.all().filter(isbanner=True)[:3]
        return render(request, 'login.html', {
            'banner_courses': banner_courses,
        })

    def post(self,request):  #重新定义post请求
        login_form = LoginFrom(request.POST)
        if login_form.is_valid():
            use_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=use_name, password=pass_word)  # 使用上面定义的认证方法
            if user is not None:
                if user.is_active:
                    login(request, user)
                    from django.core.urlresolvers import reverse
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request,'login.html',{'msg':'用户未激活'})
            else:
                return render(request,'login.html',{'msg':'用户名或密码错误'})
        else:
            return render(request,'login.html',{'login_form':login_form})


class ForgetpwdView(View):
    def get(self,request):
        forgetpwd_form = ForgetForms()
        banner_courses = Course.objects.all().filter(isbanner=True)[:3]
        return render(request,'forgetpwd.html',{
            'forgetpwd':forgetpwd_form,
            'banner_courses': banner_courses,
        })

    def post(self,request):
        forgetpwd_form = ForgetForms(request.POST)
        if forgetpwd_form.is_valid():
            email = request.POST.get('email','')
            send_register_email(email,'forget')
            return render(request, 'send_success.html')
            # return render(request, 'password_reset.html')
        else:
            return render(request, 'forgetpwd.html', {'forgetpwd': forgetpwd_form})





class ResetView(View):
    def get(self,request,active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:#如果不为空
            for records in all_records:
                email = records.email
                return render(request,'password_reset.html',{'email':email})
        else:
            return render(request,'active_fail.html')
        return render(request,'login.html')
    def post(self,request):
        modify_form = ModifypwdForms(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1','')
            pwd2 = request.POST.get('password2','')
            email = request.POST.get('email','')
            if pwd1 != pwd2:
                return render(request,'password_reset.html',{'email':email,'msg':'密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()

            return render(request,'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request,'password_reset.html',{'email':email,'modify_form':modify_form})


class ModifyView(View):
    '''
    修改密码功能
    '''
    def post(self,request):
        modify_form = ModifypwdForms(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email': email, 'msg': '密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()

            return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'modify_form': modify_form})

#用方法来实现实现判断登录功能
# def uer_longin(request):
#     if request.method == 'POST':
#         use_name = request.POST.get('username','')
#         pass_word =request.POST.get('password','')
#         user = authenticate(username=use_name, password=pass_word)  #使用上面定义的认证方法
#         if user is not None:
#             login(request,user)
#
#             return render(request,'index.html',{"msg":use_name})
#         else:
#             return render(request,'login.html',{"couwu":"用户名或密码错误"})
#     elif request.method == 'GET':
#         return render(request,'login.html',{})

class UserInfoView(View):
    #用户个人资料
    def get(self,request):
        #判断是否登录
        if request.user.is_authenticated() == False:
            return render(request,'login.html',{})
        return render(request,'usercenter-info.html',{})


class UploadImageView(View):
    #用户修改头像
    def post(self,request):
        image_form = UploadimageForm(request.POST,request.FILES)  #FILES文件类型 这样才能传进来
        if image_form.is_valid():
            # # image = image_form.request.FILES['image']
            # # request.user.image = image
            # # request.user.save()
            # image_form.save()
            image = image_form.files['image']
            request.user.image = image
            request.user.save()
            pass

# class Updatanick_nameView(View):
#     '''
#     用户昵称修改
#     '''
#     def post(self,request):
#         nick_name = Updatanicke_nameForms(request.POST)



class UpdataPwdView(View):
    '''
    在个人中心修改密码功能
    '''
    def post(self,request):
        modify_form = ModifypwdForms(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type="application/json")
            user = request.user
            user.password = make_password(pwd1)
            user.save()
            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type="application/json")



class MyCourseView(View):
    '''
    个人课程
    '''
    def get(self,request):
        #判断是否登录
        if request.user.is_authenticated() == False:
            return render(request,'login.html',{})
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request,'usercenter-mycourse.html',{
            'user_courses':user_courses,
        })



class IndexView(View):
    '''
    貫勇杰在線網首頁
    '''
    def get(self,request):
        #取出輪播圖
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.all().filter(isbanner=False)[:5]
        banner_courses = Course.objects.all().filter(isbanner=True)[:3]
        courses_orgs = CourseOrg.objects.all()[:15]
        return render(request,'index.html',{
            'all_banners':all_banners,
            'courses':courses,
            'banner_courses':banner_courses,
            'courses_orgs':courses_orgs
        })


def page404(request):
    '''
    404頁面
    '''
    from django.shortcuts import render_to_response
    response = render_to_response('500.html',{})
    response.status_code = 404
    return response







