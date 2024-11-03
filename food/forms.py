from django import forms
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.models import QuerySet, Max, Min
from django.core.exceptions import ValidationError

from .models import Group, Item, Record, Meal


class DayForm(forms.Form):
    date = forms.DateField(
        input_formats=["%Y-%m-%d"], required=True, label=_("date")
    )


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


class ItemSearchForm(forms.Form):
    template_name = "food/forms/item_search_form.html"

    query = forms.CharField(
        max_length=128, required=False, empty_value="", initial=""
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["group"] = forms.ModelChoiceField(
            user.food_groups.all(), required=False
        )
        self.queryset = user.food_items.all()

    def get_items(self) -> QuerySet | None:
        if not self.is_valid():
            return None
        items = self.queryset
        if group := self.cleaned_data["group"]:
            items = items.filter(group=group)
        if query := self.cleaned_data["query"]:
            items = items.filter(name__icontains=query)
        return items


class RecordForm(forms.ModelForm):
    template_name = "food/forms/record_form.html"

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields["item"] = forms.ModelChoiceField(
            self.user.food_items.all(), required=True
        )

    class Meta:
        model = Record
        fields = ["type", "value", "item"]
