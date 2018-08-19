# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

#分页所需要的库
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from organization.models import CourseOrg,CityDict
from .forms import UserForm
from .models import Teacher
from courses.models import Course
# Create your views here.

class OrgView(View):
    #课程机构列表功能
    def get(self,request):
        #所有课程机构
        all_orgs = CourseOrg.objects.all()
        # 授课机构排名
        hot_orgs = all_orgs.order_by('-click_nums')[:3]


        # 搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_orgs = all_orgs.filter(name__icontains=search_keywords)  # icontains 中的i表示django里面一般都是不区分大小写



        #所有城市
        all_citys = CityDict.objects.all()
        #取出筛选城市
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        #筛选出机构类别
        orgtype = request.GET.get('ct', '')
        if orgtype:
            all_orgs = all_orgs.filter(orgtype=orgtype)

        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students') # - 号代表倒叙排序
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')


        org_nums = all_orgs.count()  #统计所有课程
        #分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        #objects = ['john', 'edward', 'josh', 'frank']

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_orgs,4, request=request)  #这里的5是每一页只显示5个

        orgs = p.page(page)





        return render(request,'org-list.html',{
            'all_orgs':orgs,
            'all_citys':all_citys,
            'org_nums':org_nums,
            'city_id':city_id,
            'orgtype':orgtype,
            'hot_orgs':hot_orgs,
            'sort':sort,
        })



class AddUserAskView(View):
    '''
    用户咨询
    '''
    def post(self,request):
        userask_form = UserForm(request.POST)
        if userask_form.is_valid():
            userask = userask_form.save(commit=True)  #直接保存到数据库里面去 commit为TRUE才能保存起
            return HttpResponse("{'status':'success'}",content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加错误"}'.format(userask_form.errors),content_type='application/json')


class OrgHomeView(View):
    def get(self,request,org_id):
        page = 'home'
        course_org = CourseOrg.objects.get(id = int(org_id))
        course_org.click_nums += 1
        course_org.save()
        all_course = course_org.course_set.all()[:3]  #有外键就可以这么用
        all_teachers = course_org.teacher_set.all()[:3]
        return render(request,'org-detail-homepage.html',{
            'all_course':all_course,
            'all_teachers':all_teachers,
            'course_org':course_org,
            'page':page
        })



class OrgCourseView(View):
    def get(self,request,org_id):
        page = 'course'
        course_org = CourseOrg.objects.get(id = int(org_id))
        all_course = course_org.course_set.all()  #有外键就可以这么用
        return render(request,'org-detail-course.html',{
            'all_course': all_course,
            'course_org': course_org,
            'page':page
        })


class OrgDescView(View):
    def get(self,request,org_id):
        page = 'desc'
        course_org = CourseOrg.objects.get(id = int(org_id)) #有外键就可以这么用
        return render(request,'org-detail-desc.html',{
            'course_org': course_org,
            'page':page
        })


class OrgTeacherView(View):
    def get(self,request,org_id):
        page = 'teacher'
        course_org = CourseOrg.objects.get(id = int(org_id))
        all_teacher = course_org.teacher_set.all()  #有外键就可以这么用
        return render(request,'org-detail-teachers.html',{
            'all_teacher': all_teacher,
            'course_org': course_org,
            'page':page
        })


class TeacherListView(View):
    #课程讲师列表页
    def get(self,request):
        all_teachers = Teacher.objects.all()

        # 搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_teachers = all_teachers.filter(name__icontains=search_keywords)  # icontains 中的i表示django里面一般都是不区分大小写

        #排序
        sort = request.GET.get('sort','')
        if sort:
            if sort == 'hot':
                all_teachers = all_teachers.order_by('-click_nums')

        sort_teachers = Teacher.objects.order_by('-work_years')[:2]

        #计数
        teachers_nums = all_teachers.count()


        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # objects = ['john', 'edward', 'josh', 'frank']

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_teachers, 3, request=request)  # 这里的5是每一页只显示5个

        teachers = p.page(page)

        return render(request,'teachers-list.html',{
            'all_teachers':teachers,
            'page_teachers': teachers,
            'sort_teacher':sort_teachers,
            'sort':sort,
            'teacher_num':teachers_nums,
        })


class TeacherDetailView(View):
    #讲师详情页
    def get(self,request,teacher_id):
        teacher = Teacher.objects.get(id = int(teacher_id))
        teacher.click_nums += 1
        teacher.save()
         #拿到老师的课程
        all_courses = Course.objects.filter(teacher = teacher)

        sort_teachers = Teacher.objects.order_by('-work_years')[:2]
        return render(request,'teacher-detail.html',{
            'all_courses':all_courses,
            'sort_teacher': sort_teachers,
            'teacher':teacher,

        })


