import datetime

from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required

from ..forms import DayForm
from ..models import Day


@require_GET
@login_required
def show_day(request: HttpRequest, date: datetime.date | None = None):
    if date is None:
        day_form = DayForm(request.GET)
        if day_form.is_valid():
            date = day_form.cleaned_data["date"]
        else:
            date = datetime.date.today()

        return redirect("food:show-day", date=date)

    day_query = Day.objects.filter(date=date)
    if day_query.exists():
        day = day_query.get()
    else:
        day = {"date": date}

    if request.htmx:
        return render(request, "food/htmx/index.html", {"day": day})

    return render(
        request,
        "food/index.html",
        {"day": day},
    )
