from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponseBadRequest

from .models import Group, Task


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
