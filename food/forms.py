from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Group, Item, Record

class DayForm(forms.Form):
    date = forms.DateField(
        input_formats=["%Y-%m-%d"], required=True, label=_("date")
    )

class RecordForm(forms.Form):
    type = forms.TypedChoiceField(coerce=str, initial=Record.Type.MASS, required=True, choices=Record.Type)
    
    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

        self.fields['group'] = forms.ModelChoiceField(self.user.food_groups.all())


