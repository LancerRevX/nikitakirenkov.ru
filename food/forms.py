from django import forms


class IndexForm(forms.Form):
    from_date = forms.DateField(input_formats=["%Y-%m-%d"])
    to_date = forms.DateField(input_formats=["%Y-%m-%d"])
