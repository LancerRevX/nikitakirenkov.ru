from django import forms
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.models import QuerySet, Max, Min
from django.core.exceptions import ValidationError

from ..models import Day, Group, Item, Record, Meal


class ItemSearchForm(forms.Form):
    query = forms.CharField(max_length=128, required=False, empty_value="", initial="")

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

            def filter_item(item):
                if query.lower() in str(item).lower():
                    return True
                return False

            items = filter(filter_item, items)

        return items


class RecordDialogForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["item"] = forms.ModelChoiceField(
            user.food_items.all(), required=False
        )


class RecordForm(forms.ModelForm):
    template_name = "food/forms/record_form.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        type = self.cleaned_data.get("type")
        item = self.cleaned_data.get("item")
        if not type or not item:
            return

        if type not in item.get_available_record_types():
            raise ValidationError(f'type "{type}" is not supported by item "{item}"')

    class Meta:
        model = Record
        fields = ["type", "value", "item"]
