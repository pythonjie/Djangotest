# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from organization.models import CourseOrg,Teacher

from django.db import models

# Create your models here.


class Course(models.Model):   #课程数据库
    #添加一个外键
    course_org = models.ForeignKey(CourseOrg,verbose_name=u'课程机构',null=True,blank=True)  #这里需要添加null.blank是因为这个表里面早又数据，而添加数据这样不会出错
    name = models.CharField(max_length=50,verbose_name=u'课程名')
    desc = models.CharField(max_length=300,verbose_name=u'课程描述')
    detail = models.TextField(u'课程详情')
    degree = models.CharField(choices=(('cj',u'初级'),('zj',u'中级'),('gj',u'高级')),max_length=20)
    learn_time = models.IntegerField(default=0,verbose_name=u'学习时长（课时）')
    students = models.IntegerField(default=0,verbose_name=u'学习人数')
    fav_mums = models.IntegerField(default=0,verbose_name=u'收藏人数')
    image = models.ImageField(upload_to='courses/%Y/%m',verbose_name=u'封面图',max_length=100)
    click_nums = models.IntegerField(default=0,verbose_name=u'点击数')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')
    course_type = models.CharField(default=u'后端开发',max_length=30,verbose_name=u'课程类别')
    teacher = models.ForeignKey(Teacher,verbose_name=u'讲师',null=True,blank=True)
    youneed_known =models.CharField(max_length=300,verbose_name=u'课程须知',default='')
    teacher_tellyou = models.CharField(max_length=300,verbose_name=u'老师告诉你能学到什么',default='')
    isbanner = models.BooleanField(default=False,verbose_name=u'是否輪播')

    class Meta:
        verbose_name = u'课程名称'
        verbose_name_plural = verbose_name

    def lesson_zj_nums(self):  #章节数统计
        return self.lesson_set.all().count()

    def lean_stu_user(self):  #取出学习用户 在operation中的usercourse里
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):  #获取课程所有章节
        return self.lesson_set.all()

    def __unicode__(self):
        return  self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course,verbose_name=u'课程名')
    name = models.CharField(max_length=100, verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def get_lesson_vido(self):
        return self.video_set.all()

    def __unicode__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson,verbose_name=u'章节')
    name = models.CharField(max_length=100,verbose_name=u'视频名')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course,verbose_name=u'课程')
    name = models.CharField(max_length=100,verbose_name=u'名称')
    download = models.FileField(upload_to='course/resource',verbose_name=u'资源文件',max_length=100)
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name