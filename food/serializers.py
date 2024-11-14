from rest_framework import serializers

from .models import Day, Meal, Record, Item, Group

class ItemSerializer(serializers.ModelSerializer):
    type = serializers.StringRelatedField()
    brand = serializers.StringRelatedField()
    restaurant = serializers.StringRelatedField()
    name = serializers.StringRelatedField()

    class Meta:
        model = Item
        fields = ["id", "type", "brand", "restaurant", "name", "groups"]
        

class RecordSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    
    class Meta:
        model = Record
        fields = ['id', 'position', 'item']

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






class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name", "items"]
        extra_kwargs = {
            "url": dict(view_name="food:group-detail"),
            "items": dict(view_name="food:item-detail"),
        }
