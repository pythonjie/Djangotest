# -*- coding:utf-8 -*-
"""Xitong_django_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.views.static import serve #处理静态文件的

from django.views.generic import TemplateView
from users.views import LoginView,RegisterView,ActiveView,ForgetpwdView,ResetView,ModifyView,LogoutView,IndexView
from organization.views import OrgView
from Xitong_django_test.settings import MEDIA_ROOT,STATIC_ROOT
import xadmin

urlpatterns = [
    # url(r'^xadmin/', xadmin.site.urls),

    url(r'^xadmin/', include(xadmin.site.urls), name='xadmin'),


    url(r'^$',IndexView.as_view(),name='index'),
    url(r'^login/$',LoginView.as_view(),name='login'),
    url(r'^logout/$',LogoutView.as_view(),name='logout'),
    url(r'^register/$',RegisterView.as_view(),name='register'),
    url(r'^captcha/',include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$',ActiveView.as_view(),name='useractive'),
    url(r'forgetpwd/$',ForgetpwdView.as_view(),name='forgetpwd'),
    url(r'^reset/(?P<active_code>.*)/$',ResetView.as_view(),name='resetpwd'),
    url(r'modify/$',ModifyView.as_view(),name='modifypwd'),

    # #课程机构首页
    # url(r'^org_list/$',OrgView.as_view(),name = 'org_list'),
    #课程机构url配置
    url(r'^org/',include('organization.urls_organization',namespace='org')), #Namespace命名空间  避免出现命名问题

    #处理添加图片的url,配置上传文件的访问处理
    url(r'^media/(?P<path>.*)$',serve,{'document_root':MEDIA_ROOT}),

    #static文件的访问
    url(r'^static/(?P<path>.*)$',serve,{'document_root':STATIC_ROOT}),

    #公开课url设置
    url(r'^course/',include('courses.url_courses',namespace='course')),

    # #讲师相关url设置
    # url(r'^teacher/',include('courses.url_courses',namespace='course')),

    #个人中心url设置
    url(r'^users/',include('users.url_users',namespace='users')),

]

#全局404頁面
handler404 = 'users.views.page404'   #還需要在setting中設置DEBUG為false