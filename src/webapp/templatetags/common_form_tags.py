from __future__ import absolute_import, unicode_literals

from django import template


register = template.Library()


def add_css_class(class_name, class_list):
    if not class_list:
        return class_name
    return class_list + ' ' + class_name


@register.filter
def add_class(bound_field, class_name):
    widget = bound_field.field.widget
    class_list = widget.attrs.get('class')
    widget.attrs['class'] = add_css_class(class_name, class_list)
    return bound_field
