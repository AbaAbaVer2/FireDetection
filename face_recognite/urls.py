"""face_recognite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.shortcuts import redirect
from controller.FaceController import *

# 首页重定向视图函数
def index_redirect(request):
    return redirect('/static/index.html')

#path(route , view , name)
urlpatterns = [
    # 首页重定向到index.html
    path('', index_redirect, name='index'),
    path('admin/', admin.site.urls),
    path("face_collect/",face_collection),
    path("face_detect/",face_detect),
    path("detection_detect/",predict),
]
