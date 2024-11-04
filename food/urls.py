import datetime

from django.urls import path, include, register_converter
from django.views.generic import RedirectView

from . import views

app_name = "food"


class DateConverter:
    regex = r"\d\d\d\d-\d\d-\d\d"

    def to_python(self, value):
        return datetime.date.fromisoformat(value)

    def to_url(self, value):
        return value.isoformat()


register_converter(DateConverter, "date")

urlpatterns = [
    path("", RedirectView.as_view(url="days/")),
    path("days/", views.show_day, name="index-days"),
    path("days/<date:date>/", views.show_day, name="show-day"),
    path("days/<date:date>/meals/", views.store_meal, name="store-meal"),
    path(
        "days/<date:date>/meals/<int:meal_id>/update/",
        views.update_meal,
        name="update-meal",
    ),
    path(
        "days/<date:date>/meals/<int:meal_id>/",
        views.destroy_meal,
        name="destroy-meal",
    ),
    path(
        "days/<date:date>/meals/<int:meal_id>/records/create",
        views.create_record,
        name="create-record",
    ),
    path(
        "days/<date:date>/meals/<int:meal_id>/records/store",
        views.store_record,
        name="store-record",
    ),
    path(
        "days/<date:date>/meals/<int:meal_id>/records/<int:record_id>/edit",
        views.edit_record,
        name="edit-record",
    ),
    path(
        "days/<date:date>/meals/<int:meal_id>/records/<int:record_id>/update",
        views.update_record,
        name="update-record",
    ),
    path(
        "days/<date:date>/meals/<int:meal_id>/records/<int:record_id>/destroy",
        views.destroy_record,
        name="destroy-record",
    ),
    path("items/", views.index_items, name="index-items"),
]
