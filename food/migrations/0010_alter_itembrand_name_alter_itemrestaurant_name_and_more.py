# Generated by Django 5.0 on 2024-11-06 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0009_alter_item_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itembrand',
            name='name',
            field=models.CharField(max_length=32, unique=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='itemrestaurant',
            name='name',
            field=models.CharField(max_length=32, unique=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='itemtype',
            name='name',
            field=models.CharField(max_length=32, unique=True, verbose_name='name'),
        ),
    ]