from django import template

register = template.Library()


@register.inclusion_tag('people/includes/qualifications.html')
def qualification_badges(qualifications):
    return {'qualifications': qualifications}
