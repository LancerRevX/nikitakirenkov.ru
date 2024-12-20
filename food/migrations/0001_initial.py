# Generated by Django 5.1.2 on 2024-11-02 14:11

import django.contrib.auth.models
import django.db.models.deletion
import food.models
from django.db import migrations, models


# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# food.migrations.0002_insert_food_items


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Diet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=64, verbose_name="name")),
                (
                    "protein",
                    models.FloatField(
                        blank=True, null=True, verbose_name="protein"
                    ),
                ),
                (
                    "fat",
                    models.FloatField(
                        blank=True, null=True, verbose_name="fat"
                    ),
                ),
                (
                    "carbs",
                    models.FloatField(
                        blank=True, null=True, verbose_name="carbs"
                    ),
                ),
                (
                    "calories",
                    models.FloatField(
                        blank=True, null=True, verbose_name="calories"
                    ),
                ),
            ],
            options={
                "verbose_name": "diet",
                "verbose_name_plural": "diets",
            },
        ),
        migrations.CreateModel(
            name="ItemType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=32, verbose_name="name")),
                ("color", models.CharField(max_length=7, verbose_name="color")),
            ],
        ),
        migrations.CreateModel(
            name="FoodUser",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("auth.user",),
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Day",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "date",
                    models.DateField(
                        default=food.models.default_date, verbose_name="date"
                    ),
                ),
                (
                    "diet",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="days",
                        to="food.diet",
                        verbose_name="diet",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="days",
                        to="food.fooduser",
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "day",
                "verbose_name_plural": "days",
            },
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=256, verbose_name="name")),
                (
                    "protein",
                    models.FloatField(
                        help_text="Per 100g.", verbose_name="protein"
                    ),
                ),
                (
                    "fat",
                    models.FloatField(
                        help_text="Per 100g.", verbose_name="fat"
                    ),
                ),
                (
                    "carbs",
                    models.FloatField(
                        help_text="Per 100g.", verbose_name="carbs"
                    ),
                ),
                (
                    "calories",
                    models.FloatField(
                        help_text="Per 100g.", verbose_name="calories"
                    ),
                ),
                (
                    "piece_mass",
                    models.FloatField(
                        blank=True, null=True, verbose_name="piece mass"
                    ),
                ),
                (
                    "pack_mass",
                    models.FloatField(
                        blank=True, null=True, verbose_name="pack mass"
                    ),
                ),
                (
                    "type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="items",
                        to="food.itemtype",
                        verbose_name="type",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="food.fooduser",
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "item",
                "verbose_name_plural": "items",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Meal",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("position", models.IntegerField(default=0)),
                (
                    "day",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="meals",
                        to="food.day",
                        verbose_name="day",
                    ),
                ),
            ],
            options={
                "verbose_name": "meal",
                "verbose_name_plural": "meals",
            },
        ),
        migrations.CreateModel(
            name="Record",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("mass", "Mass"),
                            ("piece", "Piece"),
                            ("pack", "Pack"),
                        ],
                        default="mass",
                        max_length=5,
                        verbose_name="type",
                    ),
                ),
                ("value", models.FloatField(verbose_name="value")),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="records",
                        to="food.item",
                        verbose_name="item",
                    ),
                ),
                (
                    "meal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="records",
                        to="food.meal",
                        verbose_name="meal",
                    ),
                ),
            ],
            options={
                "verbose_name": "record",
                "verbose_name_plural": "records",
            },
        ),
        migrations.AddField(
            model_name="itemtype",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="item_types",
                to="food.fooduser",
                verbose_name="user",
            ),
        ),
        migrations.CreateModel(
            name="Group",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=32, verbose_name="name")),
                ("color", models.CharField(max_length=7, verbose_name="color")),
                (
                    "items",
                    models.ManyToManyField(
                        related_name="groups",
                        to="food.item",
                        verbose_name="items",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="food_groups",
                        to="food.fooduser",
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "group",
                "verbose_name_plural": "groups",
            },
        ),
        migrations.AddField(
            model_name="diet",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="diets",
                to="food.fooduser",
                verbose_name="user",
            ),
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField(verbose_name="text")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="food.fooduser",
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "comment",
                "verbose_name_plural": "comments",
            },
        ),
        migrations.AddConstraint(
            model_name="day",
            constraint=models.UniqueConstraint(
                fields=("user", "date"), name="unique_date_for_user"
            ),
        ),
        migrations.AlterModelOptions(
            name="meal",
            options={
                "ordering": ["position"],
                "verbose_name": "meal",
                "verbose_name_plural": "meals",
            },
        ),
        migrations.AlterField(
            model_name="item",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="food_items",
                to="food.fooduser",
                verbose_name="user",
            ),
        ),
    ]
