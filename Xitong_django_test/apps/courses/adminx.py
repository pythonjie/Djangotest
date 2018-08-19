# -*- coding: utf-8 -*-

import xadmin

from .models import Course,Lesson,Video,CourseResource


class CourseAdmin(object):
    list_display = ['name','desc','detail','degree','learn_time','students','fav_mums','image','click_nums','add_time']
    search_fields = ['name','desc','detail','degree']
    list_filter = ['name','desc','detail','degree','learn_time','students','fav_mums','image','click_nums','add_time']
    # ordering = ['-click_nums']  #排序


class LessonAdmin(object):
    list_display = ['course','name','add_time']
    search_fields = ['course','name']
    list_filter = ['course','name','add_time']


class VideoAdmin(object):
    list_display = ['lesson','name','add_time']
    search_fields = ['lesson','name']
    list_filter = ['lesson','name','add_time']


class CourseResoureceAdmin(object):
    list_display = ['course','name','download','add_time']
    search_fields = ['course','name','download']
    list_filter = ['course','name','download','add_time']


xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResource,CourseResoureceAdmin)