# -*- coding:utf-8 -*-


from django import forms

from operation.models import UseAsk


#使用ModelForm继承机制,解决了重复
class UserForm(forms.ModelForm):

    class Meta:
        model = UseAsk
        fields = ['name','mobile','course_name']


