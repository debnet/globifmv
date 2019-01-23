# coding: utf-8
from common.api.utils import api_view_with_serializer as api_view, create_api, create_model_serializer
from django.db.models import F
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny

from fmv.models import MODELS, Choice, Save, Scenario, Scene

# Création des APIs REST standard pour les modèles de cette application
router, all_serializers, all_viewsets = create_api(*MODELS)


@api_view(['GET'], serializer=create_model_serializer(Choice, exclude=('items', )))
@permission_classes([AllowAny, ])
def scene_choices(request, scene_id, save_uid=None):
    """
    Choix de scène
    """
    if save_uid:
        save = get_object_or_404(Save.objects.prefetch_related('items'), uuid=save_uid)
        choices = []
        query = Choice.objects.prefetch_related('items').filter(scene_from=scene_id).order_by('order')
        for choice in query:
            if choice.check_save(save):
                choices.append(choice)
        return choices
    else:
        return Choice.objects.filter(scene_from=scene_id).order_by('order')


@api_view(['GET'], serializer=create_model_serializer(Save, exclude=('scenes', 'items', )))
@permission_classes([AllowAny, ])
def start_scenario(request, scenario_id):
    """
    Démarrer un nouveau scénario
    """
    scenario = get_object_or_404(Scenario, id=scenario_id)
    save = Save.objects.create(
        user=request.user or None,
        ip_address=request.META.get('REMOTE_ADDR') or '',
        scene=scenario.intro_scene,
        health=scenario.start_health,
        money=scenario.start_money)
    if scenario.intro_scene:
        save.scenes.set(scenario.intro_scene)
    save.items.set(scenario.start_items.all())
    return save


@api_view(['GET'], serializer=create_model_serializer(Scene))
@permission_classes([AllowAny, ])
def select_choice(request, choice_id, save_uid=None):
    """
    Sélectionner un choix de la scène
    """
    choice = get_object_or_404(
        Choice.objects.select_related('scene_from', 'scene_to').prefetch_related('conditions'), id=choice_id)
    if save_uid:
        save = get_object_or_404(Save.objects.prefetch_related('items'), uuid=save_uid)
        if not choice.check_save(save):
            raise ValidationError(Choice.ERROR_CHECK)
        if save.switch_scene(choice.scene_to):
            Choice.objects.filter(id=choice_id).update(count=F('count') + 1)
    return choice.scene_to
