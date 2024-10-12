from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class FoodUser(User):
    class Meta:
        proxy = True


class Diet(models.Model):
    user = models.ForeignKey(
        FoodUser, models.CASCADE, related_name="diets", verbose_name=_("user")
    )
    name = models.CharField(_("name"), max_length=64)
    protein = models.FloatField(_("protein"))

    class Meta:
        verbose_name = _("diet")
        verbose_name_plural = _("diets")


class Day(models.Model):
    user = models.ForeignKey(
        FoodUser, models.CASCADE, related_name="days", verbose_name=_("user")
    )
    diet = models.ForeignKey(
        Diet,
        models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("diet"),
        related_name="days",
    )

    class Meta:
        verbose_name = _("day")
        verbose_name_plural = _("days")


class Comment(models.Model):
    user = models.ForeignKey(
        FoodUser,
        models.CASCADE,
        related_name="comments",
        verbose_name=_("user"),
    )
    text = models.TextField(_("text"))

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")


class Item(models.Model):
    user = models.ForeignKey(
        FoodUser, models.CASCADE, related_name="items", verbose_name=_("user")
    )
    name = models.CharField(_("name"), max_length=32)
    protein = models.FloatField(_("protein"))
    fat = models.FloatField(_("fat"))
    carbs = models.FloatField(_("carbs"))
    calories = models.FloatField(_("calories"))
