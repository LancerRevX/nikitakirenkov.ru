import datetime

from django.urls import path, include, register_converter

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
    path("days/", views.DayView.as_view(), name="days"),
    path("days/<date:date>/", views.DayView.as_view(), name="days"),
    path("days/<date:date>/meals/", views.MealView.as_view(), name="meals"),
    path(
        "days/<date:date>/meals/<int:meal_position>/",
        views.MealView.as_view(),
        name="meals",
    ),
    path(
        "days/<date:date>/meals/<int:meal_position>/records/",
        views.RecordView.as_view(),
        name="records",
    ),
    path(
        "days/<date:date>/meals/<int:meal_position>/records/<int:record_position>/",
        views.RecordView.as_view(),
        name="records",
    ),
    path(
        "days/<date:date>/meals/<int:meal_position>/records/create",
        views.create_record,
        name="create-record",
    ),
    path("items/", views.ItemView.as_view(), name="items"),
]
