import json

from django import template

register = template.Library()


@register.filter('json')
def to_json(data):
    return json.dumps(data)
