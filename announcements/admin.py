from django.contrib import admin
from import_export.admin import ExportActionModelAdmin

import announcements.models


# Register your models here.
@admin.register(announcements.models.Announcements)
class AnnouncementsAdmin(ExportActionModelAdmin, admin.ModelAdmin):
    """
    公告模型的后台管理，这里是用来注册需要的组件，
    显示字段、搜索字段、过滤字段、排序字段等（这里的排序等等只相当于formatter，不会影响实际数据库中的存储）
    以及一些自定义的按钮之类的功能
    """
    list_display = ['id', 'short_title', 'short_content', 'created_time', 'author']
    search_fields = ['title', 'content', 'author__username', 'author__nickname']
    ordering = ['-created_time', 'id']
    list_filter = ['author', 'created_time']
    list_per_page = 10
