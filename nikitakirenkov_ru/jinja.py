import os

from django.templatetags.static import static
from django.urls import reverse

from jinja2 import Environment
import jinjax
from jinja2.loaders import FileSystemLoader


def environment(loader: FileSystemLoader, **options):
    env = Environment(loader=loader, **options)
    env.globals.update(
        {
            "static": static,
            "url": reverse,
        }
    )
    env.add_extension(jinjax.JinjaX)
    catalog = jinjax.Catalog(jinja_env=env)

    catalog.add_folder("components")
    for dir in env.loader.searchpath:
        catalog.add_folder(os.path.join(dir, "components"))
    return env
