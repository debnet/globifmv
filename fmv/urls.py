# coding: utf-8
from django.urls import path

from fmv import views, api


urlpatterns = ([
    path('', views.index, name='index'),
], 'fmv')

# API REST
api_urlpatterns = ([
    path('scene/<int:scene_id>/choices/', api.get_scene_choices, name='get_scene_choices'),
    path('start/<int:scenario_id>/', api.start_scenario, name='start_scenario'),
    path('choose/<int:choice_id>/', api.select_choice, name='select_choice'),
    path('<uuid:save_uid>/', api.get_save_by_uid, name='get_save_by_uid'),
    path('<uuid:save_uid>/<int:choice_id>/', api.select_choice_from_save, name='select_choice_from_save'),
] + api.router.urls, 'fmv-api')
