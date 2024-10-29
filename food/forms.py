from django import forms
from django.utils.translation import gettext_lazy as _


class DayForm(forms.Form):
    date = forms.DateField(
        input_formats=["%Y-%m-%d"], required=True, label=_("date")
    )
