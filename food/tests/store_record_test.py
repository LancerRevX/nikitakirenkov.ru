import datetime
from random import choice, randint

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext as _
from django.db.models import Min, Max

from ..models import Item, Record


class UpdateRecordTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.get(username="nikita")
        self.client.force_login(self.user)
        self.day = self.user.food_days.create(date=datetime.date.today())

        for i in range(5):
            response = self.client.post(
                reverse("food:meals", kwargs=dict(date=self.day.date))
            )
            self.assertEqual(response.status_code, 201)
            meal = response.context.get("meal")
            self.assertIsNotNone(meal)

        return super().setUp()

    def test_create_dialog_opens(self):
        for i in range(10):
            meal = choice(self.day.meals.all())
            response = self.client.get(
                reverse(
                    "food:create-record",
                    kwargs=dict(
                        date=self.day.date, meal_id=meal.id
                    ),
                )
            )
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, _('Add new record'))
            record_form = response.context.get('form')
            self.assertIsNotNone(record_form)

    def test_record_is_stored(self):
        for i in range(10):
            meal = choice(self.day.meals.all())
            item = choice(Item.objects.all())
            response = self.client.post(
                reverse(
                    "food:records",
                    kwargs=dict(
                        date=self.day.date, meal_id=meal.id
                    ),
                ),
                { 
                    'item': item.id,
                    'type': choice(item.get_available_record_types()),
                    'value': randint(1, 100),
                }
            )
            self.assertEqual(response.status_code, 201)
            record = response.context.get('record')
            self.assertIsNotNone(record)
            self.assertIsNotNone(record.id)