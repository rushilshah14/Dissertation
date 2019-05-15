"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, re_path, include
from app import views, forms
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('',views.index,name='index'),
    path('404',views.pagenotfound,name='pagenotfound'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('dashboard',views.dashboard,name='dashboard'),
    path('newform',views.newform,name='newform'),
    path('units', views.unitcount, name='unitcount'),
    path('viewform', views.viewform, name='viewform'),
    path('userprofile', views.userprofile, name='userprofile'),
    path('secretarypanel/dashboard', views.secretarydashboard, name='secretarydashboard'),
    path('secretarypanel/viewform', views.secretaryviewform, name='secretaryviewform'),
    path('secretarypanel/publicdata', views.secretarypublicdata, name='secretarypublicdata'),
    path('studentrecord', views.studentrecord, name='studentrecord'),
    path('scrutinypanel/dashboard', views.scrutinydashboard, name='scrutinydashboard'),
    path('scrutinypanel/viewform', views.scrutinyviewform, name='scrutinyviewform')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
