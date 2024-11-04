import datetime

from django.http import HttpRequest, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django_htmx.http import trigger_client_event

from ..forms import RecordForm
from ..models import Day


@require_GET
@login_required
def create_record(request: HttpRequest, date: datetime.date, meal_id: int):
    day = get_object_or_404(Day, user=request.user, date=date)

    meal = get_object_or_404(day.meals, id=meal_id)

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


@require_POST
@login_required
def store_record(request: HttpRequest, date: datetime.date, meal_id: int):
    day = get_object_or_404(Day, user=request.user, date=date)

    meal = get_object_or_404(day.meals, id=meal_id)

    record_form = RecordForm(request.user, request.POST)
    if not record_form.is_valid():
        return HttpResponseBadRequest()

    position = meal.records.count()
    record = meal.records.create(**record_form.cleaned_data, position=position)

    response = render(
        request,
        "food/htmx/store_record.html",
        {"day": day, "meal": meal, "record": record},
    )
    return trigger_client_event(response, "close-record-dialog")


@require_GET
@login_required
def edit_record(
    request: HttpRequest,
    date: datetime.date,
    meal_id: int,
    record_id: int,
):
    day = get_object_or_404(Day, user=request.user, date=date)
    meal = get_object_or_404(day.meals, id=meal_id)
    record = get_object_or_404(meal.records, id=record_id)

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
    meal_id: int,
    record_id: int,
):
    day = get_object_or_404(Day, user=request.user, date=date)
    meal = get_object_or_404(day.meals, id=meal_id)
    record = get_object_or_404(meal.records, id=record_id)

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
    meal_id: int,
    record_id: int,
):
    day = get_object_or_404(Day, user=request.user, date=date)
    meal = get_object_or_404(day.meals, id=meal_id)
    record = get_object_or_404(meal.records, id=record_id)

    for sibling in meal.records.filter(position__gt=meal.position):
        sibling.position -= 1
        sibling.save()
    record.delete()

    return render(request, "food/htmx/destroy_record.html", {"day": day, "meal": meal})
