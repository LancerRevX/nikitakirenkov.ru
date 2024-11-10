from django import forms
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.models import QuerySet, Max, Min
from django.core.exceptions import ValidationError

from ..models import Day, Group, Item, Record, Meal

from .record import *


class DateForm(forms.Form):
    date = forms.DateField(input_formats=["%Y-%m-%d"])


class DayForm(forms.ModelForm):
    class Meta:
        model = Day
        fields = ["weight", "is_locked"]


class MealForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["position"] = forms.IntegerField(
            max_value=self.instance.day.meals.aggregate(
                position=Max("position")
            )["position"],
            min_value=self.instance.day.meals.aggregate(
                position=Min("position")
            )["position"],
            required=True,
        )

    class Meta:
        model = Meal
        fields = ["position"]


