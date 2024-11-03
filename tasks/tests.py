from random import randint, choice

from django.test import TestCase
from django.urls import reverse

from .models import Task
from .forms import TaskForm


class SaveTaskViewTests(TestCase):
    def test_change_position(self):
        pass
        # parents = set(Task.objects.values_list("parent", flat=True))
        # for parent in parents:
        #     for i in range(Task.objects.filter(parent=parent).count()):
        #         self.assertTrue(Task.objects.filter(position=i).exists())

        # for parent in parents:
        #     count = Task.objects.filter(parent=parent).count()
        #     tasks = Task.objects.filter(parent=parent)
        #     for i in range(10):
        #         task = choice(tasks)
        #         new_position = randint(0, count - 1)
        #         response = self.client.post(
        #             reverse(
        #                 "save-task",
        #                 kwargs={"task_id": task.id},
        #             ),
        #             {
        #                 "position": new_position,
        #                 "text": task.text,
        #             },
        #         )
        #         self.assertEqual(response.status_code, 200)
        #         task.refresh_from_db()
        #         self.assertEqual(task.position, new_position)
        #         for i in range(count):
        #             self.assertTrue(
        #                 tasks.filter(position=i).exists(), tasks.all()
        #             )
