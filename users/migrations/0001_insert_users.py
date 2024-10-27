from django.db import migrations
from django.conf import settings
from django.contrib.auth import get_user_model


def insert_users(apps, schema_editor):
    User = get_user_model()
    User.objects.create_superuser("nikita", password="nikita")


def delete_users(apps, schema_editor):
    get_user_model().objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [migrations.RunPython(insert_users, delete_users)]
