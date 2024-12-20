from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest

from .models import Task

class TaskInline(admin.StackedInline):
    model = Task
    extra = 0


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["id", "position", "text", "datetime"]
    list_display_links = ["id"]
    list_editable = ["position", "text", "datetime"]
    inlines = [TaskInline]

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return Task.objects.filter(parent=None)
