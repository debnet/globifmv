# coding: utf-8
from django.urls import path

from fmv import api, views


urlpatterns = ([
    path('', views.index, name='index'),
], 'fmv')

# API REST
router = api.router
api_urlpatterns = ([
] + router.urls, 'fmv-api')
