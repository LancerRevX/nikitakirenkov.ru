import datetime
from random import choice, randint
from urllib.parse import urlencode

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models import Max, Min
from django.test.client import MULTIPART_CONTENT

from ..models import Day, Meal


class UpdateMealTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(username="testuser")
        self.client.force_login(self.user)
        self.day = self.user.food_days.create(date=datetime.date.today())

    def test_day_locks(self):
        self.assertFalse(self.day.is_locked)
        response = self.client.patch(
            reverse("food:days", kwargs=dict(date=self.day.date)),
            urlencode({"is_locked": True}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context.get("day"))
        self.day.refresh_from_db()
        self.assertTrue(self.day.is_locked)

    def test_day_unlocks(self):
        self.day.is_locked = True
        self.day.save()
        response = self.client.patch(
            reverse("food:days", kwargs=dict(date=self.day.date)),
            urlencode({"is_locked": False}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context.get("day"))
        self.day.refresh_from_db()
        self.assertFalse(self.day.is_locked)

    def test_updating_weight_works(self):
        self.assertIsNone(self.day.weight)
        new_weight = randint(60, 80)
        response = self.client.patch(
            reverse("food:days", kwargs=dict(date=self.day.date)),
            urlencode({"weight": new_weight}),
        )
        self.assertEqual(response.status_code, 204)
        self.assertTemplateNotUsed(response, "food/index.html")
        self.assertTemplateNotUsed(response, "food/htmx/index.html")
        self.day.refresh_from_db()
        self.assertEqual(self.day.weight, new_weight)

    def test_sending_empty_form_responds_400(self):
        response = self.client.patch(
            reverse("food:days", kwargs=dict(date=self.day.date)),
        )
        self.assertEqual(response.status_code, 400)
