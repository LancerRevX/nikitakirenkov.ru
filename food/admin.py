from django.contrib import admin
from django import forms
import nested_admin

from . import models


@admin.register(models.Diet)
class DietAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["empty_label"] = None
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class RecordInline(nested_admin.NestedTabularInline):
    model = models.Record
    autocomplete_fields = ["item"]
    extra = 1


class MealInline(nested_admin.NestedStackedInline):
    model = models.Meal
    inlines = [RecordInline]
    extra = 1


@admin.register(models.Day)
class DayAdmin(nested_admin.NestedModelAdmin):
    inlines = [MealInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["empty_label"] = None
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ItemInline(admin.TabularInline):
    model = models.Group.items.through
    autocomplete_fields = ["item"]


class GroupForm(forms.ModelForm):

    class Meta:
        model = models.Group
        fields = "__all__"
        widgets = {"color": forms.widgets.TextInput(attrs={"type": "color"})}


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    form = GroupForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["empty_label"] = None
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "items":
            kwargs["widget"] = forms.widgets.SelectMultiple({"size": 20})
        return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    search_fields = ["name"]
