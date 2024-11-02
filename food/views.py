import datetime
import urllib
import urllib.parse

from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic.dates import DateDetailView
from django.views.decorators.http import (
    require_GET,
    require_POST,
    require_http_methods,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


from .forms import DayForm, RecordForm, ItemSearchForm
from .models import Day


class DayView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, date: datetime.date | None = None):
        if date is None:
            day_form = DayForm(request.GET)
            if day_form.is_valid():
                date = day_form.cleaned_data["date"]
            else:
                date = datetime.date.today()

            return redirect("food:days", date=date)

        day_query = Day.objects.filter(date=date)
        if day_query.exists():
            day = day_query.get()
        else:
            day = {"date": date}

        if request.htmx:
            return render(request, "food/htmx/index.html", {"day": day})

        item_search_form = ItemSearchForm(request.user)

        return render(
            request,
            "food/index.html",
            {"day": day, "item_search_form": item_search_form},
        )


class MealView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, date: datetime.date):
        day = Day.objects.get_or_create(user=request.user, date=date)[0]

        position = day.meals.count()
        meal = day.meals.create(position=position)

        return render(request, "food/meal.html", {"day": day, "meal": meal})

    def delete(
        self, request: HttpRequest, date: datetime.date, meal_position: int
    ):
        day = get_object_or_404(Day, user=request.user, date=date)

        meal = get_object_or_404(day.meals, position=meal_position)

        for sibling in day.meals.filter(position__gt=meal.position):
            sibling.position -= 1
            sibling.save()
        meal.delete()

        return render(request, "food/htmx/destroy_meal.html", {"day": day})


class RecordView(LoginRequiredMixin, View):
    def post(
        self, request: HttpRequest, date: datetime.date, meal_position: int
    ):
        day = get_object_or_404(Day, user=request.user, date=date)

        meal = get_object_or_404(day.meals, position=meal_position)

        record_form = RecordForm(request.POST)
        if not record_form.is_valid():
            return HttpResponseBadRequest()

        meal.records.create(**record_form.cleaned_data)

        return render(
            request, "food/htmx/update_record.html", {"day": day, "meal": meal}
        )


class ItemView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        item_search_form = ItemSearchForm(request.user, request.GET)

        return render(
            request, "food/items.html", {"items": item_search_form.get_items()}
        )


@require_GET
@login_required
def create_record(
    request: HttpRequest, date: datetime.date, meal_position: int
):
    day = get_object_or_404(Day, user=request.user, date=date)

    meal = get_object_or_404(day.meals, position=meal_position)

    record_form = RecordForm(None)

    return render(
        request,
        record_form.template_name,
        {"day": day, "meal": meal, "form": record_form},
    )
