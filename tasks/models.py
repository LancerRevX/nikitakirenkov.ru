from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class Group(models.Model):
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
        FAILED = "failed", _("failed")
        CANCELLED = "cancelled", _("cancelled")

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

    def get_status(self) -> str:
        if not self.parent:
            return self.status
        if self.status == self.Status.ACTIVE:
            return self.parent.get_status()
        return self.status

    def __str__(self) -> str:
        return f"{self.group.name}: {self.text}"

    class Meta:
        ordering = ["position"]
        constraints = [
            models.UniqueConstraint(
                name="unique_position", fields=["parent", "position"]
            )
        ]
