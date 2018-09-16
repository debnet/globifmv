# coding: utf-8
from django.urls import path

from fmv import views, api


urlpatterns = ([
    path('', views.index, name='index'),
], 'fmv')

# API REST
api_urlpatterns = ([

] + api.router.urls, 'fmv-api')
