# coding: utf-8
from common.api.base import CONFIGS, DEFAULT_CONFIG
from common.api.utils import api_view_with_serializer as api_view, create_api, create_model_serializer
from django.db.models import F
from rest_framework import serializers
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny

from fmv.models import MODELS, Choice, Save, Scenario, Scene


# Surcharge des options de base
CONFIGS.update({
    Save: dict(many_to_many=True, depth=1, exclude=('scenes', )),
})

# Création des APIs REST standard pour les modèles de cette application
router, all_serializers, all_viewsets = create_api(*MODELS)

# Serializers
ChoiceSerializer = create_model_serializer(Choice)
SceneSerializer = create_model_serializer(Scene)


class SaveWithChoicesSerializer(all_serializers[Save]):
    """
    Serializer de la sauvegarde avec les choix possibles
    """
    choices = serializers.SerializerMethodField()

    def get_choices(self, save):
        choices = []
        query = Choice.objects.filter(scene_from_id=save.scene_id).prefetch_related('conditions').order_by('order')
        for choice in query:
            if choice.check_save(save):
                choices.append(choice)
        return ChoiceSerializer(choices, many=True, context=self.context).data


@api_view(['GET'], serializer=ChoiceSerializer)
@permission_classes([AllowAny, ])
def get_scene_choices(request, scene_id):
    """
    Choix de scène
    """
    save_uid = request.query_params.get('save_uid')
    if save_uid:
        save = get_object_or_404(Save.objects.prefetch_related('items'), uuid=save_uid)
        choices = []
        query = Choice.objects.filter(scene_from=scene_id).order_by('order')
        for choice in query:
            if choice.check_save(save):
                choices.append(choice)
        return choices
    return Choice.objects.filter(scene_from=scene_id).order_by('order')


@api_view(['GET'], serializer=SaveWithChoicesSerializer)
@permission_classes([AllowAny, ])
def start_scenario(request, scenario_id):
    """
    Démarrer un nouveau scénario
    """
    ip_address = request.META.get('REMOTE_ADDR') or ''
    scenario = get_object_or_404(Scenario, id=scenario_id)
    save_uid = request.query_params.get('save_uid')
    if save_uid:
        save = get_object_or_404(Save, uuid=save_uid)
        save.user = request.user if not request.user.is_anonymous else None
        save.ip_address = ip_address
        save.scene = scenario.intro_scene
        save.health = scenario.start_health
        save.money = scenario.start_money
        save.save()
    else:
        save = Save.objects.create(
            user=request.user if not request.user.is_anonymous else None,
            ip_address=ip_address,
            scene=scenario.intro_scene,
            health=scenario.start_health,
            money=scenario.start_money,)
    if scenario.intro_scene:
        save.scenes.add(scenario.intro_scene)
    save.items.set(scenario.start_items.all())
    return save


@api_view(['GET'], serializer=SceneSerializer)
@permission_classes([AllowAny, ])
def select_choice(request, choice_id, save_uid=None):
    """
    Sélectionner un choix de la scène
    """
    choice = get_object_or_404(
        Choice.objects.select_related('scene_from', 'scene_to').prefetch_related('conditions'), id=choice_id)
    save_uid = save_uid or request.query_params.get('save_uid')
    if save_uid:
        save = get_object_or_404(Save.objects.prefetch_related('items'), uuid=save_uid)
        if not choice.check_save(save):
            raise ValidationError(Choice.ERROR_CHECK)
        if save.switch_scene(choice.scene_to):
            Choice.objects.filter(id=choice_id).update(count=F('count') + 1)
    return choice.scene_to


@api_view(['GET'], serializer=SaveWithChoicesSerializer)
@permission_classes([AllowAny, ])
def get_save_by_uid(request, save_uid):
    """
    Visualiser une sauvegarde à partir de son UUID
    """
    return get_object_or_404(
        Save.objects.select_related('scene', 'user', 'current_user').prefetch_related('items', 'scenes'), uuid=save_uid)


@api_view(['GET'], serializer=SaveWithChoicesSerializer)
@permission_classes([AllowAny, ])
def select_choice_from_save(request, save_uid, choice_id):
    """
    Sélectionnne un choix de la scène courante depuis la sauvegarde
    """
    choice = get_object_or_404(
        Choice.objects.select_related('scene_from', 'scene_to').prefetch_related('conditions'), id=choice_id)
    save = get_object_or_404(
        Save.objects.select_related('scene', 'user', 'current_user').prefetch_related('items', 'scenes'), uuid=save_uid)
    if not choice.check_save(save):
        raise ValidationError(Choice.ERROR_CHECK)
    if save.switch_scene(choice.scene_to):
        Choice.objects.filter(id=choice_id).update(count=F('count') + 1)
    save.refresh_from_db()
    return save
