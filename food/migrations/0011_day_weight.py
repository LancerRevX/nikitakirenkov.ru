# Generated by Django 5.0 on 2024-11-09 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0010_alter_itembrand_name_alter_itemrestaurant_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='day',
            name='weight',
            field=models.FloatField(blank=True, null=True, verbose_name='weight'),
        ),
    ]