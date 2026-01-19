from jinja2 import Environment
from django.urls import reverse
from django.utils.html import escape


def environment(**options):
    env = Environment(**options)

    # useful globals/filters
    env.globals.update({"url": reverse})
    env.filters["e"] = escape

    return env
