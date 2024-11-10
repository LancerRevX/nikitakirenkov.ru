import datetime

from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    QueryDict,
)
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.forms import modelform_factory
from django.core.exceptions import FieldError

from ..forms import DateForm, DayForm
from ..models import Day


class DayView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, date: datetime.date | None = None):
        if date is None:
            date_form = DateForm(request.GET)
            if date_form.is_valid() and date_form.cleaned_data.get("date"):
                date = date_form.cleaned_data["date"]
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
            {"day": day, "user": request.user},
        )

    def patch(self, request: HttpRequest, date: datetime.date):
        day = Day.objects.get_or_create(user=request.user, date=date)[0]

        form_data = QueryDict(request.body)
        try:
            DayForm = modelform_factory(Day, fields=form_data.keys())
        except FieldError:
            return HttpResponseBadRequest()

        day_form = DayForm(form_data, instance=day)

        if not day_form.is_valid() or not day_form.has_changed():
            return HttpResponseBadRequest()

        day_form.save()

        if day_form.data.get("is_locked") is not None:
            return render(request, "food/htmx/index.html", {"day": day})
        else:
            return HttpResponse(None, status=204)
