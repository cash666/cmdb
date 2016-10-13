"""cmdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from web import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/',views.index),
    url(r'^idc/',views.idc),
    url(r'^host/',views.host),
    url(r'^create_idc/',views.create_idc),
    url(r'^delete_idc/',views.delete_idc),
    url(r'^save_idc/',views.save_idc),
    url(r'^modify_host/',views.modify_host),
    url(r'^delete_host/',views.delete_host),
    url(r'^create_host/',views.create_host),
    url(r'^asset_count/',views.asset_count),
    url(r'^delete_asset/',views.delete_asset),
    url(r'^group_manage/',views.group_manage),
    url(r'^delete_group/',views.delete_group),
    url(r'^create_group/',views.create_group),
    url(r'^show_hosts/',views.show_hosts),
    url(r'^single_command/',views.single_command),
    url(r'^put_files/',views.put_files),
    url(r'^upload_files/',views.upload_files),
    url(r'^multi_command/',views.multi_command),
    url(r'^task/',views.task),
    url(r'^create_task/',views.create_task),
    url(r'^delete_task/',views.delete_task),
    url(r'^acc_logout/',views.acc_logout),
    url(r'^asset_collect/',views.asset_collect),
]
