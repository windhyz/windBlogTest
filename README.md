# myblog

1、说明
python django-admin.py startproject project_name
python django-admin.py startapp app_name
 
2、要求
python 2.7
django 1.11
Pillow 5.1.0
MySQL-SQLdb 1.2.5

这些包都可以通过pip install 来安装

3、在开发过程中使用虚拟环境来安装
在第一步中建立一个项目后，进入到项目的目录后执行virtualenv --no-site-packages myvenv
我加了参数--no-site-packages，这样，已经安装到系统Python环境中的所有第三方包都不会复制过来，
这样，我们就得到了一个不带任何第三方包的“干净”的Python运行环境。
virtualenv可以通过pip 来安装

4、还有很多功能没有完善，将会慢慢完善。
