# -*- coding: utf-8 -*-

import xadmin
from xadmin import views
from .models import EmailVerifyRecord,Banner


class BaseSetting(object):   #设置打开主题
    enable_themes = True  # 打开主题功能
    use_bootswatch = True


class GlobalSetting(object):  #修改上面的标题和中间下面的文字
    site_title = 'BOL杰后台课程管理系统'
    site_footer = 'BOL杰在线学习网'
    menu_style = 'accordion'  #折叠起左边的选择栏

class EmailVerifyRecordAdmin(object):
    list_display = ['code','email','send_type','send_time']
    search_fields = ['code','email']
    list_filter = ['code','email','send_type','send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index','add_time']
    search_fields = ['title', 'image']
    list_filter = ['title', 'image', 'url', 'index','add_time']


xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)

xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSetting)