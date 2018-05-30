# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
from django.db.models import Count
from blog.forms import *
from models import *

import logging

logger = logging.getLogger('blog.views')


def global_setting(request):
    # 站点基本信息
    SITE_URL = settings.SITE_URL
    SITE_NAME = settings.SITE_NAME
    SITE_DESC = settings.SITE_DESC
    #导航数据
    navs = Navigate.objects.filter(show=1)
    navslist = navs.filter(pid_id = None)
    subnavslist = navs.exclude(pid_id = None)

    #广告数据
    adslist = Ad.objects.all()
    #标签数据
    labelslist = Tag.objects.all()
    #友情链接数据
    linkslist = Links.objects.all()
    #文章归档数据
    archivelist = Article.objects.distinct_date()
    #评论排行
    commentcountlist = Comment.objects.values('article').annotate(commentcount = Count('article')).order_by('-commentcount')
    articlecommentlist = [Article.objects.get(pk=comment['article']) for comment in commentcountlist][:6]
    #浏览排行
    articleclicklist = Article.objects.all().order_by('-click_count')[:6]
    #站长推荐排行
    articlerecommendlist = Article.objects.all().order_by('-is_recommend')[:6]
    return locals()

def getPage(request,articlelist):
    paginator = Paginator(articlelist, 4)
    try:
        page = int(request.GET.get('page', 1))
        articlelist = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        articlelist = paginator.page(1)
    return articlelist

def index(request):

    try:
        #最新文章数据
        articlelist = Article.objects.all()
        articlelist = getPage(request,articlelist)
    except Exception as e:
        print(e)
        logger.error(e)
    return render(request,'index.html',locals())

#文章归档
def archive(request):
    try:
        #先获取客户提交的信息
        year = request.GET.get('year', None)
        month = request.GET.get('month', None)
        articlelist = Article.objects.filter(date_publish__icontains=year+"-"+month)
        articlelist = getPage(request,articlelist)
    except Exception as e:
        print(e)
        logger.error(e)
    return render(request, 'archive.html', locals())

# 文章详情
def article(request):
    id = request.GET.get("id", None)
    try:
        article =  Article.objects.get(pk=id)
        article.increase_click()

    except Article.DoesNotExist:
        return render(request,'failure.html',{"reason": "没找到对应的文章"})

    # 评论表单
    comment_form = CommentForm({'author': request.user.username,
                                'email': request.user.email,
                                'url': request.user.url,
                                'article': id} if request.user.is_authenticated() else {'article': id})
    # 获取评论信息
    comments = Comment.objects.filter(article=article).order_by('id')
    comment_list = []
    for comment in comments:
        for item in comment_list:
            if not hasattr(item, 'children_comment'):
                setattr(item, 'children_comment', [])
            if comment.pid == item:
                item.children_comment.append(comment)
                break
        if comment.pid is None:
            comment_list.append(comment)

    return render(request,'article.html',locals())

# 提交评论
def comment_post(request):
    try:
        commentform = CommentForm(request.POST)
        if commentform.is_valid():
            #获取表单信息
            comment = Comment.objects.create(username=commentform.cleaned_data["author"],
                                             email=commentform.cleaned_data["email"],
                                             url=commentform.cleaned_data["url"],
                                             content=commentform.cleaned_data["comment"],
                                             article_id=commentform.cleaned_data["article"],
                                             user=request.user if request.user.is_authenticated() else None)
            comment.save()
        else:
            return render(request, 'failure.html', {'reason': commentform.errors})
    except Exception as e:
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])

#登录
def bloglogin(request):
    try:
        if request.method == "POST":
            loginForm = LoginForm(request.POST)
            if loginForm.is_valid():
                # 登录
                username = loginForm.cleaned_data["username"]
                password = loginForm.cleaned_data["password"]
                user = authenticate(username=username,password=password)
                if user is not None:
                    # 指定默认的登录验证方式
                    user.backend = "django.contrib.auth.backends.ModelBackend"
                    login(request,user)
                else:
                    return render(request, 'failure.html', {'reason': '登录验证失败'})
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': loginForm.errors})
        else:
            loginForm = LoginForm()
    except Exception as e:
        logger.error(e)
    return render(request,'login.html',locals())

#注销
def bloglogout(request):

    try:
        logout(request)
    except Exception as e:
        print e
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])

#注册
def blogregister(request):
    try:
        if request.method == "POST":
            registerForm = RegisterForm(request.POST)
            if registerForm.is_valid():
                # 注册
                user = User.objects.create(username=registerForm.cleaned_data["username"],
                                           email=registerForm.cleaned_data["email"],
                                           url=registerForm.cleaned_data["url"],
                                           password=make_password(registerForm.cleaned_data["password"]),)
                user.save()
                # 登录 指定默认的登录验证方式
                user.backend = "django.contrib.auth.backends.ModelBackend"
                login(request,user)
                return redirect(request.POST.get("source_url"))
            else:
                return render(request,"failure.html",{"reason": registerForm.errors})
        else:
            registerForm = RegisterForm()
    except Exception as e:
        logger.error(e)
    return render(request,'register.html',locals())

def tagarticle(request):
    tag = request.GET.get("tag", None)
    try:
        articlelist = Article.objects.filter(tag__name__contains=tag)
        print(articlelist)
    except Exception as e:
        print(e)
        logger.error(e)
    return render(request, 'tagarticle.html', locals())