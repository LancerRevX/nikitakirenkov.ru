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
    path("", views.index, name="index"),
    path("days/<date:date>/meals/", views.store_meal, name="store-meal"),
    path('days/<date:date>/meals/<int:position>/', views.destroy_meal, name='destroy-meal'),
    path('days/<date:date>/meals/<int:meal_position>/', views.create_record, name='create-record'),
]
