from django import forms
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.models import QuerySet

from .models import Group, Item, Record


class DayForm(forms.Form):
    date = forms.DateField(
        input_formats=["%Y-%m-%d"], required=True, label=_("date")
    )


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

    class Meta:
        model = Record
        fields = ["type", "value", "item"]
