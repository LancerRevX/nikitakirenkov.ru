# Generated by Django 5.0 on 2024-11-06 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0007_alter_item_name'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='item',
            constraint=models.UniqueConstraint(fields=('type', 'brand', 'restaurant', 'name'), name='unique_item'),
        ),
    ]
