from rest_framework import serializers

from .models import Day, Meal, Record, Item, Group

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ['id', 'position']

class MealSerializer(serializers.ModelSerializer):
    records = RecordSerializer(many=True)
    class Meta:
        model = Meal
        fields = ['id', 'position', 'records']

class DaySerializer(serializers.ModelSerializer):
    meals = MealSerializer(many=True)
    class Meta:
        model = Day
        fields = ["date", 'meals']



class ItemSerializer(serializers.HyperlinkedModelSerializer):
    type = serializers.StringRelatedField()
    brand = serializers.StringRelatedField()
    restaurant = serializers.StringRelatedField()
    name = serializers.StringRelatedField()

    class Meta:
        model = Item
        fields = ["url", "type", "brand", "restaurant", "name", "groups"]
        extra_kwargs = {
            "url": dict(view_name="food:item-detail"),
            "groups": dict(view_name="food:group-detail"),
        }


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name", "items"]
        extra_kwargs = {
            "url": dict(view_name="food:group-detail"),
            "items": dict(view_name="food:item-detail"),
        }
