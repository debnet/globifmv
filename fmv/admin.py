# coding: utf-8
from common.admin import EntityAdmin, EntityStackedInline
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from fmv.models import User, Player, Scenario, Scene, Condition, Action, Choice, Item


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


@admin.register(Player)
class PlayerAdmin(EntityAdmin):
    """
    Administration des joueurs
    """
    fieldsets = (
        (_("Informations"), dict(
            fields=('name', 'description', 'user', 'ip', 'scenario', ),
            classes=('wide', ),
        )),
        (_("Ressources"), dict(
            fields=('health', 'money', 'items', 'scenes', ),
            classes=('wide', ),
        )),
    )
    inlines = []
    filter_horizontal = ('items', 'scenes', )
    list_display_links = ('name', )
    list_display = ('name', 'user', 'ip', 'scenario', 'health', 'money', )
    search_fields = ('name', 'description', )
    ordering = ('name', )
    autocomplete_fields = ('user', 'scenario', )
    save_on_top = True
    actions_on_bottom = True


@admin.register(Scenario)
class ScenarioAdmin(EntityAdmin):
    """
    Administration des scénarios
    """
    fieldsets = (
        (_("Informations"), dict(
            fields=('name', 'description', 'intro', ),
            classes=('wide', ),
        )),
        (_("Ressources"), dict(
            fields=('start_health', 'start_money', 'start_items', ),
            classes=('wide', 'hide', ),
        )),
    )
    inlines = []
    filter_horizontal = ('start_items', )
    list_display_links = ('name', )
    list_display = ('name', 'intro', )
    search_fields = ('name', 'description', )
    ordering = ('name', )
    autocomplete_fields = ('intro', )
    save_on_top = True
    actions_on_bottom = True


class ChoiceInlineAdmin(EntityStackedInline):
    """
    Administration des choix dans les scenes
    """
    model = Choice
    extra = 1
    fk_name = 'scene_from'
    autocomplete_fields = ('scene_to', )


class ActionInlineAdmin(EntityStackedInline):
    """
    Administration des actions dans les scénarios
    """
    model = Action
    extra = 1
    autocomplete_fields = ('item', 'scene', )


@admin.register(Scene)
class SceneAdmin(EntityAdmin):
    """
    Administration des scènes
    """
    fieldsets = (
        (_("Informations"), dict(
            fields=('name', 'description', 'scenario', 'url', ),
            classes=('wide',),
        )),
    )
    inlines = [ChoiceInlineAdmin, ActionInlineAdmin]
    filter_horizontal = ()
    list_display_links = ('name',)
    list_display = ('name', 'scenario', 'url', )
    search_fields = ('name', 'description', )
    ordering = ('name', )
    autocomplete_fields = ('scenario', )
    save_on_top = True
    actions_on_bottom = True


class ConditionInlineAdmin(EntityStackedInline):
    """
    Administration des conditions dans les choix
    """
    model = Condition
    extra = 1
    autocomplete_fields = ('item', 'scene', )


@admin.register(Choice)
class ChoiceAdmin(EntityAdmin):
    """
    Administration des choix
    """
    fieldsets = (
        (_("Informations"), dict(
            fields=('name', 'description', 'scene_from', 'scene_to', ),
            classes=('wide', ),
        )),
    )
    inlines = [ConditionInlineAdmin]
    filter_horizontal = ()
    list_display_links = ('name', )
    list_display = ('name', 'scene_from', 'scene_to', )
    search_fields = ('name', 'description', )
    ordering = ('name', )
    autocomplete_fields = ('scene_from', 'scene_to', )
    save_on_top = True
    actions_on_bottom = True


@admin.register(Item)
class ItemAdmin(EntityAdmin):
    """
    Administration des objets
    """
    fieldsets = (
        (_("Informations"), dict(
            fields=('name', ),
            classes=('wide', ),
        )),
    )
    filter_horizontal = ()
    list_display_links = ('name', )
    list_display = ('name', )
    search_fields = ('name', 'description', )
    ordering = ('name', )
    autocomplete_fields = ()
    save_on_top = True
    actions_on_bottom = True
