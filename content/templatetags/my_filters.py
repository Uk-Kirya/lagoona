from django import template
register = template.Library()


@register.filter(name='shorten_phone')
def shorten_phone(value):
    return value.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
