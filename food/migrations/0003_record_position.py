# Generated by Django 5.1.2 on 2024-11-02 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0002_insert_food_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='position',
            field=models.PositiveBigIntegerField(default=0, verbose_name='position'),
        ),
    ]
