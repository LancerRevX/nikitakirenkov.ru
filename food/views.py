import datetime
import urllib
import urllib.parse

from django.http import HttpRequest, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required

from .forms import DayForm
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

    return render(request, "food/index.html", {"day": day, 'user': request.user})

@require_POST
@login_required
def store_meal(request: HttpRequest, date: datetime.date):
    day = Day.objects.get_or_create(user=request.user, date=date)[0]

    position = day.meals.count()
    meal = day.meals.create(position=position)

    return render(request, 'food/meal.html', {'meal': meal})