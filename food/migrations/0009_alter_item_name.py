# Generated by Django 5.0 on 2024-11-06 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0008_item_unique_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='name'),
        ),
    ]