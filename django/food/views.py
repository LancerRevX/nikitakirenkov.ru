from datetime import date, timedelta

from django.http import HttpRequest, HttpResponseBadRequest
from django.shortcuts import render

from .forms import IndexForm
from .models import Day


def index(request: HttpRequest):
    form = IndexForm(request.GET)
    if not form.is_valid():
        return HttpResponseBadRequest("BAD REQUEST!")
    from_date: date = form.cleaned_data["from_date"]
    to_date: date = form.cleaned_data["to_date"]
    days = Day.objects.filter(date__range=(from_date, to_date)).order_by("date")
    days = list(days)
    temp_date = from_date
    i = 0
    while temp_date <= to_date:
        if i >= len(days) or days[i].date != temp_date:
            new_day = {
                "date": temp_date,
                "protein": 0.0,
                "fat": 0.0,
                "carbs": 0.0,
                "calories": 0.0,
                "meals": [],
            }
            days.insert(i, new_day)
        temp_date += timedelta(1)
        i += 1
    return render(request, "food/index.html", {"days": days})
