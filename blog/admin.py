# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from blog.models import *

class ArticleAdmin(admin.ModelAdmin):
    fieldsets = (
        (None,{'fields':('title','desc','content')}),
        ('高级设置', {
            'classes': ('collapse',),
            'fields': ('click_count', 'is_recommend','user','category','tag'),
        }),
    )

    class Media:
        js = (
            '/static/js/kindeditor-4.1.11/kindeditor-all-min.js',
            '/static/js/kindeditor-4.1.11/lang/zh_CN.js',
            '/static/js/kindeditor-4.1.11/config.js',
        )
admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Links)
admin.site.register(Ad)
admin.site.register(Navigate)
