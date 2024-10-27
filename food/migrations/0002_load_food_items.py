import csv

from django.db import migrations
from django.contrib.auth.models import User

from .. import models


def load_food_items(apps, schema_editor):
    with open("food/csv/food.csv", encoding="utf-8") as file:
        reader = csv.reader(file)
        user = User.objects.filter(username="nikita").get_or_create()[0]
        for row in reader:
            piece_mass = (
                float(row[5].replace(",", ".").replace('"', ""))
                if row[5]
                else None
            )
            item = models.Item(
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


class Migration(migrations.Migration):

    dependencies = [
        ("food", "0001_initial"),
    ]

    operations = [migrations.RunPython(load_food_items)]
