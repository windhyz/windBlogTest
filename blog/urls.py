from django.conf.urls import url
from blog.views import *

urlpatterns = [
    url(r'^archive/$', archive, name='archive'),
    url(r'^article/$',article, name='article'),
    url(r'^tag/$', tagarticle, name='tagarticle'),
    url(r'^comment/post/$', comment_post, name='comment_post'),
    url(r'^logout$', bloglogout, name='logout'),
    url(r'^register', blogregister, name='register'),
    url(r'^login', bloglogin, name='login'),
    url(r'^$', index, name='index'),
]