# coding: utf-8
from common.admin import EntityAdmin, EntityTabularInline
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Count
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from fmv.models import User, Save, Scenario, Scene, Action, Choice, Condition, Item


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Administration des utilisateurs
    """
    fieldsets = BaseUserAdmin.fieldsets + (
        (_("AMV"), {'fields': ()}), )
    filter_horizontal = ('groups', 'user_permissions', )
    search_fields = ('username', 'first_name', 'last_name')
    save_on_top = True
    actions_on_bottom = True


@admin.register(Save)
class SaveAdmin(EntityAdmin):
    """
    Administration des sauvegardes
    """
    fieldsets = (
        (_("Informations"), dict(
            fields=('name', 'description', 'image', 'ip_address', 'user', 'scene', 'scenes', ),
            classes=('wide', ),
        )),
        (_("Ressources"), dict(
            fields=('health', 'money', 'items', ),
            classes=('wide', ),
        )),
    )
    inlines = []
    list_display_links = ('name', )
    list_display = ('name', 'user', 'ip_address', 'scene', 'health', 'money', )
    list_filter = ('scene', )
    search_fields = ('name', 'description', )
    ordering = ('name', )
    autocomplete_fields = ('user', 'scene', 'scenes', 'items', )
    save_on_top = True
    actions_on_bottom = True

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'scene')


@admin.register(Scenario)
class ScenarioAdmin(EntityAdmin):
    """
    Administration des scénarios
    """
    fieldsets = (
        (_("Informations"), dict(
            fields=('name', 'description', 'image', 'intro_scene', 'death_scene', ),
            classes=('wide', ),
        )),
        (_("Ressources"), dict(
            fields=('start_health', 'start_money', 'start_items', ),
            classes=('wide', 'hide', ),
        )),
    )
    inlines = []
    list_display_links = ('name', )
    list_display = ('name', )
    search_fields = ('name', 'description', )
    ordering = ('name', )
    autocomplete_fields = ('intro_scene', 'death_scene', 'start_items', )
    save_on_top = True
    actions_on_bottom = True


class ChoiceInlineAdmin(EntityTabularInline):
    """
    Administration des choix dans les scénarios
    """
    model = Choice
    fk_name = 'scene_from'
    exclude = ('description', 'image', 'operator', )
    extra = 1
    autocomplete_fields = ('scene_to', )


class ActionInlineAdmin(EntityTabularInline):
    """
    Administration des actions dans les choix
    """
    model = Action
    extra = 1
    autocomplete_fields = ('item', )


@admin.register(Scene)
class SceneAdmin(EntityAdmin):
    """
    Administration des scènes
    """
    fieldsets = (
        (_("Informations"), dict(
            fields=('name', 'description', 'image', 'scenario', ),
            classes=('wide', ),
        )),
        (_("Scène"), dict(
            fields=('url_high', 'url_low', 'timecode', ),
            classes=('wide', ),
        )),
    )
    inlines = [ChoiceInlineAdmin, ActionInlineAdmin]
    list_display_links = ('name',)
    list_display = ('name', 'scenario', 'url_high', 'nb_choices', )
    list_filter = ('scenario', )
    search_fields = ('name', 'description', )
    ordering = ('name', )
    autocomplete_fields = ('scenario', )
    save_on_top = True
    actions_on_bottom = True

    def nb_choices(self, obj):
        url = reverse('admin:fmv_choice_changelist')
        return mark_safe(f'<a href="{url}?scene_from={obj.id}">{obj.nb_choices}</a>')
    nb_choices.short_description = _("Choix")
    nb_choices.admin_order_field = 'nb_choices'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('scenario').annotate(
            nb_choices=Count('choices'))


class ConditionInlineAdmin(EntityTabularInline):
    """
    Administration des conditions dans les choix
    """
    model = Condition
    extra = 1
    autocomplete_fields = ('items', )


@admin.register(Choice)
class ChoiceAdmin(EntityAdmin):
    """
    Administration des choix
    """
    fieldsets = (
        (_("Informations"), dict(
            fields=('name', 'description', 'image', ),
            classes=('wide', ),
        )),
        (_("Choix"), dict(
            fields=('scene_from', 'scene_to', 'timecode', 'order', 'operator', ),
            classes=('wide', ),
        )),
    )
    inlines = [ConditionInlineAdmin]
    list_display_links = ('name', )
    list_display = ('name', 'scene_from', 'scene_to', 'order', 'count', 'nb_conditions', )
    list_filter = ()
    search_fields = ('name', 'description', )
    ordering = ('name', )
    autocomplete_fields = ('scene_from', 'scene_to', )
    save_on_top = True
    actions_on_bottom = True

    def nb_conditions(self, obj):
        return obj.nb_conditions
    nb_conditions.short_description = _("Conditions")
    nb_conditions.admin_order_field = 'nb_choices'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('scene_from', 'scene_to').annotate(
            nb_conditions=Count('conditions'))


@admin.register(Item)
class ItemAdmin(EntityAdmin):
    """
    Administration des objets
    """
    fieldsets = (
        (_("Informations"), dict(
            fields=('name', 'description', 'image', 'visible', ),
            classes=('wide', ),
        )),
    )
    list_display_links = ('name', )
    list_display = ('name', )
    list_filter = ('visible', )
    search_fields = ('name', 'description', )
    ordering = ('name', )
    autocomplete_fields = ()
    save_on_top = True
    actions_on_bottom = True
