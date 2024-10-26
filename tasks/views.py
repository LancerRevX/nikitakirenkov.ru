from django.shortcuts import render, redirect, get_object_or_404
from django.http import (
    HttpRequest,
    HttpResponseBadRequest,
    HttpResponseRedirect,
    HttpResponse,
)
from django.views.decorators.http import require_GET, require_POST
from django.db import transaction

from .models import Group, Task
from .forms import TaskForm


@require_GET
def index_tasks(request: HttpRequest, group_slug=None):
    if group_slug is None:
        if group := Group.objects.first():
            return redirect("index-tasks", group_slug=group.slug)
    else:
        group = get_object_or_404(Group, slug=group_slug)

    if group is not None:
        tasks = group.tasks.filter(parent=None)

    return render(
        request,
        "tasks/index.html",
        {"current_group": group, "groups": Group.objects.all(), "tasks": tasks},
    )


# @require_POST
def save_task(request: HttpRequest, task_id: int):
    task = get_object_or_404(Task, id=task_id)
    form = TaskForm(request.POST, instance=task)
    if not form.is_valid():
        return HttpResponseBadRequest()

    task = form.save(commit=False)
    with transaction.atomic():
        parent = Task.objects.get(id=2)
        task1 = Task.objects.get(parent=parent, position=1)
        task2 = Task.objects.get(parent=parent, position=2)
        task1.position, task2.position = task2.position, task1.position
        task1.save()
        task2.save()

    return render(request, "tasks/task.html", {"task": task})
