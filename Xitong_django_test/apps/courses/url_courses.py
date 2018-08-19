# -*- coding:utf-8 -*-

from django.conf.urls import url,include

from .views import CourseListView,CourseDetailView,CourseInfoView,CommentView,AddCommentView,VideoView

#url分解,避免urks中过大不好维护
urlpatterns = [
    #课程机构首页
    url(r'^list/$',CourseListView.as_view(),name = 'course_list'),

    #课程详情页
    url(r'^detail/(?P<course_id>\d+)/$',CourseDetailView.as_view(),name = 'course_detail'),


    #课程详情页
    #课程详情页
    url(r'^info/(?P<course_id>\d+)/$',CourseInfoView.as_view(),name = 'course_info'),

    #课程评论页
    url(r'^comment/(?P<course_id>\d+)/$',CommentView.as_view(),name = 'course_comment'),

    #添加课程评论
    url(r'^add_comment/$',AddCommentView.as_view(),name = 'add_comment'),

    #视频播放
    url(r'^video/$',VideoView.as_view(),name='course_videos')
]