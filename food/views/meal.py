import datetime

from django.http import HttpRequest, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from ..forms import MealForm
from ..models import Day


@require_POST
@login_required
def store_meal(request: HttpRequest, date: datetime.date):
    day = Day.objects.get_or_create(user=request.user, date=date)[0]

    position = day.meals.count()
    meal = day.meals.create(position=position)

    return render(request, "food/htmx/store_meal.html", {"day": day, "meal": meal})


@require_POST
@login_required
def update_meal(request: HttpRequest, date: datetime.date, meal_id: int):
    day = get_object_or_404(Day, user=request.user, date=date)

    meal = get_object_or_404(day.meals, id=meal_id)
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

    return HttpResponse(status=204)


@require_POST
@login_required
def destroy_meal(request: HttpRequest, date: datetime.date, meal_id: int):
    day = get_object_or_404(Day, user=request.user, date=date)

    meal = get_object_or_404(day.meals, id=meal_id)

    for sibling in day.meals.filter(position__gt=meal.position):
        sibling.position -= 1
        sibling.save()
    meal.delete()

    return render(request, "food/htmx/destroy_meal.html", {"day": day})
