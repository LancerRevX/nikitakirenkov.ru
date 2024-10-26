from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index_tasks),
    path("<slug:group_slug>/", views.index_tasks, name="index-tasks"),
]
