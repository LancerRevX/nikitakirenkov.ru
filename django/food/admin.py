from django.contrib import admin
from django import forms
import nested_admin

from . import models


class AdminWithAutoSelectedUser(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["empty_label"] = None
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(models.Diet)
class DietAdmin(AdminWithAutoSelectedUser):
    pass


class RecordInline(nested_admin.NestedTabularInline):
    model = models.Record
    autocomplete_fields = ["item"]
    extra = 1
    readonly_fields = ["protein", "fat", "carbs", "calories"]


class MealInline(nested_admin.NestedTabularInline):
    model = models.Meal
    inlines = [RecordInline]
    extra = 1
    readonly_fields = ["protein", "fat", "carbs", "calories"]


@admin.register(models.Day)
class DayAdmin(nested_admin.NestedModelAdmin):
    inlines = [MealInline]
    readonly_fields = ["protein", "fat", "carbs", "calories"]


class GroupInline(admin.TabularInline):
    model = models.Item.groups.through
    autocomplete_fields = ["group"]
    extra = 0


class GroupForm(forms.ModelForm):

    class Meta:
        model = models.Group
        fields = "__all__"
        widgets = {"color": forms.widgets.TextInput(attrs={"type": "color"})}


@admin.register(models.Group)
class GroupAdmin(AdminWithAutoSelectedUser):
    search_fields = ["name"]
    form = GroupForm

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "items":
            kwargs["widget"] = forms.widgets.SelectMultiple({"size": 20})
            kwargs["required"] = False
        return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(models.Item)
class ItemAdmin(AdminWithAutoSelectedUser):
    search_fields = ["name"]
    inlines = [GroupInline]
    autocomplete_fields = ["type"]
    list_filter = ["groups"]


class ItemTypeForm(forms.ModelForm):
    class Meta:
        model = models.ItemType
        fields = "__all__"
        widgets = {"color": forms.widgets.TextInput(attrs={"type": "color"})}


@admin.register(models.ItemType)
class ItemTypeAdmin(AdminWithAutoSelectedUser):
    search_fields = ["name"]
    form = ItemTypeForm
