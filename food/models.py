from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _, ngettext_lazy


class FoodUser(User):
    class Meta:
        proxy = True


class Diet(models.Model):
    user = models.ForeignKey(
        FoodUser, models.CASCADE, related_name="diets", verbose_name=_("user")
    )
    name = models.CharField(_("name"), max_length=64)
    protein = models.FloatField(_("protein"), null=True, blank=True)
    fat = models.FloatField(_("fat"), null=True, blank=True)
    carbs = models.FloatField(_("carbs"), null=True, blank=True)
    calories = models.FloatField(_("calories"), null=True, blank=True)

    class Meta:
        verbose_name = _("diet")
        verbose_name_plural = _("diets")


def default_date():
    return datetime.today().date()


class Day(models.Model):

    date = models.DateField(_("date"), default=default_date)
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

    def __str__(self) -> str:
        return str(self.date)

    class Meta:
        verbose_name = _("day")
        verbose_name_plural = _("days")
        constraints = [
            models.UniqueConstraint(
                fields=["user", "date"], name="unique_date_for_user"
            )
        ]


class Comment(models.Model):
    user = models.ForeignKey(
        FoodUser,
        models.CASCADE,
        related_name="comments",
        verbose_name=_("user"),
    )
    text = models.TextField(_("text"))

    def __str__(self):
        return f'{self.user}: "{self.text}"'

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")


class Group(models.Model):
    user = models.ForeignKey(
        FoodUser, models.CASCADE, related_name="item_groups", verbose_name=_("user")
    )
    name = models.CharField(_("name"), max_length=32)
    color = models.CharField(_("color"), max_length=7)
    items = models.ManyToManyField(
        "Item", related_name="groups", verbose_name=_("items")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("group")
        verbose_name_plural = _("groups")


class Item(models.Model):
    user = models.ForeignKey(
        FoodUser, models.CASCADE, related_name="items", verbose_name=_("user")
    )
    name = models.CharField(_("name"), max_length=256)
    # groups = models.ManyToManyField(
    #     Group, related_name="items", verbose_name=_("groups")
    # )
    protein = models.FloatField(_("protein"), help_text=_("Per 100g."))
    fat = models.FloatField(_("fat"), help_text=_("Per 100g."))
    carbs = models.FloatField(_("carbs"), help_text=_("Per 100g."))
    calories = models.FloatField(_("calories"), help_text=_("Per 100g."))
    piece_mass = models.FloatField(_("piece mass"), null=True, blank=True)
    pack_mass = models.FloatField(_("pack mass"), null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("item")
        verbose_name_plural = _("items")
        ordering = ["name"]


class Meal(models.Model):
    day = models.ForeignKey(
        Day, models.CASCADE, verbose_name=_("day"), related_name="meals"
    )
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.day} - meal #{self.order}"

    class Meta:
        verbose_name = _("meal")
        verbose_name_plural = _("meals")


class Record(models.Model):
    TYPES = {
        "mass": _("Mass"),
        "piece": _("Piece"),
        "pack": _("Pack"),
    }

    meal = models.ForeignKey(
        Meal, models.CASCADE, verbose_name=_("meal"), related_name="records"
    )
    item = models.ForeignKey(
        Item, models.PROTECT, verbose_name=_("item"), related_name="records"
    )
    type = models.CharField(_("type"), max_length=5, choices=TYPES, default="mass")
    value = models.FloatField(_("value"))

    def __str__(self):
        if self.type == "mass":
            return f"{self.item} {self.value}g"
        elif self.type == "piece":
            return (
                str(self.item)
                + " "
                + ngettext_lazy("%f piece", "%f pieces", self.value)
            )
        else:
            return (
                str(self.item) + " " + ngettext_lazy("%f pack", "%f packs", self.value)
            )

    class Meta:
        verbose_name = _("record")
        verbose_name_plural = _("records")
