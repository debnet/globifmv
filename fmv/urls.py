# coding: utf-8
from django.urls import path

from fmv import views

namespace = 'fmv'
app_name = 'fmv'
urlpatterns = [
    path('', views.index, name='index'),
]
urls = (urlpatterns, namespace, app_name)
