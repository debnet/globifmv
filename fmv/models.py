# coding: utf-8
from common.models import Entity
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _, ugettext as __


class User(AbstractUser):
    """
    Utilisateur
    """

    class Meta:
        verbose_name = _("utilisateur")
        verbose_name_plural = _("utilisateurs")


class NamedModelMixin(models.Model):
    """
    Mixin de modèle avec nom et description
    """
    name = models.CharField(
        blank=True, max_length=200, verbose_name=_("nom"))
    description = models.TextField(
        blank=True, verbose_name=_("description"))
    image = models.ImageField(
        blank=True, null=True, verbose_name=_("image"))

    def __str__(self):
        return self.name or str(self.id or __("(non enregistré)"))

    class Meta:
        abstract = True


class Player(Entity, NamedModelMixin):
    """
    Joueur
    """
    ip = models.CharField(max_length=40, verbose_name=_("adresse IP"))
    scenario = models.ForeignKey(
        'Scenario', on_delete=models.CASCADE,
        related_name='players', verbose_name=_("scénario"))
    user = models.ForeignKey(
        'User', blank=True, null=True, on_delete=models.SET_NULL,
        related_name='players', verbose_name=_("utilisateur"))
    health = models.SmallIntegerField(
        blank=True, null=True, verbose_name=_("santé"))
    money = models.SmallIntegerField(
        blank=True, null=True, verbose_name=_("argent"))
    items = models.ManyToManyField(
        'Item', blank=True,
        related_name='+', verbose_name=_("objets"))
    scenes = models.ManyToManyField(
        'Scene', blank=True,
        related_name='+', verbose_name=_("scènes"))

    class Meta:
        verbose_name = _("joueur")
        verbose_name_plural = _("joueurs")


class Scenario(Entity, NamedModelMixin):
    """
    Scénario
    """
    intro = models.OneToOneField(
        'Scene', blank=True, null=True, on_delete=models.SET_NULL,
        related_name='+', verbose_name=_("intro"))
    start_health = models.SmallIntegerField(
        blank=True, null=True, verbose_name=_("santé de départ"))
    start_money = models.SmallIntegerField(
        blank=True, null=True, verbose_name=_("argent de départ"))
    start_items = models.ManyToManyField(
        'Item', blank=True, related_name='+',
        verbose_name=_("objets de départ"))

    class Meta:
        verbose_name = _("scénario")
        verbose_name_plural = _("scénarios")


class Scene(Entity, NamedModelMixin):
    """
    Scène
    """
    scenario = models.ForeignKey(
        'Scenario', on_delete=models.CASCADE,
        related_name='scenes', verbose_name=_("scénario"))
    url = models.URLField(blank=True, verbose_name=_("URL"))
    timecode = models.FloatField(
        blank=True, null=True, verbose_name=_("timecode"))
    fight = models.ForeignKey(
        'Fight', blank=True, null=True, on_delete=models.SET_NULL,
        related_name='scenes', verbose_name=_("combat"))

    class Meta:
        verbose_name = _("scène")
        verbose_name_plural = _("scènes")


class Choice(Entity, NamedModelMixin):
    """
    Choix
    """
    scene_from = models.ForeignKey(
        'Scene', on_delete=models.CASCADE,
        related_name='choices', verbose_name=_("scène précédente"))
    scene_to = models.ForeignKey(
        'Scene', on_delete=models.CASCADE,
        related_name='next', verbose_name=_("scène suivante"))
    order = models.PositiveSmallIntegerField(
        default=0, verbose_name=_("ordre"))
    count = models.PositiveSmallIntegerField(
        default=0, verbose_name=_("compteur"))

    class Meta:
        verbose_name = _("choix")
        verbose_name_plural = _("choix")


class Action(Entity):
    """
    Action
    """
    TYPE = (
        ('+', _("ajouter")),
        ('-', _("retirer")),
    )

    scene = models.ForeignKey(
        'Scene', on_delete=models.CASCADE,
        related_name='actions', verbose_name=_("scène"))
    type = models.CharField(
        max_length=1, default='+',
        choices=TYPE, verbose_name=_("type"))
    health = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name=_("santé"))
    money = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name=_("argent"))
    item = models.ForeignKey(
        'Item', blank=True, null=True, on_delete=models.SET_NULL,
        related_name='+', verbose_name=_("objets"))

    class Meta:
        verbose_name = _("action")
        verbose_name_plural = _("actions")


class Condition(Entity):
    """
    Condition
    """
    TYPE = (
        ('&', _("et")),
        ('|', _("ou")),
    )

    choice = models.ForeignKey(
        'Choice', on_delete=models.CASCADE,
        related_name='conditions', verbose_name=_("choix"))
    type = models.CharField(
        max_length=1, default='&',
        choices=TYPE, verbose_name=_("type"))
    health = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name=_("santé"))
    money = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name=_("argent"))
    item = models.ForeignKey(
        'Item', blank=True, null=True, on_delete=models.SET_NULL,
        related_name='+', verbose_name=_("objets"))

    class Meta:
        verbose_name = _("condition")
        verbose_name_plural = _("conditions")


class Item(Entity, NamedModelMixin):
    """
    Objet
    """
    attack = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name=_("attaque"))
    defense = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name=_("défense"))

    class Meta:
        verbose_name = _("objet")
        verbose_name_plural = _("objets")


class Fight(Entity, NamedModelMixin):
    """
    Combat
    """
    health = models.PositiveSmallIntegerField(
        default=0, verbose_name=_("santé"))
    attack = models.PositiveSmallIntegerField(
        default=0, verbose_name=_("attaque"))
    defense = models.PositiveSmallIntegerField(
        default=0, verbose_name=_("défense"))
    url_pc_hit = models.URLField(
        blank=True, verbose_name=_("URL coup PJ"))
    url_npc_hit = models.URLField(
        blank=True, verbose_name=_("URL coup PNJ"))
    url_pc_miss = models.URLField(
        blank=True, verbose_name=_("URL raté PJ"))
    url_npc_miss = models.URLField(
        blank=True, verbose_name=_("URL raté PNJ"))
    url_pc_dead = models.URLField(
        blank=True, verbose_name=_("URL mort PJ"))
    url_npc_dead = models.URLField(
        blank=True, verbose_name=_("URL mort PNJ"))

    class Meta:
        verbose_name = _("combat")
        verbose_name_plural = _("combats")


MODELS = (
    User,
    Player,
    Scenario,
    Action,
    Scene,
    Condition,
    Item,
    Fight,
)
