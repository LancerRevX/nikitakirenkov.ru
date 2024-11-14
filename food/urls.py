import datetime

from django.urls import path, include, register_converter
from rest_framework.routers import DefaultRouter


from .views import DayViewSet, ItemViewSet, GroupViewSet

app_name = "food"

class DateConverter:
    regex = r"\d\d\d\d-\d\d-\d\d"

    def to_python(self, value):
        return datetime.date.fromisoformat(value)

    def to_url(self, value):
        return value.isoformat()


register_converter(DateConverter, "date")

router = DefaultRouter(use_regex_path=False)
router.register('days', DayViewSet, 'day')
router.register('items', ItemViewSet, 'item')
router.register('groups', GroupViewSet, 'group')


urlpatterns = [
    path('', include(router.urls))
]
