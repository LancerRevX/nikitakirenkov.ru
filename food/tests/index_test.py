import datetime

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class IndexTest(TestCase):
    def test_day_page_opens(self):
        user = get_user_model().objects.first()
        self.client.force_login(user)
        response = self.client.get('/food', follow=True)
        self.assertEqual(response.status_code, 200)