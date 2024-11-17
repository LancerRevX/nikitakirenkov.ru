from django.shortcuts import render, redirect, get_object_or_404
from django.http import (
    HttpRequest,
    HttpResponseBadRequest,
    HttpResponseRedirect,
    HttpResponse,
)
from django.views.decorators.http import require_GET, require_POST
from django.db import transaction
from django.contrib.auth.decorators import login_required
import jinjax

from .models import Task
from .forms import TaskForm


@require_GET
@login_required
def index_tasks(request: HttpRequest):
    tasks = request.user.tasks.all()

    return render(request, "tasks/index.jinja", {"tasks": tasks})

    return render(
        request,
        "tasks/index.html",
        {"current_group": group, "groups": Group.objects.all(), "tasks": tasks},
    )


@require_POST
def save_task(request: HttpRequest, task_id: int):
    task = get_object_or_404(Task, id=task_id)
    old_position = task.position
    form = TaskForm(request.POST, instance=task)
    if not form.is_valid():
        return HttpResponseBadRequest()

    task = form.save()
    if task.position < old_position:
        for sibling in Task.objects.filter(
            position__gte=task.position,
            position__lt=old_position,
            parent=task.parent,
        ).exclude(id=task.id):
            sibling.position += 1
            sibling.save()
    elif task.position > old_position:
        for sibling in Task.objects.filter(
            position__lte=task.position,
            position__gt=old_position,
            parent=task.parent,
        ).exclude(id=task.id):
            sibling.position -= 1
            sibling.save()

    return render(request, "tasks/task.html", {"task": task})
