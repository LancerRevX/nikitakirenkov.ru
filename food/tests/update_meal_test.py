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

        for _ in range(10):
            response = self.client.post(reverse('food:meals', kwargs=dict(date=self.day.date)))
            self.assertEqual(response.status_code, 201)

        self.assertEqual(self.day.meals.count(), 10)
            
        return super().setUp()

    def make_request(self, meal, new_position):
        return self.client.patch(
            reverse(
                "food:meals",
                kwargs=dict(
                    date=self.day.date,
                    meal_id=meal.id,
                ),
            ),
            urlencode({"position": new_position}),
            content_type='application/x-www-form-urlencoded'
        )

    def test_initial_positions_are_correct(self):
        min_position = self.day.meals.aggregate(pos=Min("position"))["pos"]
        self.assertEqual(min_position, 0)

        max_position = self.day.meals.aggregate(pos=Max("position"))["pos"]
        self.assertEqual(max_position, self.day.meals.count() - 1)

        for meal in self.day.meals.all():
            self.assertEqual(
                self.day.meals.filter(position=meal.position).count(), 1
            )

    def test_positions_change_correctly(self):
        for _ in range(10):
            meal = choice(self.day.meals.all())
            new_position = choice(
                list(
                    i
                    for i in range(self.day.meals.count())
                    if i != meal.position
                )
            )
            response = self.make_request(meal, new_position)
            self.assertEqual(response.status_code, 204)
            self.assertEqual(len(response.content), 0)

            meal.refresh_from_db()
            self.assertEqual(meal.position, new_position)

            min_position = self.day.meals.aggregate(pos=Min("position"))["pos"]
            self.assertEqual(min_position, 0)

            max_position = self.day.meals.aggregate(pos=Max("position"))["pos"]
            self.assertEqual(max_position, self.day.meals.count() - 1)

            for meal in self.day.meals.all():
                self.assertEqual(
                    self.day.meals.filter(position=meal.position).count(), 1
                )

    def test_cant_provide_invalid_position(self):
        meal = choice(self.day.meals.all())

        response = self.make_request(meal, randint(-100, -1))
        self.assertEqual(response.status_code, 400)

        response = self.make_request(meal, meal.position)
        self.assertEqual(response.status_code, 400)

        response = self.make_request(meal, self.day.meals.count())
        self.assertEqual(response.status_code, 400)
