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
    path("days/", views.DayView.as_view(), name="days"),
    path("days/<date:date>/", views.DayView.as_view(), name="days"),
    path("days/<date:date>/meals/", views.MealView.as_view(), name="meals"),
    path(
        "days/<date:date>/meals/<int:meal_id>/",
        views.MealView.as_view(),
        name="meals",
    ),
    path(
        "days/<date:date>/meals/<int:meal_id>/records/",
        views.RecordView.as_view(),
        name="records",
    ),
    path(
        "days/<date:date>/meals/<int:meal_id>/records/<int:record_id>/",
        views.RecordView.as_view(),
        name="records",
    ),
    path(
        "days/<date:date>/meals/<int:meal_id>/records/create",
        views.create_record,
        name="create-record",
    ),
    path(
        "days/<date:date>/meals/<int:meal_id>/records/<int:record_id>/edit",
        views.edit_record,
        name="edit-record",
    ),
    path("items/", views.index_items, name="index-items"),
]
