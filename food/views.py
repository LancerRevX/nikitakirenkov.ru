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
from django_htmx.http import trigger_client_event

from .forms import DayForm, RecordForm, ItemSearchForm, MealForm
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

        return render(
            request, "food/htmx/create_meal.html", {"day": day, "meal": meal}
        )

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

        record_form = RecordForm(request.user, request.POST)
        if not record_form.is_valid():
            return HttpResponseBadRequest()

        position = meal.records.count()
        record = meal.records.create(
            **record_form.cleaned_data, position=position
        )

        response = render(
            request,
            "food/htmx/store_record.html",
            {"day": day, "meal": meal, "record": record},
        )
        return trigger_client_event(response, "close-record-dialog")


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

    record_form = RecordForm(request.user)

    response = render(
        request,
        "food/forms/record_form.html",
        {
            "day": day,
            "meal": meal,
            "form": record_form,
        },
    )
    return trigger_client_event(response, "open-record-dialog")


@require_GET
@login_required
def edit_record(
    request: HttpRequest,
    date: datetime.date,
    meal_position: int,
    record_position: int,
):
    day = get_object_or_404(Day, user=request.user, date=date)
    meal = get_object_or_404(day.meals, position=meal_position)
    record = get_object_or_404(meal.records, position=record_position)

    record_form = RecordForm(request.user, instance=record)

    response = render(
        request,
        "food/forms/record_form.html",
        {
            "day": day,
            "meal": meal,
            "form": record_form,
        },
    )
    return trigger_client_event(response, "open-record-dialog")


@require_POST
@login_required
def update_record(
    request: HttpRequest,
    date: datetime.date,
    meal_position: int,
    record_position: int,
):
    day = get_object_or_404(Day, user=request.user, date=date)
    meal = get_object_or_404(day.meals, position=meal_position)
    record = get_object_or_404(meal.records, position=record_position)

    record_form = RecordForm(request.user, request.POST, instance=record)
    if not record_form.is_valid():
        return HttpResponseBadRequest()

    record = record_form.save()

    response = render(
        request,
        "food/htmx/update_record.html",
        {
            "day": day,
            "meal": meal,
            "record": record,
        },
    )
    return trigger_client_event(response, "close-record-dialog")


@require_POST
@login_required
def destroy_record(
    request: HttpRequest,
    date: datetime.date,
    meal_position: int,
    record_position: int,
):
    day = get_object_or_404(Day, user=request.user, date=date)
    meal = get_object_or_404(day.meals, position=meal_position)
    record = get_object_or_404(meal.records, position=record_position)

    for sibling in meal.records.filter(position__gt=meal.position):
        sibling.position -= 1
        sibling.save()
    record.delete()

    return render(
        request, "food/htmx/destroy_record.html", {"day": day, "meal": meal}
    )


@require_POST
@login_required
def update_meal(request: HttpRequest, date: datetime.date, meal_position: int):
    day = get_object_or_404(Day, user=request.user, date=date)

    meal = get_object_or_404(day.meals, position=meal_position)
    old_position = meal.position

    meal_form = MealForm(request.POST, instance=meal)
    if not meal_form.is_valid() or not meal_form.has_changed():
        return HttpResponseBadRequest()

    new_position = meal_form.cleaned_data["position"]

    if new_position < old_position:
        for sibling in day.meals.filter(
            position__lt=old_position, position__gte=new_position
        ).exclude(id=meal.id):
            sibling.position += 1
            sibling.save()
    else:
        for sibling in day.meals.filter(
            position__gt=old_position, position__lte=new_position
        ).exclude(id=meal.id):
            sibling.position -= 1
            sibling.save()

    meal.position = new_position
    meal.save()

    return render(request, "food/meals.html", {"day": day})


@require_GET
@login_required
def preview_record(request: HttpRequest):
    record_form = RecordForm(request.GET)
    if record_form.is_valid():
        record = record_form.save(False)
    else:
        record = None

    return render(request, "food/preview_record.html", {"record": record})
