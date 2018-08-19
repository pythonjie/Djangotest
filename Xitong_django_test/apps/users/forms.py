# -*- coding:utf-8 -*-
#form验证
from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile


class LoginFrom(forms.Form):
    username = forms.CharField(required=True)  #这里的必须和login.html中定义的一致,不然不会做验证
    password = forms.CharField(required=True,min_length=3)


class RegisterForms(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    captcha = CaptchaField(error_messages={'invalid':u'验证码错误'})


class ForgetForms(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid':u'验证码错误'})


class ModifypwdForms(forms.Form):
    password1 = forms.CharField(required=True,)
    password2 = forms.CharField(required=True,)


class UploadimageForm(forms.Form):
    #用户头像上传
    class Meta:
        model = UserProfile
        fields = ['image']

class Updatauser_infoForms(forms.Form):
    nick_name = forms.CharField(required=True)
    birth_day =forms.CharField(required=True)
    address =forms.CharField(required=True)
    mobile =forms.CharField(required=True)
