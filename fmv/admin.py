# coding: utf-8
from common.admin import EntityAdmin, EntityStackedInline
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from fmv.models import User, Player, Scenario, Scene, Choice, Condition, Action, Item, Fight


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
            fields=('name', 'description', 'image', 'user', 'ip', 'scenario', ),
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
    list_filter = ('scenario', )
    search_fields = ('name', 'description', )
    ordering = ('name', )
    autocomplete_fields = ('user', 'scenario', )
    save_on_top = True
    actions_on_bottom = True

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('scenario')


@admin.register(Scenario)
class ScenarioAdmin(EntityAdmin):
    """
    Administration des scénarios
    """
    fieldsets = (
        (_("Informations"), dict(
            fields=('name', 'description', 'image', 'intro', ),
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

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('intro')


class ChoiceInlineAdmin(EntityStackedInline):
    """
    Administration des choix dans les scénarios
    """
    model = Choice
    fk_name = 'scene_from'
    exclude = ('description', 'image', )
    extra = 1
    autocomplete_fields = ('scene_to', )


class ActionInlineAdmin(EntityStackedInline):
    """
    Administration des actions dans les scénarios
    """
    model = Action
    exclude = ('description', 'image', )
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
            fields=('url', 'timecode', 'fight', ),
            classes=('wide', ),
        )),
    )
    inlines = [ChoiceInlineAdmin, ActionInlineAdmin]
    filter_horizontal = ()
    list_display_links = ('name',)
    list_display = ('name', 'scenario', 'url', )
    list_filter = ('scenario', )
    search_fields = ('name', 'description', )
    ordering = ('name', )
    autocomplete_fields = ('scenario', 'fight', )
    save_on_top = True
    actions_on_bottom = True

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('scenario', 'fight')


class ConditionInlineAdmin(EntityStackedInline):
    """
    Administration des conditions dans les choix
    """
    model = Condition
    exclude = ('description', 'image', )
    extra = 1
    autocomplete_fields = ('item', )


@admin.register(Choice)
class ChoiceAdmin(EntityAdmin):
    """
    Administration des choix
    """
    fieldsets = (
        (_("Informations"), dict(
            fields=('name', 'description', 'image', ),
            classes=('wide',),
        )),
        (_("Choix"), dict(
            fields=('scene_from', 'scene_to', 'order', 'count', ),
            classes=('wide',),
        )),
    )
    inlines = [ConditionInlineAdmin]
    filter_horizontal = ()
    list_display_links = ('name',)
    list_display = ('name', 'scene_from', 'scene_to', 'order', 'count', )
    list_filter = ()
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
            fields=('name', 'description', 'image', 'attack', 'defense', ),
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


@admin.register(Fight)
class FightAdmin(EntityAdmin):
    """
    Administration des combats
    """
    fieldsets = (
        (_("Informations"), dict(
            fields=('name', 'description', 'image', ),
            classes=('wide', ),
        )),
        (_("Ennemi"), dict(
            fields=('health', 'attack', 'defense', ),
            classes=('wide', ),
        )),
        (_("Scènes"), dict(
            fields=('url_pc_hit', 'url_npc_hit', 'url_pc_miss', 'url_npc_miss', 'url_pc_dead', 'url_npc_dead', ),
            classes=('wide', ),
        )),
    )
    inlines = []
    filter_horizontal = ()
    list_display_links = ('name', )
    list_display = ('name', 'health', 'attack', 'defense', )
    search_fields = ('name', 'description', )
    ordering = ('name', )
    autocomplete_fields = ()
    save_on_top = True
    actions_on_bottom = True
