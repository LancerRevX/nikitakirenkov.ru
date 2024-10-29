import csv

from django.db import migrations
from django.conf import settings

def insert_food_items(apps, schema_editor):
    Item = apps.get_model('food', 'Item')
    User = apps.get_model(settings.AUTH_USER_MODEL)

    with open("food/csv/food.csv", encoding="utf-8") as file:
        reader = csv.reader(file)
        user = User.objects.filter(username="nikita").get_or_create()[0]
        for row in reader:
            piece_mass = (
                float(row[5].replace(",", ".").replace('"', ""))
                if row[5]
                else None
            )
            item = Item(
                user=user,
                name=row[0],
                protein=float(row[1].replace(",", ".").replace('"', "")),
                fat=float(row[2].replace(",", ".").replace('"', "")),
                carbs=float(row[3].replace(",", ".").replace('"', "")),
                calories=float(row[4].replace(",", ".").replace('"', "")),
                piece_mass=piece_mass,
                pack_mass=piece_mass,
            )
            item.full_clean()
            item.save()

def delete_food_items(apps, schema_editor):
    Item = apps.get_model('food', 'Item')

    Item.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("food", "0001_initial"),
    ]

    operations = [migrations.RunPython(insert_food_items, delete_food_items)]
