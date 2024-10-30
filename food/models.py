from datetime import datetime, date

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

    @property
    def protein(self):
        return sum(record.protein for record in self.meals.all())

    @property
    def fat(self):
        return sum(record.fat for record in self.meals.all())

    @property
    def carbs(self):
        return sum(record.carbs for record in self.meals.all())

    @property
    def calories(self):
        return sum(record.calories for record in self.meals.all())

    def is_today(self):
        return self.date == date.today()

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
        FoodUser, models.CASCADE, related_name="food_groups", verbose_name=_("user")
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


class ItemType(models.Model):
    user = models.ForeignKey(
        FoodUser, models.CASCADE, related_name="item_types", verbose_name=_("user")
    )
    name = models.CharField(_("name"), max_length=32)
    color = models.CharField(_("color"), max_length=7)

    def __str__(self):
        return self.name


class Item(models.Model):
    user = models.ForeignKey(
        FoodUser, models.CASCADE, related_name="food_items", verbose_name=_("user")
    )
    type = models.ForeignKey(
        ItemType,
        models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("type"),
        related_name="items",
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
        result = self.name
        if self.type is not None:
            result = f"{self.type} {result}"
        if self.groups.count() > 0:
            result += f" [{', '.join(self.groups.values_list('name', flat=True))}]"
        return result

    class Meta:
        verbose_name = _("item")
        verbose_name_plural = _("items")
        ordering = ["name"]


class Meal(models.Model):
    day = models.ForeignKey(
        Day, models.CASCADE, verbose_name=_("day"), related_name="meals"
    )
    position = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.day} - meal #{self.position}"

    @property
    def protein(self):
        return sum(record.protein for record in self.records.all())

    @property
    def fat(self):
        return sum(record.fat for record in self.records.all())

    @property
    def carbs(self):
        return sum(record.carbs for record in self.records.all())

    @property
    def calories(self):
        return sum(record.calories for record in self.records.all())

    class Meta:
        verbose_name = _("meal")
        verbose_name_plural = _("meals")
        ordering = ['position']


class Record(models.Model):
    class Type(models.TextChoices):
        MASS = "mass", _("Mass")
        PIECE = "piece", _("Piece")
        PACK = "pack", _("Pack")

    meal = models.ForeignKey(
        Meal, models.CASCADE, verbose_name=_("meal"), related_name="records"
    )
    item = models.ForeignKey(
        Item, models.PROTECT, verbose_name=_("item"), related_name="records"
    )
    type = models.CharField(_("type"), max_length=5, choices=Type, default=Type.MASS)
    value = models.FloatField(_("value"))

    def __str__(self):
        if self.type == self.Type.MASS:
            return f"{self.item} {self.value}g"
        elif self.type == self.Type.PIECE:
            return (
                str(self.item)
                + " "
                + ngettext_lazy("%f piece", "%f pieces", self.value)
            )
        else:
            return (
                str(self.item) + " " + ngettext_lazy("%f pack", "%f packs", self.value)
            )

    @property
    def protein(self):
        return self.item.protein * self.mass / 100.0

    @property
    def fat(self):
        return self.item.fat * self.mass / 100.0

    @property
    def carbs(self):
        return self.item.carbs * self.mass / 100.0

    @property
    def calories(self):
        return self.item.calories * self.mass / 100.0

    @property
    def mass(self):
        if self.type == self.Type.MASS:
            return self.value
        elif self.type == self.Type.PIECE:
            return self.item.piece_mass * self.value
        else:
            return self.item.pack_mass * self.value

    class Meta:
        verbose_name = _("record")
        verbose_name_plural = _("records")
