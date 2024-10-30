import datetime
import urllib
import urllib.parse

from django.http import HttpRequest, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib.auth.decorators import login_required

from .forms import DayForm, RecordForm
from .models import Day


@require_GET
@login_required
def index(request: HttpRequest):
    day_form = DayForm(request.GET)
    if day_form.is_valid():
        date = day_form.cleaned_data["date"]
    else:
        date = datetime.date.today()

    day_query = Day.objects.filter(date=date)
    if day_query.exists():
        day = day_query.get()
    else:
        day = {"date": date}

    if request.htmx:
        return render(request, 'food/htmx/index.html', {'day': day})

    record_form = RecordForm(user=request.user)

    return render(
        request,
        "food/index.html",
        {"day": day, "user": request.user, "record_form": record_form},
    )


@require_POST
@login_required
def store_meal(request: HttpRequest, date: datetime.date):
    day = Day.objects.get_or_create(user=request.user, date=date)[0]

    position = day.meals.count()
    meal = day.meals.create(position=position)

    return render(request, "food/meal.html", {"day": day, "meal": meal})


@require_http_methods(["DELETE"])
@login_required
def destroy_meal(request: HttpRequest, date: datetime.date, position: int):
    day = get_object_or_404(Day, user=request.user, date=date)

    meal = get_object_or_404(day.meals, position=position)

    for sibling in day.meals.filter(position__gt=meal.position):
        sibling.position -= 1
        sibling.save()
    meal.delete()

    return render(request, "food/htmx/destroy_meal.html", {"day": day})


@require_GET
@login_required
def create_record(request: HttpRequest, date: datetime.date, meal_position: int):
    day = get_object_or_404(Day, user=request.user, date=date)

    meal = get_object_or_404(day.meals, position=meal_position)

    return render(request, "food/forms/record_form.html", {"day": day, "meal": meal})
