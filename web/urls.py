"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import include, url
from apps import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = 'main'),
    url(r'^namesearch/$', views.name, name = 'view_name'),
    url(r'^detail/$', views.show_detail, name = 'detail'),
    url(r'^show_map/$', views.show_map, name = 'show_map'),
    url(r'^new_detail/$', views.show_new_detail, name = 'new_detail'),
]
