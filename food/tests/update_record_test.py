import datetime
from random import choice, randint
from urllib.parse import urlencode

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext as _
from django.db.models import Min, Max


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
            for j in range(5):
                item = choice(self.user.food_items.all())
                type = choice(item.get_available_record_types())

                response = self.client.post(
                    reverse(
                        "food:records",
                        kwargs=dict(date=self.day.date, meal_id=meal.id),
                    ),
                    {
                        "item": item.id,
                        "type": type.value,
                        "value": randint(1, 300),
                    },
                )
                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(response.context.get("record"))

        return super().setUp()

    def test_edit_dialog_opens(self):
        for i in range(10):
            meal = choice(self.day.meals.all())
            record = choice(meal.records.all())
            response = self.client.get(
                reverse(
                    "food:edit-record",
                    kwargs=dict(
                        date=self.day.date, meal_id=meal.id, record_id=record.id
                    ),
                )
            )
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, _("Edit record"))
            record_form = response.context.get("form")
            self.assertIsNotNone(record_form)
            self.assertEqual(record_form["value"].value(), record.value)
            self.assertEqual(record_form["type"].value(), record.type)
            self.assertEqual(record_form["item"].value(), record.item.id)

    def test_initial_positions_are_correct(self):
        for meal in self.day.meals.all():
            min_position = meal.records.aggregate(pos=Min("position"))["pos"]
            self.assertEqual(min_position, 0)

            max_position = meal.records.aggregate(pos=Max("position"))["pos"]
            self.assertEqual(max_position, meal.records.count() - 1)

            for record in meal.records.all():
                self.assertEqual(
                    meal.records.filter(position=record.position).count(), 1
                )

    def test_positions_change_correctly(self):
        for meal in self.day.meals.all():
            for _ in range(10):
                record = choice(meal.records.all())
                new_position = choice(
                    list(
                        i
                        for i in range(meal.records.count())
                        if i != record.position
                    )
                )
                response = self.client.patch(
                    reverse(
                        "food:records",
                        kwargs=dict(
                            date=self.day.date,
                            meal_id=meal.id,
                            record_id=record.id,
                        ),
                    ),
                    urlencode({"position": new_position}),
                )
                self.assertEqual(response.status_code, 204)
                self.assertEqual(len(response.content), 0)

                meal.refresh_from_db()
                self.assertEqual(record.position, new_position)

                min_position = self.day.meals.aggregate(pos=Min("position"))[
                    "pos"
                ]
                self.assertEqual(min_position, 0)
                max_position = self.day.meals.aggregate(pos=Max("position"))[
                    "pos"
                ]
                self.assertEqual(max_position, meal.records.count() - 1)
                for record in meal.records.all():
                    self.assertEqual(
                        meal.records.filter(position=record.position).count(), 1
                    )
