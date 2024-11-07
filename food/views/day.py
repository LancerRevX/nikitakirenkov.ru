import datetime

from django.http import HttpRequest, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from ..forms import DayForm
from ..models import Day


class DayView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, date: datetime.date | None = None):
        if date is None:
            day_form = DayForm(request.GET)
            if day_form.is_valid() and day_form.cleaned_data.get('date'):
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

        return render(
            request,
            "food/index.html",
            {"day": day},
    )

    def patch(self, request: HttpRequest, date: datetime.date):
        day = Day.objects.get_or_create(user=request.user, date=date)[0]

        day_form = DayForm(request.POST, instance=day)

        if not day_form.is_valid():
            return HttpResponseBadRequest()
        
        day_form.save()

        return render(request, 'food/htmx/index.html', {'day': day})


