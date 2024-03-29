"""
URL configuration for myDjangoApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from dataHandler import views
urlpatterns = [
    path("admin/", admin.site.urls),

    # 返回obj文件
    path("objData/", views.returnObjData),

    # 返回polydata 
    path("polyData/", views.returnPolyData),

    # 保存label文件 
    path("saveLabel/", views.saveLabel),

    # 保存polydata为obj‘
    path("saveObjandsegTooth/", views.savePolyDataAsObj),

    # 接收分割请求并分割
    path("segmentBothTooth/", views.segmentBothTooth),

    # 保存label文件 by id
    path("saveLabelById/", views.saveLabelById),
]
