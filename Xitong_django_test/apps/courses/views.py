# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator,EmptyPage,PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

from .models import Course,CourseResource
from operation.models import CourseComments
# Create your views here.


class CourseListView(View):
    def get(self,request):
        all_course = Course.objects.all().order_by('-add_time')   #默认排序最新排序

        hot_course = Course.objects.all().order_by('-click_nums')[:3]

        #搜索功能
        search_keywords = request.GET.get('keywords','')
        if search_keywords:
            all_course = all_course.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(
                detail__icontains=search_keywords))  #icontains 中的i表示django里面一般都是不区分大小写

        #进行人们与参与人数排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_course = all_course.order_by('-students')  # - 号代表倒叙排序
            elif sort == 'courses':
                all_course = all_course.order_by('-click_nums')

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # objects = ['john', 'edward', 'josh', 'frank']

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_course, 6, request=request)  # 这里的5是每一页只显示5个

        courses = p.page(page)

        return render(request,'course-list.html',{
            'all_course':courses,
            'sort':sort,
            'hot_course':hot_course
        })


class CourseDetailView(View):
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        #课程点击量增加
        course.click_nums += 1
        course.save()
        return render(request,'course-detail.html',{
            'course':course
        })



class CourseInfoView(View):
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()
        all_resourse = CourseResource.objects.filter(course=course)
        return render(request,'course-video.html',{
            'course':course,
            'all_resourse':all_resourse,
        })


class CommentView(View):
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        all_resourse = CourseResource.objects.filter(course=course)
        all_comment = CourseComments.objects.all()
        return render(request,'course-comment.html',{
            'course':course,
            'all_resourse':all_resourse,
            'all_comment':all_comment
        })


class AddCommentView(View):
    '''
    用户添加课程评论
    '''
    def post(self,request):
        if not request.user.is_authenticated():#判断用户是否登录
            return HttpResponse('{"status":"fail","msg":"用户未登录"}',content_type="application/json")

        course_id = request.POST.get('course_id',0)
        comments = request.POST.get('comments',"")
        if course_id > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.filter.get(id = int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success","msg":"添加成功"}', content_type="application/json")
        else:
            return HttpResponse('{"status":"fail","msg":"添加失败"}', content_type="application/json")

class VideoView(View):
    '''
    视频播放页面
    '''

    def get(self,request):
        all_course = Course.objects.all().order_by('-add_time')   #默认排序最新排序

        # hot_course = Course.objects.all().order_by('-click_nums')[:3]
        #
        # #搜索功能
        # search_keywords = request.GET.get('keywords','')
        # if search_keywords:
        #     all_course = all_course.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(
        #         detail__icontains=search_keywords))  #icontains 中的i表示django里面一般都是不区分大小写
        #
        # #进行人们与参与人数排序
        # sort = request.GET.get('sort', '')
        # if sort:
        #     if sort == 'students':
        #         all_course = all_course.order_by('-students')  # - 号代表倒叙排序
        #     elif sort == 'courses':
        #         all_course = all_course.order_by('-click_nums')
        #
        # # 分页
        # try:
        #     page = request.GET.get('page', 1)
        # except PageNotAnInteger:
        #     page = 1
        #
        # # objects = ['john', 'edward', 'josh', 'frank']
        #
        # # Provide Paginator with the request object for complete querystring generation
        #
        # p = Paginator(all_course, 4, request=request)  # 这里的5是每一页只显示5个
        #
        # courses = p.page(page)

        return render(request,'video.html',{
            # 'all_course':courses,
            # 'sort':sort,
            # 'hot_course':hot_course
        })

