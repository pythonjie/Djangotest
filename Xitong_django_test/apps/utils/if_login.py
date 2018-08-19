# -*- coding:utf-8 -*-

from django.shortcuts import render

class LoginRequest(object):
    def login(self,request):
        if request.user.is_authenticated() == False:
            return render(request,'login.html',{})



