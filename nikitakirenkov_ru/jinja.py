import os

from django.templatetags.static import static
from django.urls import reverse
from django.utils import translation

from jinja2 import Environment
import jinjax
from jinja2.loaders import FileSystemLoader
from tailwind.templatetags.tailwind_tags import tailwind_css

def environment(loader: FileSystemLoader, **options):
    env = Environment(loader=loader, **options)
    env.globals.update(
        {
            "static": static,
            "url": reverse,
            'tailwind_css': tailwind_css,
        }
    )
    env.add_extension(jinjax.JinjaX)
    env.install_gettext_translations(translation)
    catalog = jinjax.Catalog(jinja_env=env)

    catalog.add_folder("components")
    for dir in env.loader.searchpath:
        catalog.add_folder(os.path.join(dir, "components"))
    return env
