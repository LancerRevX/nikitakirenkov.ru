from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin

from .models import Day, Item, Group
from .serializers import DaySerializer, ItemSerializer, GroupSerializer


class DayViewSet(RetrieveModelMixin, GenericViewSet):
    serializer_class = DaySerializer
    lookup_field = 'date'
    lookup_value_converter = 'date'

    def get_queryset(self):
        return self.request.user.food_days.all()

    def get_object(self):
        queryset = self.get_queryset().filter(user=self.request.user, date=self.kwargs['date'])
        if queryset.exists():
            day = queryset.get()
        else:
            day = Day(
                is_locked=False,
                date=self.kwargs['date']
            )
        return day



class ItemViewSet(ModelViewSet):
    serializer_class = ItemSerializer

    def get_queryset(self):
        return self.request.user.food_items.all()


class GroupViewSet(ModelViewSet):
    serializer_class = GroupSerializer

    def get_queryset(self):
        return self.request.user.food_groups.all()
