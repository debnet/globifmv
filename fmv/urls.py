# coding: utf-8
from django.urls import path

from fmv import views, api


urlpatterns = ([
    path('', views.index, name='index'),
], 'fmv')

# API REST
api_urlpatterns = ([
    path('scene/<int:scene_id>/choices/', api.scene_choices, name='scene_choices'),
    path('scenario/<int:scenario_id>/start/', api.start_scenario, name='start_scenario'),
    path('choice/<int:choice_id>/select/', api.select_choice, name='select_choice'),
] + api.router.urls, 'fmv-api')
