from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.conf import settings


class Group(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        verbose_name=_("user"),
        related_name="task_groups",
    )
    slug = models.SlugField(_("slug"))
    name = models.CharField(_("name"), max_length=32)
    color = models.CharField(_("color"), max_length=7, null=True, blank=True)
    # can_be_failed = models.BooleanField(_("can be failed"), default=False)

    def get_absolute_url(self):
        return reverse("index-tasks", kwargs={"group_slug": self.slug})

    def __str__(self) -> str:
        return f"{self.name}"


class Task(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", _("active")
        IN_PROGRESS = "in_progress", _("in progress")
        FINISHED = "finished", _("finished")
        QUESTIONED = "questioned", _("questioned")
        FAILED = "failed", _("failed")
        CANCELLED = "cancelled", _("cancelled")

    STATUS_ICON_TEMPLATE_NAMES = {
        Status.FINISHED: "tasks/icons/check.html",
        Status.IN_PROGRESS: "tasks/icons/dot.html",
        Status.QUESTIONED: "tasks/icons/question_mark.html",
        Status.FAILED: "tasks/icons/x_mark.html",
    }

    group = models.ForeignKey(
        Group, models.CASCADE, verbose_name=_("group"), related_name="tasks"
    )
    text = models.CharField(_("text"), max_length=128)
    parent = models.ForeignKey(
        "self", models.CASCADE, null=True, blank=True, related_name="children"
    )
    status = models.CharField(
        _("status"),
        choices=Status,
        default=Status.ACTIVE,
        max_length=max(map(len, Status.values)),
    )
    position = models.IntegerField(_("position"))

    datetime = models.DateTimeField(_("date and time"), null=True, blank=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    @property
    def status_icon_template_name(self):
        return self.STATUS_ICON_TEMPLATE_NAMES.get(self.get_status())

    def get_status(self) -> str:
        if not self.parent:
            return self.status
        if self.status == self.Status.ACTIVE:
            return self.parent.get_status()
        return self.status

    def is_status_editable(self):
        if not self.parent:
            return True
        return self.parent.get_status() in [
            self.Status.ACTIVE,
            self.Status.IN_PROGRESS,
        ]

    def __str__(self) -> str:
        if self.parent is None:
            return f"{self.group.name}#{self.position} {self.text}"
        else:
            return f"{self.parent.text}#{self.position} {self.text}"

    class Meta:
        ordering = ["position"]
