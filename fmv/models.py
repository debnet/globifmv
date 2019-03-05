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


class Save(Entity, NamedModelMixin):
    """
    Sauvegarde
    """
    user = models.ForeignKey(
        'User', blank=True, null=True, on_delete=models.SET_NULL,
        related_name='players', verbose_name=_("utilisateur"))
    ip_address = models.CharField(
        max_length=40, blank=True, verbose_name=_("adresse IP"))
    scene = models.ForeignKey(
        'Scene', blank=True, null=True, on_delete=models.SET_NULL,
        related_name='players', verbose_name=_("scène courante"))
    scenes = models.ManyToManyField(
        'Scene', blank=True,
        related_name='+', verbose_name=_("scènes"))
    health = models.SmallIntegerField(
        blank=True, null=True, verbose_name=_("santé"))
    money = models.SmallIntegerField(
        blank=True, null=True, verbose_name=_("argent"))
    items = models.ManyToManyField(
        'Item', blank=True,
        related_name='+', verbose_name=_("objets"))

    def switch_scene(self, scene):
        if self.scene_id == scene.id:
            return False
        self.scene = scene
        self.scene.apply_action(self)
        self.save()
        return True

    class Meta:
        verbose_name = _("sauvegarde")
        verbose_name_plural = _("sauvegardes")


class Scenario(Entity, NamedModelMixin):
    """
    Scénario
    """
    intro_scene = models.ForeignKey(
        'Scene', blank=True, null=True, on_delete=models.SET_NULL,
        related_name='+', verbose_name=_("scène d'intro"))
    death_scene = models.ForeignKey(
        'Scene', blank=True, null=True, on_delete=models.SET_NULL,
        related_name='+', verbose_name=_("scène de mort"))
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
    url_high = models.URLField(
        blank=True, verbose_name=_("URL haut-débit"))
    url_low = models.URLField(
        blank=True, verbose_name=_("URL bas-débit"))
    timecode = models.FloatField(
        blank=True, null=True, verbose_name=_("timecode"))

    def get_choices(self, save):
        choices = []
        for choice in self.choices.all():
            if choice.check_save(save):
                choices.append(choice)
        return choices

    def apply_action(self, save):
        for action in self.actions.all():
            factor = -1 if action.type == '-' else +1
            if action.health is not None:
                save.health += action.health * factor
            if action.money is not None:
                save.money += action.money * factor
            if action.item_id:
                if factor > 0:
                    save.items.add(action.item_id)
                else:
                    save.items.remove(action.item_id)
        save.save()

    class Meta:
        verbose_name = _("scène")
        verbose_name_plural = _("scènes")


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


class Choice(Entity, NamedModelMixin):
    """
    Choix
    """
    ERROR_CHECK = _("This choice can't be selected because the current save state don't match the requirements.")
    OPERATOR_ALL, OPERATOR_ANY, OPERATOR_ONE, OPERATOR_NONE = 'all', 'any', 'one', 'none'
    OPERATORS = (
        (OPERATOR_ALL, _("toutes les conditions")),
        (OPERATOR_ANY, _("au moins une condition")),
        (OPERATOR_ONE, _("une seule condition")),
        (OPERATOR_NONE, _("aucune condition")),
    )

    scene_from = models.ForeignKey(
        'Scene', on_delete=models.CASCADE,
        related_name='choices', verbose_name=_("scène précédente"))
    scene_to = models.ForeignKey(
        'Scene', on_delete=models.CASCADE,
        related_name='next', verbose_name=_("scène suivante"))
    timecode = models.FloatField(
        blank=True, null=True, verbose_name=_("timecode"))
    order = models.PositiveSmallIntegerField(
        default=0, verbose_name=_("ordre"))
    count = models.PositiveSmallIntegerField(
        default=0, editable=False, verbose_name=_("compteur"))
    operator = models.CharField(
        max_length=4, default=OPERATOR_ALL, choices=OPERATORS,
        verbose_name=_("évaluation"))

    def check_save(self, save):
        if self.scene_from_id != save.scene_id:
            return False
        results = []
        for condition in self.conditions.all():
            results.append(condition.check_save(save))
        return all(results) if self.operator == self.OPERATOR_ALL else \
            any(results) if self.operator == self.OPERATOR_ANY else \
            results.count(True) == 1 if self.operator == self.OPERATOR_ONE else \
            not any(results)

    class Meta:
        verbose_name = _("choix")
        verbose_name_plural = _("choix")


class Condition(Entity):
    """
    Condition
    """
    choice = models.ForeignKey(
        'Choice', on_delete=models.CASCADE,
        related_name='conditions', verbose_name=_("choix"))
    health = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name=_("santé"))
    money = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name=_("argent"))
    items = models.ManyToManyField(
        'Item', blank=True, verbose_name=_("objets"))
    reverse = models.BooleanField(
        default=False, verbose_name=_("inversé"))

    def check_save(self, save):
        health = self.health is None or save.health is None or (
            (self.health > save.health) if self.reverse else (self.health <= save.health))
        money = self.money is None or save.money is None or (
            (self.money > save.money) if self.reverse else (self.money <= save.money))
        self_items, save_items = set(self.items.all()), set(save.items.all())
        items = (not self_items) or ((save_items >= self_items) if self.reverse else (save_items < self_items))
        return health and money and items

    class Meta:
        verbose_name = _("condition")
        verbose_name_plural = _("conditions")


class Item(Entity, NamedModelMixin):
    """
    Objet
    """
    visible = models.BooleanField(
        default=True, verbose_name=_("visible"))

    class Meta:
        verbose_name = _("objet")
        verbose_name_plural = _("objets")


MODELS = (
    User,
    Save,
    Scenario,
    Scene,
    Action,
    Choice,
    Condition,
    Item,
)
