# -*- coding:utf-8 -*-

from django.conf.urls import url,include


from .views import UserInfoView,UploadImageView,UpdataPwdView,MyCourseView

#url分解,避免urks中过大不好维护
urlpatterns = [
    #个人资料
    url(r'^info/$',UserInfoView.as_view(),name = 'users_info'),

    #用户头像上传
    url(r'^image/upload/$',UploadImageView.as_view(),name = 'image_upload'),

    #用户密码
    url(r'^updata/pwd/$',UpdataPwdView.as_view(),name = 'updata_pwd'),

    #用户头像上传
    url(r'^mycourse/$',MyCourseView.as_view(),name = 'mycourse'),
]